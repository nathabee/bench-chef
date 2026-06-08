import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root',
})
export class BackendApi {
  readonly baseUrl = 'http://localhost:18071';

  apiUrl(path: string): string {
    const normalizedPath = path.startsWith('/') ? path : `/${path}`;

    return `${this.baseUrl}${normalizedPath}`;
  }

  grafanaUrl(): string {
    return 'http://localhost:18074';
  }

  prometheusUrl(): string {
    return 'http://localhost:18073';
  }
}
