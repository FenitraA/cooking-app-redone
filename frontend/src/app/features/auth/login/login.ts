import { Component, inject } from '@angular/core';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { Router } from '@angular/router';

import { Auth } from '../services/auth';
import { CurrentUser } from '../../../core/services/current-user';

@Component({
  selector: 'app-login',
  imports: [ReactiveFormsModule],
  templateUrl: './login.html',
  styleUrl: './login.css'
})
export class Login {

  private readonly fb = inject(FormBuilder);
  private readonly authService = inject(Auth);
  private readonly currentUser = inject(CurrentUser);
  private readonly router = inject(Router);

  readonly form = this.fb.nonNullable.group({
    username: ['', [Validators.required]],
    password: ['', Validators.required]
  });

  loading = false;
  errorMessage = '';

  submit() {
    if (this.form.invalid) {
      this.form.markAllAsTouched();
      return;
    }

    this.loading = true;
    this.errorMessage = '';

    this.authService.login(this.form.getRawValue()).subscribe({
      next: () => {
        this.loadCurrentUser();
      },
      error: () => {
        this.loading = false;
        this.errorMessage = 'Invalid name or password.';
      }
    });
  }

  private loadCurrentUser() {
    this.authService.me().subscribe({
      next: user => {
        this.currentUser.setUser(user);
        this.loading = false;

        this.router.navigate(['/']);
      },
      error: () => {
        this.loading = false;
        this.errorMessage = 'Unable to retrieve your account.';
      }
    });
  }
}