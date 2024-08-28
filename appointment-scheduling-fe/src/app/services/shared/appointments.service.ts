import { Injectable } from '@angular/core';
import { AxiosService } from '../network/axios.service';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class AppointmentsService {

  constructor(private axiosService: AxiosService) { }

  fetchAllAppointments(): Observable<any>{
    return new Observable((observer) => {
      this.axiosService
        .get(`/appointments/`)
        .then((response) => {
          observer.next(response.data);
          observer.complete();
        })
        .catch((error) => {
          observer.error(error);
        });
    });
  }

  fetchDoctorsAppointments(): Observable<any>{
    return new Observable((observer) => {
      this.axiosService
        .get(`/appointments/doctor/`)
        .then((response) => {
          observer.next(response.data);
          observer.complete();
        })
        .catch((error) => {
          observer.error(error);
        });
    });
  }

}
