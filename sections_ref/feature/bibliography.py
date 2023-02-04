# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import sections.utils.spa
import serializeraw
import utila

import sections_ref.biblio.strategy


def work(
    document: str,
    position: str,
    document_oneline: str,
    position_oneline: str,
    footer: str,
    publications: str,
    pages: tuple = None,
) -> str:
    nobib = skip_bibliography(
        footer,
        publications,
        pages=pages,
    )
    normal = sections.utils.spa.Data(
        document=document,
        position=position,
        pages=pages,
        skips=nobib,
    )
    oneline = sections.utils.spa.Data(
        document=document_oneline,
        position=position_oneline,
        pages=pages,
        skips=nobib,
    )
    hugest = sections_ref.biblio.strategy.extract(
        normal,
        oneline,
    )
    dumped = serializeraw.dump_likelihood(hugest)
    return dumped


def skip_bibliography(
    footer: str,
    publications: str,
    pages: tuple = None,
) -> set:
    """Determine pages where bib detection is not possbile."""
    footer = serializeraw.load_footnotes(
        footer,
        pages,
    )
    nobib = set(item.page for item in footer if len(item.content) >= 2)
    if utila.exists(publications):
        publications = serializeraw.load_likelihood(publications, pages=pages)
        for item in publications:
            if item.content.value < 1.0:
                continue
            utila.debug(f'pub can not be a bib, page: {item.page}')
            nobib.add(item.page)
    return nobib
