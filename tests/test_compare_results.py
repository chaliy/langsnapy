from langsnapy import Snapshot, Case, CaseRun, CaseRunResult
from langsnapy.compare_results import CompareResults

def test_compare_results_repr():
    runs = [
        Snapshot([
            CaseRun(
                Case(inquiry='question 1'),
                CaseRunResult(result='result 1 1')
            ),
            CaseRun(
                Case(inquiry='question 2'),
                CaseRunResult(result='result 2 1')
            )
        ]),
        Snapshot([
            CaseRun(
                Case(inquiry='question 1'),
                CaseRunResult(result='result 1 2')
            ),
            CaseRun(
                Case(inquiry='question 2'),
                CaseRunResult(result='result 2 2')
            )
        ])
    ]

    compare_results = CompareResults(runs)

    html = compare_results._repr_html_()

    assert html is not None
    assert "question 1" in html
    assert "question 2" in html
    assert "result 2 1" in html
    assert "result 2 2" in html

    md = compare_results._repr_markdown_()

    assert md is not None
    assert "question 1" in md
    assert "question 2" in md
    assert "result 2 1" in md
    assert "result 2 2" in md


def test_compare_results_repr_empty():
    runs = []

    compare_results = CompareResults(runs)

    html = compare_results._repr_html_()

    assert html is not None

    md = compare_results._repr_markdown_()

    assert md is not None


def test_compare_results_repr_three_cases():
    runs = [
        Snapshot([
            CaseRun(
                Case(inquiry='question 1'),
                CaseRunResult(result='result 1 1')
            ),
            CaseRun(
                Case(inquiry='question 2'),
                CaseRunResult(result='result 2 1')
            )
        ]),
        Snapshot([
            CaseRun(
                Case(inquiry='question 1'),
                CaseRunResult(result='result 1 2')
            ),
            CaseRun(
                Case(inquiry='question 2'),
                CaseRunResult(result='result 2 2')
            )
        ]),
        Snapshot([
            CaseRun(
                Case(inquiry='question 1'),
                CaseRunResult(result='result 1 3')
            ),
            CaseRun(
                Case(inquiry='question 2'),
                CaseRunResult(result='result 2 3')
            )
        ])
    ]

    compare_results = CompareResults(runs)

    html = compare_results._repr_html_()

    assert html is not None
    assert "question 2" in html
    assert "result 1 1" in html
    assert "result 2 2" in html
    assert "result 2 3" in html

    md = compare_results._repr_markdown_()

    assert md is not None
    assert "question 2" in md
    assert "result 1 1" in md
    assert "result 2 2" in md
    assert "result 2 3" in md

def test_compare_results_repr_new_case():
    runs = [
        Snapshot([
            CaseRun(
                Case(inquiry='question 1'),
                CaseRunResult(result='result 1 1')
            )
        ]),
        Snapshot([
            CaseRun(
                Case(inquiry='question 1'),
                CaseRunResult(result='result 1 2')
            ),
            CaseRun(
                Case(inquiry='question 2'),
                CaseRunResult(result='result 2 2')
            )
        ])
    ]

    compare_results = CompareResults(runs)

    html = compare_results._repr_html_()

    assert html is not None
    assert "question 2" in html
    assert "result 2 2" in html

    md = compare_results._repr_markdown_()

    assert md is not None
    assert "question 2" in md
    assert "result 2 2" in md
    