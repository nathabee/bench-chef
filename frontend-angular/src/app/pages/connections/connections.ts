import { Component } from '@angular/core';

import {
  ConnectionApi,
  ConnectionProfile,
  DiagnosticsResponse,
  ProbeResponse,
} from '../../services/connection-api';

@Component({
  selector: 'app-connections',
  imports: [],
  templateUrl: './connections.html',
  styleUrl: './connections.css',
})
export class Connections {
  connections: ConnectionProfile[] = [];
  loading = true;
  errorMessage = '';
  actionMessage = '';
  busyConnectionId: number | null = null;
  latestResult: ProbeResponse | DiagnosticsResponse | null = null;

  readonly probeActions = [
    { label: 'Health', action: 'test-health' },
    { label: 'Version', action: 'test-version' },
    { label: 'Monitoring', action: 'test-monitoring' },
    { label: 'Dashboard', action: 'test-dashboard-index' },
  ];

  constructor(private readonly connectionApi: ConnectionApi) {
    this.refresh();
  }

  refresh(): void {
    this.loading = true;
    this.errorMessage = '';

    this.connectionApi.list().subscribe({
      next: (connections) => {
        this.connections = connections;
        this.loading = false;
      },
      error: () => {
        this.errorMessage = 'Could not load connection profiles.';
        this.loading = false;
      },
    });
  }

  runProbe(connection: ConnectionProfile, action: string): void {
    this.busyConnectionId = connection.id;
    this.actionMessage = '';

    this.connectionApi.runProbe(connection.id, action).subscribe({
      next: (result) => {
        this.latestResult = result;
        this.actionMessage = `${result.probe.probe_type}: ${result.probe.success ? 'success' : 'failed'}`;
        this.busyConnectionId = null;
      },
      error: () => {
        this.actionMessage = 'Probe request failed.';
        this.busyConnectionId = null;
      },
    });
  }

  runDiagnostics(connection: ConnectionProfile): void {
    this.busyConnectionId = connection.id;
    this.actionMessage = '';

    this.connectionApi.runDiagnostics(connection.id).subscribe({
      next: (result) => {
        this.latestResult = result;
        this.actionMessage = `Diagnostics: ${result.diagnostic_status}`;
        this.busyConnectionId = null;
      },
      error: () => {
        this.actionMessage = 'Diagnostics request failed.';
        this.busyConnectionId = null;
      },
    });
  }

  resultJson(): string {
    if (!this.latestResult) {
      return '';
    }

    return JSON.stringify(this.latestResult, null, 2);
  }
}
