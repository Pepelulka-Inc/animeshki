
from fastapi import FastAPI, Query
from pydantic import BaseModel, Field
from typing import List, Optional
from typing_extensions import Literal
from rectools import Columns

import pandas as pd

import kagglehub

from rectools.dataset import Dataset
from rectools.models.lightfm import LightFMWrapperModel
from lightfm import LightFM
from pathlib import Path

def init_dataset_from_file(dataset_path: Path):
    return pd.read_csv(dataset_path)

def init_dataset_from_kaggle(dataset_path: Path) -> pd.DataFrame:
    path = kagglehub.dataset_download("hernan4444/anime-recommendation-database-2020")
    ratings = pd.read_csv(path + '/rating_complete.csv')
    ratings = ratings[ratings['rating']!=-1]
    ratings.columns = [Columns.User, Columns.Item,  Columns.Weight]
    ratings[Columns.Datetime] = ratings.groupby(Columns.User).cumcount()
    ratings.drop_duplicates(subset=[Columns.User,  Columns.Item], keep='last', inplace=True)
    ratings.to_csv(dataset_path, index=False)
    return ratings


def get_dataset_from_minio(dataset_path: Path):
    raise NotImplementedError

def get_model_from_minio(model_path: Path):
    raise NotImplementedError

def save_to_minio(model_path: Path, dataset_path: Path):
    raise NotImplementedError
        
        
class RecommendInput(BaseModel):
    users: List[int] = Field(..., min_items=1)
    k: int = Field(10, gt=0)
    filter_viewed: bool = True
    items_to_recommend: Optional[List[int]] = None
    add_rank_col: bool = True
    on_unsupported_targets: Literal['ignore', 'warn', 'raise'] = 'raise'

def get_recommend_input(
    users: List[int] = Query(...),
    k: int = Query(default=10),
    filter_viewed:  Optional[bool] = Query(True),
    items_to_recommend: Optional[List[int]] = Query(None),
    add_rank_col: bool = Query(True),
    on_unsupported_targets: Literal['ignore', 'warn', 'raise'] = Query('raise')
) -> RecommendInput:
    return RecommendInput(
        users=users,
        k=k,
        filter_viewed=filter_viewed,
        items_to_recommend=items_to_recommend,
        add_rank_col=add_rank_col,
        on_unsupported_targets=on_unsupported_targets
    )