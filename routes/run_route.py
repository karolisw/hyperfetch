# type: ignore
from fastapi import Depends, APIRouter
from starlette.status import HTTP_201_CREATED

from config.mongodb import get_database

from crud.run_crud import *

# prefix: start of every decorator provided by fastapi in this particular page
# tags: the functionality of this category
router = APIRouter(prefix='/api', tags=['crud/rest'])


@router.get("/", response_description="List of all unique envs in db",
            response_model=EnvsRead)
async def fetch_envs(db: AsyncIOMotorClient = Depends(get_database)):
    envs = await list_envs(conn=db)
    return envs


@router.post("/create", response_description="Creates a run and returns its RunRead object",
             response_model=RunRead, status_code=HTTP_201_CREATED,
             responses=get_exception_responses(RunAlreadyExistsException), )
async def create_run(new_run: RunCreate, db: AsyncIOMotorClient = Depends(get_database)) -> RunRead:
    created_run = await create(conn=db, new_run=new_run)
    return created_run


@router.get("/env_top_trials", response_description="List the top trial for each algorithm for selected env",
            response_model=RunsRead)
async def fetch_runs_for_env(env: str, db: AsyncIOMotorClient = Depends(get_database)):
    runs = await list_best_runs_for_env(conn=db, env=env)
    return runs


@router.get("/alg_top_trials", response_description="List the top trials for selected algorithm x env combo",
            response_model=RunsRead)
async def fetch_runs_for_env_alg(env: str, alg: str, limit: int, db: AsyncIOMotorClient = Depends(get_database)):
    runs = await list_runs_for_env_alg(env=env, alg=alg, limit=limit, conn=db)
    return runs


@router.get("/runs/{run_id}", response_description="Get a single run",
            response_model=RunRead,
            description="Get a single run by its unique ID",
            responses=get_exception_responses(RunNotFoundException))
async def fetch_run(run_id: str, db: AsyncIOMotorClient = Depends(get_database)) -> RunRead:
    run = await show_run(conn=db, run_id=run_id)
    return run
