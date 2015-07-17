#coding=utf-8
import datetime
import redis_lock

from django.db.utils import DatabaseError
from django.core.exceptions import ObjectDoesNotExist, SuspiciousOperation
from django.db import models, transaction
from django.utils.timezone import now

from collective.utils import generate_sha256_unique_id
from collective.exceptions import InvalidArgument, RuntimeException
from core import redis_connections
from core.users.models import Users
from core.publications.handlers import PublicationsPhotosHandler
from core.currencies import currencies_manager as currencies
from core.currencies.constants import CURRENCIES as currencies_constants
from core.publications import models_signals
from core.publications.constants import OBJECT_STATES, SALE_TRANSACTION_TYPES, LIVING_RENT_PERIODS, COMMERCIAL_RENT_PERIODS
from core.publications.exceptions import EmptyCoordinates, EmptyTitle, EmptyDescription, EmptySalePrice, \
    EmptyRentPrice


class AbstractModel(models.Model):
    class Meta:
        abstract = True

    #-- constraints
    max_price_symbols_count = 18

    @classmethod
    def new(cls):
        return cls.objects.create()

    @classmethod
    def by_id(cls, record_id):
        return cls.objects.filter(id=record_id)


    def print_price(self):
        if self.price is None:
            return u''

        dol = u'{:,.2f}'.format(currencies.convert(self.price, self.currency_sid, currencies_constants.dol()))
        dol = dol.replace(',', ' ')

        # Видалення копійок
        if dol[-3] == '.':
            dol = dol[:-3]

        # Підказуємо користувачу, що валюта сконвертована
        if self.currency_sid != currencies_constants.dol():
            dol = u'~' + dol

        dol += u' дол.'
        if self.transaction_sid == SALE_TRANSACTION_TYPES.for_square_meter():
            dol += u'/м²'

        if self.is_contract:
            dol += u', договорная'


        # Додаємо ціну в інших валютах
        uah = u'{:,.2f}'.format(currencies.convert(self.price, self.currency_sid, currencies_constants.uah()))
        uah = uah.replace(',', ' ')

        if uah[-3] == '.':
            uah = uah[:-3]

        if self.currency_sid != currencies_constants.uah():
            uah = u'~' + uah
        uah += u' грн.'
        if self.transaction_sid == SALE_TRANSACTION_TYPES.for_square_meter():
            uah += u'/м²'


        eur = u'{:,.2f}'.format(currencies.convert(self.price, self.currency_sid, currencies_constants.eur()))
        eur = eur.replace(',', ' ')

        if eur[-3] == '.':
            eur = eur[:-3]

        if self.currency_sid != currencies_constants.eur():
            eur = u'~' + eur
        eur += u' евро.'
        if self.transaction_sid == SALE_TRANSACTION_TYPES.for_square_meter():
            eur += u'/м²'

        return u'{dol} ({uah}, {eur})'.format(dol=dol, uah=uah, eur=eur)


    def print_add_terms(self):
        if self.add_terms is None:
            return u''
        return self.add_terms



