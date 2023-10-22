# Preprocessor command line assignement
Command line that does the job specified by the assignement (private instructions). It uses the "[typer library](https://typer.tiangolo.com)" to make a proper CLI.

## Prerequisites
The code has been implemented in python 3.8. Here's an example to get this up and running using a conda virtual env:

```
conda create -n assignement python=3.8
conda activate assignement
pip install Pillow "typer[all]" requests
```

## Usage

```bash
# inside the project directory
python main.py --help
```

The help command explains all the defined options:
- `--target-directory`: path of the directory where the dataset will be stored. A sample directory is provided in this repo: `./target_dataset`, but if the specified path does not exist, the script will create it. If the directory already exists, the script will update the existing dataset.
- `--source-directory`: path of the directory that contains all the raw images. A sample directory is provided in this repo : `./raw_images`.
- `--api-url`: URL of the JSON API that contains the labels of the raw images. A sample API is provided by default [here](https://my-json-server.typicode.com/Barchid/preprocessor_assignement/images)
- `--height` and `--width`: the dimensions of the new processed images

### Basic Usage
The most basic usage using the default values is :

```bash
python main.py --target-directory target_dataset
```