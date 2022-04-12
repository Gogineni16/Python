"""Tests for core commands"""
import os
import unittest
from pathlib import Path
from uuid import uuid1

from user import User

user = User(str(uuid1()), str(uuid1()))
user.register()


class UserTest(unittest.TestCase):
    """TestCase for core commands"""
    def test_ls(self):
        """tests list command"""
        self.assertEqual(str(os.listdir(user.curr_dir)), user.ls())

    def test_read_write(self):
        """first tests write command, then read command"""
        user.file_append('test.txt', 'Testing Write Content')
        self.assertEqual(
            (user.curr_dir / 'test.txt').read_text(), 'Testing Write Content')

    def test_mkdir_cd(self):
        """first tests mkdir command, then cd command"""
        user.mkdir('test_folder')
        self.assertTrue((user.curr_dir / 'test_folder').exists())

        # Just for copying did this
        prev_dir = Path(str(user.curr_dir))

        user.cd('test_folder')
        self.assertEqual(prev_dir / 'test_folder', user.curr_dir)


unittest.main()
