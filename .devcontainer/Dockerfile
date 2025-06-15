FROM nvcr.io/nvidia/tensorflow:24.02-tf2-py3

# --- Set environment variables ---
ENV DEBIAN_FRONTEND=noninteractive
ENV LANG=C.UTF-8

# --- Install system dependencies ---
RUN apt-get update && apt-get install --no-install-recommends -y \
    libgl1-mesa-glx \
    libosmesa6-dev \
    libglfw3 \
    libglfw3-dev \
    libglew-dev \
    libxrender1 \
    libxext6 \
    libsm6 \
    unzip \
    curl \
    git \
    nano \
    build-essential \
    liblcm-dev \
    libboost-all-dev \
    libeigen3-dev \
    ffmpeg \
    xvfb \
    wget \
    libjpeg-dev \
    cmake \
    && rm -rf /var/lib/apt/lists/*

# --- Upgrade pip and install Python dependencies ---
# RUN pip install --upgrade pip== setuptools==59.5.0 wheel

RUN wget https://github.com/Kitware/CMake/releases/download/v3.27.9/cmake-3.27.9-linux-x86_64.sh && \
    bash cmake-3.27.9-linux-x86_64.sh --skip-license --prefix=/usr/local && \
    rm cmake-3.27.9-linux-x86_64.sh

RUN pip install "pip<21" "setuptools<58"

RUN pip install \
    numpy==1.26 \
    jax[cuda] \
    --find-links https://storage.googleapis.com/jax-releases/jax_cuda_releases.html 

RUN pip install flax \
    tqdm \
    pillow \
    opencv-python==4.5.5.64 \
    gym==0.18.0 \
    tensorflow-probability==0.23.0 \
    ml_collections \
    wandb \
    dm_control==0.0.300771433 \
    pybullet==3.2.5 \
    attrs==23.1.0 \
    filterpy==1.4.5

# --- Clone Walk in the Park repo ---
WORKDIR /workspace
RUN git clone --recurse-submodules  https://github.com/karthiks1701/walk_in_the_park.git
WORKDIR /workspace/walk_in_the_park

# --- Copy Unitree SDK binary and build ---
WORKDIR /workspace/walk_in_the_park/real/third_party/unitree_legged_sdk
# Copy .so into /usr/local/lib so linker can find it
COPY .devcontainer/libunitree_legged_sdk_amd64.so /usr/local/lib/
    
# Update linker cache to register new library
RUN ldconfig
# Build inside 'build' directory
RUN mkdir build && cd build && cmake .. && make -j$(nproc)
# Optionally copy the built robot_interface .so back to main directory
RUN cp build/robot_interface*.so /workspace/walk_in_the_park/

WORKDIR /workspace/walk_in_the_park
# --- Set entrypoint ---
CMD ["/bin/bash"]