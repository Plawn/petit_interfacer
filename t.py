import asyncio
from typing import Any
from petit_interfacer import interface_binder_for, RealOptional

class Port(int):
    ...

class Address(str):
    ...

async def proto(
    port: Port,
    address: RealOptional[Address]
) -> Any:
    ...

binder = interface_binder_for(proto)

@binder
async def test(port:Port):
    await asyncio.sleep(0.1)
    return port



loop = asyncio.get_event_loop()
res = loop.run_until_complete(test(78, ''))

print(res)