import { Injectable } from '@angular/core';

import { MatDialog } from '@angular/material/dialog';
import { AlertDialogComponent } from '../../components/shared/alert-dialog/alert-dialog.component';

@Injectable({
  providedIn: 'root'
})
export class DialogService {

  constructor(private dialog: MatDialog) { }

  showAlert(title: string, message: string): void {
    this.dialog.open(AlertDialogComponent, {
      data: {
        title,
        message,
      },
    });
  }
}
