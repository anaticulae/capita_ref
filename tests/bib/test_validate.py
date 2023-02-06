# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import pytest
import serializeraw
import utila
import utilatest

import sections_ref
import tests

ARCHIVE = utila.join(sections_ref.ROOT, 'tests/bib/expected', exist=True)


@pytest.mark.parametrize(
    'source',
    utilatest.test_resources(tests.conftest.RESOURCES),
)
def test_bib(source, td, mp):
    BibliographyValidate(
        source=source,
        workdir=td.tmpdir,
        mp=mp,
    ).evaluate()


NO_BIB = [
    pytest.param(power.BOOK173_PDF, '119', id='book173p119'),
]


@pytest.mark.parametrize('source, pages', NO_BIB)
def test_no_bib(source, pages, td, mp):
    pages = extract_bibliography(source, pages, td, mp)
    assert not pages, str(pages)


def testfiles() -> list:
    result = []
    for source in tests.conftest.RESOURCES:
        pages = power.bib(source, default=None)
        if pages is None:
            utila.error(f'no pages: {source}, define in power for testing')
            continue
        testname = utila.file_name(source)
        pages: str = utila.parse_pages(pages)
        item = pytest.param(source, pages, id=testname)
        result.append(item)
    return result


@pytest.mark.parametrize('source, expected', testfiles())
def test_files(source, expected, td, mp):
    expected = list(expected)
    pages = extract_bibliography(source, ':', td, mp)
    assert pages == expected, f'{pages} != {expected}'


def extract_bibliography(source, pages, td, mp):
    source = power.link(source)
    utilatest.fixture_requires(source)
    cmd = f'-i {source} -i {td.tmpdir} --publication --bibliography --pages={pages} -VVV'
    tests.run(cmd, mp=mp)
    # verify result
    path = utila.join(td.tmpdir, 'sections_ref__bibliography_like.yaml')
    likelihood = serializeraw.load_likelihood(path)
    pages = [item.page for item in likelihood if item.content.value > 0.0]
    return pages


class BibliographyValidate(tests.Evaluate):

    def __init__(self, source, workdir, mp):
        super().__init__(
            step='bibliography',
            pages=':',
            source=source,
            mp=mp,
            workdir=workdir,
            archive=ARCHIVE,
        )

    def load_sections(self, _):  # pylint:disable=W0613
        path = utila.join(
            self.workdir,
            'sections_ref__bibliography_like.yaml',
        )
        loaded = serializeraw.load_likelihood(path)
        return loaded

    def raw(self, value) -> str:
        pages = []
        for line in value:
            raw = f'{line.page}'.zfill(3) + ' ' + str(line.content.value)
            pages.append(raw)
        result = utila.NEWLINE.join(pages)
        return result
