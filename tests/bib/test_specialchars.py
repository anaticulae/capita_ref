# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import pytest

import sections_ref.biblio.specialchars


@pytest.mark.parametrize('value, nobib_count_min', [
    pytest.param(' a) Fall 1: Kosovo             S. 184', 2),
])
def test_nobib(value, nobib_count_min):
    assert sections_ref.biblio.specialchars.nobib(value, nobib_count_min)
