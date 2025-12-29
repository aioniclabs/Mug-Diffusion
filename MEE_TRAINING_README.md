# Training and Fine-Tuning Mug Diffusion Models

This document provides a high-level guide on how to train a new charting model from scratch or fine-tune the existing model for a specialized purpose.

---

## System and Hardware Requirements

Training and fine-tuning are demanding tasks that require specific hardware.

*   **GPU**: A powerful, modern NVIDIA GPU is **essential**.
    *   **Minimum for Fine-Tuning**: NVIDIA RTX 3060 (12GB VRAM) or better. You may be able to fine-tune with an 8GB card like an RTX 3070 or 4060, but you will be limited to a very small `batch_size`, which can affect training stability.
    *   **Recommended for Training from Scratch**: NVIDIA RTX 3090 (24GB VRAM), RTX 4090 (24GB VRAM), or professional-grade cards like the A100. Training from scratch on a card with less than 24GB of VRAM will be extremely slow and difficult.
*   **System RAM**: 32 GB is recommended, 64 GB or more is ideal, especially during data pre-processing.
*   **Storage**: A fast SSD (NVMe is best) is highly recommended. The dataset can be very large (hundreds of gigabytes), and fast storage will significantly speed up data loading during training.
*   **Operating System**: Linux is the standard for deep learning development and is strongly recommended.

**Warning:** Both processes are computationally expensive. Training from scratch can take days or weeks, even on high-end hardware.

---

## Part 1: Training a New Model from Scratch

Training from scratch is a major undertaking that teaches the AI the fundamental relationship between audio and charting patterns.

### Stage 1: Data Preparation

This is the most critical and labor-intensive stage. The quality of your model will directly depend on the quality and size of your dataset.

1.  **Gather Source Data**:
    *   Collect a large and diverse set of high-quality `.osu` chart files and their corresponding audio files (`.mp3`, `.ogg`, etc.). The original model used thousands of charts from public communities like osu! and Malody.
    *   The list of beatmaps used for the original model can be found at [https://mugdiffusion.keytoix.vip/dataset.html](https://mugdiffusion.keytoix.vip/dataset.html). You can use the Beatmap IDs from this list to download the source files from osu! servers.

2.  **Pre-process the Data**:
    *   The raw chart and audio files must be converted into a format the model can understand. The `scripts/` directory contains several Python files for this purpose.
    *   `prepare_beatmap.py`: This script is likely used to convert `.osu` files into a numerical representation (like a piano roll).
    *   `prepare_beatmap_features.py`: This script analyzes the charts to extract conditioning features like difficulty (SR/MSD) and patterns (stream, jumpstream, etc.). It uses `MinaCalc` for this analysis.
    *   You will need to study and potentially adapt these scripts to process your collection of charts and organize the output into a structured dataset directory.

### Stage 2: Configuration

Training is controlled by YAML configuration files located in the `configs/` directory.

1.  **Create a Dataset Configuration**: You will need to create a new `.yaml` file that defines the structure of your dataset and points the training script to your pre-processed files.
2.  **Create a Model Configuration**: You can copy an existing configuration like `configs/mug/mug_diffusion.yaml` as a starting point. This file defines the model's architecture and training parameters.
3.  **Set Training Parameters**: Inside your main configuration file, you will set crucial hyperparameters like `base_learning_rate`, `batch_size`, and the total number of training steps.

### Stage 3: Running the Training

The training process is launched using the `main.py` script.

1.  **Launch the Training Job**: Execute a command from your terminal, pointing to your custom configuration file.

    ```bash
    # Example command to start training from scratch on the first GPU
    python main.py --train -b configs/your_new_model_config.yaml --gpus 0,
    ```

2.  **Monitor and Wait**: The script will begin the training process. It will periodically save model checkpoints (your new `.ckpt` files) to a `logs/` directory. This can take days or even weeks to complete.

---

## Part 2: Fine-Tuning an Existing Model

Fine-tuning (a form of transfer learning) is a much more practical approach for specializing the model. It takes the existing pre-trained model and adjusts it with a smaller, targeted dataset.

### Why Fine-Tune?

*   **Less Data Needed**: You only need a small, high-quality dataset (e.g., 100-200 charts) of the specific style you want to teach.
*   **Less Time & Cost**: Fine-tuning can take hours instead of weeks.
*   **Specialization**: You can create models that are experts in a specific niche, such as:
    *   Mimicking a specific charter's style.
    *   Excelling at a certain pattern (e.g., a "stamina" or "technical" specialist).
    *   Adapting to a different style of music.

### The Fine-Tuning Process

The process is similar to training, but with a few key differences.

1.  **Prepare a Specialized Dataset**:
    *   Gather a small, high-quality collection of charts that represent the specific style you want the model to learn.
    *   Use the same `scripts/` to pre-process this data as you would for training from scratch.

2.  **Configure for Fine-Tuning**:
    *   Copy the original model config: `cp configs/mug/mug_diffusion.yaml configs/mug/finetune_special_style.yaml`.
    *   In your new config file (`finetune_special_style.yaml`), point the data loader to your new specialized dataset.
    *   **Crucially, lower the learning rate**. Find the `base_learning_rate` parameter and set it to a value 10 to 100 times smaller than the original. This ensures you are gently adjusting the model, not overwriting its existing knowledge.

3.  **Run the Fine-Tuning Job**:
    *   The command is similar to the training command, but you must add the `-r` or `--resume` flag to load the original pre-trained model as the starting point.

    ```bash
    # Example command to start fine-tuning on the first GPU
    python main.py --train \
      -b configs/mug/finetune_special_style.yaml \
      -r models/ckpt/model.ckpt \
      --gpus 0,
    ```
    *   The `-r models/ckpt/model.ckpt` flag is the most important part. It tells the trainer to load the existing weights before beginning the fine-tuning process.

The script will then start training, saving your new, specialized model checkpoints in the `logs/` directory.

---

## Part 3: Using Docker for Training

The Docker container you built for generation can also be used for training. This is highly recommended as it provides a consistent environment. The key is to override the default command and use volume mounts to manage your data.

### Directory Setup

Before running the commands, create the following directories in your project root:

*   `my_processed_dataset/`: Place your pre-processed training data here.
*   `my_finetune_dataset/`: Place your smaller, pre-processed fine-tuning data here.
*   `logs/`: This empty directory will be used to save the model checkpoints generated by the container.

### Docker Command for Training from Scratch

This command mounts your dataset and logs directory, and then runs the `main.py` training script.

**Note**: Ensure your `.yaml` config file refers to the dataset path *inside the container* (e.g., `/app/data/my_dataset`).

```bash
docker run --rm --gpus all \
  -v "$(pwd)/my_processed_dataset":/app/data/my_dataset \
  -v "$(pwd)/logs":/app/logs \
  mug-diffusion-gpu \
  python main.py --train -b configs/your_new_model_config.yaml --gpus 0,
```

### Docker Command for Fine-Tuning

This command is very similar but points to your fine-tuning dataset and uses the `-r` flag to load the base model.

**Note**: Ensure your fine-tuning `.yaml` config file refers to the dataset path *inside the container* (e.g., `/app/data/finetune_data`).

```bash
docker run --rm --gpus all \
  -v "$(pwd)/my_finetune_dataset":/app/data/finetune_data \
  -v "$(pwd)/logs":/app/logs \
  mug-diffusion-gpu \
  python main.py --train \
    -b configs/mug/finetune_special_style.yaml \
    -r models/ckpt/model.ckpt \
    --gpus 0,
```
