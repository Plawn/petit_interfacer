import petit_interfacer
from petit_interfacer import RealOptional


class Port(int):
    ...


class Response(str):
    ...


class Worker:
    ...


def proto(
    port: Port,
    worker: RealOptional[Worker],
) -> Response:
    ...


bind_interface = petit_interfacer.interface_binder_for(proto)


@bind_interface
def func_a(port:Port):
    return Response(f'test: {port}')


a = func_a(port=80, worker=None)

print(f'Response is: \n{a}')