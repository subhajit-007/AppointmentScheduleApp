import { ChangeDetectorRef, Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { NavigationEnd, Router, RouterModule } from '@angular/router';


import { MatToolbarModule } from '@angular/material/toolbar';
import { MatFormFieldModule, MatLabel } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';

import { STRINGS } from '../../../configs/strings';
import { Observable, of } from 'rxjs';
import { AuthService } from '../../../services/shared/auth.service';
import { DialogService } from '../../../services/shared/dialog.service';



const MatModules = [
  MatToolbarModule,
  MatLabel,
  MatFormFieldModule,
  MatInputModule,
  MatButtonModule,
  MatIconModule,
];

@Component({
  selector: 'app-navbar',
  standalone: true,
  imports: [...MatModules, RouterModule, CommonModule],
  templateUrl: './navbar.component.html',
  styleUrl: './navbar.component.scss'
})
export class NavbarComponent {

  // strings to show in the component
  appStrings: any = STRINGS;

  role: string = '';

  isAuthScreen: boolean = false;

  isUserLoggedIn$: Observable<boolean> = of(false);

  // isUserLoggedIn: boolean = false;

  constructor(
    private router: Router,
    private changes: ChangeDetectorRef,
    private authService: AuthService,
    private dialogService: DialogService
  ) { }

  ngOnInit(): void {
    this.router.events.subscribe((event) => {
      if (event instanceof NavigationEnd) {
        this.checkIfAuthScreen(event.urlAfterRedirects);
      }
    });
    this.isLoggedIn();
  }

  ngAfterViewInit(): void {
    this.checkIfAuthScreen(this.router.url);
  }

  checkIfAuthScreen(url: string): void {
    const regexForAuthUrl = /(\/login|\/signup)/g;
    let matchFoundArr = url.match(regexForAuthUrl) ?? []
    this.isAuthScreen = matchFoundArr.length >= 1;
    this.role = this.authService.getUserRole() ?? "";
    this.changes.detectChanges();
  }

  // Checks user logged in or not
  isLoggedIn(): void {
    this.isUserLoggedIn$ = this.authService.isLoggedIn();
    // this.authService.isLoggedIn().subscribe({
    //   next: (res: any) => {
    //     console.log("logged in status: ", res)
    //     this.isUserLoggedIn = res
    //   },
    //   error: (err: any) => {
    //     console.error(err)
    //     this.isUserLoggedIn = false
    //   }
    // });
  }

  getToken(): string | null {
    return localStorage.getItem("Authorization");
  }

  logout() {
    this.authService.logout().subscribe({
      next: (res: any) => {
        // console.log("Logout response => \n", res)
        this.dialogService.showAlert("Success", "User Logged Out Successfully")
      },
      error: (err: any) => {
        console.error("Logout error => \n", err)
        this.dialogService.showAlert("Error", "Something went wrong !")
      }
    }
    )
  }

  // if user is "customer" and logged in then only show cart option
  isUserPateint(): boolean {
    return this.role === 'patient';
  }
}
