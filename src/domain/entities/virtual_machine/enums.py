from enum import StrEnum


class ConnectionProtocol(StrEnum):
    HTTP = "http"
    SOCKS5 = "socks5"
    HTTPS = "https"
