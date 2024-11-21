FROM osrf/ros:noetic-desktop-focal

ENV DEBIAN_FRONTEND=noninteractive

# Builder dependencies installation
RUN apt-get update \
    && apt-get install -qq -y --no-install-recommends \
    build-essential \
    cmake \
    git \
    libssl-dev \
    libusb-1.0-0-dev \
    pkg-config \
    libgtk-3-dev \
    libglfw3-dev \
    libgl1-mesa-dev \
    libglu1-mesa-dev \    
    curl \	
    libusb-1.0-0 \
    udev \
    apt-transport-https \
    ca-certificates \
    curl \
    swig \
    wget \
    software-properties-common \
    python3-pip

RUN apt-get update && apt-get install -y --no-install-recommends \
    ros-noetic-desktop-full=1.5.0-1* \
    ros-noetic-gazebo* ros-noetic-rviz \
    tmux ros-noetic-teleop-twist-keyboard \
    && rm -rf /var/lib/apt/lists/*

RUN echo "source /opt/ros/noetic/setup.bash " >> ~/.bashrc && \
    echo "source /workspace/mist_ws/devel/setup.bash " >> ~/.bashrc


COPY ./setup.sh /tmp/setup.sh