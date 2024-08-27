import { Component, Inject } from '@angular/core';
import { MatDialogModule, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { MatButtonModule } from '@angular/material/button';


@Component({
  selector: 'app-alert-dialog',
  standalone: true,
  imports: [MatDialogModule, MatButtonModule],
  templateUrl: './alert-dialog.component.html',
  styleUrl: './alert-dialog.component.scss'
})
export class AlertDialogComponent {
  constructor(@Inject(MAT_DIALOG_DATA) public data: { title: string; message: string }) { }
}
