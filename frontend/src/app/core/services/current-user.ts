import { Injectable, signal } from '@angular/core';

import { User } from '../models/user';

@Injectable({
  providedIn: 'root'
})
export class CurrentUser {

  private readonly _user = signal<User | null>(null);

  readonly user = this._user.asReadonly();

  setUser(user: User) {
    this._user.set(user);
  }

  clearUser() {
    this._user.set(null);
  }
}