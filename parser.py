from bs4 import BeautifulSoup
import requests

text_mapping = {
    "Объектно-ориентир.  анализ и программир.": "Объектно-ориентированный анализ и программирование",
    "Програм.  инженерия": "Программная инженерия",
    "Администрир. ОС": "Администрирование ОС",
    "Осн. web-программир. (PHP и Js)": "Основы web-программирования (PHP и Js)",
    "Шаблоны проектир. *": "Шаблоны проектирования",
    "Обеспеч. безопас. web-прилож.": "Обеспечение безопасности web-приложений",
    "Програм. инженерия":"Программная инженерия",
    "Администрир.  и защита БД":"Администрирование и защита БД",
    "Проектир. инф. систем":"Проектирование информационных систем",
}

day_mapping = {
    "Пн": "сегодня понедельник",
    "Вт": "сегодня вторник",
    "Ср": "сегодня среда",
    "Чт": "сегодня четверг",
    "Пт": "сегодня пятница",
    "Сб": "сегодня суббота",
    "Вс": "сегодня воскресенье",
}

page = requests.get("https://iubip.ru/site_schedule_group/item/id/2245/")
soup = BeautifulSoup(page.content, 'html.parser')
el = soup.find("div", string="сегодня ")
siblings = el.parent.parent.find_all('td')
check_place = str(siblings)
if "дист" in check_place.lower():
    place = " в дистанте"
else:
    place = " очно"
divs = []
for s in siblings:
    div = s.find('div')
    if div is not None and div.text:
        div_text = div.text
        for day in day_mapping:
            if day in div_text:
                div_text = div_text.replace(day, day_mapping[day])
        for text in text_mapping:
            if text in div_text:
                div_text = div_text.replace(text, text_mapping[text])
        divs.append(div_text.strip())
result = ""
result += divs[0] + ", "
n_pairs = len(divs)-1
if n_pairs == 1:
    result += f"{n_pairs} пара"+place + "\n"
elif 1 < n_pairs < 5:
    result += f"{n_pairs} пары"+place + "\n"
else:
    result += f"{n_pairs} пар"+place + "\n"

for div in divs[1:]:
    result += "> " + div + "\n"
print(result)