# Copyright 2024 Canonical Ltd.
# Licensed under the Apache V2, see LICENCE file for details.
from __future__ import annotations

import copy
import json
from typing import Any

import pytest

from juju.client._definitions import FullStatus
from juju.client.facade import _convert_response
from juju.errors import JujuAgentError, JujuAppError, JujuMachineError, JujuUnitError
from juju.model._idle import CheckStatus, check


def test_check_status(full_status: FullStatus, kwargs):
    status = check(full_status, **kwargs)
    units = {
        "grafana-agent-k8s/0",
        "hexanator/0",
        "mysql-test-app/0",
        "mysql-test-app/1",
    }
    assert status == CheckStatus(units, units, units)


def test_check_status_missing_app(full_status: FullStatus, kwargs):
    kwargs["apps"] = ["missing", "hexanator"]
    status = check(full_status, **kwargs)
    assert status is None


def test_check_status_is_selective(full_status: FullStatus, kwargs):
    kwargs["apps"] = ["hexanator"]
    status = check(full_status, **kwargs)
    assert status == CheckStatus({"hexanator/0"}, {"hexanator/0"}, {"hexanator/0"})


def test_no_apps(full_status: FullStatus, kwargs):
    kwargs["apps"] = []
    status = check(full_status, **kwargs)
    assert status == CheckStatus(set(), set(), set())


def test_missing_app(full_status: FullStatus, kwargs):
    kwargs["apps"] = ["missing"]
    status = check(full_status, **kwargs)
    assert status is None


def test_no_units(response: dict[str, Any], kwargs):
    response["response"]["applications"]["hexanator"]["units"].clear()
    kwargs["apps"] = ["hexanator"]
    status = check(convert(response), **kwargs)
    assert status == CheckStatus(set(), set(), set())


def test_app_error(response: dict[str, Any], kwargs):
    app = response["response"]["applications"]["hexanator"]
    app["status"]["status"] = "error"
    app["status"]["info"] = "big problem"

    kwargs["apps"] = ["hexanator"]
    kwargs["raise_on_error"] = True

    with pytest.raises(JujuAppError) as e:
        check(convert(response), **kwargs)

    assert "big problem" in str(e)


def test_ready_units(full_status: FullStatus, kwargs):
    kwargs["apps"] = ["mysql-test-app"]
    status = check(full_status, **kwargs)
    units = {"mysql-test-app/0", "mysql-test-app/1"}
    assert status == CheckStatus(units, units, units)


def test_active_units(full_status: FullStatus, kwargs):
    kwargs["apps"] = ["mysql-test-app"]
    kwargs["status"] = "active"
    status = check(full_status, **kwargs)
    units = {"mysql-test-app/0", "mysql-test-app/1"}
    assert status == CheckStatus(units, ready_units=set(), idle_units=units)


def test_ready_unit_requires_idle_agent(response: dict[str, Any], kwargs):
    app = response["response"]["applications"]["hexanator"]
    app["units"]["hexanator/1"] = copy.deepcopy(app["units"]["hexanator/0"])
    app["units"]["hexanator/1"]["agent-status"]["status"] = "some-other"

    kwargs["apps"] = ["hexanator"]
    kwargs["status"] = "active"

    status = check(convert(response), **kwargs)
    assert status == CheckStatus(
        {"hexanator/0", "hexanator/1"},
        {"hexanator/0", "hexanator/1"},
        idle_units={"hexanator/0"},
    )


def test_ready_unit_requires_workload_status(response: dict[str, Any], kwargs):
    app = response["response"]["applications"]["hexanator"]
    app["units"]["hexanator/1"] = copy.deepcopy(app["units"]["hexanator/0"])
    app["units"]["hexanator/1"]["workload-status"]["status"] = "some-other"

    kwargs["apps"] = ["hexanator"]
    kwargs["status"] = "active"

    status = check(convert(response), **kwargs)
    units = {"hexanator/0", "hexanator/1"}
    assert status == CheckStatus(units, ready_units={"hexanator/0"}, idle_units=units)


def test_agent_error(response: dict[str, Any], kwargs):
    app = response["response"]["applications"]["hexanator"]
    app["units"]["hexanator/0"]["agent-status"]["status"] = "error"
    app["units"]["hexanator/0"]["agent-status"]["info"] = "agent problem"

    kwargs["apps"] = ["hexanator"]
    kwargs["raise_on_error"] = True

    with pytest.raises(JujuAgentError) as e:
        check(convert(response), **kwargs)

    assert "hexanator/0" in str(e)
    assert "agent problem" in str(e)


