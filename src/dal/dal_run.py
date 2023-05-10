from starlette.status import HTTP_204_NO_CONTENT
from src.models.create_run import RunCreate
from typing import List
from src.db_config.mongodb import AsyncIOMotorClient
from src.db_config.auth_connection import MONGO_DB, MONGO_COLLECTION
from src.models.receive_run import RunRead, EnvRead, RunsRead, EnvsRead
from src.utils.db_utils import get_time, get_uuid
from src.utils.exceptions import RunNotFoundException

SUPPORTED_ALGORITHMS = [
    "ppo",
    "a2c",
    "dqn",
    "sac",
    "td3"
]


async def create(conn: AsyncIOMotorClient, new_run: RunCreate) -> RunRead:
    # From Object to dict
    document = new_run.dict()
    document["_id"] = get_uuid()
    document["created"] = get_time()
    result = await conn[MONGO_DB][MONGO_COLLECTION].insert_one(document)
    assert result.acknowledged

    run = await show_run(conn=conn, run_id=result.inserted_id)
    return run


async def list_envs(conn: AsyncIOMotorClient) -> EnvsRead:
    cursor = await conn[MONGO_DB][MONGO_COLLECTION].find().distinct('env')
    return [EnvRead(env=document) for document in cursor]


async def list_best_runs_for_env(conn: AsyncIOMotorClient, env: str) -> RunsRead:
    algs = SUPPORTED_ALGORITHMS
    runs: RunsRead = []
    for alg in algs:
        run = await _list_runs_for_env(conn, env, alg)
        if run is not None:
            runs.append(run)
    return runs


async def _list_runs_for_env(conn: AsyncIOMotorClient, env: str, alg: str) -> RunRead:
    # A for loop that queries for each alg
    cursor = conn[MONGO_DB][MONGO_COLLECTION] \
        .find({"env": env, "alg": alg}) \
        .sort("reward", -1) \
        .limit(1)

    for document in await cursor.to_list(length=1):
        return RunRead(**document)


async def list_runs_for_env_alg(conn: AsyncIOMotorClient, env: str, alg: str, limit: int) -> RunsRead:
    runs: List[RunRead] = []
    rows = await conn[MONGO_DB][MONGO_COLLECTION] \
        .find({'env': env, 'alg': alg}) \
        .sort("reward", -1) \
        .limit(limit).to_list(length=limit)
    for row in rows:
        runs.append(RunRead(**row))

    return runs


async def show_run(conn: AsyncIOMotorClient, run_id: str) -> RunRead:
    document = await conn[MONGO_DB][MONGO_COLLECTION].find_one({"_id": run_id})
    if not document:
        raise RunNotFoundException(run_id)

    return RunRead(**document)


async def delete_run(conn: AsyncIOMotorClient, run_id: str) -> HTTP_204_NO_CONTENT:
    deleted_run = await conn[MONGO_DB][MONGO_COLLECTION].delete_one({"_id": run_id})

    if deleted_run.deleted_count == 0:
        raise RunNotFoundException(run_id)

    return HTTP_204_NO_CONTENT
