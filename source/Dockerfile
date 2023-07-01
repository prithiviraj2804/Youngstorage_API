FROM ubuntu:latest
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
RUN curl -fsSL https://deb.nodesource.com/setup_18.x |sudo -E bash - &&     sudo apt-get install -y nodejs
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
COPY wgClients/bhadri2002/1/bhadri2002-1.conf /etc/wireguard/wg0.conf
#Username Variable
RUN adduser bhadri2002 --gecos "" --disabled-password
RUN echo "bhadri2002:bhadri2002@321" | sudo chpasswd
RUN usermod -aG sudo bhadri2002
COPY setup.sh /
COPY .bashrc /home/bhadri2002/
COPY /settings.js /home/bhadri2002/.node-red/
RUN chmod +x setup.sh
CMD ["./setup.sh"]
