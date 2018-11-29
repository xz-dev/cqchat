# version: v2.2.6
FROM ubuntu
MAINTAINER XZ-Dev <xiangzhedev@gmail.com>
WORKDIR /root
USER root
ENV LANG C.UTF-8
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update
RUN apt-get dist-upgrade -y
RUN apt-get install \
      make \
      cpanminus \
      libnet-ssleay-perl \
      libcrypt-openssl-bignum-perl \
      libcrypt-openssl-rsa-perl -y
RUN cpanm IO::Socket::SSL
RUN cpanm Mojo::Webqq
RUN cpanm Webqq::Encryption
Run apt-get install python3-pip -y
RUN pip3 install urwid requests
RUN apt-get autoremove -y && \
      apt-get clean -y
CMD ["python3", "-m", "Mojo-Webqq-Python"]

# echo N | sudo tee /sys/module/overlay/parameters/metacopy
