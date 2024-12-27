
from fastapi import FastAPI, Query
from pydantic import BaseModel, Field
from typing import List, Optional
from typing_extensions import Literal

import kagglehub

from rectools.dataset import Dataset
from rectools.models.lightfm import LightFMWrapperModel
from lightfm import LightFM


def init_from_kaggle(model: LightFMWrapperModel, dataset: Dataset) -> None:
        path = kagglehub.dataset_download("hernan4444/anime-recommendation-database-2020")
        
        ratings = pd.read_csv(path + '/rating_complete.csv')
        ratings = ratings[ratings['rating']!=-1]
        ratings.columns = [Columns.User, Columns.Item,  Columns.Weight]
        ratings[[Columns.Datetime]] = ratings.groupby(Columns.User).cumcount()
        ratings.drop_duplicates(subset=[Columns.User,  Columns.Item], keep='last', inplace=True)
        dataset = Dataset.construct(
            interactions_df=ratings
        )
        model.fit(dataset)


class RecommendInput(BaseModel):
    users: List[int] = Field(..., min_items=1)
    k: int = Field(..., gt=0)
    filter_viewed: bool = False
    items_to_recommend: Optional[List[int]] = None
    add_rank_col: bool = False
    on_unsupported_targets: Literal['ignore', 'warn', 'raise'] = 'raise'

def get_recommend_input(
    users: List[int] = Query(...),
    k: int = Query(default=10),
    filter_viewed:  Optional[bool] = Query(False),
    items_to_recommend: Optional[List[int]] = Query(None),
    add_rank_col: bool = Query(False),
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

