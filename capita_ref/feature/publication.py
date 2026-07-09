# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import capita.feature
import capita.utils.headline
import configos
import elementae.headline.lookup
import serializeraw
import utilo

FEATURE_PAGE_COUNT_MIN = configos.HV_INT_PLUS(default=120)

EMPTY = serializeraw.dump_likelihood([])


def work(
    oneline_text: str,
    oneline_textpositions: str,
    pdflog: str,
    pages=None,
) -> str:
    if utilo.exists(pdflog):
        loaded = serializeraw.load_pdfinfo(pdflog)
        if loaded.pages < FEATURE_PAGE_COUNT_MIN:
            utilo.log(f'skip publication, too few pages: {loaded.pages}')
            return EMPTY
    navigators = serializeraw.ptn_fromfile(
        oneline_text,
        oneline_textpositions,
        pages=pages,
    )
    result = capita.feature.pagebypage(
        navigators,
        analyse_page,
        name='publication',
    )
    dumped = serializeraw.dump_likelihood(result)
    return dumped


def analyse_page(content):
    headlines = capita.utils.headline.headlines(content)
    if not headlines:
        return capita.feature.NO_PAGE
    if utilo.similar(
            expected=elementae.headline.lookup.PUBLICATION,
            current=headlines,
            maxdiff=0.95,
    ):
        return capita.feature.PERFECT
    return capita.feature.NO_PAGE
