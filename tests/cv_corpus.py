"""A CV in every language the tool speaks, clean, and one fault at a time.

Data only. Not a test module (no ``test_`` prefix), so pytest does not
collect it; ``test_cv_corpus.py`` holds what is asserted about it.

Modelled on the shape of real applications: name and contact block, short
profile, reverse-chronological experience with duty lines under each entry,
education, a separate volunteering section, skills, languages.

Two things this is built to catch, in both directions.

The clean CV must produce nothing at all, in all seven languages. That is the
harder assertion and the one that earns its keep: a convention check is a
claim about a document that reads perfectly, so a false one is pure noise to
whoever gets it. Each clean CV therefore carries the traps on purpose -- a
duty line about instructing volunteers, an employer whose name contains the
word, a hyphenated compound, a heading that is not the first alias.

Each faulty CV carries exactly one seeded fault and must produce exactly that
finding. One at a time because the detectors are not independent: the gap
check stands down when a date range runs backwards, on purpose, so a document
holding both faults can only ever report one of them and would make a
combined expectation meaningless.

Dates are fixed rather than relative to the day the suite runs, and TODAY is
pinned to match. A fixture that drifts with the calendar reports a gap it did
not mean to seed some months after it was written.
"""

from datetime import date

TODAY = date(2026, 9, 16)

# --------------------------------------------------------------------------
# The clean CV in each language
# --------------------------------------------------------------------------

CLEAN: dict[str, str] = {}

CLEAN["de"] = """Anna Bergmann
IT-Systemadministratorin
Hauptstraße 12, 28195 Bremen
Telefon: +49 421 1234567
E-Mail: anna.bergmann@example.de

PROFIL
Systemadministratorin mit sechs Jahren Erfahrung im Betrieb von Server- und Netzwerkinfrastruktur.
Ich arbeite gern im Team und übernehme Verantwortung für den laufenden Betrieb.

BERUFSERFAHRUNG
Systemadministratorin
Nordwerk GmbH, Bremen · 03/2021 – heute
Betrieb und Wartung von 40 virtuellen Servern unter VMware
Einweisung und Schulung ehrenamtlicher Helfer an der eingesetzten Technik
Aufbau eines zentralen Monitorings mit Zabbix und Auswertung der Alarme

IT-Supportmitarbeiterin
Verein zur Förderung ehrenamtlicher Arbeit e.V., Oldenburg · 08/2018 – 02/2021
Annahme und Bearbeitung von Störungsmeldungen im First- und Second-Level
Betreuung der Kinder- und Jugendhilfe als interner Ansprechpartner
Verwaltung von Benutzerkonten und Zugriffsrechten im Active Directory

AUSBILDUNG
Fachinformatikerin für Systemintegration
Berufsbildende Schulen Bremen · 09/2015 – 07/2018

EHRENAMT
Ehrenamtliche Helferin
Tafel Bremen e.V. · 01/2019 – 12/2020

KENNTNISSE
VMware, Windows Server, Active Directory, Zabbix, PowerShell, Linux

SPRACHEN
Deutsch (Muttersprache), Englisch (B2)"""

CLEAN["en"] = """Anna Bergmann
IT Systems Administrator
12 Hauptstrasse, Bristol BS1 4ST
Phone: +44 117 496 0123
Email: anna.bergmann@example.co.uk

SUMMARY
Systems administrator with six years running server and network infrastructure.
I enjoy working in a team and take responsibility for day-to-day operations.

EXPERIENCE
Systems Administrator
Nordwerk Ltd, Bristol · 03/2021 - present
Ran and maintained 40 virtual servers on VMware across two sites
Trained volunteer helpers on the equipment used at public events
Built central monitoring with Zabbix and reviewed the alerts weekly

IT Support Officer
Dahlmann Systems, Cardiff · 08/2018 - 02/2021
Handled first and second line incidents through the service desk
Managed user accounts and access rights in Active Directory

EDUCATION
BSc Computer Science
University of Bristol · 09/2015 - 07/2018

VOLUNTEERING
Volunteer Helper
Bristol Food Bank · 01/2019 - 12/2020

SKILLS
VMware, Windows Server, Active Directory, Zabbix, PowerShell, Linux

LANGUAGES
German (native), English (C1)"""

