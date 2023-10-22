import typer
from typing import List
from typing_extensions import Annotated
from pathlib import Path
import logging
from PIL import Image
import requests

# make INFO logs visible in the command line
logging.getLogger().setLevel(logging.INFO)


def main(
    target_directory: Annotated[
        Path,
        typer.Option(
            exists=False,
            file_okay=False,
            dir_okay=True,
            readable=True,
            writable=True,
            resolve_path=True,
        ),
    ],
    source_directory: Annotated[
        Path,
        typer.Option(
            exists=True,
            file_okay=False,
            dir_okay=True,
            readable=True,
            resolve_path=True,
        ),
    ] = Path("./raw_images"),
    api_url: str = "https://my-json-server.typicode.com/Barchid/preprocessor_assignement/images",
    height: int = 512,
    width: int = 512
):
    # iterate through all .png files from the directory of raw images
    logging.info(f"\nIterate through .png image files from {source_directory}\n#############\n")

    for png_file in source_directory.glob("*.png"):
        process_png_file(png_file, height, width, target_directory, api_url)


def process_png_file(png_file: Path, height: int, width: int, target_directory: Path, api_url: str):
    """Processes the specified .png image. This function applies the following steps:
        1. Resizes the image to the dimensions (height x width)
        2. Converts to grayscale
        3. Retrieves the label name from the JSON API 
        4. Stores the processed image to the target directory

    Args:
        png_file (Path): the path of the .png file
        height (int): the new height of the image
        width (int): the new width of the image
        target_directory (Path): the path of the target directory
        api_url (str): the url of the JSON API containing the label of the .png image
    """
    logging.info(f"Processing {png_file}...")

    image = Image.open(png_file)

    # resize to 512x512
    image = image.resize((width, height))

    # convert to grayscale
    image = image.convert('L')

    # fetch labels from API
    label = fetch_label_from_url(api_url, png_file)
    
    if label is not None:
        store_result_in_target(image, label, png_file, target_directory)
        logging.info(f"Succeeded processing and storing f{png_file.name}\n")
    else:
        logging.warning(f"The label of {png_file} is not known by the JSON API {api_url}. Go to the next sample\n.")


def create_target_dataset(target_directory: Path):
    """Creates the target directory if it does not exist.

    Args:
        target_directory (Path): the path of the target directory.
    """
    if target_directory.exists():
        logging.info(
            f"Target directory already exists. This script will update the existing directory.\n")
    else:
        logging.info(
            f"Target directory does not exist. This script will create a new directory.\n")

    target_directory.mkdir(exist_ok=True, parents=True)


def fetch_label_from_url(api_url: str, png_file: Path):
    """Fetches the label of the .png file from the specified JSON API URL

    Args:
        api_url (str): the URL of the JSON API containing the label name
        png_file (Path): the target .png file

    Returns:
        str|None: the label name related to the .png file. If the API call fails, returns None.
    """
    # get ID from the png filename
    id = png_file.stem

    # HTTP GET request to the JSON API
    resp = requests.get(f"{api_url}/{id}")
    
    if resp.status_code == requests.codes.ok:
        print(logging.info(f"{resp.status_code}"))
        data = resp.json()

        # Only return the label (=classname)
        return data["classname"]
    else:
        return None


def store_result_in_target(image: Image, label: str, png_file: Path, target_directory: Path):
    """Stores the processed image in the target directory.

    Args:
        image (Image): the processed image (resized and grayscale) to store
        label (str): the fetched label name
        png_file (Path): the path of the .png file
        target_directory (Path): the target directory where all processed images are stored
    """
    class_directory = target_directory / label

    # the label does not exist in the target dataset
    if not class_directory.exists():
        logging.info(
            f"The label '{label}' is not known in {target_directory}. Creating the new class...")

        # mkdir the new directory in the dataset
        class_directory.mkdir(exist_ok=True, parents=True)

    # store the image
    image.save(class_directory / png_file.name)


if __name__ == "__main__":
    typer.run(main)
