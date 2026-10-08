from legalease.response_parser import ensure_final_report, parse_json_response


def test_parse_json_response_from_fenced_block():
    parsed = parse_json_response('```json\n{"short_summary": "Done"}\n```')
    assert parsed["short_summary"] == "Done"


def test_ensure_final_report_adds_defaults():
    report = ensure_final_report({"short_summary": "A"})
    assert report["short_summary"] == "A"
    assert "disclaimer" in report
