/// <reference path='../_references.ts' />


module mappino.main.map {
    export interface IPanelsHandler {
        open(panel_name: string): void
        close(panel_name: string): void
        isOpened(panel_name: string): boolean
    }
}