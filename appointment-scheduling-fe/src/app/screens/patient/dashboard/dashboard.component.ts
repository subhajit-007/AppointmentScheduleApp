import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';

import { MatButtonModule } from '@angular/material/button';
import { MatFormFieldModule, MatLabel } from '@angular/material/form-field';
import { MatToolbarModule } from '@angular/material/toolbar';
import { RouterModule, Router } from '@angular/router';
import { MatListModule } from '@angular/material/list';
import { MatDividerModule } from '@angular/material/divider';
import { DoctorService } from '../../../services/doctor/doctor.service';
import { MatInputModule } from '@angular/material/input';
import { MatIconModule } from '@angular/material/icon';
import { FormControl, ReactiveFormsModule } from '@angular/forms';


const MatModules = [
  MatToolbarModule,
  MatLabel,
  MatFormFieldModule,
  MatInputModule,
  MatButtonModule,
  MatIconModule,
  MatListModule,
  MatDividerModule,
];
@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [...MatModules, RouterModule, CommonModule, ReactiveFormsModule],
  templateUrl: './dashboard.component.html',
  styleUrl: './dashboard.component.scss'
})
export class DashboardComponent {
  doctorsNameList: any[] = [];

  searchText = new FormControl('')

  constructor(private doctorService: DoctorService, private router: Router) { }

  ngOnInit(): void {
    this.doctorService.searchDoctors().subscribe({
      next: (res) => {
        // console.log(res.data);
        this.doctorsNameList = res.data;
      },
      error: (err) => {
        console.error(err)
      }
    })
  }

  goToDoctorDetailPage(doctorId: any): void {
    this.router.navigate([`/doctor/${doctorId}/details`])
  }

  searchDoctors(): void {
    console.log(this.searchText.value)
    const searchQuery = `specialty=${this.searchText.value}`
    this.doctorService.searchDoctors(searchQuery).subscribe({
      next: (res) => {
        // console.log(res.data);
        this.doctorsNameList = res.data;
      },
      error: (err) => {
        console.error(err)
      }
    })
  }
}
