# Copyright 2024 Canonical Ltd.
# Licensed under the Apache V2, see LICENCE file for details.
from __future__ import annotations

import pytest
from freezegun import freeze_time

from juju.model._idle import CheckStatus, loop


# Missing tests
#
# FIXME hexanator idle period 1
# FIXME workload maintenance, idle period 0
# FIXME test exact count == 2
# FIXME test exact count != 2 (1, 3)
# FIXME exact count vs wait_for_units
# FIXME expected idle 1s below
# FIXME idle period 1
# FIXME sending status=None, meaning some apps are still missing
#
@pytest.mark.xfail(reason="FIXME I misunderstood what 'idle' means")
async def test_at_least_units():
    async def checks():
        yield CheckStatus({"u/0", "u/1", "u/2"}, {"u/0"}, set())
        yield CheckStatus({"u/0", "u/1", "u/2"}, {"u/0", "u/1"}, set())
        yield CheckStatus({"u/0", "u/1", "u/2"}, {"u/0", "u/1", "u/2"}, set())

    with freeze_time():
        assert [
            v
            async for v in loop(
                checks(),
                apps=frozenset(["u"]),
                wait_for_units=2,
                idle_period=0,
            )
        ] == [False, True, True]


async def test_ping_pong():
    good = CheckStatus({"hexanator/0"}, {"hexanator/0"}, set())
    bad = CheckStatus({"hexanator/0"}, set(), set())

    async def checks():
        with freeze_time() as clock:
            for _ in range(3):
                yield good
                clock.tick(10)
                yield bad
                clock.tick(10)

    assert [
        v
        async for v in loop(
            checks(),
            apps=frozenset(["hexanator"]),
            wait_for_units=1,
            idle_period=15,
        )
    ] == [False] * 6
