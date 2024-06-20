import random

from bemani.common.model import Model
from bemani.protocol import EAmuseProtocol
from bemani.protocol.node import Node
from fastapi import FastAPI, Request, Response

app = FastAPI()

DEBUG = True


class Node(Node):
    def __init__(
        self, name, value=None, /, children=None, type=None, **attributes
    ):
        if value is not None:
            value = str(value)
        super().__init__(name=name, type=type, value=value)
        if children:
            self.__children = children
        for attr_name, attr_value in attributes.items():
            self.set_attribute(attr_name, str(attr_value))

    @classmethod
    def void(cls, *args, **kwargs) -> "Node":
        return cls(*args, type=Node.NODE_TYPE_VOID, **kwargs)

    @classmethod
    def string(cls, *args, **kwargs) -> "Node":
        return cls(*args, type=Node.NODE_TYPE_STR, **kwargs)


def handle_eam_request(eam_request: Node, http_request: Request, path: str):
    from app.services import Service

    if path == "services/get":
        return Service().get_services(eam_request, http_request)

    node = path.split("/")[0]

    if path == "pcbtracker/alive":
        PASELI_ENABLED = True
        return Node.void(node, ecenable=int(PASELI_ENABLED), expire=600)

    if path == "pcbevent/put":
        return Node.void(node)

    if path == "package/list":
        return Node.void(node, expire=600)

    if path == "message/get":
        return Node.void(node, expire=600)

    if path == "dlstatus/progress":
        return Node.void(node)

    if path == "facility/get":
        return Service().get_facility(eam_request, http_request)

    if path == "eventlog/write":
        return Node.void(
            node,
            children=[
                Node.s64("gamesession", random.randint(1, 1000000)),
                Node.s32("logsendflg", 0),
                Node.s32("logerrlevel", 0),
                Node.s32("evtidnosendflg", 0),
            ],
        )

    if DEBUG:
        raise Exception(f"Unknown path {path}")

    return Node.void(node)


@app.post("/services/init/{gameinfo}/{route:path}")
async def eam_service(
    request: Request,
    route: str,
):
    agent = request.headers.get("User-Agent")
    if agent != "EAMUSE.XRPC/1.0":
        raise Exception("Not an eam request")

    body = await request.body()
    compression = request.headers.get("X-Compress")
    encryption = request.headers.get("X-Eamuse-Info")
    eam_encoder = EAmuseProtocol()
    root = eam_encoder.decode(compression, encryption, body)
    model = Model.from_modelstring(root.attribute("model"))
    pcbid = root.attribute("srcid")
    eam_request = root.children[0]
    method = eam_request.attribute("method")
    print("-" * 20)
    print(f"Request {method} {route}")
    print(eam_request)
    print("-" * 20)

    data = handle_eam_request(eam_request, request, route)
    data.set_attribute("status", "0")
    data = Node.void("response", dstid=pcbid, children=[data])
    print("-" * 20)
    print(f"Response {method} {route}")
    print(data)
    print("-" * 20)
    data = eam_encoder.encode(compression, encryption, data)

    headers = {}
    if encryption:
        headers["X-Eamuse-Info"] = encryption
    if compression:
        headers["X-Compress"] = compression
    return Response(
        content=data,
        headers=headers,
    )
