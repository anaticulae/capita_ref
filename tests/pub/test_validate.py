# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import hoverpower
import pytest
import serializeraw
import utilo
import utilotest

import capita_ref
import tests

PUBLICATION = utilo.join(capita_ref.ROOT, 'tests/pub/expected', exist=True)

PUBLICATIONS = [
    hoverpower.BACHELOR029A_PDF,
    hoverpower.DISS173_PDF,
    # hoverpower.HC_DISS128,
]


@pytest.mark.parametrize('source', utilotest.test_resources(PUBLICATIONS))
def test_pub(source, td, mp):
    PublicationValidate(
        source=source,
        workdir=td.tmpdir,
        mp=mp,
    ).evaluate()


class PublicationValidate(tests.Evaluate):

    def __init__(self, source, workdir, mp):
        super().__init__(
            step='publication',
            pages=':',
            source=source,
            mp=mp,
            workdir=workdir,
            archive=PUBLICATION,
        )

    def load_sections(self, _):  # pylint:disable=W0613
        path = utilo.join(
            self.workdir,
            f'{capita_ref.PROCESS}__publication_like.yaml',
        )
        loaded = serializeraw.load_likelihood(path)
        return loaded

    def raw(self, value) -> str:
        pages = []
        for line in value:
            if not line.content.value:
                # do not write zeros
                continue
            raw = f'{line.page}'.zfill(3) + ' ' + str(line.content.value)
            pages.append(raw)
        result = utilo.NEWLINE.join(pages)
        return result
