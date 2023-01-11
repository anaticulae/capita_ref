# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import genex
import power
import pytest
import utilatest
from utilatest import mp  # pylint:disable=W0611
from utilatest import td  # pylint:disable=W0611

pytest_plugins = ['pytester', 'xdist']  # pylint: disable=invalid-name

power.setup(__file__)

RESOURCES = [
    power.BACHELOR029A_PDF,
    power.BACHELOR037_PDF,
    power.BACHELOR090_PDF,
    power.BACHELOR128_PDF,
    power.BOOK173_PDF,
    power.DISS266_PDF,
    power.HOME018_PDF,
    power.MASTER110_PDF,
    power.MASTER148_PDF,
    power.MASTER193_PDF,
    power.PAPER018_PDF,
]
WORKER = utilatest.worker_count(4, onci=len(RESOURCES))


@pytest.mark.usefixtures('session')
def pytest_sessionstart():
    power.run()


def extract(resources):
    genex.extract(
        base=power.REPOSITORY,
        files=resources,
        cleanup=True,
        footnote=True,
        groupme='--hefopa',
        headnote=True,
        pagenumber=True,
        worker=WORKER,
    )
