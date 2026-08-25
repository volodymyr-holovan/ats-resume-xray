"""What the scorer accepts as a CV, decided from real document text.

The rest of the score tests build field reports by hand, which is fast and
readable and cannot see this class of bug at all: a job advert scored
100/100 in all seven languages while every one of them passed. An advert
lists "Qualifications" and "Skills" because it is asking for them, and
prints an email because it wants replies, so on the field report it looks
exactly like a CV.

These go through ``build_field_report`` from text, the way the app does.
"""

import pytest

from ats_xray.field_report import build_field_report
from ats_xray.score import score_resume

ADVERTS = {
    "en": """Warehouse Operative (full time)

Qualifications
No formal qualifications needed

Skills
Reliable, physically fit, able to work shifts

Apply: jobs@example.com or call +44 20 7946 0000""",
    "de": """Lagermitarbeiter (m/w/d)

Ausbildung
Keine formale Ausbildung erforderlich

Kenntnisse
Zuverlässig, körperlich belastbar, Schichtbereitschaft

Bewerbung an: jobs@example.com oder 040 123456""",
    "es": """Mozo de almacén

Formación
No se requiere formación reglada

Competencias
Persona responsable, buena forma física

Envía tu candidatura: empleo@example.com, +34 91 123 45 67""",
    "fr": """Agent de magasinage

Formation
Aucune formation exigée

Compétences
Sérieux, bonne condition physique

Candidature : emploi@example.com, 01 23 45 67 89""",
    "nl": """Magazijnmedewerker

Opleiding
Geen specifieke opleiding vereist

Vaardigheden
Betrouwbaar, fysiek fit

Solliciteer: banen@example.com, 020 123 4567""",
    "uk": """Комірник

Освіта
Без спеціальних вимог

Навички
Відповідальність, фізична витривалість

Надсилайте резюме: jobs@example.com, +380 44 123 4567""",
    "ru": """Кладовщик

Образование
Без специальных требований

Навыки
Ответственность, физическая выносливость

Присылайте резюме: jobs@example.com, +7 495 123 45 67""",
}


@pytest.mark.parametrize("language", sorted(ADVERTS))
def test_a_job_advert_is_not_a_resume(language):
    """The likeliest wrong upload, because the next zone asks for one."""
    text = ADVERTS[language]
    report = build_field_report(text)

    breakdown = score_resume(report, report, [], text)

    assert breakdown.cap_key == "cap_reason_not_a_resume", (
        f"{language} advert scored {breakdown.total}/100 as a CV"
    )
    assert breakdown.total == 0


NOT_RESUMES = {
    "invoice": """Rechnung Nr. 4711

Musterfirma GmbH, Musterweg 3, 20095 Hamburg
buchhaltung@musterfirma.de | 040 987654

Position         Menge   Betrag
Beratung             3   750,00 EUR
Summe                    750,00 EUR""",
    "menu": """Speisekarte

Vorspeisen
Tomatensuppe  5,50
Salat         6,00

Reservierung: 040 111222""",
    "blank form": """Charakterbogen

Name: ______  Klasse: ______  Stufe: ______
Stärke: __  Geschick: __  Weisheit: __""",
    "cover letter": """Sehr geehrte Damen und Herren,

hiermit bewerbe ich mich auf die ausgeschriebene Stelle. Über eine
Einladung zu einem Gespräch würde ich mich sehr freuen.

Mit freundlichen Grüßen
Anna Muster
anna@example.com""",
}


@pytest.mark.parametrize("name", sorted(NOT_RESUMES))
def test_other_documents_are_not_resumes(name):
    text = NOT_RESUMES[name]
    report = build_field_report(text)

    breakdown = score_resume(report, report, [], text)

    assert breakdown.cap_key == "cap_reason_not_a_resume", (
        f"{name} scored {breakdown.total}/100 as a CV"
    )


RESUMES = {
    "with headings": """Anna Muster
anna@example.com | 040 1234567

Berufserfahrung
Studio Nord, Hamburg — Grafikdesignerin      03/2019 - 08/2024
Freie Mitarbeit                              01/2015 - 02/2019

Ausbildung
HAW Hamburg, B.A. Kommunikationsdesign       10/2011 - 09/2014""",
    "no headings at all": """Anna Muster
Grafikdesignerin
anna@example.com | 040 1234567

Studio Nord, Hamburg          03/2019 - 08/2024
Freie Mitarbeit               01/2015 - 02/2019
HAW Hamburg, B.A.             10/2011 - 09/2014""",
    "no contact details": """Anna Muster

Berufserfahrung
Studio Nord, Hamburg      03/2019 - 08/2024

Ausbildung
HAW Hamburg, B.A.         10/2011 - 09/2014""",
}


@pytest.mark.parametrize("shape", sorted(RESUMES))
def test_real_resumes_are_scored(shape):
    """"No headings at all" is the one that matters: name, role, contact
    and a column of dates is a very common one-page designer CV, and the
    section-counting rule scored it zero."""
    text = RESUMES[shape]
    report = build_field_report(text)

    breakdown = score_resume(report, report, [], text)

    assert breakdown.cap_key != "cap_reason_not_a_resume", (
        f"a CV with {shape} was rejected as not a CV"
    )
