import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { MatButtonModule } from '@angular/material/button';
import { MatDividerModule } from '@angular/material/divider';
import { MatLabel } from '@angular/material/form-field';
import { MatListModule } from '@angular/material/list';
import { MatToolbarModule } from '@angular/material/toolbar';
import { RouterModule, Router } from '@angular/router';
import { DoctorService } from '../../../services/doctor/doctor.service';
import { AppointmentsService } from '../../../services/shared/appointments.service';
import { AuthService } from '../../../services/shared/auth.service';
import { AlertConfirmDialogComponent } from '../../../components/shared/alert-confirm-dialog/alert-confirm-dialog.component';
import { DialogService } from '../../../services/shared/dialog.service';
import { Title } from '@angular/platform-browser';

const MatModules = [
  MatToolbarModule,
  MatLabel,
  // MatFormFieldModule,
  // MatInputModule,
  MatButtonModule,
  // MatIconModule,
  MatListModule,
  MatDividerModule,
];

@Component({
  selector: 'app-appointments',
  standalone: true,
  imports: [...MatModules, RouterModule, CommonModule],
  templateUrl: './appointments.component.html',
  styleUrl: './appointments.component.scss',
})
export class AppointmentsComponent {
  appointmentList: any[] = [];
  role: string = '';

  constructor(
    private appointmentsService: AppointmentsService,
    private authService: AuthService,
    private router: Router,
    private dialogServce: DialogService
  ) {}

  ngOnInit(): void {
    this.role = this.authService.getUserRole() ?? '';
    this.appointmentsService.fetchDoctorsAppointments().subscribe({
      next: (res) => {
        // console.log(res.data);
        this.appointmentList = res.data;
      },
      error: (err) => {
        console.error(err);
      },
    });
  }

  setStatusToAttended(): void {
    console.log('Attended');
  }
  setStatusToCancel(): void {
    console.log('Canceled');
  }

  showActions(): void {
    this.dialogServce.showConfirmAlert(
      'Update Appointment',
      'Choose option to update appointment status',
      this.setStatusToAttended,
      this.setStatusToCancel
    );
  }
}
