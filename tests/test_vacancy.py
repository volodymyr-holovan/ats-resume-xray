import pytest

from ats_xray.skills_lexicon import find_skills
from ats_xray.vacancy import line_is_must, parse_vacancy, split_blocks

GERMAN_AD = """Junior Softwareentwickler (m/w/d)
Bremen, Vollzeit

Ihre Aufgaben
- Entwicklung von Anwendungen mit C# und .NET
- Anbindung von REST-APIs

Ihr Profil
- Abgeschlossenes Studium der Informatik oder vergleichbare Qualifikation
- Mindestens 2 Jahre Berufserfahrung
- Kenntnisse in SQL sind zwingend erforderlich
- Erfahrung mit Docker von Vorteil
- Verhandlungssichere Deutschkenntnisse
- Führerschein Klasse B erforderlich

Wir bieten
- Weiterbildung mit Kubernetes-Schulungen und Python-Kursen
- 30 Tage Urlaub
"""


def test_blocks_are_recognised_by_their_headings():
    blocks = split_blocks(GERMAN_AD)

    assert set(blocks) == {"intro", "tasks", "profile", "offer"}
    assert "Docker" in blocks["profile"]
    assert "Kubernetes" in blocks["offer"]


def test_text_without_headings_is_treated_as_requirements():
    """People paste the requirements list on its own. Treating an unlabelled
    block as anything but requirements would throw all of it away."""
    blocks = split_blocks("Kenntnisse in Python und SQL\nErfahrung mit Docker")

    assert set(blocks) == {"profile"}


def test_the_offer_block_is_never_scanned():
    """"Wir bieten" lists what the employer gives. Reading it as
    requirements is how keyword tools end up reporting a candidate is
    missing "Kubernetes-Schulungen" -- a training course the company
    offers, not a skill it asked for."""
    profile = parse_vacancy(GERMAN_AD)
    keys = {r.key for r in profile.requirements}

    assert "kubernetes" in find_skills(split_blocks(GERMAN_AD)["offer"])
    assert "kubernetes" not in keys
    assert "python" not in keys


def test_cue_phrases_separate_required_from_preferred():
    profile = parse_vacancy(GERMAN_AD)
    by_key = {r.key: r for r in profile.requirements}

    assert by_key["sql"].must, "zwingend erforderlich"
    assert not by_key["docker"].must, "von Vorteil"


def test_the_tasks_block_only_implies_requirements():
    """A skill named among the duties is not automatically demanded of the
    candidate, so it carries the lighter weight."""
    profile = parse_vacancy(GERMAN_AD)
    by_key = {r.key: r for r in profile.requirements}

    assert not by_key["rest"].must


def test_softer_cue_wins_when_a_line_carries_both():
    """Understating a requirement is the safer error: it still shows up in
    the report, just without raising an alarm."""
    assert not line_is_must("SQL erforderlich, Docker von Vorteil", default_must=True, language="de")
    assert line_is_must("SQL ist zwingend erforderlich", default_must=False, language="de")


def test_typed_requirements_are_extracted_alongside_skills():
    profile = parse_vacancy(GERMAN_AD)
    kinds = {r.kind for r in profile.requirements}

    assert {"skill", "education", "experience", "language", "licence"} <= kinds


def test_equivalent_qualification_makes_the_degree_optional():
    """The advert says the degree can be replaced, so it must not be
    reported as a blocking requirement."""
    profile = parse_vacancy(GERMAN_AD)
    education = next(r for r in profile.requirements if r.kind == "education")

    assert education.detail["equivalent_accepted"]
    assert not education.must


def test_english_headings_are_recognised_too():
    ad = """Your tasks
- Build services in Python

Requirements
- Strong SQL knowledge is required
- Experience with Docker is a plus

What we offer
- Training budget for Kubernetes
"""
    profile = parse_vacancy(ad)
    by_key = {r.key: r for r in profile.requirements}

    assert by_key["sql"].must
    assert not by_key["docker"].must
    assert "kubernetes" not in by_key


def test_requirements_carry_the_line_they_came_from():
    """Evidence is the point: a reader has to be able to check the tool
    against the advert without hunting for the sentence."""
    profile = parse_vacancy(GERMAN_AD)
    sql = next(r for r in profile.requirements if r.key == "sql")

    assert "zwingend erforderlich" in sql.evidence


