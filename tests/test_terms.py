import pytest

from ats_xray.terms import MAX_TERMS_PER_AD, extract_terms


def _folded(terms):
    return {term.lower() for term in terms}


def test_a_german_noun_the_lexicon_does_not_know_is_still_found():
    """The whole point of this module: an advert for a trade nobody added to
    the gazetteer must not produce an empty requirements list."""
    found = _folded(extract_terms("- Kenntnisse im Umgang mit Hochregallagertechnik", "de"))

    assert "hochregallagertechnik" in found


def test_the_adjective_opening_a_bullet_is_not_a_requirement():
    """German capitalises the first word of a sentence whatever it is, so
    "Abgeschlossene" and "Mindestens" look exactly like nouns."""
    found = _folded(extract_terms("- Abgeschlossene Ausbildung als Massschneiderin", "de"))

    assert "abgeschlossene" not in found
    assert "massschneiderin" in found


def test_framing_words_are_dropped_from_both_ends_of_a_phrase():
    """The introducer pattern does its job and then runs past the noun:
    "Pflegedokumentation sind zwingend" is one requirement, not three."""
    found = _folded(
        extract_terms("- Kenntnisse in der Bohrinselwartung sind zwingend erforderlich", "de")
    )

    assert "bohrinselwartung" in found
    assert not any("zwingend" in term for term in found)


def test_a_word_the_lexicon_already_claimed_is_not_repeated():
    """"HACCP-Richtlinien" beside "HACCP" would show the same requirement
    twice, once as a skill and once as a loose noun."""
    found = _folded(extract_terms("- Einhaltung der HACCP-Richtlinien", "de"))

    assert not any("haccp" in term for term in found)


def test_a_shouted_line_is_not_mined_for_nouns():
    """Every word in an all-capitals heading looks like a German noun, so
    the capitalisation signal carries no information there."""
    assert extract_terms("WIR SUCHEN AB SOFORT EINE REINIGUNGSKRAFT", "de") == []


def test_language_names_never_come_back_as_keywords():
    """Levels are read by the typed extractor; the bare name would be a
    duplicate requirement with no level attached."""
    for text, language in [
        ("- Verhandlungssichere Deutschkenntnisse", "de"),
        ("- Aleman fluido", "es"),
        ("- Німецька мова на рівні C1", "uk"),
    ]:
        assert extract_terms(text, language) == []


@pytest.mark.parametrize(
    ("line", "language", "expected"),
    [
        ("- Conocimientos de contabilidad analitica", "es", "contabilidad"),
        ("- Kennis van boekhouding", "nl", "boekhouding"),
        ("- Connaissance de la comptabilite", "fr", "comptabilite"),
        ("- Знання бухгалтерського обліку", "uk", "бухгалтерського"),
        ("- Знание бухгалтерского учета", "ru", "бухгалтерского"),
        ("- Experience with underwater welding", "en", "underwater"),
    ],
)
def test_every_language_announces_requirements_the_same_way(line, language, expected):
    found = " ".join(extract_terms(line, language)).lower()

    assert expected in found


def test_the_number_of_guesses_is_capped():
    """A list too long to read is a list nobody will correct."""
    from ats_xray.vacancy import parse_vacancy

    noisy = "Ihr Profil\n" + "\n".join(
        f"- Erfahrung mit Spezialgeraet{index} und Sonderverfahren{index}" for index in range(40)
    )
    generic = [r for r in parse_vacancy(noisy).requirements if r.key.startswith("term:")]

    assert len(generic) <= MAX_TERMS_PER_AD


def test_an_article_cannot_bite_into_the_following_word():
    """The Spanish article "el" was matched inside German "Elektronik" and
    the requirement came back as "ektronik". Articles are whole words."""
    found = extract_terms("- Fundierte Kenntnisse in Elmshorner Anlagentechnik", "de")

    assert not any(term.lower().startswith("mshorn") for term in found)
    assert any("Elmshorner" in term for term in found)


def test_the_tail_of_an_elided_compound_is_not_a_requirement():
    """"Fehlersuche und -behebung" means Fehlerbehebung; the hyphen stands in
    for the head. "behebung" on its own names nothing."""
    found = {term.lower() for term in extract_terms("- Bohrarbeit und -pruefung im Feld", "de")}

    assert "pruefung" not in found


def test_a_partly_known_phrase_keeps_its_unknown_words_whole():
    """Filtering the covered words used to work on folded tokens while
    rebuilding from the original ones, and the two lists did not line up:
    "IT-Systemen" is one word before folding and two after."""
    found = extract_terms("- Erfahrung mit Docker und Hochregallagertechnik", "de")

    assert any(term == "Hochregallagertechnik" for term in found)
