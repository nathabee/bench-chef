import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

import { BackendApi } from './backend-api';
import { ConnectionProfile, ProbeResult } from './connection-api';

export interface LatencySummary {
  count: number;
  min_latency_ms: number | null;
  max_latency_ms: number | null;
  average_latency_ms: number | null;
  p50_latency_ms?: number | null;
  p95_latency_ms?: number | null;
  p99_latency_ms?: number | null;
}

export interface ErrorSummary {
  failure_count: number;
  errors: Record<string, number>;
}

export interface RepeatProbeResponse {
  connection: Pick<ConnectionProfile, 'id' | 'name' | 'base_url'>;
  probe_type: string;
  repeat_count: number;
  delay_ms: number;
  success_count: number;
  failure_count: number;
  latency: LatencySummary;
  samples: ProbeResult[];
}

export interface DashboardResponsivenessResponse {
  connection: Pick<ConnectionProfile, 'id' | 'name' | 'base_url'>;
  repeat_count: number;
  delay_ms: number;
  success_count: number;
  failure_count: number;
  success_rate: number;
  latency: LatencySummary;
}

export interface CameraPollingResponse {
  connection: Pick<ConnectionProfile, 'id' | 'name' | 'base_url'>;
  printer_id: string;
  repeat_count: number;
  delay_ms: number;
  success_count: number;
  failure_count: number;
  latency: LatencySummary;
  snapshot_points: Array<{
    sample_id: number;
    latestSnapshotId: string | number | null;
    latestCaptureAt: string | null;
  }>;
}

@Injectable({
  providedIn: 'root',
})
export class ProbeApi {
  constructor(
    private readonly http: HttpClient,
    private readonly backendApi: BackendApi,
  ) {}

  latencySummary(probeType = ''): Observable<LatencySummary> {
    let params = new HttpParams();

    if (probeType) {
      params = params.set('probe_type', probeType);
    }

    return this.http.get<LatencySummary>(
      this.backendApi.apiUrl('/api/probe-samples/latency-summary/'),
      { params },
    );
  }

  errorSummary(): Observable<ErrorSummary> {
    return this.http.get<ErrorSummary>(
      this.backendApi.apiUrl('/api/probe-samples/error-summary/'),
    );
  }

  repeatProbe(
    connectionId: number,
    probeType: string,
    repeatCount: number,
    delayMs: number,
  ): Observable<RepeatProbeResponse> {
    return this.http.post<RepeatProbeResponse>(
      this.backendApi.apiUrl(`/api/connections/${connectionId}/repeat-probe/`),
      {
        probe_type: probeType,
        repeat_count: repeatCount,
        delay_ms: delayMs,
      },
    );
  }

  dashboardResponsiveness(
    connectionId: number,
    repeatCount: number,
    delayMs: number,
  ): Observable<DashboardResponsivenessResponse> {
    return this.http.post<DashboardResponsivenessResponse>(
      this.backendApi.apiUrl(`/api/connections/${connectionId}/dashboard-responsiveness/`),
      {
        repeat_count: repeatCount,
        delay_ms: delayMs,
      },
    );
  }

  cameraActiveJobPolling(
    connectionId: number,
    printerId: string,
    repeatCount: number,
    delayMs: number,
  ): Observable<CameraPollingResponse> {
    return this.http.post<CameraPollingResponse>(
      this.backendApi.apiUrl(`/api/connections/${connectionId}/camera-active-job-polling/`),
      {
        printer_id: printerId,
        repeat_count: repeatCount,
        delay_ms: delayMs,
      },
    );
  }
}
