import time
from dataclasses import dataclass
from enum import StrEnum
from typing import Any
from urllib.parse import urljoin

import requests

from .models import ConnectionProfile


class ProbeErrorType(StrEnum):
    NONE = 'NONE'
    TIMEOUT = 'TIMEOUT'
    CONNECTION_REFUSED = 'CONNECTION_REFUSED'
    HTTP_ERROR = 'HTTP_ERROR'
    INVALID_JSON = 'INVALID_JSON'
    REQUEST_ERROR = 'REQUEST_ERROR'


def format_probe_error(
    error_type: ProbeErrorType,
    detail: str = '',
) -> str:
    if error_type == ProbeErrorType.NONE:
        return ''

    if detail:
        return f'{error_type.value}: {detail}'

    return error_type.value


@dataclass
class ProbeResult:
    method: str
    url: str
    status_code: int | None
    latency_ms: int | None
    timed_out: bool
    success: bool
    error_message: str
    response_json: dict[str, Any] | list[Any] | None


def build_url(base_url: str, path: str) -> str:
    normalized_base_url = base_url.rstrip('/') + '/'
    normalized_path = path.lstrip('/')
    return urljoin(normalized_base_url, normalized_path)


def parse_response_json(
    response: requests.Response,
    expect_json: bool,
) -> tuple[dict[str, Any] | list[Any] | None, str]:
    if not expect_json:
        return None, ''

    try:
        return response.json(), ''
    except ValueError:
        if 200 <= response.status_code < 300:
            return None, format_probe_error(
                ProbeErrorType.INVALID_JSON,
                'Response is not valid JSON',
            )

        return None, ''


def probe_get(
    connection: ConnectionProfile,
    path: str,
    expect_json: bool = True,
) -> ProbeResult:
    method = 'GET'
    url = build_url(connection.base_url, path)
    timeout_seconds = connection.request_timeout_ms / 1000

    headers = {}
    if connection.role_header:
        headers['X-SpaghettiChef-Role'] = connection.role_header

    started_at = time.perf_counter()

    try:
        response = requests.get(
            url,
            headers=headers,
            timeout=timeout_seconds,
        )

        latency_ms = int((time.perf_counter() - started_at) * 1000)

        response_json, json_error_message = parse_response_json(
            response=response,
            expect_json=expect_json,
        )

        success = 200 <= response.status_code < 300

        if not success:
            error_message = format_probe_error(
                ProbeErrorType.HTTP_ERROR,
                f'HTTP {response.status_code}',
            )
        elif json_error_message:
            success = False
            error_message = json_error_message
        else:
            error_message = format_probe_error(ProbeErrorType.NONE)

        return ProbeResult(
            method=method,
            url=url,
            status_code=response.status_code,
            latency_ms=latency_ms,
            timed_out=False,
            success=success,
            error_message=error_message,
            response_json=response_json,
        )

    except requests.Timeout:
        latency_ms = int((time.perf_counter() - started_at) * 1000)

        return ProbeResult(
            method=method,
            url=url,
            status_code=None,
            latency_ms=latency_ms,
            timed_out=True,
            success=False,
            error_message=format_probe_error(
                ProbeErrorType.TIMEOUT,
                'Request timed out',
            ),
            response_json=None,
        )

    except requests.ConnectionError:
        latency_ms = int((time.perf_counter() - started_at) * 1000)

        return ProbeResult(
            method=method,
            url=url,
            status_code=None,
            latency_ms=latency_ms,
            timed_out=False,
            success=False,
            error_message=format_probe_error(
                ProbeErrorType.CONNECTION_REFUSED,
                'Target unreachable',
            ),
            response_json=None,
        )

    except requests.RequestException as exc:
        latency_ms = int((time.perf_counter() - started_at) * 1000)

        return ProbeResult(
            method=method,
            url=url,
            status_code=None,
            latency_ms=latency_ms,
            timed_out=False,
            success=False,
            error_message=format_probe_error(
                ProbeErrorType.REQUEST_ERROR,
                str(exc),
            ),
            response_json=None,
        )


def probe_health(connection: ConnectionProfile) -> ProbeResult:
    return probe_get(connection, connection.health_path)


def probe_version(connection: ConnectionProfile) -> ProbeResult:
    return probe_get(connection, connection.version_path)


def probe_monitoring(connection: ConnectionProfile) -> ProbeResult:
    return probe_get(connection, connection.monitoring_path)


def probe_dashboard_index(connection: ConnectionProfile) -> ProbeResult:
    return probe_get(
        connection=connection,
        path=connection.dashboard_index_path,
        expect_json=False,
    )


def probe_camera_active_job(
    connection: ConnectionProfile,
    printer_id: str,
) -> ProbeResult:
    path = f'/printers/{printer_id}/camera/jobs/active'
    return probe_get(connection, path)


def probe_camera_job_progress(
    connection: ConnectionProfile,
    printer_id: str,
    camera_job_id: str,
) -> ProbeResult:
    path = f'/admin/printers/{printer_id}/camera/jobs/{camera_job_id}/progress'
    return probe_get(connection, path)


def probe_camera_job_timeline(
    connection: ConnectionProfile,
    printer_id: str,
    camera_job_id: str,
) -> ProbeResult:
    path = f'/admin/printers/{printer_id}/camera/jobs/{camera_job_id}/timeline'
    return probe_get(connection, path)
