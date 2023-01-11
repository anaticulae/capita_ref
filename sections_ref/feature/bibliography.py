# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import sections.utils.spa
import serializeraw

import sections_ref.biblio.strategy


def work(document: str, position: str, footer: str, pages: tuple = None) -> str:
    nobib = skip_bibliography(
        footer,
        pages=pages,
    )
    data = sections.utils.spa.Data(
        document=document,
        position=position,
        pages=pages,
        skips=nobib,
    )
    hugest = sections_ref.biblio.strategy.extract(data)
    dumped = serializeraw.dump_likelihood(hugest)
    return dumped


def skip_bibliography(
    footer: str,
    pages: tuple = None,
) -> set:
    """Determine pages where bib detection is not possbile."""
    footer = serializeraw.load_footnotes(
        footer,
        pages,
    )
    nobib = set(item.page for item in footer if len(item.content) >= 2)
    return nobib
