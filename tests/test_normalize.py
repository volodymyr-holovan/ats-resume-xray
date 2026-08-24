import pytest

from ats_xray.normalize import contains_phrase, fold, same_word, tokens


def test_umlauts_expand_so_both_spellings_meet():
    """Job adverts are typed on whatever keyboard was to hand. "Qualität"
    and "Qualitaet" are the same word and have to fold to the same string,
    or every match report gains a false gap."""
    assert fold("Qualitätssicherung") == fold("Qualitaetssicherung")
    assert fold("Müller") == fold("Mueller")
    assert fold("Straße") == fold("Strasse")


def test_technology_punctuation_survives_folding():
    """C++ and C# are different languages, and both differ from C. Folding
    that discarded the punctuation would merge all three."""
    assert fold("C++") == "c++"
    assert fold("C#") == "c#"
    assert fold("Node.js") == "node.js"
    assert fold(".NET") == ".net"


def test_sentence_punctuation_does_not_fuse_into_the_word():
    """A dot ending a sentence would otherwise make "Docker." a different
    token from "Docker" and silently lose the match."""
    assert tokens("Wir nutzen Docker.") == ["wir", "nutzen", "docker"]
    assert tokens("Erfahrung mit C#.") == ["erfahrung", "mit", "c#"]


def test_non_latin_scripts_are_not_erased():
    """An ASCII-only fold turns Cyrillic into the empty string, and an empty
    needle matches every haystack -- which made every heading match every
    line until this was fixed."""
    assert fold("Ваш профіль") != ""
    assert fold("Ваш профіль") == "ваш профіль"


def test_same_word_accepts_german_inflection():
    assert same_word("kenntnis", "kenntnisse")
    assert same_word("erfahrung", "erfahrungen")
    assert same_word("entwickler", "entwicklern")


@pytest.mark.parametrize(
    ("left", "right"),
    [
        ("sql", "sqlite"),  # short: a prefix here is a different product
        ("java", "javascript"),  # too far apart to be inflection
        ("test", "tests"),  # below the minimum stem length
    ],
)
def test_same_word_refuses_look_alikes(left, right):
    assert not same_word(left, right)


def test_contains_phrase_matches_across_inflection():
    haystack = tokens("Erfahrung mit maschinellem Lernen im Projekt")
    assert contains_phrase(haystack, fold("maschinelles Lernen"))


def test_contains_phrase_requires_the_words_to_be_adjacent():
    haystack = tokens("Maschinen bauen und Lernen fördern")
    assert not contains_phrase(haystack, fold("maschinelles Lernen"))
