from core.se_digests_manager.models import SEIndexerQueue


def add_publication_to_grabber_queue(tid, hid):
	if not SEIndexerQueue.objects.filter(tid=tid, hid=hid)[:1]:
		SEIndexerQueue.objects.create(tid=tid, hid=hid)




def remove_publication_from_grabber_queue(tid, hash_id):
	pass



