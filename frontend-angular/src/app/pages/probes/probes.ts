import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';

import { ConnectionApi, ConnectionProfile } from '../../services/connection-api';
import {
  CameraPollingResponse,
  DashboardResponsivenessResponse,
  ProbeApi,
  RepeatProbeResponse,
} from '../../services/probe-api';

@Component({
  selector: 'app-probes',
  imports: [FormsModule],
  templateUrl: './probes.html',
  styleUrl: './probes.css',
})
export class Probes {
  connections: ConnectionProfile[] = [];
  selectedConnectionId: number | null = null;
  selectedProbeType = 'HEALTH_PROBE';
  repeatCount = 5;
  delayMs = 100;
  printerId = 'lux01';
  busy = false;
  message = '';
  result: RepeatProbeResponse | DashboardResponsivenessResponse | CameraPollingResponse | null = null;

  readonly probeTypes = [
    'HEALTH_PROBE',
    'VERSION_PROBE',
    'MONITORING_PROBE',
    'DASHBOARD_ASSET_PROBE',
  ];

  constructor(
    private readonly connectionApi: ConnectionApi,
    private readonly probeApi: ProbeApi,
  ) {
    this.connectionApi.list().subscribe({
      next: (connections) => {
        this.connections = connections;
        this.selectedConnectionId = connections[0]?.id ?? null;
      },
      error: () => {
        this.message = 'Could not load connection profiles.';
      },
    });
  }

  runRepeatProbe(): void {
    if (this.selectedConnectionId === null) {
      this.message = 'Select a connection first.';
      return;
    }

    this.busy = true;
    this.message = '';

    this.probeApi
      .repeatProbe(
        this.selectedConnectionId,
        this.selectedProbeType,
        this.repeatCount,
        this.delayMs,
      )
      .subscribe({
        next: (result) => {
          this.result = result;
          this.message = `${result.probe_type}: ${result.success_count}/${result.repeat_count} succeeded`;
          this.busy = false;
        },
        error: () => {
          this.message = 'Repeat probe failed.';
          this.busy = false;
        },
      });
  }

  runDashboardResponsiveness(): void {
    if (this.selectedConnectionId === null) {
      this.message = 'Select a connection first.';
      return;
    }

    this.busy = true;
    this.message = '';

    this.probeApi
      .dashboardResponsiveness(
        this.selectedConnectionId,
        this.repeatCount,
        this.delayMs,
      )
      .subscribe({
        next: (result) => {
          this.result = result;
          this.message = `Dashboard responsiveness: ${result.success_count}/${result.repeat_count} succeeded`;
          this.busy = false;
        },
        error: () => {
          this.message = 'Dashboard responsiveness failed.';
          this.busy = false;
        },
      });
  }

  runCameraPolling(): void {
    if (this.selectedConnectionId === null) {
      this.message = 'Select a connection first.';
      return;
    }

    this.busy = true;
    this.message = '';

    this.probeApi
      .cameraActiveJobPolling(
        this.selectedConnectionId,
        this.printerId,
        this.repeatCount,
        this.delayMs,
      )
      .subscribe({
        next: (result) => {
          this.result = result;
          this.message = `Camera polling: ${result.success_count}/${result.repeat_count} succeeded`;
          this.busy = false;
        },
        error: () => {
          this.message = 'Camera polling failed.';
          this.busy = false;
        },
      });
  }

  resultJson(): string {
    if (!this.result) {
      return '';
    }

    return JSON.stringify(this.result, null, 2);
  }
}
