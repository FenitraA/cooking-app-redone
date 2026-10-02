import { HttpErrorResponse, HttpInterceptorFn } from '@angular/common/http';
import { inject } from '@angular/core';
import { catchError, switchMap, throwError } from 'rxjs';

import { Refresh } from '../services/refresh';

export const authInterceptor: HttpInterceptorFn = (req, next) => {

  const refresh = inject(Refresh);

  return next(req).pipe(

    catchError((error: HttpErrorResponse) => {

      if (error.status !== 401) {
        return throwError(() => error);
      }

      return refresh.refresh().pipe(

        switchMap(() => {
          return next(req);
        }),

        catchError(refreshError => {
          return throwError(() => refreshError);
        })
      );
    })
  );
};