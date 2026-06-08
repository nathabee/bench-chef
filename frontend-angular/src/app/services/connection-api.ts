import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

import { BackendApi } from './backend-api';

export interface ConnectionProfile {
  id: number;
  name: string;
  base_url: string;
  role_header: string;
  health_path: string;
  version_path: string;
  monitoring_path: string;
  dashboard_index_path: string;
  request_timeout_ms: number;
  enabled: boolean;
  created_at: string;
  updated_at: string;
}

export interface ProbeResult {
  id: number;
  probe_type: string;
  method: string;
  url: string;
  status_code: number | null;
  latency_ms: number | null;
  timed_out: boolean;
  success: boolean;
  error_message: string;
  response_json: unknown;
}

export interface ProbeResponse {
  connection: Pick<ConnectionProfile, 'id' | 'name' | 'base_url'>;
  probe: ProbeResult;
}

export interface DiagnosticsResponse {
  connection: Pick<ConnectionProfile, 'id' | 'name' | 'base_url'>;
  diagnostic_status: 'ONLINE' | 'DEGRADED' | 'OFFLINE';
  probes: Record<string, ProbeResult>;
}

@Injectable({
  providedIn: 'root',
})
export class ConnectionApi {
  constructor(
    private readonly http: HttpClient,
    private readonly backendApi: BackendApi,
  ) {}

  list(): Observable<ConnectionProfile[]> {
    return this.http.get<ConnectionProfile[]>(
      this.backendApi.apiUrl('/api/connections/'),
    );
  }

  runProbe(connectionId: number, probeAction: string): Observable<ProbeResponse> {
    return this.http.post<ProbeResponse>(
      this.backendApi.apiUrl(`/api/connections/${connectionId}/${probeAction}/`),
      {},
    );
  }

  runDiagnostics(connectionId: number): Observable<DiagnosticsResponse> {
    return this.http.post<DiagnosticsResponse>(
      this.backendApi.apiUrl(`/api/connections/${connectionId}/diagnostics/`),
      {},
    );
  }
}
