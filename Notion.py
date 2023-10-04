import requests, json
from CONFIG import *

def get_pages_database(DataBase_ID):
    url = f"https://api.notion.com/v1/databases/{DataBase_ID}/query"

    payload = {"page_size": 100}
    response = requests.post(url, json=payload, headers=HEADERS)

    data = response.json()

    with open('DataBase.json', 'w', encoding='utf8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

    results = data["results"]
    return results

def update_page(PAGE_ID: str, NEW_DATA: dict):
    url = f"https://api.notion.com/v1/pages{PAGE_ID}"

    payload = {"properties": NEW_DATA}

    res = requests.patch(url, json=payload, headers=HEADERS)
    print(res.status_code)
    return res

# def get_pages(Page_ID): #КБ!
#     url = f"https://api.notion.com/v1/pages/{Page_ID}"
#
#     response = requests.get(url, headers=HEADERS)
#
#     data = response.json()
#
#     with open('Page.json', 'w', encoding='utf8') as file:
#         json.dump(data, file, ensure_ascii=False, indent=4)
#
#     results = data["results"]
#     return results

def fix_full_name(FULLNAME: str):
    name_parts = FULLNAME.split()
    for letter in name_parts[0]:
        if letter == ".":
            return "ФИО введенно неверно"
    formatted_name = name_parts[0].capitalize() + " "
    name_parts = name_parts[1].split(".")
    formatted_name += name_parts[0].upper() + "." + name_parts[1].upper() + "."
    return str(formatted_name.strip())

def fix_lesson(LESSON: str):
    les = LESSON.lower()
    if les == "ооп" or les == "объектно ориентированное программирование":
        return OOP_LESSON
    elif les == "опд" or les == "основы профессиональной деятельности":
        return PYTHON_LESSON
    else:
        return "Такого предмета нет"

def fix_group(GROUP: str):
    return GROUP.upper()

def find_Student(FULLNAME: str, GROUP: str, LESSON: dict):
    if LESSON.get(GROUP) is None:
        return False #"Такой группы в данном предмете не существует"
    elif FULLNAME == "ФИО введенно неверно":
        return False #"ФИО введенно неверно"
    else:
        pages = get_pages_database(LESSON[GROUP])
        for page in pages:
            props = page["properties"]
            name = props["ФИО"]["title"][0]["text"]["content"]
            if name == FULLNAME:
                return True #f"Студент {name} найден в группе {GROUP}"
        return False # f"Студент {FULLNAME} в группе {GROUP} не найден"

def show_me_my_points(FULLNAME: str, GROUP: str, LESSON: dict):
    if find_Student(FULLNAME, GROUP, LESSON) != True:
        return False
    else:
        pages = get_pages_database(LESSON[GROUP])
        for page in pages:
            props = page["properties"]
            name = props["ФИО"]["title"][0]["text"]["content"]
            points = props["Formula"]["formula"]["number"]
            if name == FULLNAME:
                return points
        return False
def main():
    # lesson = fix_lesson(input("Введите предмет: "))
    # group = fix_group(input("Введите группу: "))
    # fullname = fix_full_name(input("Введите ФИО: "))
    update_data = {"GitHub": {"url": "https://github.com/GrinyaI"}}
    update_page("685812d7-5034-48ff-a1b4-d1ef82346372", update_data)