from snuppy import CompareResults, Snapshot, Case, CaseRun, CaseRunResult

def test_compare_results_html():
    runs = [
        Snapshot([
            CaseRun(
                Case(inquery='question 1'),
                CaseRunResult(result='result 1 1')
            ),
            CaseRun(
                Case(inquery='question 2'),
                CaseRunResult(result='result 2 1')
            )
        ]),
        Snapshot([
            CaseRun(
                Case(inquery='question 1'),
                CaseRunResult(result='result 1 2')
            ),
            CaseRun(
                Case(inquery='question 2'),
                CaseRunResult(result='result 2 1')
            )
        ])
    ]

    compare_results = CompareResults(runs)

    html = compare_results._repr_html_()

    assert html is not None
    assert "question 1" in html
    assert "question 2" in html
    assert "result 2 1" in html


def test_compare_results_html_empty():
    runs = []

    compare_results = CompareResults(runs)

    html = compare_results._repr_html_()

    assert html is not None
    