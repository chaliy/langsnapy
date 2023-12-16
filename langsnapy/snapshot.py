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

    def add_meta(self, key: str, value: any):
        self.meta = self.meta or {}
        self.meta[key] = value

    def _repr_html_(self):
        from langsnapy._output_format import (
            format_markdown_as_html,
            format_dict_as_div_html
        )

        html = ''

        html += f'''
            <div style="text-align:left; vertical-align:top;">
                {format_markdown_as_html(self.result)}
            </div>
        '''

        if self.meta:
            html += format_dict_as_div_html(self.meta)

        return html

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

    def _repr_html_(self):
        from langsnapy._output_format import (
            format_dict_as_ol_html
        )

        html = '<table style="text-align:left;">'

        # Render meta
        html += f'''<tr>
            <td style="text-align:left; vertical-align:top;">
                {format_dict_as_ol_html(self.meta)}
            </td>'''

        # Render runs
        for run in self.runs:
            html += f'''<tr>
                <td style="text-align:left;">
                    <b>Inquery: {run.case.inquery}</b>
                </td>
            </tr>'''

            html += f'''<tr>
                <td style="text-align:left; vertical-align:top;">
                    {run.result._repr_html_()}
                </td>
            </tr>'''
        html += '</table>'

        return html

    @staticmethod
    def from_file(stream) -> Snapshot:
        import yaml
        return Snapshot.from_dict(
            yaml.safe_load(stream), 
            infer_missing=True
        )