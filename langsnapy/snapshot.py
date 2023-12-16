from __future__ import annotations

from dataclasses import dataclass
from dataclasses_json import dataclass_json
from yaml.dumper import SafeDumper

@dataclass
class Case:
    inquery: str | list[str]
    meta: dict[str, any] | None = None

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

@dataclass
class CaseRun:
    case: Case
    result: CaseRunResult

class _SnapshotYamlDumper(SafeDumper):
    @staticmethod 
    def str_literal_presenter(dumper, data):
        if len(data.splitlines()) > 1:
            # for multiline string
            return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')
        return dumper.represent_scalar('tag:yaml.org,2002:str', data)

_SnapshotYamlDumper.add_representer(str, _SnapshotYamlDumper.str_literal_presenter)

@dataclass_json()
@dataclass
class Snapshot:
    runs: list[CaseRun]
    meta: dict[str, any] | None = None

    def to_yaml(self, stream=None) -> str | None:
        import yaml
        def remove_none_values(d):
            if isinstance(d, dict):
                return {k: remove_none_values(v) for k, v in d.items() if v is not None}
            elif isinstance(d, list):
                return [remove_none_values(v) for v in d]
            else:
                return d

        return yaml.dump(
            remove_none_values(self.to_dict()), 
            stream,
            Dumper=_SnapshotYamlDumper,
            default_flow_style=False,
            allow_unicode=True
        )

    @staticmethod
    def from_file(stream) -> Snapshot:
        import yaml
        return Snapshot.from_dict(
            yaml.safe_load(stream), 
            infer_missing=True
        )