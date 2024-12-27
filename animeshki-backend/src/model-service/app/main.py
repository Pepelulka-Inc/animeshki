from contextlib import asynccontextmanager
from settings import MODEL_SETTINGS, PORT, USE_MINIO, DEBUG, DATA_PREFIX

from typing import List, Dict
from fastapi import FastAPI, Depends
import uvicorn

from pathlib import Path
import pandas as pd 
from rectools import Columns
from rectools.dataset import Dataset
from rectools.models.lightfm import LightFMWrapperModel
from lightfm import LightFM

from utils import (
    get_recommend_input,
    RecommendInput,
    get_dataset_from_minio,
    get_model_from_minio,
    save_to_minio,
    init_dataset_from_kaggle,
    init_dataset_from_file
    )

dataset_path = DATA_PREFIX/Path(MODEL_SETTINGS["DATASET_FILENAME"])
model_path = DATA_PREFIX/Path(MODEL_SETTINGS["FILENAME"])
models = {}
datasets = {}

def init_dataset(dataset_path: Path):
    if (dataset_path).exists():
        df = init_dataset_from_file(dataset_path)
    elif USE_MINIO:
        df = get_dataset_from_minio(dataset_path)
    else:
        df = init_dataset_from_kaggle(dataset_path)
    return Dataset.construct(df)


@asynccontextmanager
async def lifespan(app: FastAPI):
    model = LightFMWrapperModel(model=LightFM(), epochs=MODEL_SETTINGS["EPOCHS"], num_threads=MODEL_SETTINGS["NUM_THREADS"], verbose=DEBUG)
    dataset = init_dataset(dataset_path)
    print("Dataset Initialized")
    if (model_path).exists():
        model = model.load(model_path)
    elif USE_MINIO:
        model = get_model_from_minio(model)
    else:   
        model = model.fit(dataset)
        model.save(model_path)
    print("Model Initialized")
    
    models["recommender_system"] = model
    datasets["recommender_system"] = dataset
    yield
    
    datasets["recommender_system"].get_raw_interactions().to_csv(dataset_path, index=False)
    models["recommender_system"].save(model_path)
    if USE_MINIO:
        save_to_minio(models["recommender_system"], datasets["recommender_system"])
        

app = FastAPI(lifespan=lifespan)


@app.get("/recommend")
def get_recommendations(
    input_params: RecommendInput = Depends(get_recommend_input)
) -> Dict[str, List[int]]:
    recommendations_df = models["recommender_system"].recommend(
        users=input_params.users,
        dataset=datasets["recommender_system"],
        k=input_params.k,
        filter_viewed=input_params.filter_viewed,
        items_to_recommend=input_params.items_to_recommend,
        add_rank_col=input_params.add_rank_col,
        on_unsupported_targets=input_params.on_unsupported_targets
    )
    recos = recommendations_df.groupby(Columns.User)[Columns.Item].apply(list)
    return recos.to_dict()


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="info")
