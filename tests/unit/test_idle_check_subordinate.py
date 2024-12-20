# Copyright 2024 Canonical Ltd.
# Licensed under the Apache V2, see LICENCE file for details.
from __future__ import annotations

import json
from typing import Any

import pytest

from juju.client._definitions import FullStatus
from juju.client.facade import _convert_response
from juju.model._idle import CheckStatus, check


def test_subordinate_apps(response: dict[str, Any], kwargs):
    status = check(convert(response), **kwargs)
    assert status == CheckStatus(
        {"ntp/0", "ubuntu/0"},
        {"ntp/0", "ubuntu/0"},
        {"ntp/0", "ubuntu/0"},
    )


def test_subordinate_is_selective(response, kwargs):
    subordinates = response["response"]["applications"]["ubuntu"]["units"]["ubuntu/0"][
        "subordinates"
    ]
    subordinates["some-other/0"] = subordinates["ntp/0"]
    status = check(convert(response), **kwargs)
    assert status == CheckStatus(
        {"ntp/0", "ubuntu/0"},
        {"ntp/0", "ubuntu/0"},
        {"ntp/0", "ubuntu/0"},
    )


@pytest.fixture
def kwargs() -> dict[str, Any]:
    return dict(
        apps=["ntp", "ubuntu"],
        raise_on_error=False,
        raise_on_blocked=False,
        status=None,
    )


@pytest.fixture
def response(pytestconfig: pytest.Config) -> dict[str, Any]:
    """Juju rpc response JSON to a FullStatus call."""
    return json.loads(
        (
            pytestconfig.rootpath / "tests/unit/data/subordinate-fullstatus.json"
        ).read_text()
    )


@pytest.fixture
def subordinate_status(response) -> FullStatus:
    return convert(response)


def convert(data: dict[str, Any]) -> FullStatus:
    return _convert_response(data, cls=FullStatus)