PROFESSION_ADS = {
    "cleaner": """Ihr Profil
- Erfahrung in der Unterhaltsreinigung von Vorteil
- Sorgfalt und Zuverlaessigkeit im Umgang mit Reinigungsmaschinen
- Fuehrerschein Klasse B ist wuenschenswert""",
    "nurse": """Ihr Profil
- Abgeschlossene Ausbildung als Pflegefachkraft
- Mindestens zwei Jahre Berufserfahrung in der Altenpflege
- Kenntnisse in der Pflegedokumentation sind zwingend erforderlich
- Bereitschaft zum Schichtdienst wird vorausgesetzt""",
    "chef": """Ihr Profil
- Abgeschlossene Ausbildung als Koch und Freude an der Zubereitung
- Erfahrung in der gehobenen Gastronomie ist von Vorteil
- Kenntnisse in Kalkulation und in den HACCP-Vorgaben""",
    "driver": """Ihr Profil
- Fuehrerschein Klasse CE ist zwingend erforderlich
- Gueltige Fahrerkarte und die Module nach dem BKrFQG
- Erfahrung mit Ladungssicherung und mit Gefahrgut nach ADR""",
    "accountant": """Ihr Profil
- Abgeschlossene kaufmaennische Ausbildung oder ein Studium der Betriebswirtschaft
- Mehrjaehrige Erfahrung in der Finanzbuchhaltung
- Sicherer Umgang mit DATEV und mit Excel
- Kenntnisse im Steuerrecht und in der Bilanzierung""",
    "seamstress": """Ihr Profil
- Abgeschlossene Ausbildung als Massschneiderin oder eine vergleichbare Qualifikation
- Sicherer Umgang mit der Naehmaschine und mit der Overlock
- Erfahrung im Zuschnitt und mit Schnittmustern""",
    "doctor": """Ihr Profil
- Die deutsche Approbation ist zwingend erforderlich
- Facharztanerkennung fuer Innere Medizin
- Erfahrung in der Notaufnahme und in der Sonographie""",
    "architect": """Ihr Profil
- Ein abgeschlossenes Studium der Architektur
- Sicherer Umgang mit Revit und mit AutoCAD
- Kenntnisse der HOAI und der Leistungsphasen
- Erfahrung in der Bauleitung ist wuenschenswert""",
    "pastor": """Ihr Profil
- Ein abgeschlossenes Studium der Theologie
- Erfahrung in der Seelsorge und in der Gemeindearbeit
- Ein erweitertes Fuehrungszeugnis wird vorausgesetzt""",
    "salesmanager": """Ihr Profil
- Mehrjaehrige Erfahrung im Vertrieb und in der Neukundengewinnung
- Erfahrung im Key Account Management ist zwingend erforderlich
- Sicherer Umgang mit einem CRM und mit der Angebotserstellung""",
    "banker": """Ihr Profil
- Eine Ausbildung als Bankkaufmann oder eine vergleichbare Qualifikation
- Erfahrung in der Anlageberatung und im Kreditgeschaeft
- Kenntnisse in der Geldwaescherpraevention""",
    "designer": """Ihr Profil
- Ein Studium im Bereich Mediengestaltung oder eine vergleichbare Ausbildung
- Sicherer Umgang mit InDesign und mit Photoshop
- Erfahrung in der Typografie und im Corporate Design""",
    "electrician": """Ihr Profil
- Eine abgeschlossene Ausbildung als Elektroniker
- Erfahrung in der Elektroinstallation und im Schaltschrankbau
- Kenntnisse in der Steuerungstechnik sind von Vorteil
- Sorgfalt im Umgang mit den Sicherheitsvorschriften""",
    "teacher": """Ihr Profil
- Ein abgeschlossenes Studium und eine Freude an der Vermittlung
- Erfahrung im Unterricht und in der Didaktik
- Kenntnisse des Bildungsplans werden vorausgesetzt""",
    "security": """Ihr Profil
- Die Sachkundepruefung nach Paragraf 34a ist zwingend erforderlich
- Erfahrung im Objektschutz und in der Zutrittskontrolle
- Bereitschaft zum Schichtdienst und ein einwandfreies Fuehrungszeugnis""",
    "astronaut": """Requirements
- A master's degree in the natural sciences or in engineering is required
- At least three years of professional experience in a technical role
- Experience with survival training and with high altitude flight
- Excellent physical fitness and fluent Russian""",
}


@pytest.mark.parametrize("profession", sorted(PROFESSION_ADS))
def test_every_profession_yields_usable_requirements(profession):
    """The tool is not an IT tool. A cleaner, a nurse, a seamstress and an
    astronaut each have to come out of this with a list worth editing, or
    the feature only works for the trade its author happened to be in."""
    profile = parse_vacancy(PROFESSION_ADS[profession])
    skills = [r for r in profile.requirements if r.kind == "skill"]

    assert len(skills) >= 3, f"{profession}: only {[r.label for r in skills]}"
    assert any(r.must for r in profile.requirements), f"{profession}: nothing required"


@pytest.mark.parametrize("profession", sorted(PROFESSION_ADS))
def test_no_profession_produces_a_flood_of_noise(profession):
    """A list nobody will read through is a list nobody will correct."""
    profile = parse_vacancy(PROFESSION_ADS[profession])

    assert len(profile.requirements) <= 25


def test_typed_requirements_are_found_outside_it_too():
    by_kind = {}
    for profession in ("nurse", "driver", "doctor"):
        for requirement in parse_vacancy(PROFESSION_ADS[profession]).requirements:
            by_kind.setdefault(requirement.kind, set()).add(profession)

    assert "education" in by_kind
    assert "experience" in by_kind
    assert "licence" in by_kind


