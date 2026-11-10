from fastapi.testclient import TestClient


def metric_lines(client: TestClient, name: str) -> list[str]:
    response = client.get("/metrics")
    assert response.status_code == 200
    return [line for line in response.text.splitlines() if line.startswith(name + "{")]


def test_metrics_count_requests_per_route(client: TestClient, make_drop) -> None:
    drop = make_drop()
    client.get("/drops")
    client.get("/drops")
    client.get(f"/drops/{drop['id']}")

    counts = metric_lines(client, "http_requests_total")

    list_drops = [line for line in counts if 'handler="/drops"' in line and 'method="GET"' in line]
    assert len(list_drops) == 1
    assert list_drops[0].endswith(" 2.0")
    # Routes are grouped by template, not by id.
    assert any('handler="/drops/{drop_id}"' in line for line in counts)


def test_metrics_expose_the_latency_per_route(client: TestClient) -> None:
    client.get("/drops")

    durations = metric_lines(client, "http_request_duration_seconds_count")

    assert any('handler="/drops"' in line for line in durations)


def test_health_checks_and_scrapes_are_not_counted(client: TestClient) -> None:
    client.get("/health")
    client.get("/health/ready")
    client.get("/metrics")

    counts = metric_lines(client, "http_requests_total")

    assert not any("/health" in line or "/metrics" in line for line in counts)
