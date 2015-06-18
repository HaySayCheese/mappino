#coding=utf-8
import re


def format_text(value):
    # додати крапку, якщо немає.
    if value[-1] != '.':
        value += '.'

    # Замінити всі подвійні/потрійні і т.д. пробіли одним,
    # відсікти всі зайві пробіли справа.
    value = re.sub(' +', ' ', value).strip()

    return value


def format_title(value):
    value = format_text(value)
    if value[-1] == '.':
        value = value[:-1]

    return value.capitalize()