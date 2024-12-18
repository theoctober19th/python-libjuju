# Copyright 2024 Canonical Ltd.
# Licensed under the Apache V2, see LICENCE file for details.
from __future__ import annotations

from freezegun import freeze_time

from juju.model._idle import CheckStatus, loop


async def alist(agen):
    return [v async for v in agen]


async def test_wait_for_apps():
    async def checks():
        yield None
        yield None

    assert await alist(
        loop(
            checks(),
            apps={"a"},
            wait_for_units=0,
            idle_period=0,
        )
    ) == [False, False]


async def test_at_least_units():
    async def checks():
        yield CheckStatus({"u/0", "u/1", "u/2"}, {"u/0"}, {"u/0", "u/1", "u/2"})
        yield CheckStatus({"u/0", "u/1", "u/2"}, {"u/0", "u/1"}, {"u/0", "u/1", "u/2"})
        yield CheckStatus(
            {"u/0", "u/1", "u/2"}, {"u/0", "u/1", "u/2"}, {"u/0", "u/1", "u/2"}
        )

    with freeze_time():
        assert await alist(
            loop(
                checks(),
                apps={"u"},
                wait_for_units=2,
                idle_period=0,
            )
        ) == [False, True, True]


async def test_for_exact_units():
    good = CheckStatus(
        {"u/0", "u/1", "u/2"},
        {"u/1", "u/2"},
        {"u/0", "u/1", "u/2"},
    )
    too_few = CheckStatus(
        {"u/0", "u/1", "u/2"},
        {"u/2"},
        {"u/0", "u/1", "u/2"},
    )
    too_many = CheckStatus(
        {"u/0", "u/1", "u/2"},
        {"u/1", "u/2", "u/0"},
        {"u/0", "u/1", "u/2"},
    )

    async def checks():
        yield too_few
        yield good
        yield too_many
        yield good

    assert await alist(
        loop(
            checks(),
            apps={"u"},
            wait_for_units=1,
            wait_for_exact_units=2,
            idle_period=0,
        )
    ) == [False, True, False, True]


async def test_idle_ping_pong():
    good = CheckStatus({"hexanator/0"}, {"hexanator/0"}, {"hexanator/0"})
    bad = CheckStatus({"hexanator/0"}, {"hexanator/0"}, set())

    async def checks():
        with freeze_time() as clock:
            for status in [good, bad, good, bad]:
                yield status
                clock.tick(10)

    assert await alist(
        loop(
            checks(),
            apps={"hexanator"},
            wait_for_units=1,
            idle_period=15,
        )
    ) == [False, False, False, False]


async def test_idle_period():
    async def checks():
        with freeze_time() as clock:
            for _ in range(4):
                yield CheckStatus({"hexanator/0"}, {"hexanator/0"}, {"hexanator/0"})
                clock.tick(10)

    assert await alist(
        loop(
            checks(),
            apps={"hexanator"},
            wait_for_units=1,
            idle_period=15,
        )
    ) == [False, False, True, True]
