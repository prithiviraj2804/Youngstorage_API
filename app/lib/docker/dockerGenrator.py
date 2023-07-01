import os
import subprocess
from ..wg.wireguard import addWireguard
from ...database import db,mqtt_client


# create new container or to redeploy
def spawnContainer(username: str, peer: str):
    try:
        baselist = list(db.baselist.find())
        if len(baselist) == 1:
            ip = baselist[0]["ip"]
            # this function will happens very first time
            # create two peer
            # 1-container
            # 2-client
            for i in range(int(peer), 3):
                ipdata = IpRange65535(ip)
                if ipdata["status"]:
                    ip = ipdata["message"]
                    addWireguard(username, str(i), ip)
                else:
                    return ipdata
            db.baselist.update_one({"_id": baselist[0]["_id"]}, {
                                   "$set": {"ip": ip, "ipissued": baselist[0]["ipissued"]+2, "no_client": baselist[0]["no_client"]+1}})
            source = os.path.join(os.getcwd(), "source")

            # create new docker file with giver username and peer vpn connection
            with open(os.path.join(source, "Dockerfile"), "w")as dockerfile:
                dockerfile.write(dockerGenerator(username, peer))
                dockerfile.close()

            # create setup.sh file to run inside the docker container after container
            # has been spawn
            with open(os.path.join(source, "setup.sh"), "w")as setup:
                setup.write(setupSh(username))
                setup.close()

            #both image build and container run happens in single shot
            imageBuild(username)
            containerRun(username)

            return {"message": "Container Created successfully", "status": True}
        return {"message": "Issue in baselist data find", "status": False}
    except Exception as e:
        return {"message": str(e), "status": False}


# docker generator template
def dockerGenerator(username: str, peer: str):
    return f'''FROM ubuntu:latest
RUN apt-get update
ARG S6_OVERLAY_VERSION=3.1.0.1
RUN apt install -y openssh-server nano htop
RUN apt install -y sudo figlet lolcat bash-completion
ENV DEBIAN_FRONTEND noninteractive
RUN apt install -y ufw net-tools netcat curl apache2
RUN apt install -y inetutils-ping php libapache2-mod-php
RUN apt install -y iproute2 default-jre bc
RUN apt install -y build-essential git
RUN apt install -y wireguard 
RUN apt install -y zsh
RUN apt-get -y install xz-utils
RUN curl -fsSL https://deb.nodesource.com/setup_18.x |sudo -E bash - && \
    sudo apt-get install -y nodejs
RUN sudo -S npm install -g --unsafe-perm node-red
RUN service ssh start
RUN echo 'root:admin' | chpasswd
COPY wireguard /etc/init.d/
RUN echo "clear" >> /etc/bash.bashrc
RUN echo "figlet -t -c youngstorage | lolcat" >> /etc/bash.bashrc
RUN echo "echo ''" >> /etc/bash.bashrc
RUN curl -fsSL https://code-server.dev/install.sh | sh
COPY /code-server/login.html /usr/lib/code-server/src/browser/pages/
COPY /code-server/login.css /usr/lib/code-server/src/browser/pages/
COPY /code-server/global.css /usr/lib/code-server/src/browser/pages/
COPY /code-server/logo.png /usr/lib/code-server/src/browser/media/
COPY /code-server/workbench.html /usr/lib/code-server/lib/vscode/out/vs/code/browser/workbench/
COPY /index.html /var/www/html/
#peer variabl
COPY {os.path.join("wgClients", username, peer,username+'-'+peer)}.conf /etc/wireguard/wg0.conf
#Username Variable
RUN adduser {username} --gecos "" --disabled-password
RUN echo "{username}:{username}@321" | sudo chpasswd
RUN usermod -aG sudo {username}
COPY setup.sh /
COPY .bashrc /home/{username}/
COPY /settings.js /home/{username}/.node-red/
RUN chmod +x setup.sh
CMD ["./setup.sh"]
'''


