from core.signals import PublicationsSignals

def initialize_all_signals():
    from core.markers_handler import SegmentsIndex
    PublicationsSignals.daily_rent_added.connect(SegmentsIndex.add_daily_rent_terms)
    return