def test_workload_error(response: dict[str, Any], kwargs):
    app = response["response"]["applications"]["hexanator"]
    app["units"]["hexanator/0"]["workload-status"]["status"] = "error"
    app["units"]["hexanator/0"]["workload-status"]["info"] = "workload problem"

    kwargs["apps"] = ["hexanator"]
    kwargs["raise_on_error"] = True

    with pytest.raises(JujuUnitError) as e:
        check(convert(response), **kwargs)

    assert "hexanator/0" in str(e)
    assert "workload problem" in str(e)


def test_machine_ok(response: dict[str, Any], kwargs):
    app = response["response"]["applications"]["hexanator"]
    app["units"]["hexanator/0"]["machine"] = "42"
    # https://github.com/dimaqq/juju-schema-analysis/blob/main/schemas-juju-3.5.4.model-user.txt#L3611-L3674
    response["response"]["machines"] = {
        "42": {
            "instance-status": {
                "status": "running",
                "info": "RUNNING",
            },
        },
    }

    kwargs["apps"] = ["hexanator"]
    kwargs["raise_on_error"] = True

    status = check(convert(response), **kwargs)
    assert status == CheckStatus({"hexanator/0"}, {"hexanator/0"}, {"hexanator/0"})


def test_machine_error(response: dict[str, Any], kwargs):
    app = response["response"]["applications"]["hexanator"]
    app["units"]["hexanator/0"]["machine"] = "42"
    response["response"]["machines"] = {
        "42": {
            "instance-status": {
                "status": "error",
                "info": "Battery low. Try a potato?",
            },
        },
    }

    kwargs["apps"] = ["hexanator"]
    kwargs["raise_on_error"] = True

    with pytest.raises(JujuMachineError) as e:
        check(convert(response), **kwargs)

    assert "potato" in str(e)


def test_app_blocked(response: dict[str, Any], kwargs):
    app = response["response"]["applications"]["hexanator"]
    app["status"]["status"] = "blocked"
    app["status"]["info"] = "big problem"

    kwargs["apps"] = ["hexanator"]
    kwargs["raise_on_blocked"] = True

    with pytest.raises(JujuAppError) as e:
        check(convert(response), **kwargs)

    assert "big problem" in str(e)


def test_unit_blocked(response: dict[str, Any], kwargs):
    app = response["response"]["applications"]["hexanator"]
    app["units"]["hexanator/0"]["workload-status"]["status"] = "blocked"
    app["units"]["hexanator/0"]["workload-status"]["info"] = "small problem"

    kwargs["apps"] = ["hexanator"]
    kwargs["raise_on_blocked"] = True

    with pytest.raises(JujuUnitError) as e:
        check(convert(response), **kwargs)

    assert "small problem" in str(e)


def test_no_raise_on(response: dict[str, Any], kwargs):
    app = response["response"]["applications"]["hexanator"]
    app["units"]["hexanator/0"]["workload-status"]["status"] = "blocked"
    app["units"]["hexanator/0"]["workload-status"]["info"] = "small problem"
    app["units"]["hexanator/0"]["machine"] = "42"
    response["response"]["machines"] = {
        "42": {
            "instance-status": {
                "status": "running",
                "info": "RUNNING",
            },
        },
    }

    kwargs["apps"] = ["hexanator"]
    kwargs["raise_on_blocked"] = False
    kwargs["raise_on_error"] = False

    status = check(convert(response), **kwargs)
    assert status  # didn't raise an exception


def test_maintenance(response: dict[str, Any], kwargs):
    """Taken from nginx-ingress-integrator-operator integration tests."""
    app = response["response"]["applications"]["hexanator"]
    app["status"]["status"] = "maintenance"
    app["units"]["hexanator/0"]["workload-status"]["status"] = "maintenance"

    kwargs["apps"] = ["hexanator"]
    kwargs["status"] = "maintenance"

    status = check(convert(response), **kwargs)
    assert status == CheckStatus({"hexanator/0"}, {"hexanator/0"}, {"hexanator/0"})


@pytest.fixture
def kwargs() -> dict[str, Any]:
    return dict(
        apps=["hexanator", "grafana-agent-k8s", "mysql-test-app"],
        raise_on_error=False,
        raise_on_blocked=False,
        status=None,
    )


@pytest.fixture
def response(pytestconfig: pytest.Config) -> dict[str, Any]:
    return json.loads(
        (pytestconfig.rootpath / "tests/unit/data/fullstatus.json").read_text()
    )


def convert(data: dict[str, Any]) -> FullStatus:
    return _convert_response(data, cls=FullStatus)


@pytest.fixture
def full_status(response) -> FullStatus:
    return convert(response)
