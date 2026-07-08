# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import configos
import iamraw
import utilo

DIFF_MAX = configos.HolyTable(
    items=(
        (1, 0),
        (5, 0),
        (6, 1),
        (10, 2),
        (12, 2),
    ),
    right_outranges_none=False,
)


def cluster_bibpages(items):
    """Select hugest(max sum likelihood value) group."""
    if not items:
        return []
    maxdiff = DIFF_MAX(len(items)) + 1
    grouped = utilo.groupby_diff(
        items,
        maxdiff=maxdiff,
        selector=lambda x: x.page,
    )
    if not grouped:
        return []
    hugest = sorted(
        grouped,
        key=lambda x: sum(item.content.value for item in x),
    )
    hugest = hugest[-1]
    avg = sum((item.content.value for item in hugest)) / len(hugest)
    avg = utilo.roundme(avg)
    for item in hugest:
        # every item of the group should have the same likelihood
        item.content.value = avg
    result = fill_empty(hugest)
    return result


def fill_empty(items: list) -> list:
    """Fill holes inside connected bib."""
    result = list(items)
    start, end = result[0].page, result[-1].page
    done = {item.page for item in result}
    avg = result[0].content.value
    for page in utilo.rlist(start, end):
        if page in done:
            continue
        result.append(
            iamraw.PageContentLikelihood(
                page=page,
                content=iamraw.Likelihood(
                    value=avg,
                    name='bibliography_table',
                ),
            ))
    result.sort(key=lambda x: x.page)
    return result
