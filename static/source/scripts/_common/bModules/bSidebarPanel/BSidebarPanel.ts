/// <reference path='_references.ts' />

module bModules.bSidebarPanel {

    var bSidebarPanel: angular.IModule = angular.module('bModules.bSidebarPanel', ['ui.router']);

    bSidebarPanel.directive('BSidebarPanel', BSidebarPanel);
}