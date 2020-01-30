#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import telebot
import area
import graph

bot = telebot.TeleBot('')

try:
    @bot.message_handler(commands=['start'])
    def start(message):
        bot.send_message(message.chat.id, '欢迎使用。')

    @bot.message_handler(commands=['area'])
    def send_area(message):
        string_ans = area.area()
        bot.reply_to(message, string_ans)

    @bot.message_handler(commands=['graph'])
    def send_graph(message):
        file1, file2 = graph.graph()
        with open('./view/{0}.png'.format(file1), 'rb') as f:
            graph1 = f.read()
            bot.send_photo(message.chat.id, graph1)
            f.close()
        with open('./view/{0}.png'.format(file2), 'rb') as f:
            graph2 = f.read()
            bot.send_photo(message.chat.id, graph2)
            f.close()

    bot.polling(none_stop=True)
except KeyboardInterrupt:
    quit()
except Exception as e:
    print(str(e))