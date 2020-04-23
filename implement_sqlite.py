#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import logging
from pathlib import Path  # nueva forma de trabajar con rutas
from typing import List, Text, NoReturn, Dict, Any

from procamora_utils.interface_sqlite import conection_sqlite, execute_script_sqlite
from procamora_utils.logger import get_logging

from protocol import Protocol
from stats import Stats

logger: logging = get_logging(False, 'sqlite')

# Ruta absoluta de la BD
DB: Path = Path(Path(__file__).resolve().parent, "ports.db")
DB_STRUCTURE: Path = Path(Path(__file__).resolve().parent, "ports.sql")


def select_all_protocol() -> List[Protocol]:
    query: Text = "SELECT * FROM Ports"
    response_query: List[Dict[str, Any]] = conection_sqlite(DB, query, is_dict=True)
    response: List[Protocol] = list()
    for i in response_query:
        protocol: Protocol = Protocol(i['name'], i['port'], i['protocol'], i['description'])
        response.append(protocol)
    return response


def select_user_stats(id_user: int, limit) -> Stats:
    query = "SELECT Stats.id_user, Stats.successful, Ports.* " \
            "FROM Stats INNER JOIN Ports ON Stats.id_port = Ports.port " \
            "WHERE Stats.id_user=?" \
            "LIMIT ?;"

    total_fail: int = 0
    total_success: int = 0
    protocols: List[Protocol] = list()
    response_query: List[Dict[str, Any]] = conection_sqlite(DB, query, query_params=(id_user, limit), is_dict=True)
    for i in response_query:
        success: bool = False
        if i['successful'] == 'True':
            success = True
            total_success += 1
        else:
            total_fail += 1
        protocol: Protocol = Protocol(i['name'], i['port'], i['protocol'], i['description'], successful=success)
        protocols.append(protocol)

    stats: Stats = Stats(id_user, total_fail, total_success, protocols)

    return stats


def insert_stat(id_user: int, protocol: Protocol, successful: int):
    query: Text = f"INSERT INTO Stats(id_user, id_port, successful) VALUES (?, ?, ?)"
    logger.info(query)
    conection_sqlite(DB, query, query_params=(id_user, protocol.port, successful), is_dict=False)


def check_database() -> NoReturn:
    """
    Comprueba si existe la base de datos, sino existe la crea
    :return:
    """
    try:
        query: Text = "SELECT * FROM Ports"
        conection_sqlite(DB, query)
    except OSError:
        logger.info(f'the database {DB} doesn\'t exist, creating it with the default configuration')
        execute_script_sqlite(DB, DB_STRUCTURE.read_text())
