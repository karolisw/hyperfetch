'''
Methods that interact with the database
'''

from optuna_tuning.alg_samplers import SUPPORTED_ALGORITHMS
from models.create_run import RunCreate
from typing import List
from config.mongodb import AsyncIOMotorClient
from config.auth_connection import database_name, run_collection_name
from models.receive_run import *
from utils.exceptions import *
from utils.common import get_time, get_uuid


async def create(conn: AsyncIOMotorClient, new_run: RunCreate) -> RunRead:
    # From Object to dict
    document = new_run.dict()
    document["_id"] = get_uuid()
    document["created"] = get_time()
    result = await conn[database_name][run_collection_name].insert_one(document)
    assert result.acknowledged

    run = await show_run(conn=conn, run_id=result.inserted_id)
    return run


async def list_envs(conn: AsyncIOMotorClient) -> EnvsRead:
    cursor = await conn[database_name][run_collection_name].find().distinct('env')
    return [EnvRead(env=document) for document in cursor]


async def list_best_runs_for_env(conn: AsyncIOMotorClient, env: str) -> RunsRead:
    algs = SUPPORTED_ALGORITHMS
    runs: RunsRead = []
    for alg in algs:
        run = await _list_runs_for_env(conn, env, alg)
        if run is not None:
            runs.append(run)
    return runs


async def _list_runs_for_env(conn: AsyncIOMotorClient, env: str, alg: str) -> RunRead | None:
    # A for loop that queries for each alg
    cursor = conn[database_name][run_collection_name] \
        .find({"env": env, "alg": alg}) \
        .sort("reward", -1) \
        .limit(1)

    for document in await cursor.to_list(length=1):
        if document is None:
            return None
        return RunRead(**document)


async def list_runs_for_env_alg(conn: AsyncIOMotorClient, env: str, alg: str, limit: int) -> RunsRead:
    runs: List[RunRead] = []
    rows = await conn[database_name][run_collection_name]\
        .find({'env': env, 'alg': alg})\
        .sort("reward", -1)\
        .limit(limit).to_list(length=limit)
    for row in rows:
        runs.append(RunRead(**row))

    return runs


async def show_run(conn: AsyncIOMotorClient, run_id: str) -> RunRead:
    document = await conn[database_name][run_collection_name].find_one({"_id": run_id})
    if not document:
        raise RunNotFoundException(run_id)

    return RunRead(**document)
