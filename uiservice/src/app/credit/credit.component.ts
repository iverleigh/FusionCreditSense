import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms'
import { BehaviorSubject } from 'rxjs';
import { MatDialog } from '@angular/material/dialog';

import { CreditService } from './credit.service';
import { CreditApplicationDialog } from "./credit.dialog";


@Component({
    selector: 'finclude-credit-application',
    templateUrl: './credit.component.html',
})
export class CreditApplicationComponent implements OnInit {
    private loadingSubject = new BehaviorSubject<boolean>(true);
    private banksSubject = new BehaviorSubject<any>([]);
    private credibilitySubject = new BehaviorSubject<number>(null);
    private predictionSubject = new BehaviorSubject<string>(null);
    private customerSubject = new BehaviorSubject<string>(null);
    private messageSubject = new BehaviorSubject<string>(null);

    public loading$ = this.loadingSubject.asObservable();
    public banks$ = this.banksSubject.asObservable();
    public credibility$ = this.credibilitySubject.asObservable();
    public prediction$ = this.predictionSubject.asObservable();
    public customer$ = this.customerSubject.asObservable();
    public message$ = this.messageSubject.asObservable();

    private clientInitialDetails: any;
    private bankInitialDetails: any;

    clientDetailsForm: FormGroup;
    bankDetailsForm: FormGroup;

    private customerID: string;
    private loanAmount: string;

    constructor(private formBuilder: FormBuilder, private creditService: CreditService, public dialog: MatDialog) {
        this.clientDetailsForm = this.formBuilder.group({
            clientName: ['', Validators.required],
            clientAge: ['', Validators.required],
            company: ['', Validators.required],
        });
        this.clientInitialDetails = this.clientDetailsForm.value;
        
        this.bankDetailsForm = this.formBuilder.group({
            bankName: ['', Validators.required],
            accountNumber: ['', Validators.required],
            sortCode: ['', Validators.required],
        });
        this.bankInitialDetails = this.bankDetailsForm.value;
    }

    ngOnInit(): void {
    }

    onStepChange(event: any): void {
        if (event.selectedIndex == 1) {
            // Step 2 - Get banks
            this.getBanks();
        } else if (event.selectedIndex == 2) {
            // Step 3 - Get results
            this.checkHistory();
        }
    }

    getBanks(): void {
        var company = this.clientDetailsForm.value.company;
        this.loadingSubject.next(true);
        this.bankDetailsForm.disable();

        this.creditService.getBanks(company).subscribe(
            result => {
                this.bankDetailsForm.enable();
                this.loadingSubject.next(false);
                this.banksSubject.next(result);

                console.log("Result:");
                console.log(result);
            },
            error => {
                this.bankDetailsForm.enable();
                this.loadingSubject.next(false);

                console.error(error);
            }
        )
    }

    checkHistory(): void {
        var company = this.clientDetailsForm.value.company;
        var name = this.clientDetailsForm.value.clientName;
        var details = this.bankDetailsForm.value;
        this.credibilitySubject.next(null);
        this.predictionSubject.next(null);
        this.messageSubject.next(null);
        this.loadingSubject.next(true);

        this.creditService.checkHistory(company, details.accountNumber, details.sortCode).subscribe(
            result => {
                this.credibilitySubject.next(result.score);
                this.predictionSubject.next(result.credit_line);
                this.loadingSubject.next(false);

                this.loanAmount = result.credit_line;

                console.log("Result:");
                console.log(result);

                this.getCustomer(company, name);
            },
            error => {
                console.error(error);
                this.loadingSubject.next(false);
            },
        );
    }

    getCustomer(company: string, name: string): void {
        this.loadingSubject.next(true);

        this.creditService.FFDCCustomer(company, name).subscribe(
            result => {
                console.log("FFDC Customer Result:");
                console.log(result);

                if (!result.success && result.message) {
                    this.messageSubject.next(result.message);
                    this.loadingSubject.next(false);
                } else {
                    this.customerSubject.next(result.customer.customerId);
                    this.customerID = result.customer.customerId;
                    // this.listLoans(company, this.customerID);
                    this.loadingSubject.next(false);
                }
            },
            error => {
                console.error(error);
                this.loadingSubject.next(false);
            }
        );
    }

    listLoans(company: string, customerID: string): void {
        var account = this.bankDetailsForm.value.accountNumber;

        this.creditService.FFDCLoans(company, customerID, this.loanAmount, account).subscribe(
            result => {
                this.loadingSubject.next(false);

                console.log("FFDC List Loans Result:");
                console.log(result);

                if (!result.success && result.message) {
                    this.messageSubject.next(result.message);
                } else {
                    console.log("OK!")
                }
            },
            error => {
                console.error(error);
                this.loadingSubject.next(false);
            }
        );
    }

    apply(): void {
        const dialogRef = this.dialog.open(CreditApplicationDialog, {
            data: {
                customerID: this.customerID,
            }
        });

        dialogRef.afterClosed().subscribe(result => {});
    }

    reset(): void {
        if (this.loadingSubject.getValue()) {
            // Don't reset while we're loading
            return;
        }

        this.clientDetailsForm.reset(this.clientInitialDetails);
        this.bankDetailsForm.reset(this.bankInitialDetails);
        this.credibilitySubject.next(null);
        this.predictionSubject.next(null);
        this.messageSubject.next(null);
        this.customerSubject.next(null);
    }
}