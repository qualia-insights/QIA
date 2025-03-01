# ============================================================================
# QIA - Qualia Insights Accouting
# Copyright (C) 2025 Todd & Linda Rovito / Qualia Insights, LLC
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
# ============================================================================
# this is container is for QIA purposes
# This container is designed for hosts of Raspberry Pi OS which is Debian Bookworm
# includes Python, numpy, iPython, 
#
# To build container:
#	nohup podman image build -f qia.pm -t qia:20240323 . > ~/temp/20240323_qia.log 2>&1 &
#
# to run container:
#   podman run -it --rm --mount type=bind,source=/home/rovitotv,target=/home/rovitotv qia:20240323 
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
