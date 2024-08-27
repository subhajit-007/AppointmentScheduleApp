import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AlertConfirmDialogComponent } from './alert-confirm-dialog.component';

describe('AlertConfirmDialogComponent', () => {
  let component: AlertConfirmDialogComponent;
  let fixture: ComponentFixture<AlertConfirmDialogComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [AlertConfirmDialogComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(AlertConfirmDialogComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
