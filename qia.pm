# this is a small container that TVR can use for QIA purposes
# This container is designed for hosts of Raspberry Pi OS which is Debian Bookworm
# includes Python, numpy, iPython, 
#
# To build container:
#	nohup podman image build -f qia.pm -t qia:20240323 . > ~/temp/20240323_qia.log 2>&1 &
#
# to run container:
#   podman run -it --rm --mount type=bind,source=/home/rovitotv,target=/home/rovitotv qia:20240323 
#
# The above command can be used as an alias.  Run Jupyter Lab container as
# detached then use podman logs container_ID to get Jupyter Lab Token
FROM debian:bookworm

MAINTAINER rovitotv@gmail.com

# set locale setting inside of Docker container
RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y locales \
    && sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen \
    && dpkg-reconfigure --frontend=noninteractive locales \
    && update-locale LANG=en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LC_ALL en_US.UTF-8

# install the tzdata first with the environment variables 
RUN DEBIAN_FRONTEND="noninteractive" TZ="America/New_York" apt-get -y install tzdata

RUN apt-get update && apt-get install -y \
	curl \
	vim \
	bzip2 \
	git \
	tmux \
	zip \
	unzip \
        iputils-ping \
	libpng-dev \
	libjpeg-dev \
	python3-dev \
	python3-pip \
	libatlas-base-dev \
        python3-numpy \
        python3-scipy \
        python3-pandas \
        python3-matplotlib \
        ipython3 

## Debian Bookworm requires that we delete this file so pip packages can be installed
# RUN rm -rf /usr/lib/python3.11/EXTERNALLY-MANAGED
# RUN pip3 install --upgrade pip
# RUN pip3 install ipython

WORKDIR /home/rovitotv
ENV SHELL /bin/bash
ENTRYPOINT ["/bin/bash"]
