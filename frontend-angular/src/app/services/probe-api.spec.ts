import { TestBed } from '@angular/core/testing';

import { ProbeApi } from './probe-api';

describe('ProbeApi', () => {
  let service: ProbeApi;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(ProbeApi);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
