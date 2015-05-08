
module pages.map {
    export interface IFiltersService {
        filters: Object

        update(filter_object: string, filter_name: string, filter_value: any): void
    }
}