class AbstractHeadModel(models.Model):
    class Meta:
        abstract = True

    #-- override
    tid = None
    body = None
    sale_terms = None
    rent_terms = None
    photos_model = None

    #-- fields
    #
    # hash_id використовується для передачі ссилок на клієнт.
    # Передача id у відкритому вигляді небезпечна тим, що:
    #   * полегшує повний перебір записів з таблиці по інкременту, а значить — полегшує ddos.
    #   * відкриває внутрішню структуру таблиць в БД і наяні зв’язки.
    hash_id = models.TextField(unique=True, default=generate_sha256_unique_id)
    owner = models.ForeignKey(Users)


    state_sid = models.SmallIntegerField(default=OBJECT_STATES.unpublished(), db_index=True)
    for_sale = models.BooleanField(default=False)
    for_rent = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    published = models.DateTimeField(null=True)
    deleted = models.DateTimeField(null=True)
    actual = models.DateTimeField(null=True)

    #-- map coordinates
    degree_lat = models.TextField(null=True)
    degree_lng = models.TextField(null=True)

    segment_lat = models.TextField(null=True)
    segment_lng = models.TextField(null=True)

    pos_lat = models.TextField(null=True)
    pos_lng = models.TextField(null=True)
    address = models.TextField(null=True)


    @classmethod
    def new(cls, owner, for_sale=False, for_rent=False):
        model = cls.objects.create(
            body_id = cls._meta.get_field_by_name('body')[0].rel.to.new().id,
            sale_terms_id = cls._meta.get_field_by_name('sale_terms')[0].rel.to.new().id,
            rent_terms_id = cls._meta.get_field_by_name('rent_terms')[0].rel.to.new().id,

            owner = owner,
            for_sale = for_sale,
            for_rent = for_rent,
            state_sid = OBJECT_STATES.unpublished(),
        )

        # По сигналу про створення запису відбувається оновлення індексу маркерів та
        # запускається індексація запису в sphinx.
        models_signals.created.send(
            sender=None, tid=cls.tid, hid=model.id, hash_id=model.hash_id, for_sale=for_sale, for_rent=for_rent)

        return model


    @classmethod
    def by_id(cls, head_id, select_body=False, select_sale=False, select_rent=False, select_owner=False):
        try:
            query = cls.objects.filter(id = head_id).only('id')
            if select_body:
                query = query.only('id', 'body').select_related('body')
            if select_sale:
                query = query.only('id', 'sale_terms').select_related('sale_terms')
            if select_rent:
                query = query.only('id', 'rent_terms').select_related('rent_terms')
            if select_owner:
                query = query.only('id', 'owner').select_related('owner')
            return query[:1][0]
        except IndexError:
            raise ObjectDoesNotExist()


    @classmethod
    def by_hash_id(cls, head_id, select_body=False, select_sale=False, select_rent=False, select_owner=False):
        try:
            query = cls.objects.filter(hash_id = head_id).only('id')

            if select_body:
                query = query.only('id', 'body').select_related('body')
            if select_sale:
                query = query.only('id', 'sale_terms').select_related('sale_terms')
            if select_rent:
                query = query.only('id', 'rent_terms').select_related('rent_terms')
            if select_owner:
                query = query.only('id', 'owner').select_related('owner')
            return query[:1][0]

        except IndexError:
            raise ObjectDoesNotExist()


    @classmethod
    def by_user_id(cls, user_id, select_body=False, select_sale=False, select_rent=False, select_owner=False):
        query = cls.objects.filter(owner_id = user_id).only('id')
        if select_body:
            query = query.select_related('body')
        if select_sale:
            query = query.select_related('sale_terms')
        if select_rent:
            query = query.select_related('rent_terms')
        if select_owner:
            query = query.select_related('owner')
        return query


    @classmethod
    def all_published(cls):
        return cls.objects.filter(state_sid=OBJECT_STATES.published())


    def set_lat_lng(self, lat_lng):
        if not lat_lng or lat_lng is None:
            # clearing the coordinates
            self.degree_lat = self.degree_lng = None
            self.segment_lat = self.segment_lng = None
            self.pos_lat = self.pos_lng = None
            self.save(force_update=True)
            return

        splitter = ';'
        if not splitter in lat_lng:
            raise InvalidArgument('lat_lng doesnt contains ')

        lat, lng = lat_lng.split(splitter)
        if (not lat) or (not lng): # lat & lng are strings, it's OK
            raise ValueError()

        if len(lat) <= 6:
            raise ValueError()
        if len(lng) <= 6:
            raise ValueError()

        lat = lat.replace(',', '.')
        lng = lng.replace(',', '.')
        degree_lat, pos_part_lat = lat.split('.')
        degree_lng, pos_part_lng = lng.split('.')

        if abs(int(degree_lat) > 90):
            raise ValueError()
        if abs(int(degree_lng) > 180):
            raise ValueError()

        segment_lat = pos_part_lat[:2]
        segment_lng = pos_part_lng[:2]
        pos_lat = pos_part_lat[2:]
        pos_lng = pos_part_lng[2:]

        # check for int
        try:
            int(segment_lat)
            int(segment_lng)
            int(pos_lat)
            int(pos_lng)
        except:
            raise InvalidArgument()

        self.degree_lat = degree_lat
        self.degree_lng = degree_lng
        self.segment_lat = segment_lat
        self.segment_lng = segment_lng
        self.pos_lat = pos_lat
        self.pos_lng = pos_lng
        self.save(force_update=True)


    def publish(self, update_pub_date=True):
        if self.deleted is not None:
            raise SuspiciousOperation('Attempt to publish deleted publication.')

        self.check_required_fields()
        self.body.check_required_fields()

        # if self.owner.account.

        # sender=None для того, щоб django-orm не витягував автоматично дані з БД,
        # які, швидше за все, не знадобляться в подальшій обробці.
        models_signals.before_publish.send(
            sender = None,
            tid = self.tid,
            hid = self.id,
            hash_id = self.hash_id,
            for_sale = self.for_sale,
            for_rent = self.for_rent
        )

        with transaction.atomic():
            self.state_sid = OBJECT_STATES.published()
            if update_pub_date:
                self.published = now()
            self.prolong()
            self.save()


        models_signals.published.send(
            sender = None,
            tid = self.tid,
            hid = self.id,
            hash_id = self.hash_id,
            for_sale = self.for_sale,
            for_rent = self.for_rent,
        )


    def unpublish(self):
        # Moves the publication to unpublished publications.
        #
        # This method is called to move publications from trash too,
        # so no checks for deleted publication is needed here.

        # sender=None для того, щоб django-orm не витягував автоматично дані з БД,
        # які, швидше за все, не знадобляться в подальшій обробці.
        models_signals.before_unpublish.send(
            sender = None,
            tid = self.tid,
            hid = self.id,
            hash_id = self.hash_id,
            for_sale = self.for_sale,
            for_rent = self.for_rent,
        )

        self.state_sid = OBJECT_STATES.unpublished()
        self.published = None
        self.deleted = None
        self.save(force_update=True)

        # sender=None для того, щоб django-orm не витягував автоматично дані з БД,
        # які, швидше за все, не знадобляться в подальшій обробці.
        models_signals.unpublished.send(
            sender = None,
            tid = self.tid,
            hid = self.id,
            hash_id = self.hash_id,
            for_sale = self.for_sale,
            for_rent = self.for_rent,
        )


    def prolong(self, days=14):
        """
        Подовжує дію оголошення на @days днів (за замовчуванням).
        Використовується для автоматичної пролонгації оголошення при вході.
        """
        if not self.actual:
            self.actual = now() + datetime.timedelta(days=days)
        else:
            self.actual += datetime.timedelta(days=days)
        self.save(force_update=True)


    def mark_as_deleted(self):
        """
        Знімає оголошення з публікації та помічає його як видалене.
        """
        if self.deleted is not None:
            raise SuspiciousOperation('Attempt to delete already deleted publication.')

        self.state_sid = OBJECT_STATES.deleted()
        self.published = None
        self.deleted = now()
        self.save()

        models_signals.moved_to_trash.send(
            sender = None,
            tid = self.tid,
            hid = self.id,
            hash_id = self.hash_id,
            for_sale = self.for_sale,
            for_rent = self.for_rent,
        )


    def delete(self, using=None):
        # Standard delete method does not emits useful signals about deletion.
        # So this method was locked for prevent mistakes usages.
        raise RuntimeException('Method not allowed.')


    def delete_permanent(self):
        """
        Removes record permanent without possibility to restore it.
        If deletion was performed without errors - signal "deleted_permanently" will be emitted.
        """
        assert self.deleted, 'Attempt to delete publication that was not moved to trash.'

        # @deleted_permanently needs id of the publication as a parameter,
        # but the id will be None after deleting.
        #
        # So, for the correct work of all handlers related to this signal,
        # it is emitted before the physical record removing.
        models_signals.deleted_permanent.send(
            sender = None,
            tid = self.tid,
            hid = self.id,
            hash_id = self.hash_id,
            for_sale = self.for_sale,
            for_rent = self.for_rent,
        )

        super(AbstractHeadModel, self).delete()


    def check_required_fields(self):
        """
        Перевіряє чи обов’язкові поля не None, інакше - генерує виключну ситуацію.
        Не перевіряє інформацію в полях на коректність, оскільки передбачається,
        що некоректні дані не можуть потрапити в БД через обробники зміни даних.
        """

        #-- lat lng
        if (self.degree_lng is None) or (self.degree_lat is None):
            raise EmptyCoordinates('@degree is None')
        if (self.segment_lat is None) or (self.segment_lng is None):
            raise EmptyCoordinates('@segment is None')
        if (self.pos_lng is None) or (self.pos_lat is None):
            raise EmptyCoordinates('@pos is None')

        #-- sale terms
        if self.for_sale:
            self.sale_terms.check_required_fields()

        #-- rent terms
        if self.for_rent:
            self.rent_terms.check_required_fields()

        #-- body
        self.body.check_required_fields()

    def photos(self):
        return self.photos_model.objects.filter(publication = self.id).order_by('-is_title', '-created')

    def title_photo(self):
        photos = self.photos()
        if not photos:
            return None

        return photos[0]

    def is_published(self):
        return self.state_sid == OBJECT_STATES.published()


    def is_deleted(self):
        return self.state_sid == OBJECT_STATES.deleted()


