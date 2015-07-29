/// <reference path='../_all.ts' />


module Mappino.Map {
    'use strict';

    export class BriefsService {

        private _briefs = [];

        public static $inject = [
            '$rootScope'
        ];

        constructor(private $rootScope: angular.IRootScopeService) {
            // ---------------------------------------------------------------------------------------------------------

        }


        public add(brief: Object) {
            this._briefs.push(brief);
        }



        public remove(briefId: string) {
            for (var key in this._briefs) {
                if (this._briefs[key].id == briefId)
                    this._briefs.splice(this._briefs[key], 1);
            }
        }



        public get briefs() {
            return this._briefs;
        }
    }
}