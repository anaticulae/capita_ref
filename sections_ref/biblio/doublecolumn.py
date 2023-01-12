# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import configo
import geostrat
import sections.utils.spa
import texmex
import utila

import sections_ref.biblio.utils

LIKELIHOOD_MIN = configo.HV_PERCENT_PLUS(default=30)
MARKER_COUNT_MIN = configo.HV_INT_PLUS(default=50)


def extract(data: sections.utils.spa.Data) -> list:
    # configure spa
    config = sections.utils.spa.Config(
        likelihood_name='bibliography_table',
        page_analysis=analyse_page,
    )
    # run spa
    extracted = sections.utils.spa.work(data=data, config=config)
    # ignore to low valued bib pages
    valid = [item for item in extracted if item.content.value > LIKELIHOOD_MIN]
    # determine hugest connected bib cluster
    hugest = sections_ref.biblio.utils.cluster_bibpages(valid)
    return hugest


def analyse_page(ptn: texmex.PTN) -> sections.feature.StatisticalResultItem:
    parsed = geostrat.parse(ptn, column_count=2)
    if not parsed:
        # no double column page
        return len(ptn), 0
    marker = 0
    # count prenom construct for both data columns
    left, right = parsed
    for item in left + right:
        marker += len(prenom(item.text))
    if marker <= MARKER_COUNT_MIN:
        # too few matches
        return len(ptn), 0
    return len(ptn), marker


PRENOM = utila.compiles(r'[a-z]+\s(?P<prenom>\w\.)')


def prenom(raw: str) -> tuple:
    """\
    >>> prenom('Becker J. & Franz S.')
    ('J.', 'S.')
    >>> prenom('1230 1.')
    ()
    """
    result = [item[0] + '.' for item in PRENOM.findall(raw)]
    return tuple(result)
