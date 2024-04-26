FROM ubuntu:latest
LABEL authors="gabin"

ENTRYPOINT ["top", "-b"]