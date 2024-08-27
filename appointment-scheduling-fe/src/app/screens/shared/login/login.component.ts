import { Component, signal } from '@angular/core';
import { AuthService } from '../../../services/shared/auth.service';
import { STRINGS } from '../../../configs/strings';
import { FormGroup, FormControl, Validators, ReactiveFormsModule } from '@angular/forms';
import { MatButtonModule } from '@angular/material/button';
import { MatLabel, MatFormFieldModule } from '@angular/material/form-field';
import { MatIconModule } from '@angular/material/icon';
import { MatInputModule } from '@angular/material/input';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatCardModule } from '@angular/material/card';
import { ActivatedRoute, Router, RouterModule } from '@angular/router';
import { CommonModule } from '@angular/common';
import { DialogService } from '../../../services/shared/dialog.service';


const MatModules = [
  MatToolbarModule,
  MatLabel,
  MatFormFieldModule,
  MatInputModule,
  MatButtonModule,
  MatIconModule,
  MatCardModule,
];

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [...MatModules, ReactiveFormsModule, RouterModule, CommonModule],
  templateUrl: './login.component.html',
  styleUrl: './login.component.scss'
})
export class LoginComponent {
  // strings to show in the component
  appStrings: any = STRINGS;

  loginForm = new FormGroup({
    username: new FormControl('', [Validators.required]),
    password: new FormControl('', [Validators.required])
  })

  hide = signal(true);

  constructor(private authService: AuthService, private router: Router, private dialogService: DialogService, private route: ActivatedRoute) {
  }

  clickEvent(event: MouseEvent) {
    this.hide.set(!this.hide());
    event.stopPropagation();
  }

  get username() {
    return this.loginForm.get('username')
  }

  get password() {
    return this.loginForm.get('password')
  }

  login() {
    const payload = {
      username: this.username?.value ?? '',
      password: this.password?.value,
    };
    // console.log(payload);
    this.authService.login(payload).subscribe({
      next: (res) => {
        // console.log("Res from api ===> \n", res)
        localStorage.setItem('role', `${res?.role}`)
        this.dialogService.showAlert('Success', "Login Successful");
        // Add checks for any return url else got to home page
        this.route.queryParams.subscribe(params => {
          const returnUrl = params['returnUrl'] || '/';
          this.router.navigate([returnUrl]);
        });
      },
      error: (err) => { 
        console.error(err)
        // alert(err.error.message) 
      }
    })
  }
}
