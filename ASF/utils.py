import urllib.parse as urlparse

sep = '/'


def build_url(ipc, endpoint):
    ipc_split = list(urlparse.urlsplit(ipc))
    ipc_split[2] = ipc_split[2].rstrip(sep)
    endpoint = endpoint.strip(sep)
    ipc_split[2] = ipc_split[2] + sep + endpoint
    return urlparse.urlunsplit(ipc_split)


def quote(keyword):
    return urlparse.quote(keyword)


def path_parse(path):
    paths = path.strip(sep).split(sep)
    token = list()
    for index, node in enumerate(paths):
        if index != 0 and node.startswith('{') and node.endswith('}'):
            token[-1] = {

            }
