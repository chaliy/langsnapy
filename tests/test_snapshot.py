from langsnapy import Snapshot, Case, CaseRun, CaseRunResult

def test_snapshot_to_yaml():
    snapshot = Snapshot([
        CaseRun(
            Case(inquiry='question 1'),
            CaseRunResult(result='result 1')
        ),
        CaseRun(
            Case(inquiry='question 2'),
            CaseRunResult(result="""result 2
            result 2 line 2""")
        )
    ])

    yaml = snapshot.to_yaml()

    assert yaml is not None
    assert "question 1" in yaml
    assert "question 2" in yaml
    assert "result 1" in yaml
    assert "result 2 line 2" in yaml
    
def test_snapshot_repr():
    snapshot = Snapshot([
        CaseRun(
            Case(inquiry='question 1'),
            CaseRunResult(result='result 1 1')
        ),
        CaseRun(
            Case(inquiry='question 2'),
            CaseRunResult(result='result 2 1')
        )
    ])

    html = snapshot._repr_html_()

    assert html is not None
    assert "question 1" in html
    assert "question 2" in html
    assert "result 2 1" in html

    md = snapshot._repr_markdown_()

    assert md is not None
    assert "question 1" in md
    assert "question 2" in md
    assert "result 2 1" in md


def test_snapshot_repr_empty():
    snapshot = Snapshot([])

    html = snapshot._repr_html_()

    assert html is not None

    md = snapshot._repr_markdown_()

    assert md is not None
