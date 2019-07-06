FROM archlinux/base:latest
MAINTAINER ToraNova (chia_jason96@live.com)

RUN pacman -Syyu --noconfirm
RUN pacman-db-upgrade
RUN pacman -S --noconfirm python3 python-pip git mosquitto
RUN yes 36 | pacman -S base
RUN git clone https://github.com/toranova/rapidflask /home
RUN pip3 install gevent
RUN pip3 install sqlalchemy
RUN pip3 install flask flask-wtf flask-login flask-admin
RUN pip3 install flask-socketio flask-mail
RUN pip3 install paho-mqtt
EXPOSE 1883 80 443

# build with
# sudo docker build -t rapidflask:latest .
# within the dockerbuild dir
