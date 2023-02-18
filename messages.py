#  Общие
HELP = 'Этот бот даёт возможность найти профессионалов, которые помогут вам реализовать ваши идеи.' \
       'А фрилансерам поможет найти заказы и заработать.'
CHOOSE_ROLE = 'В качестве кого вы бы хотели зарегистрироваться?'
REGISTER_OK = 'Вы успешно зарегистрированы'

#  Сообщения фрилансеру
MY_ORDERS = 'Ваши текущие заказы:'
NO_ORDERS = 'У вас нет текущих заказов.'
ORDER_INFO = '<b>{title}</b>\n\n' \
             '<b>Дата начала: </b>{started_at}\n' \
             '<b>Текст: </b>{text}\n' \
             '<b>Статус: </b>{status}\n' \
             '<b>Планируемое время: </b>{estimate_time}\n'
TICKET_CHOICE = 'Вот несколько свободных тикетов:'
NO_ACTIVE_TICKETS = 'В данный момент нет активных тикетов. Попробуйте позже'
SET_EST_TIME = 'Укажите оценочную дату исполнения.'
ORDER_CLOSED = 'Заказ завершён'
ORDER_CANCELED = 'Вы отказались от заказа'

#  Сообщения клиенту
MY_TICKETS = 'Ваши текущие тикеты:'
NO_TICKETS = 'У вас нет тикетов.'
TICKET_INFO = '<b>{title}</b>\n\n' \
              '<b>Дата создания: </b>{created_at}\n' \
              '<b>Текст: </b>{text}\n' \
              '<b>Статус: </b>{status}\n' \
              '<b>Планируемое время: </b>{estimate_time}\n' \
              '<b>Дата закрытия: </b>{completed_at}'

# Создание тикета
INPUT_TITLE = 'Давайте придумаем название для тикета'
INPUT_TICKET_TEXT = 'Отлично! Теперь опишите что нужно сделать исполнителю.'
INPUT_TICKET_RATE = 'Мы почти закончили. Укажите стоимость работ.'
TICKET_DELETED = 'Тикет удалён'
TICKET_CREATED = '<b>Поздравляю! Вы создали тикет</b>\n\n' \
                 '<b>{title}</b>\n' \
                 '{text}'
#  Статусы
ORDER_STATUSES = {'in_progress': 'В работе',
                  'cancelled': 'Отменён',
                  'finished': 'Завершён'}
TICKET_STATUSES = {'waiting': 'Ожидает исполнителя',
                   'in_progress': 'В работе',
                   'finished': 'Завершён'}

# Чат
SEND_MESSAGE = 'Введите сообщение'
MESSAGE_SEND = 'Сообщение отправлено'
NO_MESSAGE = 'В чате нет сообщений'
INCOMING = 'Вам пришло новое сообщение по {order_or_ticket} <b>{title}</b>.\n\n{text}'

#  Сообщения об ошибках
REGISTER_FALSE = 'Произошла ошибка при регистрации. Попробуйте позже'
MENU_IS_NOT_ALLOWED = 'Для начала работы зарегистрируйтесь.\n/start'
CREATING_IS_NOT_ALLOWED = 'Вы не можете создать новый заказ. Зарегистрируйтесь как заказчик.\n/start'
SEARCHING_IS_NOT_ALLOWED = 'Вы не можете искать заказы. Зарегистрируйтесь как исполнитель.\n/start'
TITLE_ERROR = 'Слишком длинное название. Введите ещё раз. Уложитесь в 30 символов.'
NO_CHAT = 'Не выбран чат'
ERROR_500 = 'Внутренняя ошибка сервера'
