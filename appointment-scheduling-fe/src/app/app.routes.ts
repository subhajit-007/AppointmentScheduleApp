import { Routes } from '@angular/router';

import { PageNotFoundComponent } from './screens/shared/page-not-found/page-not-found.component';
import { PatientComponent } from './screens/patient/patient.component';
import { LoginComponent } from './screens/shared/login/login.component';
import { AppointmentsComponent } from './screens/shared/appointments/appointments.component';

export const routes: Routes = [
    {
        path: '',
        component: PatientComponent,
        loadChildren: () =>
            import('./screens/patient/patient.route').then((m) => m.PATIENT_ROUTE),
    },
    // {
    //     path: 'restaurant',
    //     component: RestaurantComponent,
    //     loadChildren: () =>
    //         import('./screens/restaurant/restaurant.route').then(
    //             (m) => m.RESTAURANT_ROUTE
    //         ),
    // },
    {
        path: 'appointments',
        component: AppointmentsComponent
    },
    {
        path: 'login',
        component: LoginComponent
    },
    // {
    //     path: 'signup',
    //     component: SignupComponent
    // },
    { path: '**', component: PageNotFoundComponent }, // This should be the last route
];
