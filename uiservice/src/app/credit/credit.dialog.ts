import { Component, Inject } from '@angular/core';
import { MatDialog, MAT_DIALOG_DATA } from '@angular/material/dialog';


export interface DialogData {
    customerID: string;
}


@Component({
    selector: 'finclude-credit-apply-dialog',
    templateUrl: './credit.dialog.html',
})
export class CreditApplicationDialog {
    constructor(@Inject(MAT_DIALOG_DATA) public data: DialogData) {}
}