class CommercialHeadModel(AbstractHeadModel):
    class Meta:
        abstract = True


class BodyModel(AbstractModel):
    class Meta:
        abstract = True

    #-- constraints
    max_title_length = 80 # todo: визначити довжину

    #-- fields
    title = models.TextField(null=True, max_length=max_title_length)
    description = models.TextField(null=True)

    def check_required_fields(self):
        """
        Перевіряє чи обов’язкові поля не None, інакше - генерує виключну ситуацію.
        Не перевіряє інформацію в полях на коректність, оскільки передбачається,
        що некоректні дані не можуть потрапити в БД через обробники зміни даних.
        """
        if (self.title is None) or (not self.title):
            raise EmptyTitle('Title is empty')
        if (self.description is None) or (not self.description):
            raise EmptyDescription('Description is empty')
        self.check_extended_fields()

    def check_extended_fields(self):
        """
        Abstract.
        Призначений для валідації моделей, унаслідуваних від поточної.
        """
        return


class SaleTermsModel(AbstractModel):
    class Meta:
        abstract = True

    #-- fields
    price = models.DecimalField(null=True, max_digits=AbstractModel.max_price_symbols_count, decimal_places=2)
    currency_sid = models.SmallIntegerField(default=currencies_constants.dol())
    is_contract = models.BooleanField(default=False)
    transaction_sid = models.SmallIntegerField(default=SALE_TRANSACTION_TYPES.for_all())
    add_terms = models.TextField(default='')

    #-- validation
    def check_required_fields(self):
        """
        Перевіряє чи обов’язкові поля не None, інакше - генерує виключну ситуацію.
        Не перевіряє інформацію в полях на коректність, оскільки передбачається,
        що некоректні дані не можуть потрапити в БД через обробники зміни даних.
        """
        if self.price is None:
            raise EmptySalePrice('Sale price is None.')



