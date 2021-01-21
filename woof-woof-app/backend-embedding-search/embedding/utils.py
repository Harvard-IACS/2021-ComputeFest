import os
import requests
import zipfile
import tarfile

DATASET_PATH = "/datastore"
IMAGES_ZIP_URL = "https://computefest2021images.s3.amazonaws.com/small/resized_dogs_small.zip"
DOGS_METADATA_URL = "https://computefest2021images.s3.amazonaws.com/small/dog_data_small.zip"
EMBEDDINGS_ZIP_URL = "https://computefest2021images.s3.amazonaws.com/small/embeddings_small.zip"

# Check if /datastore exists
if not os.path.exists(DATASET_PATH):
    DATASET_PATH = "datastore"

def download_file(packet_url, base_path="", extract=False, headers=None):
    if base_path != "":
        if not os.path.exists(base_path):
            os.mkdir(base_path)
    packet_file = os.path.basename(packet_url)
    with requests.get(packet_url, stream=True, headers=headers) as r:
        r.raise_for_status()
        with open(os.path.join(base_path, packet_file), 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

    if extract:
        if packet_file.endswith(".zip"):
            with zipfile.ZipFile(os.path.join(base_path, packet_file)) as zfile:
                zfile.extractall(base_path)
        else:
            packet_name = packet_file.split('.')[0]
            with tarfile.open(os.path.join(base_path, packet_file)) as tfile:
                tfile.extractall(base_path)

def ensure_data_loaded():
    try:
        print("ensure_data_loaded()")

        # Check if images are already downloaded
        images_path = os.path.join(DATASET_PATH,"resized_dogs_small")
        if not os.path.exists(images_path):
            download_file(IMAGES_ZIP_URL, base_path=DATASET_PATH, extract=True)

        dogs_metadata_path = os.path.join(DATASET_PATH,"dog_data_small")
        if not os.path.exists(dogs_metadata_path):
            download_file(DOGS_METADATA_URL, base_path=DATASET_PATH, extract=True)

        # Check if images are already downloaded
        embeddings_path = os.path.join(DATASET_PATH,"embeddings_small")
        if not os.path.exists(embeddings_path):
            download_file(EMBEDDINGS_ZIP_URL, base_path=DATASET_PATH, extract=True)


    except Exception as exc:
        print(str(exc))
        message = str(exc)