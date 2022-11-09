import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { CreditApplicationComponent } from './credit/credit.component';
import { LoginComponent } from './login/login.component';


const routes: Routes = [
    {
        path: '',
        redirectTo: 'login',
        pathMatch: 'full',
    },
    {
        path: 'login',
        component: LoginComponent,
        data: {
            title: 'Login',
        }
    },
    {
        path: 'apply',
        component: CreditApplicationComponent,
        data: {
            title: 'Credit Application',
        }
    },
    {
        // Unknown routes - redirect to application screen
        path: "**",
        redirectTo: 'apply',
    },
];


@NgModule({
    imports: [RouterModule.forRoot(routes)],
    exports: [RouterModule]
})
export class AppRoutingModule { }
