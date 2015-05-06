/// <reference path='_references.ts' />


module modules.Panels {
    export interface IDropPanelsHandler {
        open(panel_name: string, state?: number): void
        close(panel_name: string): void
        isOpened(panel_name: string): boolean
    }
}