CLEAN["uk"] = """Анна Бергман
Системний адміністратор
вул. Головна 12, Львів 79000
Телефон: +380 67 123 4567
Електронна пошта: anna.bergman@example.com

ПРО СЕБЕ
Системний адміністратор із шістьма роками досвіду обслуговування серверної та мережевої інфраструктури.
Основні напрями: віртуалізація, моніторинг і підтримка користувачів.

ДОСВІД РОБОТИ
Системний адміністратор
ТОВ «Нордверк», Львів · 03/2021 – дотепер
Обслуговування 40 віртуальних серверів на базі VMware
Координація роботи волонтерів під час громадських заходів
Побудова централізованого моніторингу на Zabbix

Фахівець технічної підтримки
Далманн Системи, Одеса · 08/2018 – 02/2021
Приймання та опрацювання заявок першої та другої лінії
Адміністрування облікових записів і прав доступу в Active Directory

ОСВІТА
Бакалавр комп'ютерних наук
Львівський національний університет · 09/2015 – 07/2018

ВОЛОНТЕРСТВО
Волонтер
БФ «Карітас Львів» · 01/2019 – 12/2020

НАВИЧКИ
VMware, Windows Server, Active Directory, Zabbix, PowerShell, Linux

МОВИ
Українська (рідна), англійська (B2)"""

CLEAN["ru"] = """Анна Бергман
Системный администратор
ул. Главная 12, Алматы 050000
Телефон: +7 701 123 4567
Электронная почта: anna.bergman@example.com

О СЕБЕ
Системный администратор с шестью годами опыта обслуживания серверной и сетевой инфраструктуры.
Основные направления: виртуализация, мониторинг и поддержка пользователей.

ОПЫТ РАБОТЫ
Системный администратор
ТОО «Нордверк», Алматы · 03/2021 – настоящее время
Обслуживание 40 виртуальных серверов на базе VMware
Координация работы волонтёров во время общественных мероприятий
Построение централизованного мониторинга на Zabbix

Специалист технической поддержки
Далманн Системы, Астана · 08/2018 – 02/2021
Приём и обработка заявок первой и второй линии
Администрирование учётных записей и прав доступа в Active Directory

ОБРАЗОВАНИЕ
Бакалавр компьютерных наук
Казахский национальный университет · 09/2015 – 07/2018

ВОЛОНТЕРСТВО
Волонтёр
Фонд «Каритас» · 01/2019 – 12/2020

НАВЫКИ
VMware, Windows Server, Active Directory, Zabbix, PowerShell, Linux

ЯЗЫКИ
Русский (родной), английский (B2)"""

CLEAN["es"] = """Ana Bergmann
Administradora de sistemas
Calle Mayor 12, 28013 Madrid
Teléfono: +34 910 123 456
Correo electrónico: ana.bergmann@example.es

PERFIL
Administradora de sistemas con seis años de experiencia en infraestructura de servidores y redes.
Áreas principales: virtualización, monitorización y soporte a usuarios.

EXPERIENCIA
Administradora de sistemas
Nordwerk S.L., Madrid · 03/2021 – actualidad
Operación y mantenimiento de 40 servidores virtuales sobre VMware
Formación de personal voluntario en los equipos utilizados en eventos
Implantación de la monitorización centralizada con Zabbix

Técnica de soporte informático
Dahlmann Sistemas, Valencia · 08/2018 – 02/2021
Atención y resolución de incidencias de primer y segundo nivel
Gestión de cuentas de usuario y permisos en Active Directory

EDUCACIÓN
Grado en Ingeniería Informática
Universidad Politécnica de Madrid · 09/2015 – 07/2018

VOLUNTARIADO
Voluntaria
Banco de Alimentos de Madrid · 01/2019 – 12/2020

HABILIDADES
VMware, Windows Server, Active Directory, Zabbix, PowerShell, Linux

IDIOMAS
Español (nativo), inglés (B2)"""

CLEAN["nl"] = """Anna Bergmann
Systeembeheerder
Hoofdstraat 12, 1012 AB Amsterdam
Telefoon: +31 20 123 4567
E-mailadres: anna.bergmann@example.nl

PROFIEL
Systeembeheerder met zes jaar ervaring in het beheer van server- en netwerkinfrastructuur.
Belangrijkste gebieden: virtualisatie, monitoring en gebruikersondersteuning.

WERKERVARING
Systeembeheerder
Nordwerk B.V., Amsterdam · 03/2021 – heden
Beheer en onderhoud van 40 virtuele servers op VMware
Instructie en begeleiding van vrijwilligers bij de gebruikte apparatuur
Opzetten van centrale monitoring met Zabbix

Medewerker IT-ondersteuning
Dahlmann Systemen, Utrecht · 08/2018 – 02/2021
Aannemen en afhandelen van meldingen op eerste en tweede lijn
Beheer van gebruikersaccounts en toegangsrechten in Active Directory

OPLEIDING
Bachelor Informatica
Hogeschool van Amsterdam · 09/2015 – 07/2018

VRIJWILLIGERSWERK
Vrijwilliger
Voedselbank Amsterdam · 01/2019 – 12/2020

VAARDIGHEDEN
VMware, Windows Server, Active Directory, Zabbix, PowerShell, Linux

TALEN
Nederlands (moedertaal), Engels (B2)"""

