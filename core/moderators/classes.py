#coding=utf-8
from core import redis_connections


class RedisHandler(object):
    __redis = redis_connections['steady']
    __prefix = 'moderators_pubs_check_queue'
    __splitter = ':'


    @classmethod
    def all_bound_publications(cls):
        keys = cls.__redis.keys(cls.__prefix + '*')

        publications = []
        for key in keys:
            _, moderator_id, publication_tid, publication_hash_id = key.split(cls.__splitter)
            publications.append(
                (publication_tid, publication_hash_id, moderator_id, ) # note: cortege here
            )

        return set(publications)


    @classmethod
    def publications_bound_by_moderator(cls, moderator):
        prefix = ''.join(
            cls.publication_key(moderator, '', '').split(cls.__splitter)[:2])


        keys = cls.__redis.keys(prefix + '*')

        publications = []
        for key in keys:
            _, moderator_id, publication_tid, publication_hash_id = key.split(cls.__splitter)
            publications.append(
                (publication_tid, publication_hash_id, moderator_id, ) # note: cortege here
            )

        return set(publications)


    @classmethod
    def publication_key(cls, moderator, tid, hash_id):
        return '{prefix}{splitter}{moderator_id}{splitter}{tid}{splitter}{hash_id}'.format(
            prefix=cls.__prefix, splitter=cls.__splitter, moderator_id=moderator.id, tid=tid, hash_id=hash_id)


    @classmethod
    def bind_to_the_moderator(cls, moderator, tid, hash_id):
        key = cls.publication_key(moderator, tid, hash_id)
        timeout = 60*60*24 # seconds, one day
        cls.__redis.setex(key, timeout, 'bound')


    @classmethod
    def unbind_from_the_moderator(cls, moderator, tid, hash_id):
        key = cls.publication_key(moderator, tid, hash_id)
        cls.__redis.delete(key)