class LivingRentTermsModel(AbstractModel):
    class Meta:
        abstract = True

    #-- fields
    price = models.DecimalField(null=True, max_digits=AbstractModel.max_price_symbols_count, decimal_places=2)
    currency_sid = models.SmallIntegerField(default=currencies_constants.dol())
    is_contract = models.BooleanField(default=False)
    period_sid = models.SmallIntegerField(default=LIVING_RENT_PERIODS.monthly())
    # days_reserved = ArrayField(models.DateField)
    persons_count = models.SmallIntegerField(null=True)

    family = models.BooleanField(default=False)
    foreigners = models.BooleanField(default=False)
    smoking = models.BooleanField(default=False)
    pets = models.BooleanField(default=False)
    add_terms = models.TextField(default='')

    furniture = models.BooleanField(default=False)
    refrigerator = models.BooleanField(default=False)
    tv = models.BooleanField(default=False)
    washing_machine = models.BooleanField(default=False)
    conditioner = models.BooleanField(default=False)
    home_theater = models.BooleanField(default=False)

    #-- validation
    def check_required_fields(self):
        """
        Перевіряє чи обов’язкові поля не None, інакше - генерує виключну ситуацію.
        Не перевіряє інформацію в полях на коректність, оскільки передбачається,
        що некоректні дані не можуть потрапити в БД через обробники зміни даних.
        """
        if self.price is None:
            raise EmptyRentPrice('Rent price is None.')


    def print_terms(self):
        terms = u''
        if self.period_sid == LIVING_RENT_PERIODS.daily():
            terms += u', посуточно'
        elif self.period_sid == LIVING_RENT_PERIODS.monthly():
            terms += u', помесячно'
        elif self.period_sid == LIVING_RENT_PERIODS.long_period():
            terms += u', долгосрочная аренда'

        if self.persons_count:
            terms += u', количество мест — ' + unicode(self.persons_count)

        if self.family:
            terms += u', подходит для семей с детьми'
        if self.pets:
            terms += u', питомцы разрешены'
        if self.foreigners:
            terms += u', размещение иностранцев'
        if self.smoking:
            terms += u', можно курить'

        if self.add_terms:
            terms += u'. ' + self.add_terms

        if terms:
            return terms[2:]
        return u''


    def print_facilities(self):
        facilities = u''
        if self.furniture:
            facilities += u', мебель'
        if self.refrigerator:
            facilities += u', холодильник'
        if self.tv:
            facilities += u', телевизор'
        if self.washing_machine:
            facilities += u', стиральная машина'
        if self.conditioner:
            facilities += u', кондиционер'
        if self.home_theater:
            facilities += u', домашний кинотеатр'

        if facilities:
            return facilities[2:]
        return u''


    def print_price(self):
        if self.price is None:
            return u''

        dol = u'{:,.2f}'.format(currencies.convert(self.price, self.currency_sid, currencies_constants.dol()))
        dol = dol.replace(',', ' ')

        # Видалення копійок
        if dol[-3] == '.':
            dol = dol[:-3]

        # Підказуємо користувачу, що валюта сконвертована
        if self.currency_sid != currencies_constants.dol():
            dol = u'~' + dol

        dol += u' дол.'
        if self.is_contract:
            dol += u', договорная'


        # Додаємо ціну в інших валютах
        uah = u'{:,.2f}'.format(currencies.convert(self.price, self.currency_sid, currencies_constants.uah()))
        uah = uah.replace(',', ' ')

        if uah[-3] == '.':
            uah = uah[:-3]

        if self.currency_sid != currencies_constants.uah():
            uah = u'~' + uah
        uah += u' грн.'

        eur = u'{:,.2f}'.format(currencies.convert(self.price, self.currency_sid, currencies_constants.eur()))
        eur = eur.replace(',', ' ')

        if eur[-3] == '.':
            eur = eur[:-3]

        if self.currency_sid != currencies_constants.eur():
            eur = u'~' + eur
        eur += u' евро.'

        return u'{dol} ({uah}, {eur})'.format(dol=dol, uah=uah, eur=eur)



