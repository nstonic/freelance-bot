#  Общие
CHOOSE_ROLE = 'В качестве кого вы бы хотели зарегистрироваться?'
REGISTER_OK = 'Вы успешно зарегистрированы'

#  Сообщения фрилансеру
MY_ORDERS = 'Ваши текущие заказы:'
NO_ORDERS = 'У вас нет текущих заказов.'
ORDER_INFO = '<b>{title}</b>\n\n' \
             '<b>Взят в работу: </b>{started_at}\n' \
             '<b>Задание: </b>{text}\n' \
             '<b>Статус: </b>{status}\n' \
             '<b>Планируемая дата завершения: </b>{estimate_time}\n'
TICKET_CHOICE = 'Вот несколько свободных тикетов:'
NO_ACTIVE_TICKETS = 'В данный момент нет активных тикетов. Попробуйте позже'
SET_EST_TIME = 'Укажите оценочную дату исполнения в формате YYYY-MM-DD.\n' \
               'Например: 2000-12-31'
CLOSED = 'Заказ завершён'
CANCELED = 'Вы отказались от заказа'

#  Сообщения клиенту
MY_TICKETS = 'Ваши текущие тикеты:'
NO_TICKETS = 'У вас нет активных тикетов.'
TICKET_INFO = '<b>{title}</b>\n\n' \
              '<b>Создан: </b>{created_at}\n' \
              '<b>Задание: </b>{text}\n' \
              '<b>Статус: </b>{status}\n' \
              '<b>Планируемая дата завершения: </b>{estimate_time}\n'
TICKET_TAKEN = 'Тикет <b>{}</b> взят в работу'
TICKET_CLOSED = 'Тикет <b>{}</b> выполнен'
TICKET_CANCELED = 'Исполнитель отказался от тикета <b>{}</b>'

# Создание тикета
INPUT_TITLE = 'Придумайте название для тикета'
INPUT_TICKET_TEXT = 'Отлично! Теперь опишите, что нужно сделать исполнителю.'
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
MESSAGE_SENT = 'Сообщение отправлено'
NO_MESSAGES = 'В чате нет сообщений'
INCOMING = 'Вам пришло новое сообщение по {order_or_ticket} <b>{title}</b>'

#  Сообщения об ошибках
REGISTER_FALSE = 'Произошла ошибка при регистрации. Попробуйте позже'
MENU_IS_NOT_ALLOWED = 'Для начала работы зарегистрируйтесь.\n/start'
CREATING_IS_NOT_ALLOWED = 'Вы не можете создать новый тикет. Зарегистрируйтесь как заказчик.\n/start'
SEARCHING_IS_NOT_ALLOWED = 'Вы не можете искать заказы. Зарегистрируйтесь как исполнитель.\n/start'
TITLE_LEN_ERROR = 'Слишком длинное название. Введите ещё раз. Уложитесь в 30 символов.'
TITLE_EXIST = 'У вас уже есть тикет с таким названием. Введите другое.'
CANT_DELETE = 'Тикет взят в работу. Его нельзя удалить'
INVALID_DATE = 'Неверный формат даты. Попробуйте еще раз.'
WRONG_DATE = 'Дата исполнения не может быть в прошлом'
ERROR_500 = 'Внутренняя ошибка сервера'
