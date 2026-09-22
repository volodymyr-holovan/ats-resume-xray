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
        ("- Conocimientos de vitivinicultura ecologica", "es", "vitivinicultura"),
        ("- Kennis van scheepsbetimmering", "nl", "scheepsbetimmering"),
        ("- Connaissance de la vinification biologique", "fr", "vinification"),
        ("- Знання бджільництва", "uk", "бджільництва"),
        ("- Знание пчеловодства", "ru", "пчеловодства"),
        ("- Experience with underwater welding", "en", "underwater"),
    ],
)
def test_every_language_announces_requirements_the_same_way(line, language, expected):
    """The trade in each line is one the gazetteer does not know, which is
    the only way to see the introducer working. Accountancy used to stand
    here and stopped testing anything the day the gazetteer learned to say
    it in five more languages: the phrase still matched, the word was
    already explained, and the extractor correctly returned nothing."""
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


@pytest.mark.parametrize(
    ("line", "language", "expected"),
    [
        ("- Ervaring met bedrijfsschoonmaak is vereist", "nl", "bedrijfsschoonmaak"),
        ("- Conocimientos de automatismos valorables", "es", "automatismos"),
        ("- La connaissance des programmes est exigee", "fr", "programmes"),
    ],
)
def test_the_boilerplate_after_a_requirement_is_not_part_of_it(line, language, expected):
    """Dutch, Spanish and French mark a requirement as required after naming
    it, not before: "is vereist", "valorables", "est exigee". The introducer
    pattern reaches the end of the line and hands back the whole tail, so the
    keyword arrived as "bedrijfsschoonmaak is vereist" -- a phrase no CV will
    ever contain, scored as a missing requirement on every match."""
    assert extract_terms(line, language) == [expected]


def test_a_head_noun_is_not_trimmed_off_the_phrase_it_heads():
    """"Planning" is furniture at the edge of a phrase ("planning of the
    rota") and the subject in the middle of one. Dropping it wherever it sat
    last turned "lesson planning" into "lesson", which is not a skill."""
    assert extract_terms("- Experience with lesson planning and with didactics", "en") == [
        "lesson planning"
    ]


@pytest.mark.parametrize(
    ("line", "language"),
    [
        ("- At least three years of experience in a professional kitchen", "en"),
        ("- Une experience du nettoyage industriel est exigee", "fr"),
    ],
)
def test_an_adjective_left_behind_by_a_known_skill_is_not_a_requirement(line, language):
    """The lexicon takes "kitchen" and "nettoyage" out of the phrase and
    leaves the word that was describing them. On its own "professional" asks
    for nothing, and it counted against every CV that did not say it."""
    assert extract_terms(line, language) == []


@pytest.mark.parametrize(
    ("line", "language", "expected"),
    [
        ("- Erfahrung mit Docker Swarm", "de", "Swarm"),
        ("- Connaissance des soins de plaies et de l'administration", "fr", "plaies"),
        ("- Manejo de maquinaria de limpieza y de productos quimicos", "es", "maquinaria"),
    ],
)
def test_a_noun_left_behind_by_a_known_skill_is_still_a_requirement(line, language, expected):
    """The other half of the rule above, and the reason it tests the shape of
    the word rather than counting how many are left. "Swarm" is the part of
    "Docker Swarm" the gazetteer does not know; wound care and machinery are
    the trade itself. A rule that dropped every single-word leftover lost all
    three."""
    assert extract_terms(line, language) == [expected]

