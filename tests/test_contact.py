import time

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


def test_find_email_stays_fast_on_adversarial_input_with_no_at_sign():
    """Regression test: an earlier version of _EMAIL_RE used unbounded
    quantifiers ([a-zA-Z0-9_.+-]+@...). On a long run of characters that
    match the local-part class but never reach an "@", that pattern
    re-attempts a full greedy-match-then-backtrack at every position in
    the string — quadratic in input length. A malicious resume containing
    a large block of filler text (no "@" anywhere) could hang the process
    for any caller, including the public web app. Must stay well under a
    second even for several MB of adversarial input.
    """
    adversarial_text = "A" * (2 * 1024 * 1024)

    start = time.monotonic()
    result = find_email(adversarial_text)
    elapsed = time.monotonic() - start

    assert result is None
    assert elapsed < 2.0, f"find_email took {elapsed:.2f}s on 2MB of adversarial input — possible ReDoS regression"


def test_find_phone_stays_fast_on_adversarial_input_with_no_terminator():
    """Same regression class as the email test, aimed at the phone regex's
    formerly-unbounded {5,} quantifier.
    """
    adversarial_text = "1" + "." * (2 * 1024 * 1024)

    start = time.monotonic()
    result = find_phone(adversarial_text)
    elapsed = time.monotonic() - start

    assert result is None
    assert elapsed < 2.0, f"find_phone took {elapsed:.2f}s on 2MB of adversarial input — possible ReDoS regression"
