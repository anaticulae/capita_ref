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
import serializeraw
import utilatest

import sections_ref.biblio.specialchars


@pytest.mark.parametrize('value, nobib_count_min', [
    pytest.param(' a) Fall 1: Kosovo             S. 184', 2),
])
def test_nobib(value, nobib_count_min):
    assert sections_ref.biblio.specialchars.nobib(value, nobib_count_min)


@pytest.mark.parametrize('source, page', [
    pytest.param(power.DISS172_PDF, 90, id='diss172_90'),
    pytest.param(power.DISS172_PDF, 142, id='diss172_142'),
    pytest.param(power.DISS172_PDF, 143, id='diss172_143'),
])
def test_document_page_nobib(source, page):
    utilatest.fixture_requires(source)
    source = power.link(source)
    content = serializeraw.ptcn_frompath(source, pages=page)[0]
    assert not sections_ref.biblio.specialchars.nobib(content.debug)