def setupSh(username: str):
    return f'''#!/bin/sh
#services start
wg-quick up wg0 #Peer Variable
iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
sudo iptables -A FORWARD  -p tcp -i wg0 --dst 172.20.0.0/16
wget https://github.com/just-containers/s6-overlay/releases/download/v3.1.0.1/s6-overlay-noarch.tar.xz /tmp
tar -Jxpf s6-overlay-noarch.tar.xz
wget https://github.com/just-containers/s6-overlay/releases/download/v3.1.0.1/s6-overlay-x86_64.tar.xz /tmp
nohup tar -Jxpf s6-overlay-x86_64.tar.xz
rm -rf /tmp s6-overlay-noarch.tar.xz
rm -rf /tmp s6-overlay-x86_64.tar.xz
mkdir /tmp
chmod 777 /tmp
nohup /usr/sbin/sshd -D &

# htdocs symlink
mkdir /home/{username}/htdocs #username variable
cp /var/www/html/index.html /home/{username}/htdocs/
rm -rf /var/www/html
ln -s /home/{username}/htdocs/ /var/www/html #username variable


#apache config file symlink
mkdir /home/{username}/htconfig/
cp -rn /etc/apache2/sites-available/* /home/{username}/htconfig
rm -rf /etc/apache2/sites-available
ln -s /home/{username}/htconfig /etc/apache2/sites-available

# change permissions to htdocs
cd /home
chmod 775 {username} #username variable
chown -R {username}:{username} /home/{username}/htdocs #username variable
adduser www-data {username} #username variable
# echo "Options +FollowSymLinks +SymLinksIfOwnerMatch" > /home/{username}/htdocs/html/.htaccess #username variable
cd /home/{username}/htdocs #username variable
chmod o+x *

#chaning permissions to htconfig
chown -R {username}:{username} /home/{username}/htconfig
chown -R {username}:{username} /home/{username}/.ssh
chown -R {username}:{username} /home/{username}/.bashrc

#remove password
echo "{username} ALL=(ALL:ALL) NOPASSWD: /usr/sbin/a2ensite" | sudo tee -a /etc/sudoers.d/{username} > /dev/null
echo "{username} ALL=(ALL:ALL) NOPASSWD: /usr/sbin/a2enmod" | sudo tee -a /etc/sudoers.d/{username} > /dev/null
echo "{username} ALL=(ALL:ALL) NOPASSWD: /usr/sbin/a2dismod" | sudo tee -a /etc/sudoers.d/{username} > /dev/null
echo "{username} ALL=(ALL:ALL) NOPASSWD: /usr/sbin/a2dissite" | sudo tee -a /etc/sudoers.d/{username} > /dev/null

cd /home/{username}
touch init.sh
chmod +x  init.sh
chown -R {username}:{username} init.sh
./init.sh
#code-server configuration
cd /home/{username} #username variable
mkdir .config
mkdir .config/code-server
cd .config/code-server
#username variable
whoami >> id
echo "bind-addr: 0.0.0.0:1111
auth: password
password: {username}@321 
cert: false" > config.yaml
echo "hello" > hello.txt
service apache2 start
chown -R {username}:{username} /home/{username}/.node-red/
npm i bcryptjs -g
# cd /home/{username}/{username}
#username variable
su {username} <<EOF 
node-red &
cd /home/{username} && ./init.sh
echo {username}@321 | sudo -S service apache2 restart
nohup code-server
EOF
'''


def IpRange65535(ipaddress):
    ip = list(map(int, str(ipaddress).split(".")))
    for i in ip:
        if i > 255:
            return {"message": "not a ipv4 format", "status": False}

    if len(ip) == 4:
        if ip[3] < 255:
            ip[3] += 1
        elif ip[3] == 255:
            if ip[2] < 255:
                ip[3] = 0
                ip[2] += 1
            else:
                return {"message": "End of ipv4 list", "status": False}
        ip = list(map(str, ip))
        return {"message": ".".join(ip), "status": True}
    else:
        return {"message": "not a ipv4 format", "status": False}

# docker image build function
def imageBuild(username: str):
    source = os.path.join(os.getcwd(), "source")
    cmd = ["docker", "build", "-t", f"{username}", f"{source}"]
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    mqtt_client.publish("/topic/sample", "image build started.....")
    # Read and print the output
    for line in process.stdout:
        print(line.decode().rstrip())

    # Wait for the process to finish
    process.wait()
    mqtt_client.publish("/topic/sample", "image build done!!")

# docker container run function
def containerRun(username: str):
    cmd = ["docker", "run", "--hostname",
           "youngstorage", "--name", f"{username}", "-d",
           "--cap-add=NET_ADMIN",
           f"{username}"]
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    mqtt_client.publish("/topic/sample", "container run started.....")
    # Read and print the output
    for line in process.stdout:
        mqtt_client.publish("/topic/sample", line.decode().rstrip())

    # Wait for the process to finish
    process.wait()
    mqtt_client.publish("/topic/sample", "container successfully running.....")