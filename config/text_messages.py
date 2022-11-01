# Этот файл с текстами бота. Здесь прописываются все стандартные фразы.

start_messages = {"greeting": "Дарова, это бот который собирает афишу в одном месте для вашего удобства. "
                  "\nКоманда /start вызывает это сообщение \n"
                  "Команда /add_my_vk_group добавляет группу в ВК для постоянной проверки на новую афишу.\n"
                  "\n"
                  "Чтобы добавить новую афишу, вам требуется написать #афиша и свой текст, добавить фотографию афиши, "
                  "например: ",
                  "description": "#афиша\nОписание вашей афиши. \nЗаметьте, любое сообщение для публикации ДОЛЖНО "
                                 "СОДЕРЖАТЬ ХЭШТЕГ! ",
                  "posting": 'При этом в беседе ВК "Гиги Архив"(https://vk.me/join/AJQ1dwt1thv1/NzRg32loLYG)'
                             ' и канале ТГ (https://t.me/GigsArchive) появится отправленная вами афиша'
                  }

new_poster_messages = {
    "on_moderation":
        "Отправил картинку и текст к ней на модерацию. А то мало ли, дикпики там отправляете на 200 человек)",
    "trust_message":
        "Вы уже три раза отправляли афишу, через бота!"
        " Теперь вы можете отправлять новую афишу без подтверждения модератором!"
}

error_messages = {
    'user_error': "используй /help чтобы разобраться",
}

poster_status_messages = {
    "message_ok": "Вы отметили данный постер как ДОПУСТИМЫЙ",
    "message_nok": "Вы отметили данный постер как НЕДОПУСТИМЫЙ",
    "answer_ok": "Ваша афиша уже отправлена в канал и беседу!\nСпасибо, что пользуетесь нашим ботом!",
    "answer_not_ok": "Модератор не принял вашу афишу.\n"
                     "Вы можете попробовать отправить еще раз с другим текстом или картинкой.\n"
                     "Или перестать страдать херней!",
    "on_poster_for_tomorrow_none": "К сожалению, я могу сообщить афишу на завтра только после 17. \n"
                                   "Хотите я сообщу вам, что есть на сегодня?",
    "on_poster_tomorrow": "Сейчас я отправлю вам 5 афиш, на завтра)"
    }


subscriber_messages = {
    "new_subscriber": "Вы подписались на рассылку афиш.\n"
                      "Вы в любой момент можете отписаться от рассылки с помощью команды <b>/unsubscribe</b> \n"
                      "Примерно в <b>21:15</b>,"
                      " когда редакция соберет подборку интересных мероприятий, сразу же вышлю)",
    "unsubscribe": "Вы только что отписались от ежедневной рассылки. Очень жаль 😔\n"
                   "Но вы можете в любой момент подписатся снова с помощью команды /subscribe 😄"
}

