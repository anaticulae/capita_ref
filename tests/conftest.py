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
    power.BACHELOR051_PDF,
    power.BACHELOR056_PDF,
    power.BACHELOR063_PDF,
    power.BACHELOR076_PDF,
    power.BACHELOR077_PDF,
    power.BACHELOR090_PDF,
    power.BACHELOR111_PDF,
    power.BACHELOR128_PDF,
    power.BOOK173_PDF,
    power.DISS143_PDF,
    power.DISS167_PDF,
    power.DISS173_PDF,
    power.DOCU007_PDF,
    power.DOCU009_PDF,
    power.DOCU014_PDF,
    power.DOCU027_PDF,
    power.DOCU035_PDF,
    power.HOME018_PDF,
    power.MASTER031_PDF,
    power.MASTER049_PDF,
    power.MASTER072_PDF,
    power.MASTER075_PDF,
    power.MASTER083_PDF,
    power.MASTER091A_PDF,
    power.MASTER098_PDF,
    power.MASTER110_PDF,
    power.MASTER112_PDF,
    power.MASTER116_PDF,
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
