from ats_xray.field_report import build_field_report


def test_build_field_report_all_fields_found():
    text = (
        "Jane Doe\n"
        "jane@example.com | +1 555 123 4567\n\n"
        "Experience\n"
        "Senior Engineer at Acme\n\n"
        "Education\n"
        "BSc Computer Science\n\n"
        "Skills\n"
        "Python, SQL"
    )

    report = build_field_report(text)

    assert report["name"] == {"found": True, "value": "Jane Doe"}
    assert report["email"]["found"] is True
    assert report["phone"]["found"] is True
    assert report["sections"]["experience"]["found"] is True
    assert report["sections"]["education"]["found"] is True
    assert report["sections"]["skills"]["found"] is True


def test_build_field_report_missing_fields():
    text = "Just a block of unstructured text with no name line even, actually this becomes the name."

    report = build_field_report(text)

    assert report["email"] == {"found": False, "value": None}
    assert report["phone"] == {"found": False, "value": None}
    assert report["sections"]["experience"] == {"found": False, "value": None}
    assert report["sections"]["education"] == {"found": False, "value": None}
    assert report["sections"]["skills"] == {"found": False, "value": None}
