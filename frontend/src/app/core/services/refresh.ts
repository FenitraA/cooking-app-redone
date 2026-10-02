import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class Refresh {

  private readonly http = inject(HttpClient);

  refresh() {
    return this.http.post<void>(
      '/api/auth/refresh',
      {}
    );
  }
}