"""What the advert reader is allowed to come back with.

The other tests here check one rule at a time on one line. This one checks
the answer: twelve whole adverts across the seven languages, each with the
requirements a reader would expect to see and the words that used to arrive
beside them and are not requirements at all.

Both halves matter and the second half is the one that rots. Precision has
no natural floor -- every stoplist entry, every widened pattern, every new
introducer buys recall somewhere and pays for it in noise somewhere else,
and the payment is invisible unless something counts it. The rejected lists
below are the actual output of the extractor before it was rewritten, so a
change that brings any of them back has undone a specific thing rather than
drifted.
"""

from pathlib import Path

import pytest

from ats_xray.normalize import fold
from ats_xray.vacancy import parse_vacancy

ADVERTS = Path(__file__).parent / "extraction" / "adverts"
CORPUS = Path(__file__).parent / "corpus" / "vacancies"

MAX_GUESSES_OVERALL = 35
"""Across all twelve adverts. It was 104.

A ceiling on the total rather than per advert: one advert going quiet while
another floods is the same failure, and the sum is what a reader would feel
if they pasted several."""


def _requirements(path: Path):
    return parse_vacancy(path.read_text(encoding="utf-8")).requirements


def _labels(requirements) -> set[str]:
    return {fold(r.label) for r in requirements}


def _guesses(requirements) -> list[str]:
    return [r.label for r in requirements if r.key.startswith("term:")]


# Each case is (file, must_find, must_not_find). ``must_find`` is checked
# against every requirement, typed or guessed, because the reader does not
# care which route it came by. ``must_not_find`` is matched on the whole
# label: "Grund" is noise and "Grundpflege" is not.
#
# The subject of a degree rides on the degree -- "Bachelor / Studium
# (computer science)" -- rather than standing beside it as a keyword of
# its own, so the expected label here is the whole thing, folded.
CASES = [
    (
        ADVERTS / "de_erzieher.txt",
        ("sprachfoerderung", "paedagogik"),
        ("eltern", "planung", "begleitung", "gruppenalltag", "angeboten",
         "konzept", "portfolio", "ansatz", "bildungsverlaeufe", "foerderung",
         "entwicklungsgespraechen"),
    ),
    (
        ADVERTS / "en_devops.txt",
        ("docker", "kubernetes", "linux", "terraform",
         "bachelor studium computer science"),
        ("take", "operate", "automate", "in production", "work", "rotation"),
    ),
    (
        ADVERTS / "es_camarero.txt",
        ("barista", "haccp", "service", "kassiertaetigkeit"),
        ("apoyo", "atencion", "montaje", "toma", "al menos 2", "menos"),
    ),
    (
        ADVERTS / "fr_comptable.txt",
        ("excel", "buchhaltung", "fiscalite des pme"),
        ("etablissement", "preparation", "relation", "saisie", "3 ans minimum",
         "d'excel", "d excel"),
    ),
    (
        ADVERTS / "nl_monteur.txt",
        ("hydraulik", "elektroinstallation", "schweissen", "wartung"),
        ("onderhoud", "rapporteren", "storingen", "vervangen", "lassen is een"),
    ),
    (
        ADVERTS / "ru_povar.txt",
        ("kueche", "haccp", "санитарных норм"),
        ("контроль", "поддержание", "приготовление", "приём", "прием",
         "медицинская", "санитарных норм и"),
    ),
    (
        ADVERTS / "uk_frontend.txt",
        ("react", "typescript", "rest"),
        ("взаємодія", "підтримка", "розробка", "участь", "від трьох", "трьох"),
    ),
    (
        CORPUS / "lagerlogistik.txt",
        ("staplerschein", "kommissionierung", "lagerverwaltungssystem"),
        ("buchung", "entladen", "sendungen", "warenbewegungen", "auslagerung",
         "zusammenstellung", "containern"),
    ),
    (
        CORPUS / "mediengestalter.txt",
        ("figma", "kommunikationsdesign"),
        ("katalogen", "motiven", "freisteller", "anzeigen", "druckerei",
         "uebergabe"),
    ),
    (
        CORPUS / "pflegefachkraft.txt",
        ("behandlungspflege", "wundmanagement", "altenpfleger"),
        ("fachgerechte", "grund", "anordnung", "zusammenarbeit", "angehoerigen",
         "aerzten", "therapeuten", "stationaeren"),
    ),
    (
        CORPUS / "python_engineer.txt",
        ("python", "django", "kubernetes", "softwareentwicklung",
         "bachelor studium informatik"),
        ("entwicklung", "betrieb", "code", "reviews", "konzeption", "releases",
         "services", "weiterentwicklung"),
    ),
    (
        CORPUS / "verkauf.txt",
        ("kundenberatung", "inventur"),
        ("flaeche", "kassiertaetigkeit am", "mitwirkung"),
    ),
]

IDS = [path.stem for path, _, _ in CASES]


@pytest.mark.parametrize(("path", "must_find", "must_not_find"), CASES, ids=IDS)
def test_the_advert_yields_what_it_asks_for(path, must_find, must_not_find):
    labels = _labels(_requirements(path))

    missing = [term for term in must_find if term not in labels]

    assert not missing, f"{path.name}: not found {missing}"


@pytest.mark.parametrize(("path", "must_find", "must_not_find"), CASES, ids=IDS)
def test_the_advert_yields_nothing_that_is_not_a_requirement(path, must_find, must_not_find):
    labels = _labels(_requirements(path))

    leaked = [term for term in must_not_find if term in labels]

    assert not leaked, f"{path.name}: not a requirement {leaked}"


def test_the_whole_set_stays_readable():
    """Twelve adverts, and the guesses across all of them have to stay
    something a person would work through."""
    total = sum(len(_guesses(_requirements(path))) for path, _, _ in CASES)

    assert total <= MAX_GUESSES_OVERALL, f"{total} guesses across {len(CASES)} adverts"


@pytest.mark.parametrize(("path", "must_find", "must_not_find"), CASES, ids=IDS)
def test_no_advert_comes_back_empty(path, must_find, must_not_find):
    """The failure the guessing exists to prevent. An advert for a trade the
    gazetteer never heard of must still produce a list to correct."""
    assert _requirements(path), f"{path.name} produced no requirements"
