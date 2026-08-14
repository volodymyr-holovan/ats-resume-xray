from ats_xray._pdf_words import group_words_into_lines


def word(text, x0, x1, top, bottom=None):
    return {"text": text, "x0": x0, "x1": x1, "top": top, "bottom": bottom if bottom is not None else top + 10}


def test_group_words_into_lines_orders_and_groups_by_proximity():
    words = [word("World", 50, 90, 0), word("Hello", 0, 40, 0), word("Second", 0, 40, 20)]
    lines = group_words_into_lines(words)
    assert [line["text"] for line in lines] == ["Hello World", "Second"]
    assert lines[0]["top"] == 0
    assert lines[1]["top"] == 20


def test_group_words_into_lines_empty_input():
    assert group_words_into_lines([]) == []
