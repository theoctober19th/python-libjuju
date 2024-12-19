# Copyright 2024 Canonical Ltd.
# Licensed under the Apache V2, see LICENCE file for details.
from __future__ import annotations

from typing import AbstractSet, Iterable

from freezegun import freeze_time

from juju.model._idle import CheckStatus, Loop


def unroll(
    statuses: Iterable[CheckStatus | None],
    *,
    apps: AbstractSet[str],
    wait_for_exact_units: int | None = None,
    wait_for_units: int,
    idle_period: float,
) -> list[bool]:
    loop = Loop(
        apps=apps,
        wait_for_exact_units=wait_for_exact_units,
        wait_for_units=wait_for_units,
        idle_period=idle_period,
    )
    return [loop.next(s) for s in statuses]


def test_wait_for_apps():
    def checks():
        yield None
        yield None

    assert unroll(
        checks(),
        apps={"a"},
        wait_for_units=0,
        idle_period=0,
    ) == [False, False]


def test_at_least_units():
    def checks():
        units = {"u/0", "u/1", "u/2"}
        yield CheckStatus(units, ready_units={"u/0"}, idle_units=units)
        yield CheckStatus(units, ready_units={"u/0", "u/1"}, idle_units=units)
        yield CheckStatus(units, ready_units={"u/0", "u/1", "u/2"}, idle_units=units)

    with freeze_time():
        assert unroll(
            checks(),
            apps={"u"},
            wait_for_units=2,
            idle_period=0,
        ) == [False, True, True]


def test_for_exact_units():
    units = {"u/0", "u/1", "u/2"}
    good = CheckStatus(units, ready_units={"u/1", "u/2"}, idle_units=units)
    too_few = CheckStatus(units, ready_units={"u/2"}, idle_units=units)
    too_many = CheckStatus(units, ready_units={"u/1", "u/2", "u/0"}, idle_units=units)

    def checks():
        yield too_few
        yield good
        yield too_many
        yield good

    assert unroll(
        checks(),
        apps={"u"},
        wait_for_units=1,
        wait_for_exact_units=2,
        idle_period=0,
    ) == [False, True, False, True]


def test_idle_ping_pong():
    good = CheckStatus({"hexanator/0"}, {"hexanator/0"}, idle_units={"hexanator/0"})
    bad = CheckStatus({"hexanator/0"}, {"hexanator/0"}, idle_units=set())

    def checks():
        with freeze_time() as clock:
            for status in [good, bad, good, bad]:
                yield status
                clock.tick(10)

    assert unroll(
        checks(),
        apps={"hexanator"},
        wait_for_units=1,
        idle_period=15,
    ) == [False, False, False, False]


def test_idle_period():
    def checks():
        with freeze_time() as clock:
            for _ in range(4):
                yield CheckStatus({"hexanator/0"}, {"hexanator/0"}, {"hexanator/0"})
                clock.tick(10)

    assert unroll(
        checks(),
        apps={"hexanator"},
        wait_for_units=1,
        idle_period=15,
    ) == [False, False, True, True]
