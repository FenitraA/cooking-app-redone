import { Routes } from '@angular/router';

import { Login } from './features/auth/login/login';
import { authGuard } from './core/guards/auth-guard';

export const routes: Routes = [

  {
    path: 'login',
    component: Login
  },

  {
    path: '',
    canActivate: [authGuard],
    children: [
      {
        path: '',
        loadComponent: () =>
          import('./features/home/home')
            .then(m => m.Home)
      }
    ]
  },

  {
    path: '**',
    redirectTo: ''
  }
];