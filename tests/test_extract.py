from ats_xray.extract import _cluster_columns, _words_to_text


def word(text, x0, x1, top):
    return {"text": text, "x0": x0, "x1": x1, "top": top, "bottom": top + 10}


def test_cluster_columns_splits_on_wide_gap():
    words = [
        word("Left", 0, 40, 0),
        word("Column", 0, 40, 12),
        word("Right", 200, 240, 0),
        word("Column", 200, 240, 12),
    ]
    columns = _cluster_columns(words, min_gap=50)
    assert len(columns) == 2
    assert {w["text"] for w in columns[0]} == {"Left", "Column"}
    assert {w["text"] for w in columns[1]} == {"Right", "Column"}


def test_cluster_columns_keeps_single_column_together():
    words = [word("Hello", 0, 40, 0), word("World", 45, 90, 0)]
    columns = _cluster_columns(words, min_gap=50)
    assert len(columns) == 1
    assert len(columns[0]) == 2


def test_cluster_columns_empty_input():
    assert _cluster_columns([]) == []


def test_words_to_text_reading_order():
    words = [
        word("World", 50, 90, 0),
        word("Hello", 0, 40, 0),
        word("Second", 0, 40, 20),
        word("Line", 45, 80, 20),
    ]
    text = _words_to_text(words)
    assert text == "Hello World\nSecond Line"


def test_naive_vs_layout_aware_two_column_interleaving():
    """This is the core bug the whole project exists to surface: a naive,
    order-blind read of a two-column page interleaves unrelated lines that
    happen to sit at the same vertical position, while column clustering
    keeps each column's content together and in order.
    """
    words = [
        word("Left1", 0, 40, 0),
        word("Right1", 200, 240, 0),
        word("Left2", 0, 40, 20),
        word("Right2", 200, 240, 20),
    ]

    naive_text = _words_to_text(words)
    assert naive_text == "Left1 Right1\nLeft2 Right2"

    columns = _cluster_columns(words, min_gap=50)
    aware_text = "\n\n".join(_words_to_text(col) for col in columns)
    assert aware_text == "Left1\nLeft2\n\nRight1\nRight2"
