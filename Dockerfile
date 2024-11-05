FROM ubuntu:latest

RUN apt-get update && \
    apt-get install -y gcc gdb make g++ git python3 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN git config --global pull.rebase false

ARG GITHUB_PROJECT_NAME

RUN mkdir /root/work
WORKDIR /root/work

COPY entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/entrypoint.sh

ENTRYPOINT ["entrypoint.sh"]
CMD ["tail", "-f", "/dev/null"]
