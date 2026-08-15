"""FieldReport: a transparent summary of which resume fields were found and
what evidence backs each finding — found/missing per field, with the
matched value, not an opaque score.
"""

from .contact import find_email, find_name, find_phone
from .sections import split_into_sections

EXPECTED_SECTIONS = ("experience", "education", "skills")


def build_field_report(text: str) -> dict:
    """Return a report of the form::

        {
          "name": {"found": bool, "value": str | None},
          "email": {"found": bool, "value": str | None},
          "phone": {"found": bool, "value": str | None},
          "sections": {
              "experience": {"found": bool, "value": str | None},
              "education": {"found": bool, "value": str | None},
              "skills": {"found": bool, "value": str | None},
          },
        }
    """
    sections = split_into_sections(text)

    return {
        "name": _field(find_name(text)),
        "email": _field(find_email(text)),
        "phone": _field(find_phone(text)),
        "sections": {section: _field(sections.get(section) or None) for section in EXPECTED_SECTIONS},
    }


def _field(value: str | None) -> dict:
    return {"found": bool(value), "value": value}
