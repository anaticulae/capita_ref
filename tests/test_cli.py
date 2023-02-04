# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import pytest
import utila
import utilatest

import tests


@utilatest.requires(power.HC_DISS128)
def test_run_diss128_hc(testdir, mp):
    source = power.link(power.HC_DISS128)
    if not utila.exists(source):
        # TODO: REMOVE AFTER FIXING UTILATEST
        pytest.skip(f'require/generated: {source}')
    cmd = f'-i {source} -o {testdir.tmpdir}'
    tests.run(cmd, mp=mp)
