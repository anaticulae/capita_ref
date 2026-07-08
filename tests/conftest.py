# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import gennex
import hoverpower
import pytest
import utilotest
from utilotest import mp  # pylint:disable=W0611
from utilotest import td  # pylint:disable=W0611

pytest_plugins = ['pytester', 'xdist']  # pylint: disable=invalid-name

hoverpower.setup(__file__)

RESOURCES = [
    hoverpower.BACHELOR029A_PDF,
    hoverpower.BACHELOR037_PDF,
    hoverpower.BACHELOR051_PDF,
    hoverpower.BACHELOR056_PDF,
    hoverpower.BACHELOR063_PDF,
    hoverpower.BACHELOR076_PDF,
    hoverpower.BACHELOR077_PDF,
    hoverpower.BACHELOR090_PDF,
    hoverpower.BACHELOR111_PDF,
    hoverpower.BACHELOR128_PDF,
    hoverpower.BOOK173_PDF,
    hoverpower.DISS143_PDF,
    hoverpower.DISS167_PDF,
    hoverpower.DISS172_PDF,
    hoverpower.DISS173_PDF,
    hoverpower.DOCU007_PDF,
    hoverpower.DOCU009_PDF,
    hoverpower.DOCU014_PDF,
    hoverpower.DOCU027_PDF,
    hoverpower.DOCU035_PDF,
    hoverpower.HC_DISS128,
    hoverpower.HOME018_PDF,
    hoverpower.MASTER031_PDF,
    hoverpower.MASTER049_PDF,
    hoverpower.MASTER072_PDF,
    hoverpower.MASTER075_PDF,
    hoverpower.MASTER083_PDF,
    hoverpower.MASTER091A_PDF,
    hoverpower.MASTER098_PDF,
    hoverpower.MASTER110_PDF,
    hoverpower.MASTER112_PDF,
    hoverpower.MASTER116_PDF,
    hoverpower.MASTER148_PDF,
    hoverpower.MASTER193_PDF,
    hoverpower.PAPER018_PDF,
]
WORKER = utilotest.worker_count(4, onci=len(RESOURCES))


@pytest.mark.usefixtures('session')
def pytest_sessionstart():
    hoverpower.run()


def extract(resources):
    gennex.extract(
        base=hoverpower.REPO,
        files=resources,
        cleanup=True,
        footnote=True,
        groupme='--hefopa',
        headnote=True,
        pagenumber=True,
        worker=WORKER,
    )
