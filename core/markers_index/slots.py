# coding=utf-8
from core.publications import signals as publication


class SlotsInitializer(object):
    def __init__(self, segments_index_model):
        assert segments_index_model is not None

        self.segments_index_model = segments_index_model


    def connect_all(self):
        # slots that handle publication publication and creation
        publication.before_publish.connect(self.__add_publication_marker)

        # slots that handles publication removing and unpublishing
        publication.before_unpublish.connect(self.__remove_publication_marker)
        publication.moved_to_trash.connect(self.__remove_publication_marker)
        publication.deleted_permanent.connect(self.__remove_publication_marker)

        # slots that handles publication daily reservations updates
        publication.DailyRentSignals.booked.connect(self.__update_daily_rent_reservations_index)
        publication.DailyRentSignals.order_removed.connect(self.__update_daily_rent_reservations_index)


    def __add_publication_marker(self, sender, **kwargs):
        tid = kwargs['tid']
        hid = kwargs['hid']
        for_sale = kwargs.get('for_sale', False)
        for_rent = kwargs.get('for_rent', False)

        # Таким чином, навіть якщо оголошення одночасно подається
        # і на продаж і в оренду - воно попаде в 2 індекса одночасно.
        if for_sale:
            self.segments_index_model.add_record(tid, hid, True, False)
        if for_rent:
            self.segments_index_model.add_record(tid, hid, False, True)


    def __remove_publication_marker(self, sender, **kwargs):
        tid = kwargs['tid']
        hid = kwargs['hid']
        for_sale = kwargs.get('for_sale', False)
        for_rent = kwargs.get('for_rent', False)

        # Таким чином, навіть якщо оголошення одночасно подавалось
        # і на продаж і в оренду - воно зникне з 2х індексів одночасно.
        if for_sale:
            self.segments_index_model.remove_record(tid, hid, True, False)
        if for_rent:
            self.segments_index_model.remove_record(tid, hid, False, True)


    def __update_daily_rent_reservations_index(self, sender, **kwargs):
        tid = kwargs['tid']
        hid = kwargs['publication_id']

        self.segments_index_model.update_daily_rent_reservation_days(tid, hid)