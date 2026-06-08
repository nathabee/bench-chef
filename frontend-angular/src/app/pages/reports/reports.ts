import { Component } from '@angular/core';
import { DatePipe } from '@angular/common';

import { ReportApi, ReportRecord } from '../../services/report-api';

@Component({
  selector: 'app-reports',
  imports: [DatePipe],
  templateUrl: './reports.html',
  styleUrl: './reports.css',
})
export class Reports {
  reports: ReportRecord[] = [];
  loading = true;
  errorMessage = '';

  constructor(private readonly reportApi: ReportApi) {
    this.refresh();
  }

  refresh(): void {
    this.loading = true;
    this.errorMessage = '';

    this.reportApi.list().subscribe({
      next: (reports) => {
        this.reports = reports;
        this.loading = false;
      },
      error: () => {
        this.errorMessage = 'Could not load report records.';
        this.loading = false;
      },
    });
  }

  statusCount(status: ReportRecord['status']): number {
    return this.reports.filter((report) => report.status === status).length;
  }

  typeCount(reportType: ReportRecord['report_type']): number {
    return this.reports.filter((report) => report.report_type === reportType).length;
  }
}
