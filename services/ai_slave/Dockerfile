FROM arm32v7/python:3.5

ENV HOME /root
ENV PYTHONPATH "/usr/lib/python3/dist-packages:/usr/local/lib/python3.5/site-packages"

RUN apt-get update && apt-get install -y build-essential \
    curl \
    netcat \
    pkg-config \
    python \
    python-dev \
    python-pip \
    python-h5py \
    unzip \
    libblas3 \
    liblapack3 \
    liblapack-dev \
    libblas-dev \
    libhdf5-dev \
    gcc \
    gfortran

# set current working directory
WORKDIR /usr/src/ml-framework

# copy everything into working directory
COPY . /usr/src/ml-framework

# install prebuild tensorflow image
RUN pip install wheels/tensorflow-1.14.0-cp35-none-linux_armv7l.whl
RUN pip install wheels/scipy-1.3.3-cp35-cp35m-linux_armv7l.whl
RUN pip install wheels/numpy-1.18.5-cp35-cp35m-linux_armv7l.whl

# install keras dependencies
RUN pip install keras==2.3.0

# install pillow and its dependencies
RUN apt-get install -y python-pil
RUN pip install pillow

RUN pip install -r requirements.txt

CMD ["/bin/bash", "/usr/src/ml-framework/entrypoint.sh"]








































# FROM arm32v7/ubuntu:18.04
#
# ENV DEBIAN_FRONTEND noninteractive
#
# # install initial packages
# RUN apt-get update && apt-get install -y build-essential \
#     cmake \
#     netcat \
#     wget \
#     gcc \
#     pkg-config \
#     libswscale-dev \
#     libtbb2 \
#     libtbb-dev \
#     libjpeg-dev \
#     libpng-dev \
#     libtiff-dev \
#     libavformat-dev \
#     python3 \
#     python3-dev \
#     python3-pip \
#     python3-h5py \
#     unzip \
#     libblas3 \
#     liblapack3 \
#     liblapack-dev \
#     libblas-dev \
#     gfortran \
#     python-opencv \
#     python-pandas
#
# # RUN pip3 install opencv-python
# # RUN mkdir -p ~/opencv cd ~/opencv && \
# #      wget https://github.com/opencv/opencv/archive/3.0.0.zip && \
# #      unzip 3.0.0.zip && \
# #      rm 3.0.0.zip && \
# #      mv opencv-3.0.0 OpenCV && \
# #      cd OpenCV && \
# #      mkdir build && \
# #      cd build && \
# #      cmake \
# #      -D WITH_QT=ON \
# #      -D WITH_OPENGL=ON \
# #      -D FORCE_VTK=ON \
# #      -D WITH_TBB=ON \
# #      -D WITH_GDAL=ON \
# #      -D WITH_XINE=ON \
# #      -D BUILD_EXAMPLES=ON .. && \
# #      make -j4 && \
# #      make install && \
# #      ldconfig
#
# WORKDIR /usr/src/ml-framework
# # COPY ./wheels /usr/src/ml-framework/wheels
# #
# # RUN pip3 install wheels/numpy-1.18.5-cp35-cp35m-linux_armv7l.whl
# # RUN pip3 install wheels/scipy-1.5.1-cp37-cp37m-linux_armv7l.whl
# # RUN pip3 install wheels/scikit_learn-0.23.2-cp37-cp37m-linux_armv7l.whl
# # RUN pip3 install wheels/tensorflow-1.14.0-cp37-none-linux_armv7l.whl
# #
# # COPY ./requirements.txt /usr/src/ml-framework/requirements.txt
# #
# # RUN pip3 install -r requirements.txt
# #
# # RUN pip3 install keras==2.2.3
# #
# # COPY ./entrypoint.sh /usr/src/ml-framework/entrypoint.sh
# # RUN chmod +x /usr/src/ml-framework/entrypoint.sh
#
# COPY . /usr/src/ml-framework
#
# CMD ["/bin/bash", "/usr/src/ml-framework/entrypoint.sh"]
