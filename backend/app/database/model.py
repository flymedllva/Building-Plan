import asyncio

import ujson
from arango import ArangoClient
from arango.database import StandardDatabase, AsyncDatabase
from arango.job import AsyncJob


class ArangoDB:
    client: ArangoClient
    db: StandardDatabase
    async_db: AsyncDatabase
    tasks: dict

    def __init__(
        self,
        hosts: str = "http://127.0.0.1:8529",
        database: str = "test",
        username: str = "root",
        password: str = "passwd",
        host_resolver: str = "roundrobin",
    ):
        self.client = ArangoClient(
            hosts=hosts,
            serializer=ujson.dumps,
            deserializer=ujson.loads,
            host_resolver=host_resolver,
        )
        self.db = self.client.db(database, username=username, password=password)
        self.async_db = self.db.begin_async_execution(return_result=True)

    async def receive_asynс_response(self, task: AsyncJob):
        while task.status() != "done":
            await asyncio.sleep(0.1)
        return [i for i in task.result()]

    async def find_shortest_path(self, of: str, to: str, graph: str):
        task = self.async_db.aql.execute(
            """
            FOR v, e IN OUTBOUND SHORTEST_PATH @of TO @to
              GRAPH @graph
            RETURN { "connection":  v._key, "object": RTRIM(e._key, "___2") }
            """,
            bind_vars={"of": of, "to": to, "graph": graph},
        )
        task, paths = await self.receive_asynс_response(task), set()
        for item in task:
            if item["connection"]:
                paths.add(item["connection"])
            if item["object"]:
                paths.add(item["object"])
        return paths
