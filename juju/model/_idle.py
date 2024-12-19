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
    """Units in good status (workload, agent, machine?)."""
    idle_units: set[str]
    """Units with stable agent status (FIXME details)."""


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

        # FIXME there's some confusion about what a "busy" unit is
        # are we ready when over the last idle_period, every time sampled:
        # a. >=N units were ready (possibly different each time), or
        # b. >=N units were ready each time
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

    # Order of errors:
    #
    # Machine error (any unit of any app from apps)
    # Agent error (-"-)
    # Workload error (-"-)
    # App error (any app from apps)
    #
    # Workload blocked (any unit of any app from apps)
    # App blocked (any app from apps)
    units: dict[str, UnitStatus] = {}

    for app_name in apps:
        units.update(_app_units(full_status, app_name))

    for unit_name, unit in units.items():
        if unit.machine:
            machine = full_status.machines[unit.machine]
            assert isinstance(machine, MachineStatus)
            assert machine.instance_status
            if machine.instance_status.status == "error" and raise_on_error:
                raise JujuMachineError(
                    f"{unit_name!r} machine {unit.machine!r} has errored: {machine.instance_status.info!r}"
                )

    for unit_name, unit in units.items():
        assert unit.agent_status
        if unit.agent_status.status == "error" and raise_on_error:
            raise JujuAgentError(
                f"{unit_name!r} agent has errored: {unit.agent_status.info!r}"
            )

    for unit_name, unit in units.items():
        assert unit.workload_status
        if unit.workload_status.status == "error" and raise_on_error:
            raise JujuUnitError(
                f"{unit_name!r} workload has errored: {unit.workload_status.info!r}"
            )

    for app_name in apps:
        app = full_status.applications[app_name]
        assert isinstance(app, ApplicationStatus)
        assert app.status
        if app.status.status == "error" and raise_on_error:
            raise JujuAppError(f"{app_name!r} has errored: {app.status.info!r}")

    for unit_name, unit in units.items():
        assert unit.workload_status
        if unit.workload_status.status == "blocked" and raise_on_blocked:
            raise JujuUnitError(
                f"{unit_name!r} workload is blocked: {unit.workload_status.info!r}"
            )

    for app_name in apps:
        app = full_status.applications[app_name]
        assert isinstance(app, ApplicationStatus)
        assert app.status
        if app.status.status == "blocked" and raise_on_blocked:
            raise JujuAppError(f"{app_name!r} is blocked: {app.status.info!r}")

    rv = CheckStatus(set(), set(), set())

    for app_name in apps:
        app = full_status.applications[app_name]
        assert isinstance(app, ApplicationStatus)
        for unit_name, unit in _app_units(full_status, app_name).items():
            rv.units.add(unit_name)
            assert unit.agent_status
            assert unit.workload_status

            if unit.agent_status.status == "idle":
                rv.idle_units.add(unit_name)

            if not status or unit.workload_status.status == status:
                rv.ready_units.add(unit_name)

    return rv


def _app_units(full_status: FullStatus, app_name: str) -> dict[str, UnitStatus]:
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
