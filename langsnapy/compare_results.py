from langsnapy.snapshot import Snapshot

class CompareResults:
    """
        CompareResults is a class that can be used to compare the results of runs.
    """

    def __init__(self, snapshots: list[Snapshot]):
        self.snapshots = snapshots

    def _repr_html_(self):
        from langsnapy._output_format import (
            format_dict_as_ol_html
        )

        # NOTE: This assumes that all listed snapshots have the same runs in same order
        # this behavior will change in the future 

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
                    {run.result._repr_html_()}
                </td>
                '''

            html += '</tr>'
        html += '</table>'

        return html