"""One realistic line per trade, and the skill it has to find.

The lexicon was skewed: around ninety entries for the software stack and
nine for nursing, in a country where nursing is the larger employer. These
are the fields that had one or two rows standing in for a whole occupation
— aviation, human resources, property, public administration — plus the
care work that had a single broad "Pflege" covering everything from washing
a patient to running an intensive-care ventilator.

Each line here is written the way an advert or a CV writes it, not the way
the lexicon stores it. That is the point: a test that quotes the alias back
at itself only proves the file was read.
"""

import pytest

from ats_xray.skills_lexicon import find_skills, label_for

TRADE_LINES = [
    # care and health
    ("Grundpflege und Prophylaxen bei bettlägerigen Bewohnern", "grundpflege"),
    ("Medikamentengabe, Verbandwechsel und Injektionen nach Anordnung", "behandlungspflege"),
    ("Begleitung Sterbender im Hospiz, Schmerzmanagement", "palliativpflege"),
    ("Betreuung von Menschen mit Demenz, Validation nach Naomi Feil", "gerontopsychiatrie"),
    ("Neonatologie und Säuglingspflege auf der Kinderstation", "kinderkrankenpflege"),
    ("Begutachtung durch den Medizinischen Dienst nach SGB XI", "pflegegrad"),
    ("Instrumentieren und Springerdienst im Operationsdienst", "op_pflege"),
    ("Probenaufbereitung und klinische Chemie im Labor", "laborassistenz"),
    # education and social work
    ("Erzieherin in Krippe und Hort, pädagogische Fachkraft", "kinderbetreuung"),
    ("Heilpädagogik und Entwicklungsförderung in der Frühförderung", "fruehfoerderung"),
    ("Seminarleitung in der Weiterbildung, ADA-Schein vorhanden", "erwachsenenbildung"),
    ("Ausbildereignung nach AEVO, Betreuung der Azubis", "ausbildereignung"),
    # human resources and office
    ("Personalakte, Zeugniserstellung und Vertragswesen", "personaladministration"),
    # production, vehicles, aviation
    ("Spritzguss und Extrusion in der Kunststofftechnik", "kunststofftechnik"),
    ("Abfüllung nach IFS Standard, Hygieneschulung", "lebensmittelproduktion"),
    ("Motorinstandsetzung und Fehlerdiagnose am Fahrzeug", "kfz_mechatronik"),
    ("LKW-Werkstatt und Landmaschinentechnik", "nutzfahrzeuge"),
    ("Fluggerätmechaniker, Line Maintenance nach Part-145", "luftfahrttechnik"),
    ("Kabinenpersonal, Safety and Emergency Procedures", "flugbegleitung"),
    ("Gepäckabfertigung und Vorfelddienst, Luftsicherheit", "bodenabfertigung"),
    # retail, hospitality
    ("Kassieren am Kassensystem, Tagesabschluss und Geldzählung", "kassiertaetigkeit"),
    ("Front Office, Reservierungen, Opera PMS", "hotelrezeption"),
    ("Zimmerreinigung und Wäschepflege im Housekeeping", "hauswirtschaft"),
    # property, public service, security
    ("Hausverwaltung mit Nebenkostenabrechnung, WEG-Verwaltung", "immobilienverwaltung"),
    ("Objektbesichtigung, Exposé und Wertermittlung", "immobilienvermittlung"),
    ("Haustechnik und Störungsdienst, Kleinreparaturen", "facility_technik"),
    ("Einwohnermeldeamt, Ausweisdokumente, Publikumsverkehr", "buergerservice"),
    ("Leistungsgewährung nach SGB II, Wohngeld und Antragsbearbeitung", "sozialleistungen"),
    ("Einlasskontrolle und Crowd Management bei Veranstaltungen", "veranstaltungssicherheit"),
    # consulting
    ("Digitalisierungsstrategie und IT-Strategie beraten", "digitalberatung"),
    ("Angebotserstellung und Bid Management für Ausschreibungen", "ausschreibungsmanagement"),
]


@pytest.mark.parametrize("line,skill_id", TRADE_LINES)
def test_a_line_from_the_trade_finds_its_skill(line, skill_id):
    found = find_skills(line)

    assert skill_id in found, (
        f"{line!r} found {[label_for(i) for i in found]} instead of {label_for(skill_id)}"
    )


MERGED_INTO_EXISTING = [
    ("Physiotherapie mit manueller Therapie und Lymphdrainage", "therapie"),
    ("Active Sourcing und Bewerbermanagement", "personalwesen"),
    ("Kündigungsschutz und Betriebsverfassungsgesetz", "rechtsgebiete"),
    ("Vorbeugende Instandhaltung nach TPM", "wartung"),
    ("Schaufenstergestaltung und Warendekoration", "warenpraesentation"),
    ("Chef de rang im Restaurant", "service_gastro"),
]


@pytest.mark.parametrize("line,skill_id", MERGED_INTO_EXISTING)
def test_vocabulary_merged_into_an_existing_entry_still_resolves(line, skill_id):
    """Several trades already had a broad entry that owned the narrower
    name. Rather than add an unreachable duplicate, the new wording was
    merged into the entry that already held the ground -- and that is only
    worth anything if the words actually reach it."""
    assert skill_id in find_skills(line)


CARE_SPECIFICS = [
    ("Grundpflege", "grundpflege"),
    ("Behandlungspflege", "behandlungspflege"),
    ("Intensivpflege", "intensivpflege"),
    ("Altenpflege", "pflege"),
    ("Krankenpflege", "pflege"),
]


@pytest.mark.parametrize("word,skill_id", CARE_SPECIFICS)
def test_the_broad_care_entry_gave_up_the_names_it_was_squatting(word, skill_id):
    """"Pflege" listed Grundpflege, Behandlungspflege and Intensivpflege as
    its own aliases, so those three could never be found under their own
    labels. The specific entries own their names now; the broad one still
    answers to the broad words."""
    assert find_skills(word) == [skill_id]
