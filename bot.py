#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# https://geekytheory.com/telegram-programando-un-bot-en-python/
# https://bitbucket.org/master_groosha/telegram-proxy-bot/src/07a6b57372603acae7bdb78f771be132d063b899/proxy_bot.py?at=master&fileviewer=file-view-default
# https://github.com/eternnoir/pyTelegramBotAPI/blob/master/telebot/types.py

"""commands
Name:
Network Common Ports

username:
procamora_common_ports_bot

Description:
This is a bot to study the most important network ports

About:
This bot has been developed by @procamora

Botpic:
<imagen del bot>

Commands:
get_port - get a random port number
get_name - get a random service name
stats - see statistics
help - Show help
start - Start the bot
"""

import configparser
import logging
import random
import re
import sys
from pathlib import Path
from typing import NoReturn, Tuple, List, Text, Callable

from procamora_utils.logger import get_logging
from requests import exceptions
from telebot import TeleBot, types, apihelper

from implement_sqlite import select_all_protocol, check_database, insert_stat, select_user_stats
from protocol import Protocol
from stats import Stats

logger: logging = get_logging(False, 'bot_scan')


def get_basic_file_config():
    return '''[BASICS]
ADMIN = 111111
BOT_TOKEN = 1069111113:AAHOk9K5TAAAAAAAAAAIY1OgA_LNpAAAAA
DEBUG = 0
'''


my_commands: Tuple[Text, ...] = (
    '/get_port',  # 0
    '/get_name',  # 1
    '/stats',  # 2
    '/start',  # 3
    '/help',  # 4
    '/exit',  # 5 (SIEMPRE TIENE QUE SER EL ULTIMO, ACCEDO CON -1)
)

FILE_CONFIG: Path = Path(Path(__file__).resolve().parent, "settings.cfg")
if not FILE_CONFIG.exists():
    logger.critical(f'File {FILE_CONFIG} not exists and is necesary')
    FILE_CONFIG.write_text(get_basic_file_config())
    logger.critical(f'Creating file {FILE_CONFIG}. It is necessary to configure the file.')
    sys.exit(1)

config: configparser.ConfigParser = configparser.ConfigParser()
config.read(FILE_CONFIG)

config_basic: configparser.SectionProxy = config["BASICS"]

if bool(int(config_basic.get('DEBUG'))):
    bot: TeleBot = TeleBot(config["DEBUG"].get('BOT_TOKEN'))
else:
    bot: TeleBot = TeleBot(config_basic.get('BOT_TOKEN'))

owner_bot: int = int(config_basic.get('ADMIN'))

check = b'\xE2\x9C\x94'
cross = b'\xE2\x9D\x8C'


def get_markup_cmd() -> types.ReplyKeyboardMarkup:
    markup: types.ReplyKeyboardMarkup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.row(my_commands[0], my_commands[1])
    markup.row(my_commands[2])
    markup.row(my_commands[-2], my_commands[-1])
    # markup.row(my_commands[4])
    return markup


def is_valid_port(protocol: Protocol, response: int):
    return protocol.port == response


def is_valid_name(protocol: Protocol, response: str):
    logger.debug(f'({protocol.name}|{protocol.description})')
    return re.search(f'{response}', f'({protocol.name}|{protocol.description})')


def get_random_protocol() -> Protocol:
    """
    Obtengo todos los protocolos disponibles y aleatoriamente selecciono uno para retornarlo
    :return Protocol:
    """
    response_query: List[Protocol] = select_all_protocol()
    element: int = random.randrange(0, len(response_query) - 1)
    logger.debug(response_query[element])
    return response_query[element]


def check_port():
    protocol: Protocol = get_random_protocol()
    question: str = f'What is the name of the protocol used by port {protocol.port}?'
    logger.debug(question)

    if is_valid_port(protocol, 3389):
        logger.debug('correcto')


# Handle always first "/start" message when new chat with your bot is created
@bot.message_handler(commands=["start"])
def command_start(message) -> NoReturn:
    bot.send_message(message.chat.id,
                     f"Welcome to the bot Network Common Ports\nThis is a bot to study the most important network ports"
                     f"\nYour id is: {message.chat.id}",
                     reply_markup=get_markup_cmd())
    command_system(message)
    return  # solo esta puesto para que no falle la inspeccion de codigo


@bot.message_handler(commands=["help"])
def command_help(message: types.Message) -> NoReturn:
    markup = types.InlineKeyboardMarkup()
    itembtna = types.InlineKeyboardButton('Github', url="https://github.com/procamora/bot_common_ports")
    markup.row(itembtna)
    bot.send_message(message.chat.id, 'You can find the source code for this bot in:', reply_markup=markup)
    command_system(message)
    return  # solo esta puesto para que no falle la inspeccion de codigo


@bot.message_handler(commands=["system"])
def command_system(message) -> NoReturn:
    commands: Text = '\n'.join(i for i in my_commands)
    bot.send_message(message.chat.id, f"List of available commands\nChoose an option:\n{commands}",
                     reply_markup=get_markup_cmd())
    return  # solo esta puesto para que no falle la inspeccion de codigo


