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
            console.log(briefId);
            for (var key in this._briefs) {
                if (this._briefs[key].id == briefId)
                    this._briefs.splice(key, 1);
            }
        }



        public get briefs() {
            return this._briefs;
        }
    }
}