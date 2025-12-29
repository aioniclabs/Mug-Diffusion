# Mug Diffusion with Docker

This document provides instructions on how to build and run the Mug Diffusion project using Docker for command-line based chart generation.

## Prerequisites

1.  **Docker**: Ensure Docker is installed and running on your system.
2.  **NVIDIA GPU**: A compatible NVIDIA GPU is required.
3.  **NVIDIA Container Toolkit**: You must have the NVIDIA Container Toolkit installed to allow Docker to access your GPU. [Installation Guide](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html).
4.  **Model Files**: Download the `ckpt.zip` file containing the model weights. Create a `models` directory in the project root if it doesn't exist. Unzip the file and place the `ckpt` folder inside the `models` directory. The final structure must be `models/ckpt/model.ckpt` and `models/ckpt/model.yaml`.

## 1. The Dockerfile

A `Dockerfile` is provided in the root of the project to containerize the application for a GPU environment.

## 2. The Generation Script (`generate.py`)

A command-line interface script, `generate.py`, is included to act as the entrypoint for the Docker container. It calls the core generation logic from the web UI.

## 3. Building and Running

Follow these steps from your terminal in the project's root directory.

### Step 1: Build the Docker Image

This command builds the container image and tags it as `mug-diffusion-gpu`.

```bash
docker build -t mug-diffusion-gpu .
```

### Step 2: Run the Generation

This command runs the container, generates the chart, and saves the output to your local machine.

**Before running, make sure to:**
1.  Create two local directories: `input` and `output`.
2.  Place your audio file (e.g., `my_song.mp3`) inside the `input` directory.
3.  Replace the placeholder values in the command below.

```bash
docker run --rm --gpus all \
  -v "$(pwd)/input":/app/input \
  -v "$(pwd)/output":/app/outputs \
  mug-diffusion-gpu \
  --audio-path /app/input/welcome_to_the_Jungle.mp3 \
  --title "welcome to the Jungle" \
  --artist "Guns N' Roses"
```

The final `.osz` file (a zip archive containing the `.osu` file and audio) will be saved in your local `output` directory.

```
