from __future__ import annotations
import asyncio
import inspect

import unittest
from dataclasses import dataclass
from typing import Optional

from .. import BlindBind, Dataclass, RealOptional, interface_binder_for
from ..exceptions import MissingHints, TooManyBlindBinds
from ..utils import Remove, is_already_described_prototype


class Port(int):
    ...


class Response(str):
    ...


class Worker:
    ...


def proto(
    worker: RealOptional[Worker],
    port: Port,
    deb: BlindBind[Dataclass],
) -> Optional[Response]:
    ...  # pragma: no cover


bind_interface = interface_binder_for(proto)


@dataclass
class Data:
    jeb: int


class BasicTests(unittest.TestCase):
    def test_interface_binder_for(self):
        def func_a(port: Port, k: Data) -> Response:
            return Response(f'test: {port}')
        bound_a = bind_interface(func_a)
        port = 80
        self.assertEqual(bound_a(worker=None, port=port,
                                 deb=None), f'test: {port}')

    def test_fail_bind(self):
        def f(port, p):
            pass  # pragma: no cover
        with self.assertRaises(MissingHints):
            a = bind_interface(f)

    def test_with_one_missing(self):
        def f(port: Port, p):
            return Response(f'port: {port} and BlindBind: {p}')
        bound_a = bind_interface(f)
        port = 80
        deb = 81
        self.assertEqual(bound_a(worker=None, port=port,
                                 deb=deb), f'port: {port} and BlindBind: {deb}')

    def test_too_many_blindbind(self):
        def f(a: BlindBind[Port], b: BlindBind[Response]):
            pass  # pragma: no cover
        with self.assertRaises(TooManyBlindBinds):
            interfacer = interface_binder_for(f)

    def test_async_binder(self):
        async def f(a:RealOptional[Port], b:Response):
            pass  # pragma: no cover
        interfacer = interface_binder_for(f)
        @interfacer
        async def f1(b:Response):
            await asyncio.sleep(0.1)
            return b
        loop = asyncio.get_event_loop()
        res = loop.run_until_complete(f1(10, 20))
        self.assertEqual(res, 20)

    def test_expected_async(self):
        async def f(a:RealOptional[Port], b:Response):
            pass  # pragma: no cover
        
        interfacer = interface_binder_for(f)
        with self.assertRaises(TypeError):
            @interfacer
            def f1(b:Response):
                return b # pragma: no cover
        
    def test_expected_sync(self):
        def f(a:RealOptional[Port], b:Response):
            pass  # pragma: no cover
        
        interfacer = interface_binder_for(f)
        with self.assertRaises(TypeError):
            @interfacer
            async def f1(b:Response):
                asyncio.sleep(1) # pragma: no cover
                return b # pragma: no cover
    

    def test_is_same_proto(self):
        def f1(a:int, b:str):
            pass
        def f2(k:int, b:str):
            pass

        self.assertEqual(is_already_described_prototype(f1, f2), True)

    def test_is_same_proto_false(self):
        def f1(a:int, b:str):
            pass
        def f2(a:int, b:int):
            pass

        self.assertEqual(is_already_described_prototype(f1, f2), False)

    def test_is_same_proto_false_and_handled(self):
        def f1(a:int, b:str):
            pass
        
        interfacer = interface_binder_for(f1)
        def f2(a:int, b:str):
            pass
    
        f3 = interfacer(f2)

        self.assertEqual(id(f2), id(f3))

    def test_remove_int(self):
        def proto(
            a: Remove[int],
            b: str
        ): ...
        interfacer = interface_binder_for(proto)

        @interfacer
        def f(o: int, b:str):
            pass
        
        print(inspect.signature(f))
        self.assertEqual(True, True)
