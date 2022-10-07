import os
import requests
import zipfile
import tarfile

DATASET_PATH = "/datastore"
TRAINED_MODEL_URL = "https://computefest2021images.s3.amazonaws.com/language_models/finetuned_model_c_epochs_1.zip"
DOGS_METADATA_URL = "https://computefest2021images.s3.amazonaws.com/small/dog_data_small.zip"

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
                def is_within_directory(directory, target):
                    
                    abs_directory = os.path.abspath(directory)
                    abs_target = os.path.abspath(target)
                
                    prefix = os.path.commonprefix([abs_directory, abs_target])
                    
                    return prefix == abs_directory
                
                def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
                
                    for member in tar.getmembers():
                        member_path = os.path.join(path, member.name)
                        if not is_within_directory(path, member_path):
                            raise Exception("Attempted Path Traversal in Tar File")
                
                    tar.extractall(path, members, numeric_owner=numeric_owner) 
                    
                
                safe_extract(tfile, base_path)

def ensure_data_loaded():
    try:
        print("ensure_data_loaded()")

        # Check if model is already downloaded
        model_path = os.path.join(DATASET_PATH,"trained_model")
        if not os.path.exists(model_path):
            download_file(TRAINED_MODEL_URL, base_path=DATASET_PATH, extract=True)

        dogs_metadata_path = os.path.join(TRAINED_MODEL_URL, "dog_data_small")
        if not os.path.exists(dogs_metadata_path):
            download_file(DOGS_METADATA_URL, base_path=DATASET_PATH, extract=True)

    except Exception as exc:
        print(str(exc))