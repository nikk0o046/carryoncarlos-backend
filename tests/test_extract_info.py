from app.api.kiwi_output_parser import extract_info

SAMPLE_FLIGHT = {
    "cityFrom": "Madrid",
    "cityTo": "Paris",
    "duration": {"total": 9000},  # 9000s total -> 4500s avg -> 1h 15m
    "route": [{"id": 1}, {"id": 2}],  # 2 segments = 0 stopovers
    "price": 120,
    "deep_link": "https://example.com/book",
}


def test_extract_info_basic():
    response = {"currency": "EUR", "data": [SAMPLE_FLIGHT]}

    result = extract_info(response, "test-user")

    assert len(result) == 1
    flight = result[0]
    assert flight["from"] == "Madrid"
    assert flight["to"] == "Paris"
    assert flight["price"] == {"value": 120, "currency": "EUR"}
    assert flight["stop_overs"] == 0
    assert flight["booking_link"] == "https://example.com/book"


def test_extract_info_duration_calculation():
    response = {"currency": "EUR", "data": [SAMPLE_FLIGHT]}

    result = extract_info(response, "test-user")

    # total=9000 -> avg=4500 -> 1h 15m
    assert result[0]["average_duration"]["hours"] == 1.0
    assert result[0]["average_duration"]["minutes"] == 15.0


def test_extract_info_deduplicates_by_city():
    cheaper_paris = {**SAMPLE_FLIGHT, "price": 80}
    response = {"currency": "EUR", "data": [SAMPLE_FLIGHT, cheaper_paris]}

    result = extract_info(response, "test-user")

    assert len(result) == 1  # second Paris flight is dropped


def test_extract_info_empty_and_invalid_input():
    assert extract_info(None, "test-user") == []
    assert extract_info({}, "test-user") == []
    assert extract_info({"data": []}, "test-user") == []
