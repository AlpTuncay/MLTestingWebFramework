FROM ubuntu:18.04

RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y locales \
    && sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen \
    && dpkg-reconfigure --frontend=noninteractive locales \
    && update-locale LANG=en_US.UTF-8 \
    && apt-get install -y \
        netcat \
        build-essential \
        cmake \
        git \
        wget \
        unzip \
        yasm \
        pkg-config \
        libswscale-dev \
        libtbb2 \
        libtbb-dev \
        libjpeg-dev \
        libpng-dev \
        libtiff-dev \
        libavformat-dev \
        libhdf5-dev \
        libpq-dev \
        python3.6-dev \
        python3-pip \
        && python3 -m pip install pip --upgrade

ENV LANG en_US.UTF-8
ENV LC_ALL en_US.UTF-8

RUN apt-get install -y python3.6-dev \
    && apt-get install -y python3-pip \
    && python3 -m pip install pip --upgrade

# RUN apt-get install -y \
#         netcat \
#         build-essential \
#         cmake \
#         git \
#         wget \
#         unzip \
#         yasm \
#         pkg-config \
#         libswscale-dev \
#         libtbb2 \
#         libtbb-dev \
#         libjpeg-dev \
#         libpng-dev \
#         libtiff-dev \
#         libavformat-dev \
#         libhdf5-dev \
#         libpq-dev

WORKDIR /usr/src/ml-framework

COPY ./requirements.txt /usr/src/ml-framework/requirements.txt
RUN pip3 install -r requirements.txt

RUN pip3 --no-cache-dir install \
    numpy \
    hdf5storage \
    h5py \
    scipy \
    py3nvml

RUN pip3 install opencv-python

RUN pip3 install --no-cache-dir tensorflow==1.15 keras

COPY ./entrypoint.sh /usr/src/ml-framework/entrypoint.sh
RUN chmod +x /usr/src/ml-framework/entrypoint.sh

COPY . /usr/src/ml-framework

CMD ["/bin/bash", "/usr/src/ml-framework/entrypoint.sh"]