class CommercialRentTermsModel(AbstractModel):
    class Meta:
        abstract = True

    #-- constraints
    max_price_symbols_count = 18

    #-- fields
    price = models.DecimalField(null=True, max_digits=max_price_symbols_count, decimal_places=2)
    currency_sid = models.SmallIntegerField(default=currencies_constants.dol())
    is_contract = models.BooleanField(default=False)
    period_sid = models.SmallIntegerField(default=COMMERCIAL_RENT_PERIODS.monthly())
    add_terms = models.TextField(default='')


    #-- validation
    def check_required_fields(self):
        """
        Перевіряє чи обов’язкові поля не None, інакше - генерує виключну ситуацію.
        Не перевіряє інформацію в полях на коректність, оскільки передбачається,
        що некоректні дані не можуть потрапити в БД через обробники зміни даних.
        """
        if self.price is None:
            raise EmptyRentPrice('Rent price is None.')


    def print_price(self):
        if self.price is None:
            return u''

        dol = u'{:,.2f}'.format(currencies.convert(self.price, self.currency_sid, currencies_constants.dol()))
        dol = dol.replace(',', ' ')

        # Видалення копійок
        if dol[-3] == '.':
            dol = dol[:-3]

        # Підказуємо користувачу, що валюта сконвертована
        if self.currency_sid != currencies_constants.dol():
            dol = u'~' + dol

        dol += u' дол.'
        if self.is_contract:
            dol += u', договорная'


        # Додаємо ціну в інших валютах
        uah = u'{:,.2f}'.format(currencies.convert(self.price, self.currency_sid, currencies_constants.uah()))
        uah = uah.replace(',', ' ')

        if uah[-3] == '.':
            uah = uah[:-3]

        if self.currency_sid != currencies_constants.uah():
            uah = u'~' + uah
        uah += u' грн.'

        eur = u'{:,.2f}'.format(currencies.convert(self.price, self.currency_sid, currencies_constants.eur()))
        eur = eur.replace(',', ' ')

        if eur[-3] == '.':
            eur = eur[:-3]

        if self.currency_sid != currencies_constants.eur():
            eur = u'~' + eur
        eur += u' евро.'

        return u'{dol} ({uah}, {eur})'.format(dol=dol, uah=uah, eur=eur)


    #-- output
    def print_terms(self):
        terms = u''
        if self.period_sid == COMMERCIAL_RENT_PERIODS.monthly():
            terms += u', помесячно'
        elif self.period_sid == COMMERCIAL_RENT_PERIODS.long_period():
            terms += u', долгосрочная аренда'

        if self.add_terms:
            terms += u'. ' + self.add_terms

        if terms:
            return terms[2:]
        return u''



