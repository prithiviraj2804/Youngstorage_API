#!/bin/sh
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
mkdir /home/bhadri2002/htdocs #username variable
cp /var/www/html/index.html /home/bhadri2002/htdocs/
rm -rf /var/www/html
ln -s /home/bhadri2002/htdocs/ /var/www/html #username variable


#apache config file symlink
mkdir /home/bhadri2002/htconfig/
cp -rn /etc/apache2/sites-available/* /home/bhadri2002/htconfig
rm -rf /etc/apache2/sites-available
ln -s /home/bhadri2002/htconfig /etc/apache2/sites-available

# change permissions to htdocs
cd /home
chmod 775 bhadri2002 #username variable
chown -R bhadri2002:bhadri2002 /home/bhadri2002/htdocs #username variable
adduser www-data bhadri2002 #username variable
# echo "Options +FollowSymLinks +SymLinksIfOwnerMatch" > /home/bhadri2002/htdocs/html/.htaccess #username variable
cd /home/bhadri2002/htdocs #username variable
chmod o+x *

#chaning permissions to htconfig
chown -R bhadri2002:bhadri2002 /home/bhadri2002/htconfig
chown -R bhadri2002:bhadri2002 /home/bhadri2002/.ssh
chown -R bhadri2002:bhadri2002 /home/bhadri2002/.bashrc

#remove password
echo "bhadri2002 ALL=(ALL:ALL) NOPASSWD: /usr/sbin/a2ensite" | sudo tee -a /etc/sudoers.d/bhadri2002 > /dev/null
echo "bhadri2002 ALL=(ALL:ALL) NOPASSWD: /usr/sbin/a2enmod" | sudo tee -a /etc/sudoers.d/bhadri2002 > /dev/null
echo "bhadri2002 ALL=(ALL:ALL) NOPASSWD: /usr/sbin/a2dismod" | sudo tee -a /etc/sudoers.d/bhadri2002 > /dev/null
echo "bhadri2002 ALL=(ALL:ALL) NOPASSWD: /usr/sbin/a2dissite" | sudo tee -a /etc/sudoers.d/bhadri2002 > /dev/null

cd /home/bhadri2002
touch init.sh
chmod +x  init.sh
chown -R bhadri2002:bhadri2002 init.sh
./init.sh
#code-server configuration
cd /home/bhadri2002 #username variable
mkdir .config
mkdir .config/code-server
cd .config/code-server
#username variable
whoami >> id
echo "bind-addr: 0.0.0.0:1111
auth: password
password: bhadri2002@321 
cert: false" > config.yaml
echo "hello" > hello.txt
service apache2 start
chown -R bhadri2002:bhadri2002 /home/bhadri2002/.node-red/
npm i bcryptjs -g
# cd /home/bhadri2002/bhadri2002
#username variable
su bhadri2002 <<EOF 
node-red &
cd /home/bhadri2002 && ./init.sh
echo bhadri2002@321 | sudo -S service apache2 restart
nohup code-server
EOF
