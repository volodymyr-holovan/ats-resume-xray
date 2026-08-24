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
    assert not line_is_must("SQL erforderlich, Docker von Vorteil", default_must=True)
    assert line_is_must("SQL ist zwingend erforderlich", default_must=False)


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
