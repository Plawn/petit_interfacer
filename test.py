from __future__ import annotations
from typing import Optional

import petit_interfacer
from petit_interfacer import RealOptional


class Port(int):
    ...


class Response(str):
    ...


def proto(
    worker: RealOptional[Worker],
    port: Port,
) -> Optional[Response]:
    ...


class Worker:
    ...


bind_interface = petit_interfacer.interface_binder_for(proto)


@bind_interface
def func_a(port: Port):
    return Response(f'test: {port}')


a = func_a(worker=None, port=80)

print(f'Response is: \n{a}')
