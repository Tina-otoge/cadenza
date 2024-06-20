import enum
from enum import StrEnum

from fastapi import Request

from app import Node


class Service:
    class Mode(StrEnum):
        operation = enum.auto()
        debug = enum.auto()
        test = enum.auto()
        factory = enum.auto()

    def get_services(self, eam_request: Node, http_request: Request):
        def item(name, url):
            return Node.void("item", name=name, url=url)

        url = "http://localhost:8000/services/init"
        return Node.void(
            "services",
            expire=600,
            mode=self.Mode.operation,
            product_domain=1,
            children=[
                item(service, url)
                for service in (
                    "facility",
                    "message",
                    "apsmanager",
                    "cardmng",
                    "dlstatus",
                    "eacoin",
                    "ins",
                    "package",
                    "package2",
                    "pcbevent",
                    "pcbtracker",
                    "local2",
                    "local",
                    "lobby",
                )
            ]
            + [
                item("ntp", "ntp://pool.ntp.org/"),
                item(
                    "keepalive",
                    "http://127.0.0.1/keepalive?pa=127.0.0.1&ia=127.0.0.1&ga=127.0.0.1&ma=127.0.0.1&t1=2&t2=10",
                ),
            ],
        )

    def get_facility(self, eam_request: Node, http_request: Request):
        COUNTRY = "XX"
        REGION = ""  # JP-13
        ARCADE_NAME = "CADENZA Test"
        PUBLIC_IP = "127.0.0.1"
        PUBLIC_PORT = 8000
        ADVERTISED_URL = "http://eagate.573.jp"
        ADVERTISED_URL = "http://cadenza.test"

        return Node.void(
            "facility",
            expire=600,
            children=[
                Node.void(
                    "location",
                    children=[
                        Node.string("id", "EA000001"),
                        Node.string("country", COUNTRY),
                        Node.string("region", REGION),
                        Node.string("name", ARCADE_NAME),
                        Node.u8("type", 0),
                    ],
                ),
                Node.void(
                    "line",
                    children=[
                        Node.string("id", "."),
                        Node.u8("class", 0),
                    ],
                ),
                Node.void(
                    "portfw",
                    children=[
                        Node.string("globalip", PUBLIC_IP),
                        Node.u16("globalport", PUBLIC_PORT),
                        Node.u16("privateport", PUBLIC_PORT),
                    ],
                ),
                Node.void(
                    "public",
                    children=[
                        Node.u8("flag", 1),
                        Node.string("name", ARCADE_NAME),
                        Node.string("latitude", 0),
                        Node.string("longitude", 0),
                    ],
                ),
                Node.void(
                    "share",
                    children=[
                        Node.void(
                            "eacoin",
                            children=[
                                Node.s32("notchamount", 3000),
                                Node.s32("notchcount", 3),
                                Node.s32("supplylimit", 10000),
                            ],
                        ),
                        Node.void(
                            "eapass",
                            children=[
                                Node.u16("valid", 365),
                            ],
                        ),
                        Node.void(
                            "url",
                            children=[
                                Node.string("eapass", ADVERTISED_URL),
                                Node.string("arcadefan", ADVERTISED_URL),
                                Node.string("konaminetdx", ADVERTISED_URL),
                                Node.string("konamiid", ADVERTISED_URL),
                                Node.string("eagate", ADVERTISED_URL),
                            ],
                        ),
                    ],
                ),
            ],
        )
