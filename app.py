import logging
import graphene
from api.project import ProjectDetails
from api.transfer import (
    AssociationsImport,
    FileExport,
    JSONImport,
    KnowledgeBaseExport,
    Notify,
    PrepareFileImport,
    UploadTask,
)
from middleware.database_session import DatabaseSessionHandler
from starlette.applications import Starlette
from starlette.graphql import GraphQLApp
from starlette.middleware import Middleware
from starlette.routing import Route

from graphql_api import schema

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


routes = [
    Route(
        "/graphql/",
        GraphQLApp(
            schema=graphene.Schema(query=schema.Query, mutation=schema.Mutation)
        ),
    ),
    Route("/notify/{path:path}", Notify),
    Route("/project/{project_id:str}", ProjectDetails),
    Route(
        "/project/{project_id:str}/knowledge_base/{knowledge_base_id:str}",
        KnowledgeBaseExport,
    ),
    Route("/project/{project_id:str}/associations", AssociationsImport),
    Route("/project/{project_id:str}/export", FileExport),
    Route("/project/{project_id:str}/import_file", PrepareFileImport),
    Route("/project/{project_id:str}/import_json", JSONImport),
    Route("/project/{project_id:str}/import/task/{task_id:str}", UploadTask),
]

middleware = [Middleware(DatabaseSessionHandler)]

app = Starlette(routes=routes, middleware=middleware)

if __name__ == "__main__":
    import uvicorn
    import docker
    import os
    from dotenv import load_dotenv

    load_dotenv(dotenv_path='.env')

    client = docker.from_env()

    network = client.networks.get("bridge")
    credential_ip = network.attrs["IPAM"]["Config"][0]["Gateway"]
    cred_endpoint = f"http://{credential_ip}:7053"

    os.environ["S3_ENDPOINT"] = cred_endpoint

    uvicorn.run(app, host="0.0.0.0", port=7051)