CLEAN["fr"] = """Anna Bergmann
Administratrice systèmes
12 rue Principale, 75011 Paris
Téléphone : +33 1 23 45 67 89
Adresse électronique : anna.bergmann@example.fr

PROFIL
Administratrice systèmes avec six années d'expérience en infrastructure serveurs et réseaux.
Domaines principaux : virtualisation, supervision et support aux utilisateurs.

EXPÉRIENCE
Administratrice systèmes
Nordwerk SARL, Paris · 03/2021 – aujourd'hui
Exploitation et maintenance de 40 serveurs virtuels sous VMware
Formation des bénévoles aux équipements utilisés lors des événements
Mise en place de la supervision centralisée avec Zabbix

Technicienne support informatique
Dahlmann Systèmes, Lyon · 08/2018 – 02/2021
Prise en charge et traitement des incidents de premier et second niveau
Gestion des comptes utilisateurs et des droits dans Active Directory

FORMATION
Licence en informatique
Université Paris-Saclay · 09/2015 – 07/2018

BÉNÉVOLAT
Bénévole
Banque alimentaire de Paris · 01/2019 – 12/2020

COMPÉTENCES
VMware, Windows Server, Active Directory, Zabbix, PowerShell, Linux

LANGUES
Français (langue maternelle), anglais (B2)"""


# --------------------------------------------------------------------------
# One seeded fault per document
# --------------------------------------------------------------------------


def _replace(language: str, old: str, new: str) -> str:
    text = CLEAN[language]
    assert old in text, f"{language}: {old!r} is not in the clean CV any more"
    return text.replace(old, new, 1)


def _backwards_dates(language: str) -> str:
    """An end that precedes its start -- the commonest typed date fault."""
    pairs = {
        "de": ("08/2018 – 02/2021", "08/2018 – 02/2016"),
        "en": ("08/2018 - 02/2021", "08/2018 - 02/2016"),
        "uk": ("08/2018 – 02/2021", "08/2018 – 02/2016"),
        "ru": ("08/2018 – 02/2021", "08/2018 – 02/2016"),
        "es": ("08/2018 – 02/2021", "08/2018 – 02/2016"),
        "nl": ("08/2018 – 02/2021", "08/2018 – 02/2016"),
        "fr": ("08/2018 – 02/2021", "08/2018 – 02/2016"),
    }
    return _replace(language, *pairs[language])


def _far_future(language: str) -> str:
    """A year typed with the wrong first digit, landing decades ahead."""
    pairs = {
        "de": ("03/2021 – heute", "03/2201 – heute"),
        "en": ("03/2021 - present", "03/2201 - present"),
    }
    return _replace(language, *pairs[language])


def _volunteering_as_a_job(language: str) -> str:
    """The volunteer entry moved up under experience, its own section gone."""
    if language == "de":
        text = CLEAN["de"].replace(
            "EHRENAMT\nEhrenamtliche Helferin\nTafel Bremen e.V. · 01/2019 – 12/2020\n\n", ""
        )
        return text.replace(
            "AUSBILDUNG",
            "Ehrenamtliche Helferin\nTafel Bremen e.V. · 01/2019 – 12/2020\nAusgabe von Lebensmitteln an Bedürftige\n\nAUSBILDUNG",
            1,
        )
    text = CLEAN["uk"].replace(
        "ВОЛОНТЕРСТВО\nВолонтер\nБФ «Карітас Львів» · 01/2019 – 12/2020\n\n", ""
    )
    return text.replace(
        "ОСВІТА",
        "Волонтер\nБФ «Карітас Львів» · 01/2019 – 12/2020\nВидача продуктових наборів\n\nОСВІТА",
        1,
    )


def _first_person(language: str) -> str:
    """Whole sentences about oneself, outside the profile where they belong."""
    if language == "de":
        return _replace(
            "de",
            "Betrieb und Wartung von 40 virtuellen Servern unter VMware",
            "Ich habe 40 virtuelle Server unter VMware betrieben und gewartet\nIch war für die Verfügbarkeit der Systeme verantwortlich",
        )
    return _replace(
        "en",
        "Ran and maintained 40 virtual servers on VMware across two sites",
        "I ran and maintained 40 virtual servers on VMware across two sites\nI was responsible for the availability of every system",
    )


