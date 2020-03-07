# -*- coding:utf-8 -*-
import os
import unittest
from xini import Settings, Section


class ConfigObject:
    SOME_CONFIG_KEY = 'some-value'


class TestSettings(unittest.TestCase):

    def setUp(self) -> None:
        self.test_dir = os.path.dirname(__file__)
        self.configfile = os.path.join(self.test_dir, 'case_files', 'config.ini')

        self.config_object = ConfigObject()
        self.config_mapping = {
            'key1': 'value1',
            'key-some-custom': 'value2'
        }

    def test_from_object(self):
        conf = Section(__name__)
        conf.from_object(self.config_object)

        self.assertEqual(self.config_object.SOME_CONFIG_KEY, conf.SOME_CONFIG_KEY)

    def test_from_mapping(self):
        conf = Section(__name__)
        conf.from_mapping(self.config_mapping)

        self.assertEqual(self.config_mapping['key1'], conf.KEY1)
        self.assertEqual(self.config_mapping['key-some-custom'], conf.KEY_SOME_CUSTOM)

    def test_append(self):
        conf = Section(__name__)
        conf_sub = Section('sub')

        conf.from_object(self.config_object)
        conf.append('value1', 'some-key')

        conf_sub.append(self.config_mapping)
        conf.append(conf_sub)

        self.assertEqual('value1', conf.SOME_KEY)
        self.assertEqual(self.config_mapping['key1'], conf.SUB.KEY1)
        self.assertEqual(self.config_mapping['key-some-custom'], conf.SUB.KEY_SOME_CUSTOM)

    def test_configfile(self):
        conf = Settings(self.configfile, base_section='base')

        self.assertEqual('user-defined-value', conf.USER_DEFINED_KEY)

        # Nested
        self.assertEqual('user-defined-value-2', conf.LISTENER.USER_DEFINED_KEY_2)

        # Array
        self.assertEqual(['value1', 'value2', 'value3'], conf.LISTENER.ITERABLE_VALUES)

        # Boolean
        self.assertFalse(conf.LISTENER.BOOLEAN_VALUE)

        # JSON formatted.
        self.assertEqual({
            'a': True,
            'b': 1,
            'c': ['a', 'b'],
            'd': None
        }, conf.LISTENER.JSON_OBJECT)
