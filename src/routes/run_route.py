# type: ignore
from fastapi import Depends
from starlette.status import HTTP_404_NOT_FOUND, HTTP_201_CREATED
from src.config.mongodb import get_database
from src.dal.dal_run import *
from src.models.receive_run import EnvsRead, RunsRead
from src.utils.exceptions import RunAlreadyExistsException, get_exception_responses, RunNotFoundException
from typing import Any, Callable
from fastapi import APIRouter as FastAPIRouter
from fastapi.types import DecoratedCallable


class APIRouter(FastAPIRouter):
    def api_route(
            self, path: str, *, include_in_schema: bool = True, **kwargs: Any
    ) -> Callable[[DecoratedCallable], DecoratedCallable]:
        if path.endswith("/"):
            path = path[:-1]

        add_path = super().api_route(
            path, include_in_schema=include_in_schema, **kwargs
        )

        alternate_path = path + "/"
        add_alternate_path = super().api_route(
            alternate_path, include_in_schema=False, **kwargs
        )

        def decorator(func: DecoratedCallable) -> DecoratedCallable:
            add_alternate_path(func)
            return add_path(func)

        return decorator


# tags: the functionality of this category
router = APIRouter(tags=['dal/rest'])


@router.get("/api/", response_description="List of all unique envs in db",
            response_model=EnvsRead)
async def fetch_envs(db: AsyncIOMotorClient = Depends(get_database)):
    envs = await list_envs(conn=db)
    return envs


# Not in use and must be commented out if the project should be made public.
@router.post("/api/create", response_description="Creates a run and returns its RunRead object",
             response_model=RunRead, status_code=HTTP_201_CREATED,
             responses=get_exception_responses(RunAlreadyExistsException), )
async def create_run(new_run: RunCreate, db: AsyncIOMotorClient = Depends(get_database)) -> RunRead:
    created_run = await create(conn=db, new_run=new_run)
    return created_run


@router.get("/api/env_top_trials", response_description="List the top trial for each algorithm for selected env",
            response_model=RunsRead)
async def fetch_runs_for_env(env: str, db: AsyncIOMotorClient = Depends(get_database)):
    runs = await list_best_runs_for_env(conn=db, env=env)
    return runs


@router.get("/api/alg_top_trials", response_description="List the top trials for selected algorithm x env combo",
            response_model=RunsRead)
async def fetch_runs_for_env_alg(env: str, alg: str, limit: int, db: AsyncIOMotorClient = Depends(get_database)):
    runs = await list_runs_for_env_alg(env=env, alg=alg, limit=limit, conn=db)
    return runs


@router.get("/api/runs/{run_id}", response_description="Get a single run",
            response_model=RunRead,
            responses=get_exception_responses(RunNotFoundException))
async def fetch_run(run_id: str, db: AsyncIOMotorClient = Depends(get_database)) -> RunRead:
    run = await show_run(conn=db, run_id=run_id)
    return run


# Not in use and must be commented out if the project should be made public.
@router.delete("/api/delete/{run_id}", response_description="Delete a single run by its unique ID",
               response_model=None, status_code=HTTP_204_NO_CONTENT,
               responses=get_exception_responses(RunNotFoundException))
async def remove_run(run_id: str, db: AsyncIOMotorClient = Depends(get_database)) -> HTTP_204_NO_CONTENT:
    deleted_run = await delete_run(conn=db, run_id=run_id)
    if deleted_run.deleted_count == 1:
        return HTTP_204_NO_CONTENT
    else:
        return HTTP_404_NOT_FOUND
