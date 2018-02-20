# ASF_IPC

[![license](https://img.shields.io/github/license/deluxghost/ASF_IPC.svg?style=flat-square)](https://github.com/deluxghost/ASF_IPC/blob/master/LICENSE)
[![PyPI](https://img.shields.io/badge/Python-3.6-blue.svg?style=flat-square)](https://pypi.python.org/pypi/ASF-IPC)
[![PyPI](https://img.shields.io/pypi/v/ASF-IPC.svg?style=flat-square)](https://pypi.python.org/pypi/ASF-IPC)
[![ASF](https://img.shields.io/badge/ASF-3.1.0.5-orange.svg?style=flat-square)](https://github.com/JustArchi/ArchiSteamFarm)

A simple Python 3.6+ library of [ArchiSteamFarm IPC API](https://github.com/JustArchi/ArchiSteamFarm/wiki/IPC)

## Examples

* [telegram-asf](https://github.com/deluxghost/telegram-asf)

## Requirements

* Python 3.6+
* requests
* websockets

## Installation

```shell
pip3 install ASF_IPC
```

## Getting Started

This example shows how to post a command to ASF:

```python
import ASF_IPC as asf

api = asf.IPC(ipc='http://127.0.0.1:1242/', password='YOUR IPC PASSWORD')
command = input('Enter a command:')
output = api.command(command)
print(output)
```

For further usage examples, read our [wiki](https://github.com/deluxghost/ASF_IPC/wiki) pages.


