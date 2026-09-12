import json
import sqlite3
from urllib.error import HTTPError
from urllib.request import Request, urlopen

import pytest

from compiler.bytecode.encoder import BytecodeEncoder
from compiler.ir.pipeline import IRPipeline
from compiler.lexer.lexer import Lexer
from compiler.parser.parser import Parser
from compiler.semantic.analyzer import SemanticAnalyzer
from runtime.vm.vm import VirtualMachine


def compile_source(source: str):
    ast = Parser(Lexer(source).tokenize()).parse()
    semantic = SemanticAnalyzer().analyze(ast)
    pipeline = IRPipeline()
    lir = pipeline.to_lir(pipeline.to_mir(pipeline.to_hir(semantic)))
    return BytecodeEncoder().encode(lir)


def test_aayu_page_model_and_http_route_work_together():
    program = compile_source(
        """
        app AayuWeb
        model Greeting {
            message: String
        }
        route "/hello"
            get
                return "hello from AAYU"
            end
        end
        page Home
            heading "AAYU Studio"
        end
        """
    )
    vm = VirtualMachine()
    vm.api_router.port = 0
    vm.load(program.bytecode, program.constant_pool.values(), program.action_addresses)

    try:
        vm.execute()
        assert "Greeting" in vm.database.models
        assert "/hello" in vm.api_router.routes

        with urlopen(f"http://127.0.0.1:{vm.api_router.port}/hello") as response:
            assert response.status == 200
            assert response.read().decode("utf-8") == "hello from AAYU"
    finally:
        vm.api_router.stop()


def test_unknown_route_returns_not_found():
    program = compile_source(
        """
        route "/hello"
            get
                return "ok"
            end
        end
        """
    )
    vm = VirtualMachine()
    vm.api_router.port = 0
    vm.load(program.bytecode, program.constant_pool.values(), program.action_addresses)

    try:
        vm.execute()
        try:
            urlopen(f"http://127.0.0.1:{vm.api_router.port}/missing")
        except HTTPError as error:
            assert error.code == 404
        else:
            raise AssertionError("Unknown route unexpectedly returned success")
    finally:
        vm.api_router.stop()


def test_oversized_request_body_is_rejected():
    program = compile_source(
        """
        route "/submit"
            post
                return "ok"
            end
        end
        """
    )
    vm = VirtualMachine()
    vm.api_router.port = 0
    vm.api_router.max_body_bytes = 2
    vm.load(program.bytecode, program.constant_pool.values(), program.action_addresses)

    try:
        vm.execute()
        request = Request(
            f"http://127.0.0.1:{vm.api_router.port}/submit",
            data=b"too-large",
            method="POST",
        )
        try:
            urlopen(request)
        except HTTPError as error:
            assert error.code == 413
        else:
            raise AssertionError("Oversized request unexpectedly returned success")
    finally:
        vm.api_router.stop()


def test_rate_limit_returns_too_many_requests():
    program = compile_source(
        """
        route "/hello"
            get
                return "ok"
            end
        end
        """
    )
    vm = VirtualMachine()
    vm.api_router.port = 0
    vm.api_router.rate_limit = 1
    vm.api_router.rate_window_seconds = 60
    vm.load(program.bytecode, program.constant_pool.values(), program.action_addresses)

    try:
        vm.execute()
        urlopen(f"http://127.0.0.1:{vm.api_router.port}/hello").read()
        try:
            urlopen(f"http://127.0.0.1:{vm.api_router.port}/hello")
        except HTTPError as error:
            assert error.code == 429
        else:
            raise AssertionError("Rate-limited request unexpectedly returned success")
    finally:
        vm.api_router.stop()


def test_vm_shutdown_stops_route_server_and_closes_resources():
    vm = VirtualMachine()
    vm.api_router.start()
    assert vm.api_router.server is not None

    vm.shutdown()

    assert vm.api_router.server is None
    with pytest.raises(sqlite3.ProgrammingError):
        vm.database.conn.execute("SELECT 1")


def test_protected_route_requires_bearer_token_and_sets_security_headers():
    program = compile_source(
        """
        route "/private"
            get
                return "private"
            end
        end
        """
    )
    vm = VirtualMachine()
    vm.api_router.port = 0
    vm.api_router.require_auth = True
    vm.api_router.auth_verifier = lambda token: token == "valid"
    vm.load(program.bytecode, program.constant_pool.values(), program.action_addresses)

    try:
        vm.execute()
        url = f"http://127.0.0.1:{vm.api_router.port}/private"
        try:
            urlopen(url)
        except HTTPError as error:
            assert error.code == 401
        else:
            raise AssertionError("Protected route accepted an anonymous request")

        request = Request(url, headers={"Authorization": "Bearer valid"})
        with urlopen(request) as response:
            assert response.status == 200
            assert response.read().decode("utf-8") == "private"
            assert response.headers["X-Request-ID"]
            assert response.headers["X-Content-Type-Options"] == "nosniff"
            assert response.headers["X-Frame-Options"] == "DENY"
    finally:
        vm.api_router.stop()