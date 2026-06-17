FROM alpine:3.20

RUN apk add --no-cache \
    bash \
    curl \
    jq \
    python3 \
    rtl-sdr \
    git \
    cmake \
    make \
    gcc \
    g++ \
    musl-dev \
    sox \
    lame \
    busybox-extras

RUN git clone https://github.com/EliasOenal/multimon-ng.git /tmp/multimon-ng && \
    cd /tmp/multimon-ng && \
    mkdir build && \
    cd build && \
    cmake .. && \
    make && \
    make install && \
    rm -rf /tmp/multimon-ng

COPY run.sh /run.sh
COPY same_eas.py /same_eas.py
COPY web.py /web.py

RUN chmod +x /run.sh

CMD ["/run.sh"]
