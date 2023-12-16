from langsnapy.snapshot import Snapshot

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