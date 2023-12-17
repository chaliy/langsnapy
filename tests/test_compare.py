from pathlib import Path
from unittest.mock import patch
from datetime import datetime

from langsnapy.project import Project
from langsnapy.snapshot import Snapshot


FIXTURES_PATH = Path(__file__).parent / "fixtures"

def  test_compare_last_two_snapshots():
    prj = Project()

    with patch.object(prj, '_read_snapshots', return_value=[
        ("run-2023-12-15-00-00-00",Snapshot([], meta={"time_stamp": datetime(2023, 12, 15)})),
        ("run-2023-12-11-00-00-00", Snapshot([], meta={"time_stamp": datetime(2023, 12, 11)})),
        ("run-2023-12-13-00-00-00",Snapshot([], meta={"time_stamp": datetime(2023, 12, 13)})),
        ("run-2023-12-10-00-00-00",Snapshot([], meta={"time_stamp": datetime(2023, 12, 10)})),
    ]):
        compare = prj.compare_last_two_snapshots()

        assert compare.snapshots is not None
        assert len(compare.snapshots) == 2
        assert compare.snapshots[0].meta["time_stamp"] == datetime(2023, 12, 13)
        assert compare.snapshots[1].meta["time_stamp"] == datetime(2023, 12, 15)


def test_compare_last_two_snapshots_prefix():
    prj = Project()

    with patch.object(prj, '_read_snapshots', return_value=[
        ("prefix1-2023-12-15-00-34-12", Snapshot([], meta={"time_stamp": datetime(2023, 12, 15, 0, 34, 12)})),
        ("prefix2-2023-12-15-00-34-18",Snapshot([], meta={"time_stamp": datetime(2023, 12, 15, 0, 34, 18)})),
    ]):
        compare = prj.compare_last_two_snapshots(prefix="prefix1")

        assert compare.snapshots is not None
        assert len(compare.snapshots) == 1


def  test_compare_last_two_snapshots_e2e():
    prj = Project(
        snapshot_folder_path=FIXTURES_PATH / "snapshots",
    )
    compare = prj.compare_last_two_snapshots()

    assert compare.snapshots is not None
    assert len(compare.snapshots) == 2
    assert compare._repr_html_() is not None


def  test_compare_snapshots_by_run_ids():
    prj = Project(
        snapshot_folder_path=FIXTURES_PATH / "snapshots",
    )
    compare = prj.compare_snapshots_by_run_ids([
        "run-2023-12-15-00-34-12",
        "run-2023-12-15-00-34-18",
        "unknown"
    ])

    assert compare.snapshots is not None
    assert len(compare.snapshots) == 2
    assert compare._repr_html_() is not None