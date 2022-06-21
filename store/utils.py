from django.db.models.query import QuerySet
from django.db.models.manager import BaseManager

cyrillic_letters = {
    u'а': u'a',
    u'б': u'b',
    u'в': u'v',
    u'г': u'g',
    u'д': u'd',
    u'е': u'e',
    u'ё': u'e',
    u'ж': u'zh',
    u'з': u'z',
    u'и': u'i',
    u'й': u'i',
    u'к': u'k',
    u'л': u'l',
    u'м': u'm',
    u'н': u'n',
    u'о': u'o',
    u'п': u'p',
    u'р': u'r',
    u'с': u's',
    u'т': u't',
    u'у': u'u',
    u'ф': u'f',
    u'х': u'h',
    u'ц': u'ts',
    u'ч': u'ch',
    u'ш': u'sh',
    u'щ': u'sch',
    u'ь': u'',
    u'ы': u'y',
    u'ъ': u'',
    u'э': u'e',
    u'ю': u'u',
    u'я': u'ya',

}


def custom_slugify(text: str):
    text = text.replace(' ', '-').lower()
    result = ''
    for char in text:
        result += cyrillic_letters.get(char, char)
    return result


def get_object_or_null(model, **kwargs):
    if isinstance(model, QuerySet) or isinstance(model, BaseManager):
        return model.filter(**kwargs).first()
    return model.objects.filter(**kwargs).first()
