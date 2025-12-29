
# Use an NVIDIA CUDA runtime as a parent image
FROM nvidia/cuda:12.1.1-cudnn8-devel-ubuntu22.04

# Set environment variables to prevent interactive prompts during installation
ENV DEBIAN_FRONTEND=noninteractive

# Set the working directory in the container
WORKDIR /app

# Install Python, pip, FFmpeg, and the necessary build tools
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    python3.10 \
    python3.10-dev \
    python3-pip \
    ffmpeg \
    build-essential && \
    rm -rf /var/lib/apt/lists/*

# Make python3 the default python
RUN ln -s /usr/bin/python3 /usr/bin/python

# Install the GPU-enabled version of PyTorch for CUDA 12.1
RUN pip install torch==2.1.0 torchvision==0.16.0 torchaudio==2.1.0 --index-url https://download.pytorch.org/whl/cu121

# Copy the entire project directory into the container FIRST
COPY . .

# Now, install the requirements, including the local .tar.gz file
RUN pip install --no-cache-dir -r requirements.txt

# Set the entrypoint to run the generation script
ENTRYPOINT ["python", "generate.py"]

