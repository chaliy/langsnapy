from __future__ import annotations

import logging
from datetime import datetime
from typing import Callable
from pathlib import Path

from langsnapy.compare_results import CompareResults
from langsnapy.snapshot import Snapshot, Case, CaseRun, CaseRunResult

logger = logging.getLogger(__name__)

class Project:

    def __init__(self, snapshot_folder_path: Path = Path("./snapshots")):
        self.snapshot_folder_path = snapshot_folder_path

    def run_cases(
        self,
        cases: list[Case], 
        runner: Callable[[Case], CaseRunResult | str],
        meta: dict[str, any] | None = None,
        prefix: str = "run",
        run_id: str | None = None,
        dry_run: bool = False,
    ) -> Snapshot:
        time_stamp = datetime.now()

        def run_case(case: Case) -> CaseRunResult:
            time_start = datetime.now()
            run_result = CaseRunResult.from_any(runner(case))
            run_result.add_meta("duration (sec)", int((datetime.now() - time_start).total_seconds()))
            return run_result

        snapshot = Snapshot(
            runs=[CaseRun(c, run_case(c)) for c in cases]
        )

        snapshot.meta = {
            "time_stamp": time_stamp
        }
        if meta:
            snapshot.meta.update(meta)

        if not dry_run:
            output_folder = self.snapshot_folder_path

            time_stamp_str = time_stamp.strftime("%Y-%m-%d-%H-%M-%S")
            run_id = run_id or f"{prefix}-{time_stamp_str}"
            output_path = output_folder / f"{run_id}-snapshot.yaml"
            logger.info(f"Writing snapshot to {output_path}")
            output_folder.mkdir(parents=True, exist_ok=True)
            with open(output_path, "w") as f:
                snapshot.to_yaml(f)
        else:
            print(snapshot.to_yaml())

        return snapshot

    def _read_snapshot(self, path: Path) -> Snapshot:
        with open(path, "r") as f:
            return Snapshot.from_file(f)

    def _read_snapshots(self) -> list[(str, Snapshot)]:
        def get_run_id(path: Path) -> str:
            return path.name.replace("-snapshot.yaml", "")

        return [
            (get_run_id(path), self._read_snapshot(path))
            for path in self.snapshot_folder_path.glob("*.yaml")
        ]

    def compare_last_two_snapshots(self, prefix: str = None) -> CompareResults:
        """
        Compares the last two snapshots in the snapshot folder.

        param prefix: If specified, only snapshots with the given prefix will be considered.
        """

        all_snapshots = [
            snapshot 
            for (_, snapshot) in self._read_snapshots() 
            if prefix is None or _.startswith(prefix)
        ]
        all_snapshots.sort(key=lambda snapshot: snapshot.meta.get("time_stamp", datetime.min), reverse=True)
        
        snapshots = all_snapshots[:2]
        snapshots.reverse()
        
        return CompareResults(snapshots)

    def compare_snapshots(self, snapshots: list[Snapshot]) -> CompareResults:
        return CompareResults(snapshots)

    def compare_snapshots_by_run_ids(self, run_ids: list[str]) -> CompareResults:
        index = {run_id: snapshot for (run_id, snapshot) in self._read_snapshots()}
        snapshots = [
            index[run_id] 
            for run_id in run_ids 
            if run_id in index
        ]
        return CompareResults(snapshots)

