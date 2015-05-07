


module pages.map {
    'use strict';

    export class FiltersService {
        private _filters: Object = {
            map: {
                c: null,    // city
                l: null,    // lat_lng
                v: null,    // viewport
                z: null     // zoom
            },
            panels: {
                red: {
                    t_sid: 1
                }
            }
        };

        constructor() {
            this._filters['map']['z'] = 6;
            this._filters['map']['l'] = "48.455935,34.41285";
        }



        //get map() {
        //    return this._filters[0]['map'];
        //}
        public mapp(map_filter: any) {
            console.log(map_filter.c)

            this._filters['map'][map_filter[0]] = map_filter[1];
            console.log(this._filters)
        }

        get panels() {
            return this._filters['panels'];
        }
    }
}