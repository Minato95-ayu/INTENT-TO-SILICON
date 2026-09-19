# ==============================================================================
# COPYRIGHT (C) 2026 AYUSH GHRIT KAUSHIK. ALL RIGHTS RESERVED.
# 
# This source code is the proprietary intellectual property of Ayush Ghrit Kaushik.
# GitHub: https://github.com/Minato95-ayu
# 
# UNAUTHORIZED COPYING, REPRODUCTION, OR DISTRIBUTION IS STRICTLY PROHIBITED.
# ANY ATTEMPT TO CLONE OR CREATE DERIVATIVE WORKS FROM AAYU WILL BE SUBJECT
# TO LEGAL ACTION.
# ==============================================================================

import pytest

from runtime.stdlib.modules.auth_lib import get_jwt_secret, mint_jwt, verify_jwt


def test_auth_uses_configured_secret(monkeypatch):
    monkeypatch.setenv("AAYU_JWT_SECRET", "x" * 32)
    token = mint_jwt({"sub": "demo"})

    assert verify_jwt(token)["sub"] == "demo"


def test_auth_rejects_short_production_secret(monkeypatch):
    monkeypatch.setenv("AAYU_JWT_SECRET", "too-short")

    with pytest.raises(RuntimeError, match="at least 32 characters"):
        get_jwt_secret()


def test_auth_can_require_configured_secret(monkeypatch):
    monkeypatch.delenv("AAYU_JWT_SECRET", raising=False)

    with pytest.raises(RuntimeError, match="required in production"):
        get_jwt_secret(require_configured=True)