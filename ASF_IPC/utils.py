import urllib.parse as urlparse


def build_url(ipc, endpoint):
    sep = '/'
    ipc_split = list(urlparse.urlsplit(ipc))
    ipc_split[2] = ipc_split[2].rstrip(sep)
    endpoint = endpoint.strip(sep)
    ipc_split[2] = ipc_split[2] + sep + endpoint
    return urlparse.urlunsplit(ipc_split)