class PhotosModel(AbstractModel):
    # class variables
    tid = None # note: override to real tid # todo: inherit this model from the special model to prevent manual tid handling
    photos_handler = PublicationsPhotosHandler

    # fields
    publication = None # note: override to FK(PublicationHeadModel)
    hash_id = models.TextField(db_index=True)
    original_image_url = models.TextField()
    photo_url = models.TextField()
    big_thumb_url = models.TextField()
    is_title = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)


    class Meta:
        abstract = True
        unique_together = (('hid', 'is_title'), )


    @classmethod
    def by_publication(cls, publication_id):
        return cls.objects.filter(hid=publication_id).order_by('-created', '-is_title')


    @classmethod
    def add(cls, img, publication_head):
        """
        Processes image "img", generates all needed thumbnails and slides,
        and uploads it to the google cloud storage.

        :param img: file object that represents an image.
        :param publication_head: head record of the publication.
        :returns: record of this model with newly created publication.
        """
        original_image_url, \
        photo_url, \
        big_thumb_url = cls.photos_handler.process_and_upload_to_gcs(cls.tid, img)


        # If user will send several photos at a time - there are no guarantee about photos order.
        # Oly one photo should be marked as a title, so some kind of transaction is needed here.
        # Django transactions does not allow to lock tables for selecting, so django-transactions are not
        # helpful here, and redis lock is used instead.
        redis_connection = redis_connections['steady']
        lock_unique_identifier = "{0}:{1}".format(cls.tid, publication_head.id)

        lock = redis_lock.Lock(redis_connection, lock_unique_identifier)
        photo_is_title = False

        # Only first thread will lock the token and mark it's photo as title,
        # all other threads will mark their photos as non-title, because failed lock attempts.
        if lock.acquire(blocking=False) and \
                        cls.objects.filter(publication=publication_head, is_title=True).count() == 0:
            photo_is_title = True

        try:
            record = cls.objects.create(
                publication = publication_head,
                original_image_url = original_image_url,
                photo_url = photo_url,
                big_thumb_url = big_thumb_url,
                is_title = photo_is_title,
            )

            try:
                lock.release()
            except redis_lock.NotAcquired:
                pass

            return record

        except DatabaseError as e:
            # release lock even in case of error.
            try:
                lock.release()
            except redis_lock.NotAcquired:
                pass

            # Images are already uploaded to the cloud storage,
            # so we need to remove them now.
            #
            # Otherwise we will loose possibility to do this in the future,
            # because all the filenames are unique (based on uuid4)
            # and exists only now in this context.

            cls.photos_handler.remove_photo_from_google_cloud_storage(original_image_url.split('.com/mappino/')[1])
            cls.photos_handler.remove_photo_from_google_cloud_storage(photo_url.split('.com/mappino/')[1])
            cls.photos_handler.remove_photo_from_google_cloud_storage(big_thumb_url.split('.com/mappino/')[1])

            # ...
            # other images deletion should go here
            # ...

            raise cls.UnknownError('Database error: {}'.format(e.message))


    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        # This method is overridden to automatically save hash_id for the photo.
        if not self.hash_id:
            self.hash_id = generate_sha256_unique_id(str(self.id))
        super(PhotosModel, self).save(
            force_insert, force_update, using, update_fields)

    def delete(self, using=None):
        raise RuntimeError('This method is overridden to prevent inappropriate photo deletion. Use "remove()" instead.')

    def remove(self):
        """
        Removes original photo, processed photo and thumb from google cloud storage.
        Deletes the record of this photo from the database.

        :returns:
            record with next title photo if exists, or None.
        """
        try:
            # In some cases photos are already removed from the GCS and one more delete request will generate 404 error.
            # In this case photo record should be removed from the database too, and 404 error should be ignored.
            self.photos_handler.remove_photo_from_google_cloud_storage(self.original_image_url.split('.com/mappino/')[1])
            self.photos_handler.remove_photo_from_google_cloud_storage(self.photo_url.split('.com/mappino/')[1])
            self.photos_handler.remove_photo_from_google_cloud_storage(self.big_thumb_url.split('.com/mappino/')[1])

            # todo: add message about inappropriate deletion to the log.
        except:
            pass

        if self.is_title:
            photos = self.publication.photos()
            if photos:
                next_title_photo = photos[0]
                next_title_photo.mark_as_title()
                return next_title_photo

        super(PhotosModel, self).delete()


    def check_is_title(self):
        """
        Photo may by considered as title photo in 2 cases:

        1. There are no photos of this publication that are marked as title.
        In such case title is photo is the first created photo for this publication.

        2. There is one publication that is marked as title,
        and all other publications are not marked as title.

        There is another case when two or more photos are marked as title.
        If it is happened - then system is broken)

        :returns:
            True - if photo is marked as title for it's publication,
            False - in all other cases.

        :raises:
            RuntimeError - when system detects that two or more photos of one publication
                           are marked as title.
        """

        # check if system is not broken
        photos_of_its_publication = self.publication.photos()
        if photos_of_its_publication.filter(is_title=True).count() > 1:
            first_created_photo = photos_of_its_publication[:1][0]
            first_created_photo.mark_as_title()

            # current photo (self) may not be the first photo of the publication.
            return self.check_is_title()

        # check if current photo is marked as title
        if self.is_title:
            return True

        return False


    def mark_as_title(self):
        """
        Sets this photo as title photo for it's publication.
        """
        self.publication.photos().update(is_title=False)
        self.is_title = True
        self.save()