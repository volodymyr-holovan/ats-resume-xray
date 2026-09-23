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


def test_boxes_drifting_downwards_chain_into_one_line():
    """The tolerance is measured against the previous box, not the first.

    Five boxes three points apart are twelve points apart end to end and
    still come back as one line, because each one is within tolerance of its
    neighbour. That is deliberate -- a scanned or slightly rotated page has
    lines that drift, and reading them as one line each is the whole point
    -- but it is the kind of rule that gets "simplified" into comparing
    against the first box by someone who has not met a crooked scan.
    """
    drifting = [word("a", 0, 10, 0), word("b", 20, 30, 3), word("c", 40, 50, 6),
                word("d", 60, 70, 9), word("e", 80, 90, 12)]

    assert [line["text"] for line in group_words_into_lines(drifting)] == ["a b c d e"]


def test_a_single_step_past_the_tolerance_is_a_new_line():
    """The other half of the rule: without the chain, four points is two
    lines. Ordinary body text is twelve to fifteen points apart, so this
    only ever has to separate things that are genuinely close."""
    apart = [word("a", 0, 10, 0), word("b", 0, 10, 4)]

    assert [line["text"] for line in group_words_into_lines(apart)] == ["a", "b"]
