/// <reference path='../_all.ts' />


module Mappino.Cabinet {
    export interface IPublicationsService {

        /**
         * Create publication
         */
        create(publicationNew: IPublicationNew, successCallback?: IPublicationCreateSuccessCallback, errorCallback?: IPublicationBaseCallback): void


        /**
         * Remove publication
         */
        remove(publicationIds: IPublicationIds, successCallback?: IPublicationBaseCallback, errorCallback?: IPublicationBaseCallback): void


        /**
         * Publish publication
         */
        publish(publicationIds: IPublicationIds, successCallback?: IPublicationBaseCallback, errorCallback?: IPublicationBaseCallback): void


        /**
         * Load publication data
         */
        load(publicationIds: IPublicationIds, successCallback?: IPublicationLoadSuccessCallback, errorCallback?: IPublicationBaseCallback): void


        /**
         * Upload publication photo
         */
        uploadPhoto(publicationIds: IPublicationIds, photo: File, successCallback?: IPublicationUploadPhotoSuccessCallback, errorCallback?: IPublicationBaseCallback): void


        /**
         * Remove publication photo
         */
        removePhoto(publicationIds: IPublicationIds, photoId: string|number, successCallback?: IPublicationRemovePhotoSuccessCallback, errorCallback?: IPublicationBaseCallback): void


        /**
         * Set publication title photo
         */
        setTitlePhoto(publicationIds: IPublicationIds, photoId: string|number, successCallback?: IPublicationBaseCallback, errorCallback?: IPublicationBaseCallback): void


        /**
         * Set publication title photo
         */
        checkField(publicationIds: IPublicationIds, field: IPublicationCheckField, successCallback?: IPublicationCheckFieldSuccessCallback, errorCallback?: IPublicationBaseCallback): void


        /**
         * Load publications brief
         */
        loadBriefs(successCallback?: IPublicationLoadBriefsSuccessCallback, errorCallback?: IPublicationBaseCallback): void
    }





    /**
     * Success create publication callback
     * @callback Mappino.Cabinet.PublicationService~IPublicationCreateSuccessCallback
     * @param {object} response         Response object
     * @param {number} response.code    Server error code
     * @param {string} response.message Server error message
     * @param {string} response.data    Response data
     * @returns {void}
     */
    export interface IPublicationCreateSuccessCallback {
        (response: { code: number; message: string; data: { id: string } }): void
    }



    /**
     * Success remove publication callback
     * @callback Mappino.Cabinet.PublicationService~IPublicationRemoveSuccessCallback
     * @param {number} ticketId
     * @returns {void}
     */
    export interface IPublicationRemoveSuccessCallback {
        (tickets: ITicket[]): void
    }



    /**
     * Success publication data callback
     * @callback Mappino.Cabinet.PublicationService~IPublicationLoadSuccessCallback
     * @param {IPublication} publication
     * @returns {void}
     */
    export interface IPublicationLoadSuccessCallback {
        (publication: IPublication): void
    }



    /**
     * Success upload publication photo callback
     * @callback Mappino.Cabinet.PublicationService~IPublicationUploadPhotoSuccessCallback
     * @param {IPublicationPhoto} publicationPhoto
     * @returns {void}
     */
    export interface IPublicationUploadPhotoSuccessCallback {
        (publicationPhoto: IPublicationPhoto): void
    }



    /**
     * Success remove publication photo callback
     * @callback Mappino.Cabinet.PublicationService~IPublicationRemovePhotoSuccessCallback
     * @param {string|number} hashId hash_id of next title photo if not null
     * @returns {void}
     */
    export interface IPublicationRemovePhotoSuccessCallback {
        (hashId?: string|number): void
    }



    /**
     * Success check publication field callback
     * @callback Mappino.Cabinet.PublicationService~IPublicationCheckFieldSuccessCallback
     * @param {string|number} fieldValue New value of publication field
     * @returns {void}
     */
    export interface IPublicationCheckFieldSuccessCallback {
        (fieldValue: string|number): void
    }



    /**
     * Success load publications brief callback
     * @callback Mappino.Cabinet.PublicationService~IPublicationLoadBriefsSuccessCallback
     * @param {string|number} fieldValue New value of publication field
     * @returns {void}
     */
    export interface IPublicationLoadBriefsSuccessCallback {
        (briefs: Array<IBrief>): void
    }




    /**
     * Base callback
     * @callback Mappino.Cabinet.PublicationService~IPublicationBaseCallback
     * @param {object} response         Response object
     * @param {number} response.code    Server error code
     * @param {string} response.message Server error message
     * @returns {void}
     */
    export interface IPublicationBaseCallback {
        (response: { code: number; message: string }): void
    }
}