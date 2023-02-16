START = 'Здравствуй, {}!\n Для начала работы зарегистрируйся'
LETS_WORK = 'Что бы вы хотели сделать?'
HELP = 'Это бот даёт возможность найти профессионалов, которые помогут вам реализовать ваши идеи.' \
       ' А фрилансерам поможет найти заказы и заработать.'
CHOOSE_ROLL = 'В качестве кого вы бы хотели зарегистрироваться?'
REGISTER_OK = 'Вы успешно зарегистрированы'

MY_ORDERS = 'Ваши текущие заказы:'
ORDER_INFO = '<b>Название: </b>{title}\n' \
             '<b>Дата создания: </b>{started_at}\n' \
             '<b>Текст: </b>{text}\n' \
             '<b>Стоимость: </b>{rate}\n' \
             '<b>Статус: </b>{status}\n' \
             '<b>Заказчик: </b>{client}\n' \
             '<b>Планируемое время: </b>{estimate_time}\n'

MY_TICKETS = 'Ваши текущие тикеты:'
TICKET_INFO = '<b>Название: </b>{title}\n' \
              '<b>Дата создания: </b>{started_at}\n' \
              '<b>Текст: </b>{text}\n' \
              '<b>Стоимость: </b>{rate}\n' \
              '<b>Статус: </b>{status}\n' \
              '<b>Исполнитель: </b>{freelanser}\n' \
              '<b>Планируемое время: </b>{estimate_time}\n' \
              '<b>Дата закрытия: </b>{completed_at}'

# Создание тикета
INPUT_TITLE = 'Давайте придумаем название для тикета'
INPUT_TICKET_TEXT = 'Отлично! Теперь опишите что нужно сделать исполнителю.'
INPUT_TICKET_RATE = 'Мы почти закончили. Укажите стоимость работ.'
TICKET_CREATED = '<b>Поздравляю! Вы создали тикет</b>\n<b>Название:</b> "{}"\n<b>Описание</b>: "{}"\n<b>Стоимость</b>: {}'

#  Сообщения об ошибках
MENU_IS_NOT_ALLOWED = 'Для начала работы зарегистрируйтесь.\n/start'
CREATING_IS_NOT_ALLOWED = 'Вы не можете создать новый заказ. Зарегистрируйтесь как заказчик.\n/start'
SEARCHING_IS_NOT_ALLOWED = 'Вы не можете искать заказы. Зарегистрируйтесь как исполнитель.\n/start'
