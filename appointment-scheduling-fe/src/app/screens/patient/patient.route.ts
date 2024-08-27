import { Route } from '@angular/router';
import { DashboardComponent } from './dashboard/dashboard.component';
// import { customerAuthGuard } from '../../guards/customer-auth.guard';

export const PATIENT_ROUTE: Route[] = [
  { path: '', redirectTo: 'dashboard', pathMatch: 'full' },
  {
    path: 'dashboard',
    component: DashboardComponent
  },
  // {
  //   path: 'orders',
  //   loadComponent: () =>
  //     import('./orders-screen/orders-screen.component').then(
  //       (comp) => comp.OrdersScreenComponent
  //     ),
  //   canActivate: [customerAuthGuard]
  // },
  // {
  //   path: 'cart',
  //   loadComponent: () =>
  //     import('./cart-screen/cart-screen.component').then(
  //       (comp) => comp.CartScreenComponent
  //     ),
  //   canActivate: [customerAuthGuard]
  // },
];
