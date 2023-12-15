# %%
from __future__ import annotations
import logging
import yaml
from datetime import datetime
from typing import Callable
from pathlib import Path
from dataclasses import dataclass
from dataclasses_json import dataclass_json

logger = logging.getLogger(__name__)


def str_presenter(dumper, data):
  if len(data.splitlines()) > 1:  # check for multiline string
    return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')
  return dumper.represent_scalar('tag:yaml.org,2002:str', data)

yaml.representer.SafeRepresenter.add_representer(str, str_presenter)


class MarkdownString(str):
    pass


@dataclass_json
@dataclass
class Case:
    inquery: str | list[str]
    meta: dict[str, any] | None = None

@dataclass_json
@dataclass
class CaseRunResult:
    result: str
    meta: dict[str, any] | None = None

    @staticmethod
    def from_any(result: str | CaseRunResult) -> CaseRunResult:
        if isinstance(result, CaseRunResult):
            return result
        
        if not isinstance(result, str):
            result = str(result)

        return CaseRunResult(result=result)
        

@dataclass_json
@dataclass
class CaseRun:
    case: Case
    result: CaseRunResult

@dataclass_json()
@dataclass
class Snapshot:
    runs: list[CaseRun]
    meta: dict[str, any] | None = None

    def to_yaml(self, stream=None) -> str | None:
        def remove_none_values(d):
            if isinstance(d, dict):
                return {k: remove_none_values(v) for k, v in d.items() if v is not None}
            elif isinstance(d, list):
                return [remove_none_values(v) for v in d]
            else:
                return d

        return yaml.safe_dump(
            remove_none_values(self.to_dict()), 
            stream, 
            default_flow_style=False,
            allow_unicode=True
        )

    @staticmethod
    def from_file(stream) -> Snapshot:
        return Snapshot.from_dict(
            yaml.safe_load(stream), 
            infer_missing=True
        )


class CompareResults:
    """
        CompareResults is a class that can be used to compare the results of runs.
    """

    def __init__(self, snapshots: list[Snapshot]):
        self.snapshots = snapshots

    def _repr_html_(self):
        from langsnapy._markdown import (
            format_markdown_as_html,
            format_dict_as_html
        )

        # NOTE: This assumes that all listed snapshots have the same runs in same order
        # this behavior will change in the future 

        html = '<table style="text-align:left;">'

        # Render meta
        html += '<tr>'
        for snapshot in self.snapshots:
            html += f'''
            <td style="text-align:left; vertical-align:top;">
                {format_dict_as_html(snapshot.meta)}
            </td>
            '''
        html += '</tr>'

        # Render runs
        num_snapshots = len(self.snapshots)
        all_runs = zip(*[s.runs for s in self.snapshots])
        for runs in all_runs:
            html += f'''<tr>
                <td style="text-align:left;" colspan="{num_snapshots}">
                    <b>Inquery: {runs[0].case.inquery}</b>
                </td>
            </tr>'''

            html += '<tr>'

            for run in runs:
                html += f'''
                <td style="text-align:left; vertical-align:top;">
                    <div data-mime-type="text/markdown" style="text-align:left; vertical-align:top;">
                        {format_markdown_as_html(run.result.result)}
                    </div>
                </td>
                '''

            html += '</tr>'
        html += '</table>'

        return html

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
            return CaseRunResult.from_any(runner(case))

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

    def compare_last_two_snapshots(self) -> CompareResults:
        snapshots = [snapshot for (_, snapshot) in self._read_snapshots()[-2:]]
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


# %%
