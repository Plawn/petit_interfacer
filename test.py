from __future__ import annotations

import unittest
from dataclasses import dataclass
from typing import Optional

import petit_interfacer
from petit_interfacer import RealOptional, BlindBind, Dataclass
from petit_interfacer.exceptions import MissingHints, TooManyBlindBinds


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
    ... #pragma: no cover


bind_interface = petit_interfacer.interface_binder_for(proto)


@dataclass
class Data:
    jeb: int


def func_a(port: Port, k: Data) -> Response:
    return Response(f'test: {port}')


class BasicTests(unittest.TestCase):
    def test_interface_binder_for(self):
        bound_a = bind_interface(func_a)
        port = 80
        self.assertEqual(bound_a(worker=None, port=port,
                                 deb=None), f'test: {port}')

    def test_fail_bind(self):
        def f(port, p):
            pass #pragma: no cover
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
            pass #pragma: no cover
        with self.assertRaises(TooManyBlindBinds):
            interfacer = petit_interfacer.interface_binder_for(f)

    # def test_blind_bind(self):
    #     pass


if __name__ == '__main__':
    # bound = bind_interface(func_a)
    # a = bound(worker=None, port=80)
    # print(f'Response is: \n{a}')
    unittest.main()
