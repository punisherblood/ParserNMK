import vk_api
import json
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
# Подключение группы к скрипту
vk_session = vk_api.VkApi(token = '3bc699d3cda7db8d3529e6426703c9a1d914fe1812d2fc5d41f61f5b87703a7db9c697694e2edd53f749a')
longpoll = VkBotLongPoll(vk_session,209960585)
# Подключение Расписания
with open('resul.json','r', encoding='utf-8') as json_file:
    dict = json.load(json_file)
# Отправка сообщения в беседу (Функция)
def sender(id,text):
    vk_session.method('messages.send', {'chat_id': id, 'message': text, 'random_id':0})
# Отправка сообщения по запросу
for event in longpoll.listen():
    if event.type == VkBotEventType.MESSAGE_NEW:
            if event.from_chat:
                if event.object.message['text'][:1] == '!':
                    msg = event.object.message['text'][1:].upper()
                    id = event.chat_id
                    try:
                        gift = 'Раписание на '+dict["Дата"]+'\n'
                        for i in range(1,7):
                            gift += str(i)+'&#8419;'+'  '+dict.get(msg).get(str(i))
                        sender(id,gift)
                    except Exception:
                        sender(id,'Неверное название группы!')