def _oldest_first(language: str) -> str:
    """The two jobs swapped, so the timeline climbs instead of descending."""
    if language == "de":
        newer = """Systemadministratorin
Nordwerk GmbH, Bremen · 03/2021 – heute
Betrieb und Wartung von 40 virtuellen Servern unter VMware
Einweisung und Schulung ehrenamtlicher Helfer an der eingesetzten Technik
Aufbau eines zentralen Monitorings mit Zabbix und Auswertung der Alarme"""
        older = """IT-Supportmitarbeiterin
Verein zur Förderung ehrenamtlicher Arbeit e.V., Oldenburg · 08/2018 – 02/2021
Annahme und Bearbeitung von Störungsmeldungen im First- und Second-Level
Betreuung der Kinder- und Jugendhilfe als interner Ansprechpartner
Verwaltung von Benutzerkonten und Zugriffsrechten im Active Directory"""
        oldest = """Auszubildende Fachinformatikerin
Weser IT Service, Bremen · 09/2015 – 07/2018
Mitarbeit im Anwendersupport und in der Geräteverwaltung"""
    else:
        newer = """Systems Administrator
Nordwerk Ltd, Bristol · 03/2021 - present
Ran and maintained 40 virtual servers on VMware across two sites
Trained volunteer helpers on the equipment used at public events
Built central monitoring with Zabbix and reviewed the alerts weekly"""
        older = """IT Support Officer
Dahlmann Systems, Cardiff · 08/2018 - 02/2021
Handled first and second line incidents through the service desk
Managed user accounts and access rights in Active Directory"""
        oldest = """IT Apprentice
Severn IT Services, Bristol · 09/2015 - 07/2018
Assisted with user support and device management"""
    text = CLEAN[language]
    assert newer in text and older in text
    return text.replace(newer + "\n\n" + older, oldest + "\n\n" + older + "\n\n" + newer, 1)


def _unexplained_gap(language: str) -> str:
    """Fourteen months with nothing in them, between the two jobs."""
    return _replace("de", "Nordwerk GmbH, Bremen · 03/2021 – heute",
                    "Nordwerk GmbH, Bremen · 05/2022 – heute")


def _outdated_details(language: str) -> str:
    """Fields a German CV has not needed since the AGG."""
    return _replace(
        "de",
        "E-Mail: anna.bergmann@example.de",
        "E-Mail: anna.bergmann@example.de\nFamilienstand: verheiratet, zwei Kinder\nKonfession: evangelisch",
    )


FAULTY: list[tuple[str, str, str]] = [
    # (language, the one rule that must fire, the document)
    *[(lang, "impossible_dates", _backwards_dates(lang))
      for lang in ("de", "en", "uk", "ru", "es", "nl", "fr")],
    ("de", "impossible_dates", _far_future("de")),
    ("en", "impossible_dates", _far_future("en")),
    ("de", "volunteering_listed_as_employment", _volunteering_as_a_job("de")),
    ("uk", "volunteering_listed_as_employment", _volunteering_as_a_job("uk")),
    ("de", "first_person_in_cv", _first_person("de")),
    ("en", "first_person_in_cv", _first_person("en")),
    ("de", "oldest_entry_first", _oldest_first("de")),
    ("en", "oldest_entry_first", _oldest_first("en")),
    ("de", "unexplained_gap", _unexplained_gap("de")),
    ("de", "outdated_personal_details", _outdated_details("de")),
]


# --------------------------------------------------------------------------
# Faults in how the file parses, rather than in what it says
# --------------------------------------------------------------------------

