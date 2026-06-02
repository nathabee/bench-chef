import { ComponentFixture, TestBed } from '@angular/core/testing';

import { Probes } from './probes';

describe('Probes', () => {
  let component: Probes;
  let fixture: ComponentFixture<Probes>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [Probes],
    }).compileComponents();

    fixture = TestBed.createComponent(Probes);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
