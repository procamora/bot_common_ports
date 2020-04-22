#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import logging
from pathlib import Path  # nueva forma de trabajar con rutas
from typing import List, Text, NoReturn, Dict, Any

from procamora_utils.interface_sqlite import conection_sqlite, execute_script_sqlite
from procamora_utils.logger import get_logging

from protocol import Protocol

logger: logging = get_logging(False, 'sqlite')

# Ruta absoluta de la BD
DB: Path = Path(Path(__file__).resolve().parent, "ports.db")
DB_STRUCTURE: Path = Path(Path(__file__).resolve().parent, "ports.sql")


def select_all_protocol() -> List[Protocol]:
    query = "SELECT * FROM Ports"
    response_query: List[Dict[str, Any]] = conection_sqlite(DB, query, is_dict=True)
    response: List[Protocol] = list()
    for i in response_query:
        protocol: Protocol = Protocol(i['Name'], i['Port'], i['Protocol'], i['Description'])
        response.append(protocol)
    return response


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
