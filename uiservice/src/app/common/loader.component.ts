import { Component, Input } from '@angular/core';

@Component({
    selector: 'finclude-loader',
    templateUrl: './loader.component.html',
    styleUrls: ['./loader.component.scss']
})
export class LoaderComponent {
    private _radius: number = 80;
    private _inner: number = 64;
    private _thickness: number = 6;
    private _margin: number = 8;

    @Input()
    get radius(): number { return this._radius; }
    set radius(value: number) {
        this._radius = value;
        this._inner = value * 0.8;
    }

    @Input()
    get thickness(): number { return this._thickness; }
    set thickness(value: number) {
        if (typeof value === 'string') {
            // Despite expecting this to be a number, we may in fact have a
            // string
            this._thickness = parseInt(value);
        } else {
            this._thickness = value;
        }
        this._margin = this._thickness + 2;
    }

    get margin(): number { return this._margin; }

    get inner(): number { return this._inner; }
}