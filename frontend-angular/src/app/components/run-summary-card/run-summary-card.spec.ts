import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RunSummaryCard } from './run-summary-card';

describe('RunSummaryCard', () => {
  let component: RunSummaryCard;
  let fixture: ComponentFixture<RunSummaryCard>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [RunSummaryCard],
    }).compileComponents();

    fixture = TestBed.createComponent(RunSummaryCard);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
