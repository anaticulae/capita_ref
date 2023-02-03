# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import elements.headline.lookup
import sections.feature
import sections.utils.headline
import serializeraw
import utila


def work(oneline_text: str, oneline_textpositions: str, pages=None) -> str:
    navigators = serializeraw.ptn_fromfile(
        oneline_text,
        oneline_textpositions,
        pages=pages,
    )
    result = sections.feature.pagebypage(
        navigators,
        analyse_page,
        name='publication',
    )
    dumped = serializeraw.dump_likelihood(result)
    return dumped


def analyse_page(content):
    headlines = sections.utils.headline.headlines(content)
    if not headlines:
        return sections.feature.NO_PAGE
    if utila.similar(
            expected=elements.headline.lookup.PUBLICATION,
            current=headlines,
            maxdiff=0.95,
    ):
        return sections.feature.PERFECT
    return sections.feature.NO_PAGE
