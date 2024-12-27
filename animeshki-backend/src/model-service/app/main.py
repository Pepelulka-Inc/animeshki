from contextlib import asynccontextmanager
from settings import MODEL_SETTINGS, PORT, USE_MINIO, DEBUG 

from typing import Dict
from fastapi import FastAPI, Depends
import uvicorn

from pathlib import Path
    
from rectools.dataset import Dataset
from rectools.models.lightfm import LightFMWrapperModel
from lightfm import LightFM

from handlers import get_recommend_input, RecommendInput

model: LightFMWrapperModel
dataset: Dataset
    
@asynccontextmanager
async def lifespan(app: FastAPI):
    model = LightFMWrapperModel(model=LightFM(), epochs=MODEL_SETTINGS["EPOCHS"], num_threads=MODEL_SETTINGS["NUM_THREADS"], verbose=DEBUG)
    if ('bin' / Path(MODEL_SETTINGS["FILENAME"])).exists():
        model.load_model('bin' / Path(MODEL_SETTINGS["FILENAME"]))
    elif USE_MINIO:
        # TODO
        pass
    else:
        init_from_kaggle(model, dataset) 
        
    print("MODEL IS READY")  
    yield
    model.save(MODEL_SETTINGS["FILENAME"])
    if USE_MINIO:
        pass
        #TODO
        

app = FastAPI(lifespan=lifespan)


@app.get("/recommend")
def get_recommendations(
    input_params: RecommendInput = Depends(get_recommend_input)
) -> Dict:
    recommendations_df = model.recommend(
        users=input_params.users,
        dataset=dataset,
        k=input_params.k,
        filter_viewed=input_params.filter_viewed,
        items_to_recommend=input_params.items_to_recommend,
        add_rank_col=input_params.add_rank_col,
        on_unsupported_targets=input_params.on_unsupported_targets
    )

    # Convert DataFrame to dict for JSON serialization
    recommendations = recommendations_df.to_dict(orient='records')

    return recommendations

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=PORT, log_level="debug")
