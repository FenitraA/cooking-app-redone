import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';

import { User } from '../../../core/models/user';
import { LoginRequest } from '../models/login-request';

@Injectable({
  providedIn: 'root'
})
export class Auth {

  private readonly http = inject(HttpClient);

  login(credentials: LoginRequest) {
    return this.http.post<void>(
      '/api/auth/login',
      credentials
    );
  }

  logout() {
    return this.http.post<void>(
      '/api/auth/logout',
      {}
    );
  }

  me() {
    return this.http.get<User>(
      '/api/auth/me'
    );
  }
}