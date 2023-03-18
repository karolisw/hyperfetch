from optuna_tuning.alg_samplers import SUPPORTED_ALGORITHMS
from fastapi import APIRouter, Request, status, HTTPException
from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse
from models.run import BaseRun
from typing import List
from optuna_tuning.manager import collection

# prefix: start of every decorator provided by fastapi in this particular page
# tags: the functionality of this category
router = APIRouter(prefix='/api', tags=['crud/rest'])

@router.get("/", response_description="List of all unique envs in db",
            response_model=List[BaseRun])  # TODO probably change response model entity
async def list_envs():
    envs = await collection.distinct('env')
    return envs


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


@router.get("/env/alg/{id}", response_description="Get a single run")
async def show_run(id: str) -> BaseRun:
    if (run := await collection.find_one({"_id": id})) is not None:
        return run

    raise HTTPException(status_code=404, detail=f"Run with id {id} not found")
