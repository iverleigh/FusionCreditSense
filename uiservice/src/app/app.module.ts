import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { FlexLayoutModule } from '@angular/flex-layout';
import { HttpClientModule } from '@angular/common/http';
import { ReactiveFormsModule } from '@angular/forms'

import { MaterialModule } from './material/material.module';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { LoaderComponent } from './common/loader.component';

import { LoginComponent } from './login/login.component';
import { CreditApplicationComponent } from './credit/credit.component';
import { CreditApplicationDialog } from "./credit/credit.dialog";


@NgModule({
    declarations: [
        AppComponent,
        CreditApplicationComponent,
        CreditApplicationDialog,
        LoaderComponent,
        LoginComponent,
    ],
    exports: [
        MaterialModule,
    ],
    imports: [
        // Core Angular modules
        AppRoutingModule,
        BrowserModule,
        BrowserAnimationsModule,
        FlexLayoutModule,
        HttpClientModule,
        ReactiveFormsModule,

        // Material module
        MaterialModule,
    ],
    providers: [],
    bootstrap: [AppComponent]
})
export class AppModule { }
