from pathlib import Path

from snuppy import Project

FIXTURES_PATH = Path(__file__).parent / "fixtures"

def  test_compare_last_two_runs():
    prj = Project(
        snapshot_folder_path =FIXTURES_PATH / "snapshots",
    )
    compare = prj.compare_last_two_runs()

    assert compare.snapshots is not None
    assert len(compare.snapshots) == 2
    assert compare._repr_html_() is not None