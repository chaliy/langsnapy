from pathlib import Path

from langsnapy.project import Project

FIXTURES_PATH = Path(__file__).parent / "fixtures"

def  test_compare_last_two_snapshots():
    prj = Project(
        snapshot_folder_path =FIXTURES_PATH / "snapshots",
    )
    compare = prj.compare_last_two_snapshots()

    assert compare.snapshots is not None
    assert len(compare.snapshots) == 2
    assert compare._repr_html_() is not None


def  test_compare_snapshots_by_run_ids():
    prj = Project(
        snapshot_folder_path =FIXTURES_PATH / "snapshots",
    )
    compare = prj.compare_snapshots_by_run_ids([
        "run-2023-12-15-00-34-12",
        "run-2023-12-15-00-34-18",
        "unknown"
    ])

    assert compare.snapshots is not None
    assert len(compare.snapshots) == 2
    assert compare._repr_html_() is not None