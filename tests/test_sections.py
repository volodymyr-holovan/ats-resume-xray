from ats_xray.sections import find_section_headers, split_into_sections


def test_find_section_headers_matches_standalone_english_headers():
    text = "Jane Doe\n\nExperience\nSenior Engineer at Acme\n\nEducation\nBSc Computer Science"
    headers = find_section_headers(text)
    assert [h["section"] for h in headers] == ["experience", "education"]


def test_find_section_headers_matches_german_headers():
    text = "Max Mustermann\n\nBerufserfahrung\nEntwickler bei Acme\n\nAusbildung\nInformatik"
    headers = find_section_headers(text)
    assert [h["section"] for h in headers] == ["experience", "education"]


def test_find_section_headers_ignores_word_inside_a_sentence():
    text = "My experience includes leading three teams over five years."
    assert find_section_headers(text) == []


def test_find_section_headers_tolerates_trailing_colon():
    text = "Skills:\nPython, SQL"
    headers = find_section_headers(text)
    assert [h["section"] for h in headers] == ["skills"]


def test_split_into_sections_assigns_content_between_headers():
    text = "Jane Doe\njane@example.com\n\nExperience\nSenior Engineer at Acme\n\nEducation\nBSc Computer Science"
    sections = split_into_sections(text)
    assert sections["preamble"] == "Jane Doe\njane@example.com"
    assert sections["experience"] == "Senior Engineer at Acme"
    assert sections["education"] == "BSc Computer Science"


def test_split_into_sections_no_headers_returns_whole_text_as_preamble():
    text = "Just some unstructured text with no recognizable headers."
    assert split_into_sections(text) == {"preamble": text}


def test_split_into_sections_merges_repeated_section_type():
    text = "Skills\nPython\n\nLanguages\nEnglish\n\nSkills\nSQL"
    sections = split_into_sections(text)
    assert sections["skills"] == "Python\nSQL"
    assert sections["languages"] == "English"
