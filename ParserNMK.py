from bs4 import BeautifulSoup
import json
from fake_useragent import UserAgent
import requests
maindict = {}

# Html код страницы
ua = UserAgent()
s = requests.Session()
response = s.get( url = 'http://www.nmt.edu.ru/html/hg.htm', headers = {'user-agent': f'{ua.random}'})
response.encoding = response.apparent_encoding
src = BeautifulSoup(response.text, 'lxml')
# Дата
def get_data():
    data = src.find('ul',class_='zg').find('li',class_='zgr').text
    return data
# получение рассписания для группы
def group():
    for item in src.find_all('tr')[6:]:
# Название группы
        try:
            group_name = item.find('a', class_='hd', title="Текущее расписание на неделю").text
            maindict[group_name] = ''
            groupdict = {}
            number = 1
        except Exception:
            pass
        try:
# 2 подгруппы
            if item.find('td', class_="ur").get('colspan') == '1':
                lesson = []
                for K in item.find_all('td')[1:]:
                    try:
                        lesson.append(K.find('a', class_='z1').text + '  |  ' + K.find('a', class_='z2').text) #+ '  |   '+ K.find('a', class_='z3').text
                    except Exception:
                        lesson.append('Нет пары')
                groupdict[number] = '1ПГ: ' + lesson[-2]+' 2ПГ: ' + lesson[-1] + ' \n'
# 1 подгруппа
            else:
                lesson = item.find('a', class_='z1').text + '  |  ' +  item.find('a', class_='z2').text #+ '  |   '+ item.find('a', class_='z3').text
                groupdict[number] = lesson + '\n'
        except Exception:
            lesson = 'Нет пары'
            groupdict[number] = lesson + '\n'
        number +=1
        maindict[group_name] = groupdict

# Вывод/сохранение асписания для групп
if __name__ == '__main__':
    maindict = {'Дата': get_data()}
    group()
    with open('resul.json','w', encoding='utf-8') as file:
        json.dump(maindict, file, ensure_ascii=False, indent=4)
