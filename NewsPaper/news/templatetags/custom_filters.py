from django import template

register = template.Library()

@register.filter()
def censor(value):
    bad_words = ['упал','землетрясение', 'сил','мобилизация']

    if not isinstance(value, str):
        raise TypeError(f'Недопустимое значение{type(value)} Нужно ввести строковое значение')

    for word in value.split():
        if word.lower() in bad_words:
            value = value.replace(word, f'{word[0]}{"*" * (len(word) - 1)}')
    return value

