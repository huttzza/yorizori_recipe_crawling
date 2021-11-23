import csv
import requests
import json
from bs4 import BeautifulSoup
from tqdm import tqdm
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import re
from time import sleep

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)


def Recipe(url):
    # print(url)
    res = requests.get(url, timeout=10)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "lxml")

    title = []

    ingredients = []

    steps = []

    views = []

    writer = ''

    created_date = ''

    # Title
    res = soup.find('div', 'view2_summary')
    res = res.find('h3')
    title.append(res.get_text())

    # Main_Image
    thumb = ''
    images = soup.find_all("img", attrs={"id": "main_thumbs"})
    for image in images:
        image_url = image["src"]
        thumb = image_url

    # Ingredients
    b_ = soup.find_all("b", attrs={"class": "ready_ingre3_tt"})
    try:
        for b in b_:
            ingre_list = b.find_next_siblings("a")
            for ingre in ingre_list:
                ingre_set = []

                # ingre name
                name = ingre.li.get_text()
                name = name.split("   ", 1)[0]

                driver.get(url)
                script = re.split('[:;]', ingre['href'])[1]
                driver.execute_script(script)
                driver.implicitly_wait(10)
                try:
                    tmp = driver.find_element_by_class_name("ingredient_tit")
                    driver.implicitly_wait(10)
                    if tmp:
                        name = tmp.find_element_by_tag_name('b').text
                except Exception:
                    print("please check ", title[0], ":", name)
                    pass
                ingre_set.append(name)

                # ingre
                ingre_set.append(ingre.li.span.get_text())
                ingredients.append(ingre_set)
    except (AttributeError):
        return

    # Steps
    res = soup.find('div', 'view_step')
    i = 0
    for n in res.find_all('div', 'view_step_cont'):
        i = i + 1
        tem = []
        tem.append(str(i))
        tem.append(n.get_text().replace('\n', '\n\n'))

        img = n.find("img")
        if img != None:
            img_src = img.get("src")
        else:
            img_src = ''
        tem.append(img_src)
        steps.append(tem)

    # Views
    res = soup.find('div', 'view_cate_num')
    views = int(res.get_text().replace(',', ''))

    # writer
    writer = int(0)

    # Created Date
    res = soup.find('p', 'view_notice_date')
    res = res.find('b')
    created_date = (res.get_text().replace('등록일 : ', ''))

    if steps and ingredients:
        recipe = [title, thumb, writer, ingredients,
                  steps, views, created_date]
        # recipe = [title, thumb, ingred_name, ingred_amount,
        #           recipe_step, recipe_image, views, writer]
    else:
        recipe = []

    return recipe


def Search(name):
    url = "https://www.10000recipe.com/recipe/list.html?q=" + name
    res = requests.get(url, timeout=10)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "lxml")

    recipe_url = []

    a = soup.find("ul", attrs={"class": "common_sp_list_ul ea4"})
    links = a.find_all("div", attrs={"class": "common_sp_thumb"})

    for link in links:
        # print(link.a["href"])
        recipe_url.append('https://www.10000recipe.com' + link.a["href"])

    recipe_all = []
    for u in tqdm(recipe_url, desc=name):
        recipe = Recipe(u)
        if recipe:
            recipe_all.append(recipe)

    recipe_all_len = len(recipe_all)
    print('\t' + name + ' ' + str(recipe_all_len) + ' generated')

    return recipe_all, recipe_all_len


def save_as_file(result, json_file, csv_file, is_header):
    data = dict()
    index = 0
    for recipe in result:
        tem = dict()
        tem["title"] = recipe[0][0]
        tem["thumb"] = recipe[1]
        tem["writer"] = recipe[2]
        tem["ingredients"] = recipe[3]
        tem["steps"] = recipe[4]
        tem["views"] = recipe[5]
        tem["created_date"] = recipe[6]

        data[str(index)] = tem
        index += 1

    # json file writing
    json.dump(data, json_file, ensure_ascii=False)

    # csv file writing
    w = csv.DictWriter(csv_file, fieldnames=data["0"].keys())
    if is_header:
        w.writeheader()

    for key in data.keys():
        w.writerow(data[key])


if __name__ == "__main__":
    # food_list = ["마늘", "양상추", "단호박", "아보카도", "쪽파", "달걀", "양파", "토마토", "당근",
    #              "콩나물", "감자", "소세지", "두부", "파프리카", "새송이버섯", "오렌지", "무"]
    '''
    result = Recipe('https://www.10000recipe.com/recipe/6880246')
    print(result)
    '''
    food_list = ['가지', '고구마', '고추', '단호박', '달걀', '당근', '대파', '두부', '레몬', '마늘',
                 '무우', '배추', '버섯', '브로콜리', '빵', '사과', '아보카도', '애호박', '양배추', '양파',
                 '오이', '콩나물', '토마토', '파프리카', '피망']

    json_file = open("recipe.json", "w", encoding="utf8")
    csv_file = open("recipe.csv", "w", encoding="utf-8-sig", newline='')
    total = 0

    for i, food in enumerate(food_list):
        result, result_len = Search(food)
        save_as_file(result, json_file, csv_file, i == 0)
        total += result_len

    json_file.close()
    csv_file.close()
    driver.quit()

    print("[%d recipe dataset generated]" % (total))
