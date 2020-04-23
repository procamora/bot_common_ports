#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations

from dataclasses import dataclass
from typing import Text


@dataclass()
class Protocol:
    name: Text
    port: int
    protocol: Text
    description: Text = str()
    successful: bool = False

    def __hash__(self):
        return hash((self.name, str(self.port), self.protocol))
