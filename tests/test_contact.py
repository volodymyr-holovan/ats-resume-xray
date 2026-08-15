from ats_xray.contact import find_email, find_name, find_phone


def test_find_name_returns_first_non_empty_line():
    text = "\n\nJane Doe\nSoftware Engineer\n"
    assert find_name(text) == "Jane Doe"


def test_find_name_none_for_empty_text():
    assert find_name("   \n\n  ") is None


def test_find_email_found():
    text = "Contact: jane.doe+resume@example.co.uk for details"
    assert find_email(text) == "jane.doe+resume@example.co.uk"


def test_find_email_none_when_absent():
    assert find_email("No contact info here.") is None


def test_find_phone_found_with_common_formatting():
    assert find_phone("Call me at +1 (555) 123-4567 anytime") == "+1 (555) 123-4567"


def test_find_phone_none_for_short_number():
    assert find_phone("I have 5 years of experience, graduated in 2019") is None


def test_find_phone_none_when_absent():
    assert find_phone("No numbers relevant here.") is None
