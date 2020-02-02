#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Protocol():
    name: str
    port: int
    protocol: str
    description: str = str()
