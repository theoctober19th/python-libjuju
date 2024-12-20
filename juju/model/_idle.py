# Copyright 2024 Canonical Ltd.
# Licensed under the Apache V2, see LICENCE file for details.
"""Implementation of Model.wait_for_idle(), analog to `juju wait_for`."""

from __future__ import annotations

import logging
import time
from dataclasses import dataclass
from typing import AbstractSet

from ..client._definitions import (
    ApplicationStatus,
    FullStatus,
    MachineStatus,
    UnitStatus,
)
from ..errors import JujuAgentError, JujuAppError, JujuMachineError, JujuUnitError

logger = logging.getLogger(__name__)


@dataclass
class CheckStatus:
    """Return type check(), represents single loop iteration."""

    units: set[str]
    """All units visible at this point."""
    ready_units: set[str]
    """Units with the expected workload status."""
    idle_units: set[str]
    """Units with stable (idle) agent status."""


class Loop:
    def __init__(
        self,
        *,
        apps: AbstractSet[str],
        wait_for_exact_units: int | None = None,
        wait_for_units: int,
        idle_period: float,
    ):
        self.apps = apps
        self.wait_for_exact_units = wait_for_exact_units
        self.wait_for_units = wait_for_units
        self.idle_period = idle_period
        self.idle_since: dict[str, float] = {}

    def next(self, status: CheckStatus | None) -> bool:
        logger.info("wait_for_idle iteration %s", status)
        now = time.monotonic()

        if not status:
            return False

        expected_idle_since = now - self.idle_period

        for name in status.units:
            if name in status.idle_units:
                self.idle_since[name] = min(
                    now, self.idle_since.get(name, float("inf"))
                )
            else:
                self.idle_since[name] = float("inf")

        if busy := {n for n, t in self.idle_since.items() if t > expected_idle_since}:
            logger.info("Waiting for units to be idle enough: %s", busy)
            return False

        for app_name in self.apps:
            ready_units = [
                n for n in status.ready_units if n.startswith(f"{app_name}/")
            ]
            if len(ready_units) < self.wait_for_units:
                logger.info(
                    "Waiting for app %r units %s >= %s",
                    app_name,
                    len(status.ready_units),
                    self.wait_for_units,
                )
                return False

            if (
                self.wait_for_exact_units is not None
                and len(ready_units) != self.wait_for_exact_units
            ):
                logger.info(
                    "Waiting for app %r units %s == %s",
                    app_name,
                    len(ready_units),
                    self.wait_for_exact_units,
                )
                return False

        return True


def check(
    full_status: FullStatus,
    *,
    apps: AbstractSet[str],
    raise_on_error: bool,
    raise_on_blocked: bool,
    status: str | None,
) -> CheckStatus | None:
    """A single iteration of a wait_for_idle loop."""
    for app_name in apps:
        if not full_status.applications.get(app_name):
            logger.info("Waiting for app %r", app_name)
            return None

    units: dict[str, UnitStatus] = {}
    rv = CheckStatus(set(), set(), set())

    for app_name in apps:
        units.update(app_units(full_status, app_name))

    if raise_on_error:
        check_errors(full_status, apps, units)

    if raise_on_blocked:
        check_blocked(full_status, apps, units)

    for app_name in apps:
        app = full_status.applications[app_name]
        assert isinstance(app, ApplicationStatus)

        for unit_name, unit in app_units(full_status, app_name).items():
            rv.units.add(unit_name)
            assert unit.agent_status
            assert unit.workload_status

            if unit.agent_status.status == "idle":
                rv.idle_units.add(unit_name)

            if not status or unit.workload_status.status == status:
                rv.ready_units.add(unit_name)

    return rv


def check_errors(
    full_status: FullStatus, apps: AbstractSet[str], units: dict[str, UnitStatus]
) -> None:
    """Check the full status for error conditions, in this order:

    - Machine error (any unit of any app from apps)
    - Agent error (-"-)
    - Workload error (-"-)
    - App error (any app from apps)
    """
    for unit_name, unit in units.items():
        if unit.machine:
            machine = full_status.machines[unit.machine]
            assert isinstance(machine, MachineStatus)
            assert machine.instance_status
            if machine.instance_status.status == "error":
                raise JujuMachineError(
                    f"{unit_name!r} machine {unit.machine!r} has errored: {machine.instance_status.info!r}"
                )

    for unit_name, unit in units.items():
        assert unit.agent_status
        if unit.agent_status.status == "error":
            raise JujuAgentError(
                f"{unit_name!r} agent has errored: {unit.agent_status.info!r}"
            )

    for unit_name, unit in units.items():
        assert unit.workload_status
        if unit.workload_status.status == "error":
            raise JujuUnitError(
                f"{unit_name!r} workload has errored: {unit.workload_status.info!r}"
            )

    for app_name in apps:
        app = full_status.applications[app_name]
        assert isinstance(app, ApplicationStatus)
        assert app.status
        if app.status.status == "error":
            raise JujuAppError(f"{app_name!r} has errored: {app.status.info!r}")


def check_blocked(
    full_status: FullStatus, apps: AbstractSet[str], units: dict[str, UnitStatus]
) -> None:
    """Check the full status for blocked conditions, in this order:

    - Workload blocked (any unit of any app from apps)
    - App blocked (any app from apps)
    """
    for unit_name, unit in units.items():
        assert unit.workload_status
        if unit.workload_status.status == "blocked":
            raise JujuUnitError(
                f"{unit_name!r} workload is blocked: {unit.workload_status.info!r}"
            )

    for app_name in apps:
        app = full_status.applications[app_name]
        assert isinstance(app, ApplicationStatus)
        assert app.status
        if app.status.status == "blocked":
            raise JujuAppError(f"{app_name!r} is blocked: {app.status.info!r}")


def app_units(full_status: FullStatus, app_name: str) -> dict[str, UnitStatus]:
    """Fish out the app's units' status from a FullStatus response."""
    rv: dict[str, UnitStatus] = {}
    app = full_status.applications[app_name]
    assert isinstance(app, ApplicationStatus)

    if app.subordinate_to:
        parent_name = app.subordinate_to[0]
        parent = full_status.applications[parent_name]
        assert isinstance(parent, ApplicationStatus)
        for parent_unit in parent.units.values():
            assert isinstance(parent_unit, UnitStatus)
            for name, unit in parent_unit.subordinates.items():
                if not name.startswith(f"{app_name}/"):
                    continue
                assert isinstance(unit, UnitStatus)
                rv[name] = unit
    else:
        for name, unit in app.units.items():
            assert isinstance(unit, UnitStatus)
            rv[name] = unit

    return rv
