FROM bamos/ubuntu-opencv-dlib-torch:ubuntu_14.04-opencv_2.4.11-dlib_19.0-torch_2016.07.12
MAINTAINER Brandon Amos <brandon.amos.cs@gmail.com>

# TODO: Should be added to opencv-dlib-torch image.
RUN ln -s /root/torch/install/bin/* /usr/local/bin

RUN apt-get update -y && apt-get install -y \
    curl \
    git \
    graphicsmagick \
    python-dev \
    python-pip \
    python-numpy \
    python-nose \
    python-scipy \
    python-pandas \
    python-protobuf\
    wget \
    zip \
    supervisor \
    && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*


ADD . /code
WORKDIR /code

# Seutup supervisor
RUN mkdir -p /var/log/supervisor
ADD ./conf/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Install and pushing PIP to latest version
RUN apt-get install -y python-pip
RUN pip install --ignore-installed pip
RUN pip install -r requirements.txt

ENV PYTHONPATH $PYTHONPATH:/code
EXPOSE 8000

RUN cd /code/trained_models && \
    ./get-models.sh
