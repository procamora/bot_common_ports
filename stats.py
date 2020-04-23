#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Set, Dict, Tuple

from protocol import Protocol


def sort_protocol_based_attempts(protocol: Protocol, repeat: Dict[int, int]):
    return repeat[protocol.port]


@dataclass
class Stats:
    id_user: int
    total_fail: int
    total_success: int
    questions: List[Protocol]

    def __post_init__(self):
        self.questions = sorted(self.questions, key=lambda p: p.port, reverse=False)

    def get_top_questions_failed_attempts(self, top: int) -> Tuple[List[Protocol], List[int]]:
        """
        Metodo para obtener los n puertos que mas fallos has tenido. Esta funciona puede ser costosa en tiempo
        :param top:
        :return:
        """
        # obtengo un set con los protocolos, eliminando repetidos (necesario implementar func hash en stats y protocols)
        # filtrando unicamente los que se han fallado
        unic_protocols: Set[Protocol] = set(filter(lambda p: p.successful == False, self.questions))
        # unic_protocols: Set[Protocol] = set([i for i in self.questions])

        # Obtener repeticiones totales de cada elemento del set
        repeat: Dict[int, int] = dict()
        for prt in unic_protocols:
            cont: int = 0
            for y in self.questions:
                if prt.port == y.port:
                    cont += 1
            repeat[prt.port] = cont

        # Ordenar set en base a las repeticiones
        sort_protocols: List[Protocol] = sorted(unic_protocols,
                                                key=lambda p: sort_protocol_based_attempts(p, repeat),
                                                reverse=True)

        response_prot: List[Protocol] = list()
        response_fail: List[int] = list()

        # size max: len(sort_protocols)
        if len(sort_protocols) < top:
            top = len(sort_protocols)

        # listas con los n elementos con mas intentos
        for i in range(0, top):
            response_prot.append(sort_protocols[i])
            response_fail.append(repeat[sort_protocols[i].port])

        return response_prot, response_fail

    def __hash__(self):
        return hash((self.id_user, self.questions))
