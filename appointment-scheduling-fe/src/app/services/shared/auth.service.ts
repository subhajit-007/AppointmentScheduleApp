// import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';
import { environment } from '../../../environments/environment';
import { AxiosService } from '../network/axios.service';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private apiUrl = environment.apiUrl;
  private tokenKey = environment.tokenKey;
  private loggedIn = new BehaviorSubject<boolean>(false);

  constructor(private axiosService: AxiosService) { }

  isLoggedIn(): Observable<boolean> {
    // return this.checkTokenValidity(token);
    const token = this.getToken();
    if (token) {
      this.loggedIn.next(true);
    }
    return this.loggedIn.asObservable();
  }

  login(credentials: any): Observable<any> {
    return new Observable(observer => {
      this.axiosService.post('/auth/login/', credentials).then(response => {
        localStorage.setItem('Authorization', `Token ${response.data?.token}`);
        this.loggedIn.next(true);
        observer.next(response.data);
        observer.complete();
      }).catch(error => {
        observer.error(error);
      });
    });
  }

  logout(): Observable<any> {
    return new Observable(observer => {
      this.axiosService.post('/auth/logout/', {}).then(response => {
        localStorage.removeItem('Authorization');
        this.loggedIn.next(false);
        observer.next(response.data);
        observer.complete();
      }).catch(error => {
        observer.error(error);
      });
    });
  }


  getToken(): string | null {
    return localStorage.getItem(this.tokenKey);
  }

  getUserRole(): string | null {
    // Get user role from locastorage
    return localStorage.getItem(environment.roleKey);
  }
}
