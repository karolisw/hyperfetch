from optuna_tuning.alg_samplers import SUPPORTED_ALGORITHMS
from fastapi import APIRouter, Request, status, HTTPException
from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse
from models.run import BaseRun
from typing import List
import utils

# TODO for tomorrow:
#  research how the REST endpoints should look when using @router instead of @app
#  figure out if the imports are correct or not

# prefix: start of every decorator provided by fastapi in this particular page
# tags: the functionality of this category
router = APIRouter(prefix='/runs', tags=['crud/rest'])

storage = utils.get_yaml_val("../config/db_config.yml", "storage")
db = utils.get_yaml_val("../config/db_config.yml", "db")
collection = utils.get_yaml_val("../config/db_config.yml", "collection")


# TODO No need for this one
@router.post("/", response_description="Add new run", status_code=status.HTTP_201_CREATED, response_model=BaseRun)
async def create_run(request: Request, run: BaseRun):
    # Decode JSON request body into Python dictionary before passing to client
    run = jsonable_encoder(run)
    new_run = await request.app.database['runs']['run'].insert_one(run)
    # new_run = await db[collection].insert_one(run)
    created_run = await request.app.database['runs']['run'].find_one({"_id": new_run.inserted_id})
    # created_run = await db[collection].find_one({"_id": new_run.inserted_id})
    # return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_run)
    return created_run


@router.get("/env", response_description="List the top trial for each algorithm for selected env",
            response_model=List[BaseRun])
async def list_runs_for_env(env: str):
    runs = []

    # List of all supported algorithms
    algs = SUPPORTED_ALGORITHMS

    # A for loop that queries for each alg
    for index in range(len(algs)):
        # todo add check for if exists here
        # todo should i have await before find?
        if (run := await collection.find({'env': env, 'alg': algs[index]}).sort("reward", -1).limit(1)) is not None:
            # Add the found trial to a list to be returned
            runs[index] = run

    return runs


@router.get("/env/alg", response_description="List the top trials for selected algorithm x env combo")
async def list_runs_for_env_alg(env: str, alg: str, limit: int) -> List[BaseRun]:
    runs = await collection.find({'env': env, 'alg': alg}).sort("reward", -1).limit(limit).tolist()
    return runs


@router.get("/{id}", response_description="Get a single run")
async def show_run(id: str) -> BaseRun:
    if (run := await collection.find_one({"_id": id})) is not None:
        return run

    raise HTTPException(status_code=404, detail=f"Run with id {id} not found")


@router.delete("/{id}", response_description="Delete a run")
async def delete_student(id: str):
    delete_result = await collection.delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"Run with {id} not found")
