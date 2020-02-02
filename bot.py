#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import configparser
import random
import re
from typing import List, Dict, NoReturn

from telebot import TeleBot, types  # Importamos la librería Y los tipos especiales de esta

from connect_sqlite import select_all_protocol
from logger import logger
from protocol import Protocol

FILE_CONFIG = 'settings.ini'
config = configparser.ConfigParser()
config.read(FILE_CONFIG)

config_basic = config["BASICS"]
config_ssh = config["SSH"]

administrador = 33063767
users_permitted = [33063767, 40522670]

bot = TeleBot(config_basic.get('BOT_TOKEN'))
# bot.send_message(administrador, "El bot se ha iniciado")
logger.info("El bot se ha iniciado")

dicc_botones: Dict[str, str] = {
    'get_port': '/get_port',
    'get_name': '/get_name',
    'halt': '/halt',
    'exit': '/exit',
}

check = b'\xE2\x9C\x94'
cross = b'\xE2\x9D\x8C'


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
def command_start(message: types.Message) -> NoReturn:
    bot.send_message(message.chat.id, f"Bienvenido al bot\nTu id es: {message.chat.id}")
    command_system(message)
    return  # solo esta puesto para que no falle la inspeccion de codigo


@bot.message_handler(commands=["help"])
def command_help(message: types.Message) -> NoReturn:
    markup = types.InlineKeyboardMarkup()
    itembtna = types.InlineKeyboardButton('Github', url="https://github.com/procamora/bot_common_ports")
    markup.row(itembtna)
    bot.send_message(message.chat.id, "Aqui pondre todas las opciones", reply_markup=markup)
    return  # solo esta puesto para que no falle la inspeccion de codigo


@bot.message_handler(commands=["system"])
def command_system(message: types.Message) -> NoReturn:
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.row(dicc_botones['get_port'], dicc_botones['get_name'])
    # markup.row(dicc_botones['poweroff'], dicc_botones['halt'])
    markup.row(dicc_botones['exit'])
    bot.send_message(message.chat.id, "Escoge una opcion: ", reply_markup=markup)
    return  # solo esta puesto para que no falle la inspeccion de codigo


@bot.message_handler(func=lambda message: message.chat.id == administrador, commands=['exit'])
def send_exit(message: types.Message) -> NoReturn:
    pass


# @bot.message_handler(func=lambda message: message.chat.id == administrador, content_types=["text"])
# def my_text(message: types.Message) -> NoReturn:
#    if message.text in dicc_botones.values():
#        if message.text == dicc_botones['get_port']:
#            send_port(message)
#        elif message.text == dicc_botones['get_name']:
#            send_name(message)
# elif message.text == dicc_botones['poweroff']:
#    send_poweroff(message)
# elif message.text == dicc_botones['halt']:
#    send_halt(message)
#        elif message.text == dicc_botones['exit']:
#            send_exit(message)
#    else:
#        bot.send_message(message.chat.id, "Comando desconocido")
#    return  # solo esta puesto para que no falle la inspeccion de codigo


@bot.message_handler(commands=['get_name'])
def send_port(message: types.Message) -> NoReturn:
    # bot.reply_to(message, stdout)
    protocol: Protocol = get_random_protocol()
    question: str = f'What is the name of the protocol used by port {protocol.port}?'
    logger.debug(question)
    bot.reply_to(message, question)

    pass
    return


@bot.message_handler(commands=['get_port'])
def send_name(message: types.Message) -> NoReturn:
    protocol: Protocol = get_random_protocol()

    question: str = f'What is the protocol port {protocol.name}?'
    logger.debug(question)
    bot.reply_to(message, question)

    # if is_valid_port(protocol, 3389):
    #    logger.debug('correcto')

    print('my_text')
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
    bot.reply_to(message, 'Enter a valid port number')
    bot.register_next_step_handler(message, check_name, protocol=protocol)


def check_name(message: types.Message, protocol: Protocol):
    # Si no es un integer repetimos la pregunta
    if not re.search(r'^\d+$', message.text):
        check_name_aux(message, protocol)

    if protocol.port == int(message.text):
        bot.reply_to(message, check)
    else:
        bot.reply_to(message, cross.decode("utf-8"))
        # bot.reply_to(message, f'The answer is incorrect {cross.decode("utf-8")}')

    bot.reply_to(message, str(protocol))
    logger.info(f'{protocol.port} == {message.text}')
    logger.info(protocol)

    send_name(message)


@bot.message_handler(func=lambda message: message.chat.id == administrador, content_types=["photo"])
def my_photo(message) -> NoReturn:
    if message.reply_to_message:
        bot.send_photo(message.chat.id, list(message.photo)[-1].file_id)
    else:
        bot.send_message(message.chat.id, "No one to reply photo!")
    return  # solo esta puesto para que no falle la inspeccion de codigo


@bot.message_handler(func=lambda message: message.chat.id == administrador, content_types=["voice"])
def my_voice(message: types.Message) -> NoReturn:
    if message.reply_to_message:
        bot.send_voice(message.chat.id, message.voice.file_id, duration=message.voice.duration)
    else:
        bot.send_message(message.chat.id, "No one to reply voice!")
    return  # solo esta puesto para que no falle la inspeccion de codigo


@bot.message_handler(func=lambda message: message.chat.id in users_permitted, content_types=["document"])
def my_document(message: types.Message) -> NoReturn:
    # if message.reply_to_message:
    #    bot.send_voice(message.chat.id, message.voice.file_id, duration=message.voice.duration)
    # else:
    bot.reply_to(message, f'Aun no he implementado este tipo de ficheros: "{message.document.mime_type}"')
    return  # solo esta puesto para que no falle la inspeccion de codigo


@bot.message_handler(regexp=".*")
def handle_resto(message: types.Message) -> NoReturn:
    texto = 'Unknown command'
    bot.reply_to(message, texto)
    return  # solo esta puesto para que no falle la inspeccion de codigo


# Con esto, le decimos al bot que siga funcionando incluso si encuentra
# algun fallo.
bot.polling(none_stop=False)
