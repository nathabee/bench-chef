import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

import { BackendApi } from './backend-api';

export interface ReportRecord {
  id: number;
  title: string;
  report_type: 'BENCHMARK' | 'PROBE' | 'SYSTEM' | 'SUMMARY';
  status: 'CREATED' | 'GENERATING' | 'READY' | 'FAILED';
  output_format: 'JSON' | 'CSV' | 'MARKDOWN' | 'HTML';
  file_path: string;
  message: string;
  created_at: string;
  updated_at: string;
}

@Injectable({
  providedIn: 'root',
})
export class ReportApi {
  constructor(
    private readonly http: HttpClient,
    private readonly backendApi: BackendApi,
  ) {}

  list(): Observable<ReportRecord[]> {
    return this.http.get<ReportRecord[]>(
      this.backendApi.apiUrl('/api/report-records/'),
    );
  }
}
