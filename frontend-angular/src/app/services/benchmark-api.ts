import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

import { BackendApi } from './backend-api';

export interface BenchmarkRun {
  id: number;
  name: string;
  scenario_name: string;
  status: 'CREATED' | 'QUEUED' | 'RUNNING' | 'COMPLETED' | 'FAILED' | 'CANCELLED';
  target_base_url: string;
  started_at: string | null;
  finished_at: string | null;
  message: string;
  created_at: string;
  updated_at: string;
}

@Injectable({
  providedIn: 'root',
})
export class BenchmarkApi {
  constructor(
    private readonly http: HttpClient,
    private readonly backendApi: BackendApi,
  ) {}

  list(): Observable<BenchmarkRun[]> {
    return this.http.get<BenchmarkRun[]>(
      this.backendApi.apiUrl('/api/benchmark-runs/'),
    );
  }
}
