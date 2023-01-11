# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import functools

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
def test_validate_bibliography(source, td, mp):
    BibliographyValidate(
        source=source,
        workdir=td.tmpdir,
        mp=mp,
    ).evaluate()


@pytest.mark.parametrize('source, expected', [
    pytest.param(power.BACHELOR029A_PDF, [28], id='bachelor029a'),
])
def test_valdiate(source, expected, td, mp):
    pages = extract_bibliography(source, ':', td, mp)
    assert pages == expected


def extract_bibliography(source, pages, td, mp):
    source = power.link(source)
    utilatest.fixture_requires(source)
    tests.run(
        f'-i {source} --bibliography --pages={pages} -VVV',
        mp=mp,
    )
    # verify result
    path = utila.join(td.tmpdir, 'sections_ref__bibliography_like.yaml')
    likelihood = serializeraw.load_likelihood(path)
    pages = [item.page for item in likelihood if item.content.value > 0.0]
    return pages


class Evaluate(utilatest.BaseLiner):

    def __init__(self, step, source, pages, workdir, mp):
        super().__init__(
            # step=f'pdf {source}',
            step=step,
            program=functools.partial(
                tests.run,
                mp=mp,
            ),
            pages=pages,
            source=power.link(source),
            workdir=workdir,
            archive=ARCHIVE,
            loader=self.load_sections,
            convert_source=False,
        )

    def load_sections(self, _):  # pylint:disable=W0613
        loaded = serializeraw.load_sections(self.workdir)
        return loaded

    def raw(self, value) -> str:
        result = []
        for section in value:
            line = rawline(section)
            result.append(line)
            for item in section:
                line = rawline(item)
                result.append('    ' + line)
        raw = utila.NEWLINE.join(result)
        return raw


def rawline(item) -> str:
    start = str(item.start).zfill(3)
    end = str(item.end).zfill(3)
    line = f'{start} {end} {item.__class__.__name__}'
    return line


class BibliographyValidate(Evaluate):

    def __init__(self, source, workdir, mp):
        super().__init__(
            step='bibliography',
            pages=':',
            source=source,
            mp=mp,
            workdir=workdir,
        )
        self.archive = ARCHIVE

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