CREATIVE_HEADINGS: dict[str, dict[str, str]] = {
    "de": {"PROFIL": "ÜBER MEINEN WEG", "BERUFSERFAHRUNG": "MEIN WERDEGANG",
           "AUSBILDUNG": "MEINE LERNJAHRE", "EHRENAMT": "WAS MIR WICHTIG IST",
           "KENNTNISSE": "WAS MITGEBRACHT WIRD", "SPRACHEN": "GESPROCHENE WORTE"},
    "en": {"SUMMARY": "ABOUT MY PATH", "EXPERIENCE": "MY JOURNEY SO FAR",
           "EDUCATION": "MY LEARNING YEARS", "VOLUNTEERING": "GIVING SOMETHING BACK",
           "SKILLS": "WHAT IS BROUGHT ALONG", "LANGUAGES": "SPOKEN WORDS"},
    "uk": {"ПРО СЕБЕ": "МІЙ ШЛЯХ", "ДОСВІД РОБОТИ": "ЧИМ ЗАЙМАВСЯ",
           "ОСВІТА": "РОКИ НАВЧАННЯ", "ВОЛОНТЕРСТВО": "ЩО ВАЖЛИВО",
           "НАВИЧКИ": "ЩО ВМІЮ", "МОВИ": "ЯКОЮ ГОВОРЮ"},
    "ru": {"О СЕБЕ": "МОЙ ПУТЬ", "ОПЫТ РАБОТЫ": "ЧЕМ ЗАНИМАЛСЯ",
           "ОБРАЗОВАНИЕ": "ГОДЫ УЧЁБЫ", "ВОЛОНТЕРСТВО": "ЧТО ВАЖНО",
           "НАВЫКИ": "ЧТО УМЕЮ", "ЯЗЫКИ": "НА КАКОМ ГОВОРЮ"},
    "es": {"PERFIL": "MI CAMINO", "EXPERIENCIA": "A QUÉ ME DEDIQUÉ",
           "EDUCACIÓN": "AÑOS DE APRENDIZAJE", "VOLUNTARIADO": "LO QUE ME IMPORTA",
           "HABILIDADES": "LO QUE APORTO", "IDIOMAS": "LO QUE HABLO"},
    "nl": {"PROFIEL": "MIJN WEG", "WERKERVARING": "WAARMEE IK BEZIG WAS",
           "OPLEIDING": "MIJN LEERJAREN", "VRIJWILLIGERSWERK": "WAT BELANGRIJK IS",
           "VAARDIGHEDEN": "WAT WORDT MEEGEBRACHT", "TALEN": "GESPROKEN WOORDEN"},
    "fr": {"PROFIL": "MON PARCOURS", "EXPÉRIENCE": "CE QUI A ÉTÉ FAIT",
           "FORMATION": "MES ANNÉES D'APPRENTISSAGE", "BÉNÉVOLAT": "CE QUI COMPTE",
           "COMPÉTENCES": "CE QUI EST APPORTÉ", "LANGUES": "CE QUI EST PARLÉ"},
}
"""Headings a person might reasonably write and the software cannot know.

Each replaces every recognised heading in that language, because the check
only speaks up when nothing at all was recognised -- one creative label
beside a plain "Experience" leaves the parser the anchor it needs.

Written to avoid tripping the other checks on the way past: no first-person
pronoun a detector would count, and nothing that happens to be another
language's alias. The runner asserts the rename really did leave the
document without a single recognised heading, so a label that turns out to
be in the vocabulary fails loudly instead of quietly testing nothing."""

CONTACT_LABELS: dict[str, tuple[str, str]] = {
    "de": ("Telefon: +49 421 1234567", "E-Mail: anna.bergmann@example.de"),
    "en": ("Phone: +44 117 496 0123", "Email: anna.bergmann@example.co.uk"),
    "uk": ("Телефон: +380 67 123 4567", "Електронна пошта: anna.bergman@example.com"),
    "ru": ("Телефон: +7 701 123 4567", "Электронная почта: anna.bergman@example.com"),
    "es": ("Teléfono: +34 910 123 456", "Correo electrónico: ana.bergmann@example.es"),
    "nl": ("Telefoon: +31 20 123 4567", "E-mailadres: anna.bergmann@example.nl"),
    "fr": ("Téléphone : +33 1 23 45 67 89", "Adresse électronique : anna.bergmann@example.fr"),
}


def creative_headings(language: str) -> str:
    text = CLEAN[language]
    for old, new in CREATIVE_HEADINGS[language].items():
        assert f"\n{old}\n" in text, f"{language}: heading {old!r} is not in the clean CV"
        text = text.replace(f"\n{old}\n", f"\n{new}\n")
    return text


def no_contact(language: str) -> str:
    """Both ways of reaching the applicant gone. The rule wants neither: a
    CV with a phone and no email is reachable, and is scored down without
    being told it is unreachable."""
    text = CLEAN[language]
    for line in CONTACT_LABELS[language]:
        assert line in text, f"{language}: contact line {line!r} is not in the clean CV"
        text = text.replace(line + "\n", "")
    return text


PARSING_FAULTS: list[tuple[str, str, str]] = [
    *[(lang, "unrecognised_section_headings", creative_headings(lang))
      for lang in ("de", "en", "uk", "ru", "es", "nl", "fr")],
    *[(lang, "missing_contact_field", no_contact(lang))
      for lang in ("de", "en", "uk", "ru", "es", "nl", "fr")],
]
