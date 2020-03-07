# -*- coding:utf-8 -*-
import os
import re
import json
import configparser
from typing import Any, AnyStr, Optional, Mapping

WRAPPED_ITEM = '_wrapped'
GLOBAL_SECTION_NAME = 'global'
KEY_CLEAN_PATTERN = re.compile(r'[^A-Za-z0-9_]')


def clean_key(k: AnyStr) -> str:
    k_ = str(k).upper()
    k_ = KEY_CLEAN_PATTERN.sub('_', k_).strip('_')

    return k_


def clean_item(k: AnyStr, v: AnyStr) -> (str, Any):
    if k.startswith('@'):
        # Comma-Separated list.
        v = v.strip(',')
        v = list(map(lambda x: x.strip(), v.split(',')))
    elif k.startswith('^'):
        # JSON object.
        v = json.loads(v)
    elif v in ('yes', 'no'):
        v = 'yes' == v

    k = clean_key(k)
    return k, v


class Section:

    def __init__(self, section_name: AnyStr):
        self.SECTION_NAME = clean_key(section_name)

    def from_mapping(self, section: Mapping):
        for item in section.items():
            k, v = clean_item(*item)

            setattr(self, k, v)

    def from_object(self, section: Any):
        for item in dir(section):
            if not item.isupper():
                continue

            setattr(self, *clean_item(item, getattr(section, item)))

    def append(self, v: Any, k: Optional[AnyStr] = None):
        if isinstance(v, Section):
            setattr(self, v.SECTION_NAME, v)
            return
        elif isinstance(v, Mapping):
            self.from_mapping(v)
            return
        elif k:
            setattr(self, *clean_item(k, v))


class Settings:
    _wrapped: Optional[Section] = None

    def __init__(self, configfile: Optional[AnyStr] = None, base_section=GLOBAL_SECTION_NAME):
        self._wrapped = Section(base_section)
        self.base_section = base_section

        if not configfile:
            return

        self.load_configfile(configfile)

    def load_configfile(self, configfile: AnyStr):
        if not os.path.exists(configfile):
            raise ValueError(f'Config file {configfile} does not exist.')

        parser = configparser.ConfigParser()
        parser.read(configfile)

        # Global Section
        self.append(parser[self.base_section])

        # Anything else
        sections = parser.sections()
        sections.remove(self.base_section)
        for s in sections:
            section = Section(s)
            section.append(parser[s])
            self.append(section)

    def __getattr__(self, item):
        return getattr(self._wrapped, item)

    def __setattr__(self, item, value):
        if WRAPPED_ITEM == item:
            self.__dict__[WRAPPED_ITEM] = value
            return

        setattr(self._wrapped, item, value)
