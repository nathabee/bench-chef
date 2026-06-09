import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root',
})
export class BackendApi {
  private readonly config = (globalThis as {
    BenchChefConfig?: {
      backendUrl?: string;
      frontendUrl?: string;
      prometheusUrl?: string;
      grafanaUrl?: string;
      spaghettiChefUrl?: string;
    };
  }).BenchChefConfig ?? {};

  get baseUrl(): string {
    return this.config.backendUrl ?? 'http://localhost:18071';
  }

  frontendUrl(): string {
    return this.config.frontendUrl ?? 'http://localhost:18072';
  }

  apiUrl(path: string): string {
    const normalizedPath = path.startsWith('/') ? path : `/${path}`;

    return `${this.baseUrl}${normalizedPath}`;
  }

  grafanaUrl(): string {
    return this.config.grafanaUrl ?? 'http://localhost:18074';
  }

  prometheusUrl(): string {
    return this.config.prometheusUrl ?? 'http://localhost:18073';
  }

  spaghettiChefUrl(): string {
    return this.config.spaghettiChefUrl ?? 'http://localhost:18080';
  }
}
