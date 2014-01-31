#coding=utf-8
from django.db.models.signals import post_delete
from core.dirtags.models import DirTags
from core.publications.constants import HEAD_MODELS, OBJECTS_TYPES


#
# Обробник коректного видалення оголошень з реєстру тегів
# у випадку видалення самого оголошення з БД.
#
def delete_publication(sender, **kwargs):
    for tid, model in HEAD_MODELS.items():
        if model == kwargs['instance'].__class__:
            DirTags.rm_all_publication_occurrences(tid, kwargs['instance'].id)
            break

def init_models_delete_handler():
    for tid in OBJECTS_TYPES.values():
        post_delete.connect(delete_publication, HEAD_MODELS[tid], weak=False)

init_models_delete_handler()
# todo: check me