def test_a_lower_cased_advert_reads_the_same_as_a_normal_one():
    """Adverts are pasted from all sorts of places, and case is not a
    requirement of the format."""
    normal = parse_vacancy(PROFESSION_ADS["accountant"])
    lowered = parse_vacancy(PROFESSION_ADS["accountant"].lower())

    known = lambda profile: {r.key for r in profile.requirements if not r.key.startswith("term:")}
    assert known(normal) == known(lowered)


# --------------------------------------------------------------------------
# Regressions from real adverts. Every one of these was found by running the
# parser over live postings rather than over text written for the tests.
# --------------------------------------------------------------------------

HOSPITAL_KITCHEN_AD = """Koch (m/w/d)
Krankenhaus Neuwittelsbach, München

Wir sind die Kongregation der Barmherzigen Schwestern. Das Krankenhaus
Neuwittelsbach im Muenchner Stadtteil Nymphenburg ist eine Fachklinik fuer
Innere Medizin. Mit 132 Betten ist die Klinik ein kleines, familiaeres Haus,
sie verfuegt aber ueber ein hauseigenes Labor und eine Roentgenabteilung.

Was Sie bei uns erwartet - wir freuen uns auf Sie:
- Eine attraktive Verguetung nach AVR Caritas
- 31 Tage Urlaub und eine betriebliche Altersvorsorge
- Kostenlose Getraenke am Arbeitsplatz

Ihre Aufgaben:
- Zubereitung von Diaet- und Normalkost
- Mitarbeit bei der Umsetzung aller geforderten HACCP-Vorgaben

Voraussetzungen - darum sind Sie unsere erste Wahl:
- Eine abgeschlossene Ausbildung als Koch/Koechin mit mehrjaehriger Berufserfahrung
- Eine selbststaendige Arbeitsweise
"""

INFORMAL_AD = """Elektroniker (m/w/d) Geraete und Systeme

Dich zeichnet aus:
- Abgeschlossene elektrotechnische Ausbildung oder mehrjaehrige Berufserfahrung
- Fundierte Kenntnisse in Elektronik und IT-Systemen
- Reisebereitschaft, ca. 20 Wochen jaehrlich im Aussendienst
- Fuehrerschein Klasse B

In deinem neuen Job gibt es fuer dich:
- Attraktive Verguetungs- und Weiterbildungsmoeglichkeiten
- Hochwertiges Werkzeug und ein Dienstfahrzeug

Deine Aufgaben als Elektroniker (m/w/d):
- Installation, Wartung und Reparatur elektronischer Geraete
- Fehlersuche und -behebung in IT-gestuetzten Systemen
"""


def test_the_company_blurb_is_not_mined_for_requirements():
    """A real hospital advert opens with three sentences about the order that
    founded it. Reading those produced "Nymphenburg", "Religion" and "Betten"
    as things the candidate should have."""
    labels = {r.label.lower() for r in parse_vacancy(HOSPITAL_KITCHEN_AD).requirements}

    for boilerplate in ("nymphenburg", "betten", "klinik", "kongregation", "labor"):
        assert boilerplate not in labels, boilerplate


def test_an_unlabelled_intro_is_still_read_when_no_profile_block_exists():
    """Skipping the intro is only safe when the requirements were found
    somewhere else. Otherwise it throws away the only place they can be."""
    bare = "Wir suchen eine Reinigungskraft.\nErfahrung in der Unterhaltsreinigung und Sorgfalt."

    assert parse_vacancy(bare).requirements


def test_headings_that_address_the_reader_informally_are_recognised():
    """"Dich zeichnet aus" is as common as "Ihr Profil" and was not in the
    list, so a real advert came back with no requirements at all."""
    profile = parse_vacancy(INFORMAL_AD)
    must = {r.label for r in profile.requirements if r.must}

    assert "profile" in profile.blocks
    assert must, "the requirements block was not recognised"
    assert "Reisebereitschaft" in must


def test_the_offer_block_is_recognised_however_it_is_worded():
    """Two real phrasings that are neither "Wir bieten" nor a synonym of it:
    "Was Sie bei uns erwartet" and "In deinem neuen Job gibt es fuer dich"."""
    for advert, benefit in (
        (HOSPITAL_KITCHEN_AD, "urlaub"),
        (INFORMAL_AD, "werkzeug"),
    ):
        labels = {r.label.lower() for r in parse_vacancy(advert).requirements}
        assert not any(benefit in label for label in labels), benefit


def test_a_real_advert_keeps_its_typed_requirements():
    profile = parse_vacancy(HOSPITAL_KITCHEN_AD)
    by_kind = {r.kind: r for r in profile.requirements}

    assert by_kind["education"].key == "ausbildung"
    assert by_kind["experience"].detail["years"] == 3
