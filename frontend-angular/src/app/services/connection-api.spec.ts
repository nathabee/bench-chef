import { TestBed } from '@angular/core/testing';

import { ConnectionApi } from './connection-api';

describe('ConnectionApi', () => {
  let service: ConnectionApi;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(ConnectionApi);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
