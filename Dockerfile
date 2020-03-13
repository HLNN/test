FROM debian:buster

RUN apt-get -y update; apt-get install -y python3-pip python3-dev python3-setuptools python3-wheel x11-apps

ENV DISPLAY :0
CMD xeyes

# ENTRYPOINT ["/bin/bash", ""]
