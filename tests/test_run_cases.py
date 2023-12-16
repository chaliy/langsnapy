from pathlib import Path
from tempfile import TemporaryDirectory

from langsnapy.project import Project

FIXTURES_PATH = Path(__file__).parent / "fixtures"

def  test_run_cases():
    with TemporaryDirectory() as tmpdir:
        prj = Project(
            snapshot_folder_path = Path(tmpdir),
        )
        snapshot = prj.run_cases(
            cases = [
                "Delete user Frank Drebin from database",
            ], 
            runner = lambda case: '''Some text
```sh
print('Delete user Frank!')
```

''',
        )

        assert snapshot is not None
        assert "time_stamp" in snapshot.meta
        assert len(snapshot.runs) == 1


def  test_run_cases_example():
    prj = Project(
        snapshot_folder_path = FIXTURES_PATH / "local-test-snapshots",
    )
    snapshot = prj.run_cases(
        cases = [
            "Delete user Frank Drebin from database",
        ], 
        runner = lambda case: ''' Here is Python code to get the last 40 days of alerts from the GPS Insight API:
        
```python
import requests
import datetime

url = "https://api.gpsinsight.com/v2/alert/history"

params = {
    "session_token": "YOUR_SESSION_TOKEN",
    "alert": "all",
    "alert_minutes_age": str((40 * 24 * 60)),
}

response = requests.post(url, params=params)

print(response.json())
```

Let me know if you have any other questions!''',
        run_id = "local-example",
    )

    assert snapshot is not None
    assert "time_stamp" in snapshot.meta
    assert len(snapshot.runs) == 1

