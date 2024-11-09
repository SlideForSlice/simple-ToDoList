FROM ubuntu:latest
LABEL authors="kenig"

ENTRYPOINT ["top", "-b"]