import os
import io
import pandas as pd
from glob import glob
from fastapi import APIRouter, Path, Query
from starlette.responses import FileResponse
from urllib.parse import urlparse

import api.utils as api_utils

router = APIRouter()

dogs_path = os.path.join(api_utils.DATASET_PATH,"dog_data_small","dogs.csv")
dog_images_path = os.path.join(api_utils.DATASET_PATH,"resized_dogs_small")

# Dataframe to hold the dogs metadata
dogs = None

def load_dogs():
    global dogs
    if dogs is None:
        print("Loading dogs data...")
        # Load data into pandas dataframe
        dogs_with_images = glob(os.path.join(dog_images_path,"*"))

        dogs_all = pd.read_csv(dogs_path)
        # Filter the dogs with images
        id_list = []
        for path in dogs_with_images:
            id = path.split("/")[3]
            id_list.append(int(id))

        dogs = dogs_all[dogs_all["AnimalInternal-ID"].isin(id_list)]
        dogs["ImageID"] = ''

        # Find one image for very dog and set as image id
        for index, row in dogs.iterrows():
            image_path = os.path.join(dog_images_path, str(row["AnimalInternal-ID"]), "*.png")
            all_images = glob(image_path)
            dogs.at[index, 'ImageID'] = os.path.basename(all_images[0])

        print(dogs_with_images[:5])
        print(dogs.shape)
        dogs = dogs.rename(columns={"AnimalInternal-ID": "AnimalInternalID"})
        dogs = dogs.drop(columns=["AnimalPattern"])

        # Compute age of dog
        dogs['DOB'] = pd.to_datetime(dogs['AnimalDOB'], format='%Y%m%d')
        dogs["Year"] = pd.DatetimeIndex(dogs['DOB']).year
        dogs["Age"] = (pd.to_datetime('now') - dogs['DOB']).astype('<m8[Y]')

        print(dogs.head())
    return dogs

@router.get(
    "/breeds",
    summary="Get List of Dog Breeds",
    description="Get List of Dog Breeds"
)
async def get_breeds():
    dogs = load_dogs()
    # Get the unique values
    breed_counts = dogs["AnimalBreed"].value_counts()
    print(breed_counts.shape)
    breeds = breed_counts.head(50).index.tolist()

    return breeds

@router.get(
    "/dogs",
    summary="Get List of Dogs",
    description="Get List of Dogs"
)
async def get_dogs(
    breed: str = Query(None, description="The dog breed to filter by")
):
    print("breed",breed)
    dogs = load_dogs()
    rows = dogs.copy()

    # Breed filter
    if breed != '':
        rows = rows[rows["AnimalBreed"] == breed]

    # Sample "n" rows
    if rows.shape[0] > 30:
        rows = rows.sample(n=30)
    print("rows:",rows.shape)

    return rows.to_dict('records')

@router.get(
    "/view_image",
    summary="View Image given animal id",
    description="View Image given animal id"
)
async def view_image(
    animal_internal_id: int = Query(1, description="Animal internal id"),
    image_id: str = Query(None, description="The dog image id")
):
    print(animal_internal_id)
    # Get the path
    image_path = os.path.join(dog_images_path,str(animal_internal_id),image_id)
    return FileResponse(image_path, media_type="image/png")