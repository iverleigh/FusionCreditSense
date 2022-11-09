import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms'
import { Router } from '@angular/router';

@Component({
    selector: 'finclude-login',
    templateUrl: './login.component.html',
})
export class LoginComponent {
    loginForm: FormGroup;

    constructor(private formBuilder: FormBuilder, private router: Router) {
        this.loginForm = this.formBuilder.group({
            username: ['', Validators.required],
            password: ['', Validators.required],
        });
    }

    login(): void {
        if (!this.loginForm.invalid) {
            this.router.navigate(['apply']);
        }
    }
}