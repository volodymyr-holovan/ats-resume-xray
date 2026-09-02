"""Reading the dates people actually write on a CV.

The reader used to understand only "03/2019 - 08/2022" and "2019 - 2022".
Everything written in words -- which is the ordinary form in English and
German alike -- was invisible, and silently so: the year inside the phrase
still matched on its own, so "März 2019 bis August 2022" was read as
January 2019 to August 2022 and quietly added two months of experience that
nobody had. A CV with fourteen years of history could report nothing at
all, and that number is what an advert asking for five years is measured
against.
"""

from datetime import date

import pytest

from ats_xray.credentials import MONTH_NAMES, find_experience_months

TODAY = date(2026, 9, 1)

SPELLED_RANGES = [
    ("March 2019 - August 2022", 42),
    ("March 2019 to August 2022", 42),
    ("Jan. 2019 – Dez. 2021", 36),
    ("Sept 2020 - present", 73),
    ("März 2019 bis August 2022", 42),
    ("Oktober 2015 — Dezember 2018", 39),
    ("січня 2019 — грудня 2021", 36),
    ("Березень 2019 - Грудень 2021", 34),
    ("января 2019 — декабря 2021", 36),
    ("enero 2019 - agosto 2022", 44),
    ("janvier 2019 au août 2022", 44),
    ("février 2020 à décembre 2022", 35),
    ("maart 2019 tot augustus 2022", 42),
]


@pytest.mark.parametrize("text,months", SPELLED_RANGES)
def test_a_range_written_in_words_is_read(text, months):
    assert find_experience_months(text, today=TODAY) == months


NUMERIC_RANGES = [
    ("03/2019 - 08/2022", 42),
    ("03.2019 - 08.2022", 42),
    ("2019 - 2022", 48),
    ("seit 03/2023", 43),
    ("seit März 2023", 43),
    ("since March 2023", 43),
]


@pytest.mark.parametrize("text,months", NUMERIC_RANGES)
def test_the_numeric_forms_still_work(text, months):
    """The month names went in around the existing patterns, not instead of
    them."""
    assert find_experience_months(text, today=TODAY) == months


def test_a_spelled_month_is_not_read_as_a_bare_year():
    """The failure that hid this: when the month name did not match, the
    year inside it still did, so a range starting in September was read as
    starting in January. Wrong in the direction that flatters the CV."""
    spelled = find_experience_months("September 2021 - Dezember 2021", today=TODAY)
    numeric = find_experience_months("09/2021 - 12/2021", today=TODAY)

    assert spelled == numeric == 4


def test_overlapping_entries_are_still_merged():
    """Two jobs held at once are not twice the experience."""
    both = find_experience_months(
        "March 2019 - August 2022\nJanuary 2020 - June 2021", today=TODAY
    )

    assert both == 42


def test_no_spelling_maps_to_two_different_months():
    """The abbreviations are generated, so a collision would be silent --
    two languages whose month names share a prefix but not a number."""
    assert MONTH_NAMES["jan"] == 1
    assert MONTH_NAMES["dez"] == MONTH_NAMES["dec"] == 12
    assert all(1 <= number <= 12 for number in MONTH_NAMES.values())


def test_a_year_alone_is_not_mistaken_for_a_month():
    """"2019" beside "2022" is a range of years, not a month name."""
    assert find_experience_months("2019 - 2022", today=TODAY) == 48


def test_nonsense_dates_are_ignored_rather_than_guessed():
    for text in ("March 1200 - August 1300", "13/2019 - 14/2022", "August - March"):
        assert find_experience_months(text, today=TODAY) == 0
