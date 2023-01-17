# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Special Chars
=============

Determine potential bib pages dues analysing the structure of used
characters on a page. Bib pages contain a lot of brackets, dots,
semicolons. etc.

A document contains only one bib page(s) block. Therefore we look for
the highest rated valued block of bib pages and return only this single
one. Without selecting the biggest cluster, more than one bib can be
detected.
"""

import statistics

import configo
import elements.headline.lookup
import german
import german.pattern.author
import sections.feature
import sections.utils.headline
import sections.utils.spa
import texmex
import utila

import sections_ref.biblio
import sections_ref.biblio.utils

LIKELIHOOD_MIN = configo.HV_PERCENT_PLUS(default=30.0)


def extract(data: sections.utils.spa.Data) -> list:
    config = sections.utils.spa.Config(
        likelihood_name='bibliography_table',
        page_analysis=analyse_page,
    )
    extracted = sections.utils.spa.work(data=data, config=config)
    # ignore to low valued bib pages
    valid = [item for item in extracted if item.content.value > LIKELIHOOD_MIN]
    hugest = sections_ref.biblio.utils.cluster_bibpages(valid)
    return hugest


SPECIAL_CHAR_BONUS = configo.HV_PERCENT_PLUS(default=30)


def analyse_page(ptn: texmex.PTN) -> sections.feature.StatisticalResultItem:
    raw = ptn.debug
    marker = special_pattern(raw, page=ptn.page)
    if special_chars(raw):
        # thirty percent bonus
        marker *= (1 + SPECIAL_CHAR_BONUS)
    if content_page(raw):
        if marker:
            utila.debug(f'contentpage p{ptn.page}/marker{marker}=0')
        marker = 0
    likelihood = 0.0
    if marker and len(ptn) >= 1:
        likelihood = marker / len(ptn)
    if likelihood < LIKELIHOOD_MIN:
        # TODO: CHECK THIS
        # this can not be a bib table
        marker = 0
    if marker >= 5:  # TODO: HOLY VALUE
        # Bibliography headline on page
        headline = bib_headline(ptn)
        if headline:
            return len(ptn), len(ptn)
    return len(ptn), marker


def bib_headline(ptn: texmex.PTN) -> bool:
    """Determine if a BIB-HEADLINE is on current navigator."""
    headlines = sections.utils.headline.headlines(ptn)
    if not headlines:
        return False
    similar = utila.similar(
        expected=elements.headline.lookup.BIBLIOGRAPHY,
        current=headlines,
        maxdiff=0.95,
    )
    if not similar:
        return False
    return True


VOLUME = utila.compiles(r"""
(
    (AUFLAGE|VOL\.)
    [ ]{0,2}
    (\d{1,2})
    |
    (\d)\.
    [ ]{0,2}
    (AUFLAGE)
)
""")


def volume(text, verbose: bool = True):
    """\
    >>> volume('(The Formation of the Classical Islamic World). Vol. 36, S. 225-234.')
    [(36, 'Vol. 36')]
    >>> volume('Schriftsprache der Gegenwart. 5. Auflage.')
    [(5, '5. Auflage')]
    """
    # TODO: MOVE TO GERMAN
    result = []
    for item in VOLUME.finditer(text):
        group = item.groups()
        value = group[3] if group[3] and group[3].isnumeric() else group[2]
        if verbose:
            result.append((int(value), item[0]))
        else:
            result.append(int(value))
    return result


BIBS = utila.compiles(r"""
(
    Hrsg\.|
    Aufl\.|
    Verlag
)
""")


def bibtext(text, verbose: bool = True):
    """\
    >>> bibtext(' Adler und Jung. 2. Aufl. Zürich 1996.')
    [('Aufl.', 'Aufl.')]
    """
    result = []
    for item in BIBS.finditer(text):
        if verbose:
            result.append((item[0], item[0]))
        else:
            result.append(item[0])
    return result


YEARS = utila.compiles(r'\b(((19|20)\d{2})[a-z]?)\b')


def years(raw: str, min_=1950, max_=2025, verbose: bool = False):
    """Extract sorted list of years out of `raw` text.

    >>> years('1999, Helm was born in 1987. Mud exists since 1800. 2050 20000 2020')
    [1987, 1999, 2020]
    >>> years('Helm was born in 1987a.', verbose=True)
    [(1987, '1987a')]
    """
    result = []
    for item in YEARS.finditer(raw):
        year = int(item.groups()[1])
        if min_ <= year <= max_:
            parsed = year
            if verbose:
                parsed = (year, item.groups()[0])
            result.append(parsed)
    result = sorted(result, key=lambda x: x[0] if verbose else x)
    return result


AUTHORS = utila.compiles(r"""
    (
        [a-z]{4,18}[ ]{1,4}[a-z]\.|
        [a-z]\.[ ]{1,4}[a-z]{4,18}
        # [a-z]{4,18}\,[ ]{1,2}[a-z]{4,18}
    )