@bot.message_handler(commands=['exit'])
def send_exit(message) -> NoReturn:
    bot.send_message(message.chat.id, "Nothing", reply_markup=get_markup_cmd())
    return


@bot.message_handler(commands=['stats'])
def send_stats(message: types.Message) -> NoReturn:
    """
    Muestra las estadisticas del usuario
    :param message:
    :return:
    """
    stat: Stats = select_user_stats(message.chat.id, 500)
    logger.debug(stat)
    print(message)
    response: Text = f"user: {message.from_user.username}\n" \
                     f"total questions: {len(stat.questions)}\n" \
                     f"total successful: {stat.total_success}\n" \
                     f"total failed: {stat.total_fail}\n" \
                     "Top failed:\n"

    list_protocols: List[Protocol]
    list_attemps: List[int]
    list_protocols, list_attemps = stat.get_top_questions_failed_attempts(40)
    for protocol, attemp in zip(list_protocols, list_attemps):
        response += f'   - {attemp} (attemps) -> name={protocol.name.upper()}, port={protocol.port}, ' \
                    f'protocol={protocol.protocol}\n'

    bot.reply_to(message, response, reply_markup=get_markup_cmd())
    return


@bot.message_handler(commands=['get_name'])
def send_port(message: types.Message) -> NoReturn:
    # bot.reply_to(message, stdout)
    protocol: Protocol = get_random_protocol()
    question: str = f'What is the name of the protocol used by port {protocol.port}?'
    logger.debug(question)
    bot.reply_to(message, question, reply_markup=get_markup_cmd())

    pass
    return


@bot.message_handler(commands=['get_port'])
def send_name(message: types.Message, reply: bool = True) -> NoReturn:
    protocol: Protocol = get_random_protocol()

    question: str = f'What is the protocol port {protocol.name}?'
    logger.debug(question)
    if reply:
        bot.reply_to(message, question, reply_markup=get_markup_cmd())
    else:
        bot.send_message(message.chat.id, question, reply_markup=get_markup_cmd())

    # if is_valid_port(protocol, 3389):
    #    logger.debug('correcto')

    # Definimos siguiente accion a realizar
    bot.register_next_step_handler(message, check_name, protocol=protocol)
    return


def check_name_aux(message: types.Message, protocol: Protocol):
    """
    Metodo auxiliar con el que volver esperar respuesta para el metodo check_name
    :param message:
    :param protocol:
    :return:
    """
    bot.reply_to(message, 'Enter a valid port number', reply_markup=get_markup_cmd())
    bot.register_next_step_handler(message, check_name, protocol=protocol)


def check_name(message: types.Message, protocol: Protocol) -> NoReturn:
    # Si no es un integer repetimos la pregunta
    if message.text == my_commands[-1]:  # exit
        bot.reply_to(message, "return main menu", reply_markup=get_markup_cmd())
        return

    if not re.search(r'^\d+$', message.text):
        check_name_aux(message, protocol)
        return

    if protocol.port == int(message.text):
        bot.reply_to(message, check, reply_markup=get_markup_cmd())
    else:
        bot.reply_to(message, cross.decode("utf-8"), reply_markup=get_markup_cmd())
        # bot.reply_to(message, f'The answer is incorrect {cross.decode("utf-8")}')

    response: Text = f'{protocol.name}\nport={protocol.port}\nprotocol={protocol.protocol}\n' \
                     f'description={protocol.description}'
    bot.reply_to(message, response, reply_markup=get_markup_cmd())
    logger.info(f'{protocol.port} == {message.text}')
    logger.info(protocol)

    send_name(message, reply=False)


@bot.message_handler(func=lambda message: message.chat.id == owner_bot)
def text_not_valid(message) -> NoReturn:
    texto: Text = 'unknown command, enter a valid command :)'
    command_system(message)
    # bot.reply_to(message, texto, reply_markup=get_markup_cmd())
    return


@bot.message_handler(regexp=".*")
def handle_resto(message) -> NoReturn:
    texto: Text = "You're not allowed to perform this action, that's because you're not me.\n" \
                  'As far as you know, it disappears -.-'
    bot.reply_to(message, texto, reply_markup=get_markup_cmd())
    return  # solo esta puesto para que no falle la inspeccion de codigo


def main():
    check_database()  # create db if not exists
    try:
        import urllib
        bot.send_message(owner_bot, 'Starting bot', reply_markup=get_markup_cmd(), disable_notification=True)
        logger.info('Starting bot')
    except (apihelper.ApiException, exceptions.ReadTimeout) as e:
        logger.critical(f'Error in init bot: {e}')
        sys.exit(1)

    # Con esto, le decimos al bot que siga funcionando incluso si encuentra algun fallo.
    bot.infinity_polling(none_stop=True)


if __name__ == "__main__":
    main()
