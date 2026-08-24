"""The report has to separate a CV that fits from one that does not.

A matcher that scores everything in the middle is useless however clever its
extraction is, so these tests check the ends: a CV written for the advert, a
CV from another trade, a CV that says almost nothing, and -- the case this
tool exists for -- a CV with the right content in a place the parser cannot
read.
"""

from datetime import date

import pytest

from ats_xray.match import evaluate_match
from ats_xray.vacancy import parse_vacancy

TODAY = date(2026, 8, 24)

ADVERT = """Elektroniker (m/w/d) Geraete und Systeme

Dich zeichnet aus:
- Abgeschlossene elektrotechnische Ausbildung oder mehrjaehrige Berufserfahrung
- Fundierte Kenntnisse in Elektronik und IT-Systemen
- Erfahrung in Wartung und Reparatur elektronischer Geraete
- Gute Kommunikationsfaehigkeiten und Serviceorientierung
- Reisebereitschaft, ca. 20 Wochen jaehrlich im Aussendienst
- Fuehrerschein Klasse B

In deinem neuen Job gibt es fuer dich:
- Attraktive Verguetungs- und Weiterbildungsmoeglichkeiten
- Hochwertiges Werkzeug und ein Dienstfahrzeug
"""

FITS = """Thomas Berger
thomas.berger@example.com | +49 171 2223344 | Fuehrerschein Klasse B

Ausbildung
Abgeschlossene Ausbildung als Elektroniker fuer Geraete und Systeme
Berufsschule Hamburg, 09/2015 - 07/2018

Berufserfahrung
Servicetechniker im Aussendienst, 08/2018 - 06/2026
Installation, Wartung und Reparatur elektronischer Geraete beim Kunden
Fehlersuche in IT-Systemen und Erstellung von Fehlerberichten

Kenntnisse
Elektronik, Elektroinstallation, Messtechnik, Reisebereitschaft
Kommunikationsfaehigkeit und Kundenorientierung

Sprachen
Deutsch - Muttersprache, Englisch - B2"""

WRONG_TRADE = """Marco Rossi
marco@example.com | +49 160 5556677

Ausbildung
Abgeschlossene Ausbildung als Koch
Berufsschule Muenchen, 09/2014 - 07/2017

Berufserfahrung
Chef de Partie im Restaurant, 08/2017 - 06/2026
Zubereitung von Speisen und Einhaltung der Lebensmittelhygiene

Kenntnisse
HACCP, Kalkulation, Warenwirtschaft, Teamfaehigkeit

Sprachen
Deutsch - B2, Italienisch - Muttersprache"""

SAYS_NOTHING = """Thomas Berger
thomas.berger@example.com

Erfahrung
Servicetechniker, 2018 - 2026
Verschiedene Aufgaben im technischen Bereich

Sonstiges
Teamfaehig und motiviert"""


@pytest.fixture(scope="module")
def requirements():
    return list(parse_vacancy(ADVERT).requirements)


def _report(requirements, cv, naive=None):
    return evaluate_match(requirements, cv, cv if naive is None else naive, today=TODAY)


def test_a_cv_written_for_the_advert_scores_well(requirements):
    report = _report(requirements, FITS)

    assert report.score >= 75
    assert report.missing_must == ()


def test_a_cv_from_another_trade_scores_badly(requirements):
    report = _report(requirements, WRONG_TRADE)

    assert report.score <= 25
    assert len(report.missing_must) >= 5


def test_a_cv_that_says_nothing_scores_badly(requirements):
    """Not the same failure as the wrong trade: this candidate may well be
    right for the job and simply has not written anything down. The report
    cannot tell, and says the same thing either way."""
    report = _report(requirements, SAYS_NOTHING)

    assert report.score <= 25
    assert len(report.missing_must) >= 5


def test_the_two_ends_are_far_apart(requirements):
    """Whatever the exact numbers, a fitting CV and an unfitting one must not
    land near each other, or the score tells the reader nothing."""
    good = _report(requirements, FITS).score
    bad = _report(requirements, WRONG_TRADE).score

    assert good - bad >= 50


def test_content_the_parser_cannot_see_is_flagged_without_changing_the_score(requirements):
    """The case this whole project is about. The CV is the same; only the
    layout-blind read differs. A human reader would score it identically, and
    the report says so -- while warning that the software filtering the pile
    may not agree."""
    hidden = FITS.split("Kenntnisse")[0]

    visible = _report(requirements, FITS)
    at_risk = _report(requirements, FITS, naive=hidden)

    assert at_risk.score == visible.score
    assert not visible.at_risk
    assert at_risk.at_risk, "a match only the layout-aware read can see was not flagged"


def test_a_wrong_trade_cv_still_reports_what_it_does_cover(requirements):
    """A bad score is not a reason to hide the parts that did match: the
    reader is deciding whether to apply, not being graded."""
    report = _report(requirements, WRONG_TRADE)

    assert report.of_status("met"), "nothing at all was reported as covered"
    assert report.extras, "skills the CV has but the advert did not ask for"
