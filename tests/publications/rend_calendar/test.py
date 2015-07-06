from core.markers_handler.models import FlatsRentIndex

class TestFlatsRentIndex(object):

    def setup(self):
        self.publication = FlatsRentIndex()

        self.publication.hash_id = '837ba60b149c4e7d956286cdc3b4e3f6'
        self.publication.publication_id = 5
        self.publication.lat = 48.2862770650364
        self.publication.lng = 25.90572014451027
        self.publication.period_sid = 0
        self.publication.publication.price = 250
        self.publication.currency_sid = 0
        self.publication.persons_count = 1
        self.publication.family = False
        self.publication.foreigners = False
        self.publication.total_area = 40
        self.publication.floor = 4
        self.publication.floor_type_sid = 0
        self.publication.lift = False
        self.publication.hot_water = False
        self.publication.cold_water = False
        self.publication.gas = False
        self.publication.electricity = False

    def test_add_dates_rent(self):

        pass
