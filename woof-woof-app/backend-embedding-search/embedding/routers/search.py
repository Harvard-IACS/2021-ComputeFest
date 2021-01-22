import os
import numpy as np
import pandas as pd
import cv2
from tempfile import TemporaryDirectory
from glob import glob
from fastapi import APIRouter, Path, Query, File, Form
from starlette.responses import FileResponse
from urllib.parse import urlparse
import pyarrow.parquet as pq
import faiss
import tensorflow as tf
from efficientnet.tfkeras import EfficientNetB0

import embedding.utils as embedding_utils

router = APIRouter()

dogs_path = os.path.join(embedding_utils.DATASET_PATH,"dog_data_small","dogs.csv")
dogs_photos_path = os.path.join(embedding_utils.DATASET_PATH,"dog_data_small","dogs_photos.csv")
dog_images_path = os.path.join(embedding_utils.DATASET_PATH,"resized_dogs_small")
embeddings_path = os.path.join(embedding_utils.DATASET_PATH,"embeddings_small")

# Variable to hold the dogs embeddings
embeddings = None
stacked_embeddings = None
embeddings_id_to_name = None
faiss_index = None
dogs = None
efficientnet_model = EfficientNetB0(weights='imagenet', include_top=False, pooling="avg")

def create_faiss_index(stacked_embeddings):
    d = 1280
    index = faiss.IndexFlatIP(d)
    index.add(stacked_embeddings)
    return index

def faiss_search(index, id_to_name, emb, k=5):
    # Peform actual search
    D, I = index.search(np.expand_dims(emb, 0), k)
    return list(zip(D[0], [id_to_name[x] for x in I[0]]))

def process_search(search_embeddings):
    results_df = []
    for embd in search_embeddings:
        results = faiss_search(faiss_index, embeddings_id_to_name, embd, k=5)
        print(results)

        # Get the image folder to extract animalid, image id
        for itm in results:
            folder = itm[1]
            results_df.append({
                'AnimalInternalID': int(folder.split("/")[0]),
                'ImageID': folder.split("/")[1]
            })

    results_df = pd.DataFrame(results_df)
    # Drop duplicates if found by multiple searches
    results_df.drop_duplicates(subset="AnimalInternalID", keep=False, inplace=True)
    print(results_df.shape)
    print(results_df.head())

    # Join with dogs meta data to return to api
    dogs = load_dogs()
    outputs = dogs.merge(results_df, on=["AnimalInternalID"], how="inner")
    print(outputs.shape)
    print(outputs.head())

    return outputs

def load_embeddings():
    global embeddings
    global stacked_embeddings
    global faiss_index
    global embeddings_id_to_name

    if embeddings is None:
        print("Loading dogs data...")

        # merges dogs_photo's and embeddings. We want the filename and folder for similar image.
        embeddings = pq.read_table(embeddings_path).to_pandas()
        dogs_photos = pd.read_csv(dogs_photos_path)
        dogs_photos['filename'] = dogs_photos["PhotoUrl"].apply(lambda url: os.path.basename(urlparse(url).path))
        embeddings['new_image_name'] = embeddings.image_name.apply(lambda x: x.decode("utf-8") + ".png")  # convert byte literal to string
        embeddings = embeddings.merge(dogs_photos, left_on='new_image_name', right_on='filename')
        embeddings['folder'] = embeddings['AnimalInternal-ID'].astype(str) + '/' + embeddings['new_image_name'].astype(str)

        stacked_embeddings = np.stack(embeddings["embedding"].to_numpy())
        embeddings_id_to_name = {k: v for k, v in enumerate(list(embeddings["folder"]))}
        faiss_index = create_faiss_index(stacked_embeddings)

    return embeddings

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
            id = path.split("/")[-1]
            id_list.append(int(id))

        dogs = dogs_all[dogs_all["AnimalInternal-ID"].isin(id_list)]

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
    "/find_similar_from_ids",
    summary="Get list of similar dogs",
    description="Get list of similar dogs"
)
async def find_similar_from_ids(
    ids: str = Query('', description="The list of image ids")
):
    print("ids",ids)
    ids = ids.split(",")
    embeddings = load_embeddings()

    # Find embeddings of the images passed in
    search_embeddings = embeddings[embeddings["filename"].isin(ids)]['embedding'].values
    print(search_embeddings)

    outputs = process_search(search_embeddings)

    return outputs.to_dict('records')

@router.post(
    "/find_similar_from_image",
    summary="Get list of similar dogs",
    description="Get list of similar dogs"
)
async def find_similar_from_image(
        file: bytes = File(...),
        filename: str = Form(...)
):
    print("find_similar_from_image")
    print(len(file),type(file),filename)
    embeddings = load_embeddings()

    with TemporaryDirectory() as temp_dir:
        # Save the image
        image_path = os.path.join(temp_dir, filename)
        with open(image_path, "wb") as output:
            output.write(file)

        # Read the image
        cur_img = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
        input_image = cv2.cvtColor(cv2.resize(cur_img, (224, 224), interpolation=cv2.INTER_AREA), cv2.COLOR_BGRA2RGB)
        is_success, im_buf_arr = cv2.imencode(".jpg", input_image)
        input_image = im_buf_arr.tobytes()

        resized = tf.image.decode_jpeg(input_image, channels=3)
        resized = tf.image.convert_image_dtype(resized, tf.float32).numpy()
        search_embedding = efficientnet_model.predict(resized.reshape(1, 224, 224, 3))[0]
        print(search_embedding)

        outputs = process_search([search_embedding])

    return outputs.to_dict('records')