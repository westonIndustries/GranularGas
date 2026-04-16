#!/usr/bin/env python
"""Generate pipeline integration test report."""

from tests.test_pipeline_integration_property13 import generate_pipeline_integration_report

if __name__ == '__main__':
    report = generate_pipeline_integration_report()
    print(f"Report status: {report.get('status', 'generated')}")
    if report.get('status') != 'skipped':
        print(f"Report generated successfully")
        print(f"  Total rows: {report['results_summary']['total_rows']}")
        print(f"  Years: {report['results_summary']['years_count']}")
        print(f"  End-uses: {report['results_summary']['end_uses_count']}")
