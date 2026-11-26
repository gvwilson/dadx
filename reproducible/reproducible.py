# mccole:dodo
def task_make_data():
    """Generate the raw CSV files."""
    return {
        "actions": ["python bin/make_data.py"],
        "targets": ["data/records.csv", "data/events.csv"],
    }

def task_report():
    """Build the report from the data and the analysis script."""
    return {
        "file_dep": ["bin/script.py", "data/*.csv"],
        "targets": ["report.html"],
        "actions": ["python bin/script.py"],
    }
# mccole:/dodo
