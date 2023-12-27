from typing import Generator
from langsnapy.snapshot import Snapshot, CaseRun

class CompareResults:
    """
        CompareResults is a class that can be used to compare the results of runs.
    """

    def __init__(self, snapshots: list[Snapshot]):
        self.snapshots = snapshots

    def _get_all_runs(self) -> Generator[list[CaseRun], None, None]:
        """
        Returns all runs from all snapshots backfilling missing items.

        For two snapshots, this method does some magic with difflib, attempting to
        find changes based on the inquiry matching.
        """
        if not self.snapshots or len(self.snapshots) == 0:
            return

        if len(self.snapshots) == 2:
            from difflib import SequenceMatcher

            a = [r.case.inquiry for r in self.snapshots[0].runs]
            b = [r.case.inquiry for r in self.snapshots[1].runs]

            cruncher = SequenceMatcher(None, a, b)
            for tag, alo, ahi, blo, bhi in cruncher.get_opcodes():
                if tag == 'replace':
                    raise ValueError('Error when sorting Snapshots, cannot do replace yet :(')
                elif tag == 'delete':
                    for i in range(alo, ahi):
                        yield [self.snapshots[0].runs[i], None]
                elif tag == 'insert':
                    for i in range(blo, bhi):
                        yield [None, self.snapshots[1].runs[i]]
                elif tag == 'equal':
                    for runs in zip(self.snapshots[0].runs[alo:ahi], self.snapshots[1].runs[blo:bhi]):
                        yield runs
                else:
                    raise ValueError('Error when sorting Snapshots, unknown tag %r' % (tag,))
        else:
            for runs in zip(*[s.runs for s in self.snapshots]):
                yield runs


    def _repr_html_(self):
        from langsnapy._output_format import (
            format_dict_as_ol_html
        )

        html = '<table style="text-align:left; width: 100%; table-layout: fixed">'

        # Render meta
        html += '<tr>'
        for snapshot in self.snapshots:
            html += f'''
            <td style="text-align:left; vertical-align:top;">
                {format_dict_as_ol_html(snapshot.meta)}
            </td>
            '''
        html += '</tr>'

        # Render runs
        num_snapshots = len(self.snapshots)
        all_runs = list(self._get_all_runs())
        for runs in all_runs:
            inquiry = next(r.case.inquiry for r in runs if r)
            html += f'''<tr>
                <td style="text-align:left;" colspan="{num_snapshots}">
                    <b>Inquiry: {inquiry}</b>
                </td>
            </tr>'''

            html += '<tr>'

            for run in runs:
                html += f'''
                <td style="text-align:left; vertical-align:top;">
                    {run.result._repr_html_() if run else 'N/A'}
                </td>
                '''

            html += '</tr>'
        html += '</table>'

        return html


    def _repr_markdown_(self):
        from langsnapy._output_format import (
            format_dict_as_ol_html
        )

        md = ''

        # Render meta
        md += '|' + '|'.join(' <!-- --> ' for s in self.snapshots) + '|\n'
        md += '|' + '|'.join(' -------- ' for s in self.snapshots) + '|\n'
        md += '|' + '|'.join(format_dict_as_ol_html(s.meta) for s in self.snapshots) + '|\n'
        
        # Render runs
        all_runs = list(self._get_all_runs())
        for runs in all_runs:
            inquiry = next(r.case.inquiry for r in runs if r)
            md += f'#### Inquiry: {inquiry}\n'

            md += '|' + '|'.join(' <!-- --> ' for s in self.snapshots) + '|\n'
            md += '|' + '|'.join(' -------- ' for s in self.snapshots) + '|\n'

            md += '|' + '|'.join(r.result._repr_html_() if r else 'N/A' for r in runs) + '|\n'

        return md