from fastapi import Depends, APIRouter
from models.run import RunInResponse, ManyRunsInResponse
from config.mongodb import get_database
from crud.run_functions import *
from utils.db_utils import create_aliased_response

# prefix: start of every decorator provided by fastapi in this particular page
# tags: the functionality of this category
router = APIRouter(prefix='/api', tags=['crud/rest'])


@router.get("/", response_description="List of all unique envs in db",
            response_model=ManyRunsInResponse)
async def fetch_envs(db: AsyncIOMotorClient = Depends(get_database)):
    envs = await list_envs(conn=db)
    return create_aliased_response(ManyRunsInResponse(runs=envs))


@router.get("/env", response_description="List the top trial for each algorithm for selected env",
            response_model=ManyRunsInResponse)
async def fetch_runs_for_env(env: str, db: AsyncIOMotorClient = Depends(get_database)):
    runs = await list_runs_for_env(conn=db, env=env)
    return create_aliased_response(ManyRunsInResponse(runs=runs))


@router.get("/env/alg", response_description="List the top trials for selected algorithm x env combo",
            response_model=ManyRunsInResponse)
async def fetch_runs_for_env_alg(env: str, alg: str, limit: int, db: AsyncIOMotorClient = Depends(get_database)):
    runs = await list_runs_for_env_alg(env=env, alg=alg, limit=limit, conn=db)
    return create_aliased_response(ManyRunsInResponse(runs=runs))


@router.get("/env/alg/{id}", response_description="Get a single run",
            response_model=RunInResponse)
async def fetch_run(run_id: str, db: AsyncIOMotorClient = Depends(get_database)):
    run = await show_run(conn=db, id=run_id)
    return create_aliased_response(RunInResponse(run))
    # TODO create handling for the error that might occur....
    # raise HTTPException(status_code=404, detail=f"Run with id {id} not found")
