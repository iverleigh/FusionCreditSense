import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';


@Injectable({
    providedIn: 'root'
})
export class CreditService {
    // Edge Service URL
    private readonly API_URL = "http://" + location.href.split("/")[2].split(":")[0] + ":8000/api/";

    // Open Banking API Credentials
    private readonly username = 'phil';
    private readonly password = 'Password01';

    constructor(
        private http: HttpClient
    ) {}

    buildURL(call: string): string {
        return this.API_URL + call
    }

    buildParams(company: string): HttpParams {
        // company = testing2

        return new HttpParams()
        .set('username', this.username)
        .set('password', this.password)
        .set('company', company);
    }

    getBanks(company: string): Observable<any> {
        var url = this.buildURL('banks');
        var queryParams = this.buildParams(company);

        return this.http.get(url, { params: queryParams });
    }

    checkHistory(company: string, accountNumber: string, sortCode: string): Observable<any> {
        var url = this.buildURL('checkhistory');
        var queryParams = this.buildParams(company)
            .set('accountNumber', accountNumber)
            .set('sortCode', sortCode);

        return this.http.get(url, { params: queryParams });
    }

    predictCredit(company: string, accountReference: string): Observable<any> {
        var url = this.buildURL('predictcredit');
        var queryParams = this.buildParams(company)
            .set('accountReference', accountReference);

        return this.http.get(url, { params: queryParams });
    }

    FFDCCustomer(company: string, name: string): Observable<any> {
        var url = this.buildURL('ffdc/customer');
        var queryParams = this.buildParams(company)
            .set('name', name);
        return this.http.get(url, { params: queryParams });
    }

    FFDCLoans(company: string, customerID: string, amount: string, account: string): Observable<any> {
        var url = this.buildURL('ffdc/loans');
        var queryParams = this.buildParams(company)
            .set('customer_id', customerID)
            .set('loan_amount', amount)
            .set('account', account);
        return this.http.get(url, { params: queryParams });
    }
}