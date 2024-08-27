import { Injectable } from '@angular/core';
import { AxiosService } from '../network/axios.service';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class DoctorService {
  constructor(private axiosService: AxiosService) {}

  searchDoctors(searchQuery: string = ''): Observable<any> {
    return new Observable((observer) => {
      this.axiosService
        .get(`/appointments/doctors/search/?${searchQuery}`)
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
