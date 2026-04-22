FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Etc/UTC

# Fix interactive tzdata issues and install Mininet/Ryu dependencies
RUN apt-get update && \
    apt-get install -y tzdata && \
    apt-get install -y \
    mininet \
    python3-pip \
    iproute2 \
    net-tools \
    iputils-ping \
    openvswitch-switch \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install ryu eventlet==0.30.2

WORKDIR /app

CMD service openvswitch-switch start && /bin/bash
