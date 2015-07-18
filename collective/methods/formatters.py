#coding=utf-8
import re


def format_text(text):
    # Перша літера у великий регістр
    text = text.capitalize()

    # додати крапку, якщо немає.
    if text[-1] != '.':
        text += '.'

    # Замінити всі подвійні/потрійні і т.д. пробіли одним,
    # відсікти всі зайві пробіли справа.
    text = re.sub(' +', ' ', text).strip()

    # Кожне нове речення - великий регістр
    # todo: add here

    return text


def format_title(text):
    # Форматує текст за звичними правилами.
    # Видаляє точку в кінці тексту.

    text = format_text(text)
    text = text.strip()

    # Якщо в кінці тексту наявна крапка, видалити її
    if len(text) > 1:
        if len(text) < 3:
            if text[-1] == '.':
                text = text[:-1]

        else:
            while text[-1] == '.':
                text = text[:-1]

    return text