""")


def authors(text, verbose: bool = True):
    """\
    >>> authors('HUG T. und POSCHESCHNIK G. ( **************** ): Empirisch Forschen.')
    [('POSCHESCHNIK G.', 'POSCHESCHNIK G.')]
    """
    # TODO: REPLACE WITH GERMAN CODE
    result = []
    for item in AUTHORS.finditer(text):
        valid = german.pattern.author.simple(item[0])
        if not valid:
            continue
        if verbose:
            result.append((item[0], item[0]))
        else:
            result.append(item[0])
    return result


PATTERN = (
    german.hyperlink,
    german.authors,
    volume,
    bibtext,
    german.dates,
    german.pagenumbers,
    years,
    authors,
)


def special_pattern(raw: str, page: int) -> int:
    """Search for bib page typical pattern like: authors, dates, years...

    If too few pages occurs, disable pattern approach, because its may
    not a bib may a toc or table table.
    """
    if nobib(raw, page=page):
        return 0
    collected = collect_and_replace(raw, PATTERN)
    # this patterns typically occurs mostly once's.
    allmarker = len(collected)
    collected: set = set(collected)
    marker = len(collected)
    lines = len(raw.splitlines())
    marker_min = MARKER_COUNT_MIN(lines)
    if marker < marker_min:
        utila.debug(f'too few marker p{page}/{lines}l: {marker}/{marker_min} '
                    f'{allmarker}')
        return 0
    pages = collect_and_replace(raw, (german.pagenumbers,))
    pagerate = len(pages) / allmarker
    if pagerate > 0.8:
        msg = f'too many pages {page}: {pagerate} {len(pages)} {allmarker}'
        utila.debug(msg)
        return 0
    return allmarker


MARKER_COUNT_MIN = configo.HolyTable(items=(
    (0, 5),
    (5, 5),
    (10, 8),
    (15, 12),
    #(30, 25),
))


def collect_and_replace(raw: str, pattern: list) -> list:
    """Collect due list of pattern and avoids parsing items twice."""
    collected = []
    for method in pattern:
        parsed = method(raw, verbose=True)
        for _, itemraw in parsed:
            # do not parse pattern twice
            raw = raw.replace(itemraw, ' **************** ')
            collected.append(itemraw)
    return collected


SPECIAL_CHARS = ";,/:[]()&"

SPECIAL_CHARS_CLASSIFIER_MIN = configo.HV_PERCENT_PLUS(default=30.0)

SPECIAL_CHARS_WORDCOUNT_MIN = configo.HV_INT_PLUS(default=40)


def special_chars(raw: str) -> bool:
    # TODO: A LOT OF MISMATCHES AS A RESULT OF PROGRAM CODE IN DOCUMENT
    result = []
    for line in raw.splitlines():
        parsed = german.word_tokenize(line, validate_sentences=False)
        result.extend(parsed)
    word_count = len(result)
    if word_count < SPECIAL_CHARS_WORDCOUNT_MIN:
        return False
    counted = sum((raw.count(char) for char in SPECIAL_CHARS))
    classifier = counted / word_count if word_count else 0
    if classifier < SPECIAL_CHARS_CLASSIFIER_MIN:
        return False
    return True


SENTENCE_MEAN_TRUST_MIN = configo.HV_INT_PLUS(default=100)

SENTENCE_SIGN_COUNT_MAX = configo.HV_INT_PLUS(default=20)


def content_page(raw: str) -> bool:
    """Verify that page contains a `normal` number of sentences."""
    sentences = german.sentence_tokenize(raw, normalize_spaces=True)
    if not sentences:
        return False
    # german does not split sentences at `:` but bib tables uses : often
    # for separating parts. If we do not split by double collon we archive
    # a lot of false postive results.
    sentences = utila.flat([split_doublecolon(item) for item in sentences])
    length_mean = statistics.mean([len(sentence) for sentence in sentences])
    signs = [
        item.count(',') + item.count(';') + item.count('.') + item.count('-')
        for item in sentences
    ]
    signs_max = max(signs)
    if signs_max > SENTENCE_SIGN_COUNT_MAX:
        return False
    if length_mean > SENTENCE_MEAN_TRUST_MIN:
        return True
    return False


DOUBLE_COLON = utila.compiles(r"""
    (?!https?)
    \:
    (?!//)
""")


def split_doublecolon(text: str) -> list:
    """\
    >>> split_doublecolon('Ich glaube:"Heute is ein guter Tag"')
    ['Ich glaube', '"Heute is ein guter Tag"']
    >>> split_doublecolon('http://donotsplit.com https://donotsplit.com')
    ['http://donotsplit.com https://donotsplit.com']
    >>> split_doublecolon('Literaturverzeichnis:')
    ['Literaturverzeichnis']
    """
    text = text.strip(': ')
    return DOUBLE_COLON.split(text)


NOBIB_COUNT_MIN = configo.HV_INT_PLUS(default=35)

NOBIB = utila.compiles(r"""
    \s
    (
        [a-h]{1,2}[ ]{0,2}[\.\)][ ]{0,3}\w|
        \d{1,2}[ ]{0,2}\.[ ]{0,3}\w|
        S\.[ ]{0,3}\d{1,3}
    )
""")


def nobib(
    raw: str,
    nobib_count_min: int = NOBIB_COUNT_MIN,
    page: int = None,
) -> bool:
    """\
    >>> nobib(' a) Fall 1: Kosovo             S. 184', nobib_count_min=2)
    True

    A. Einführung                                                       S. 178
    B. Selbstbestimmungsrecht und Demokratie                            S. 180
        I. Das Selbstbestimmungsrecht                                   S. 180
            1. Das Selbstbestimmungsrecht im Völkerrecht                S. 180
            2. Selbstbestimmungsrecht und Staatenzerfall                S. 182
            3. Die Beziehung zwischen dem Selbstbestimmungsrecht und    S. 183
                a) Fall 1: Kosovo                                       S. 184
    """
    tocs = list(NOBIB.finditer(raw))
    if len(tocs) >= nobib_count_min:
        utila.debug(f'too many toc pattern inside bib: {len(tocs)}; p{page}')
        return True
    return False
