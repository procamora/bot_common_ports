#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sqlite3
from pathlib import Path  # nueva forma de trabajar con rutas
from threading import Lock
from typing import Dict, Any, List, Union, Tuple, Optional

from protocol import Protocol

DB = "ports.db"


def conection_sqlite(db: str, query: str, mutex: Lock = None, is_dict: bool = False) \
        -> Union[List[Dict[str, Any]], None]:
    if mutex is not None:
        mutex.acquire()  # bloqueamos acceso a db
    try:
        if os.path.exists(db):
            conn = sqlite3.connect(db)
            if is_dict:
                conn.row_factory = dict_factory
            cursor = conn.cursor()
            cursor.execute(query)

            if query.upper().startswith('SELECT'):
                data = cursor.fetchall()  # Traer los resultados de un select
            else:
                conn.commit()  # Hacer efectiva la escritura de datos
                data = None

            cursor.close()
            conn.close()
            return data
    except sqlite3.OperationalError:
        print(f'LOCK {query}, sorry...')
    finally:
        if mutex is not None:
            mutex.release()  # liberamos mutex


def dict_factory(cursor: sqlite3.Cursor, row: Tuple[str]) -> Dict[str, str]:
    d: Dict = dict()
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def execute_script_sqlite(database: Path, script: str) -> None:
    conn = sqlite3.connect(str(database))
    cursor = conn.cursor()
    cursor.executescript(script)
    conn.commit()
    cursor.close()
    conn.close()


def dump_database(database: Path) -> Optional[str]:
    """
    Hace un dump de la base de datos y lo retorna
    :param database: ruta de la base de datos
    :return dump: volcado de la base de datos
    """
    if database.exists():
        con = sqlite3.connect(str(database))
        a: str = '\n'.join(con.iterdump())
        return str(a)
    return None


def select_all_protocol() -> List[Protocol]:
    query = "SELECT * FROM Ports"
    response_query: List[Dict[str, Any]] = conection_sqlite(DB, query, is_dict=True)
    response: List[Protocol] = list()
    for i in response_query:
        protocol: Protocol = Protocol(i['Name'], i['Port'], i['Protocol'], i['Description'])
        response.append(protocol)
    return response
