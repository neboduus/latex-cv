import unittest

from chat_parser import ChatParser
from utils import get_test_case


class TestClient(unittest.TestCase):
    maxDiff = None
    parser = ChatParser()

    def test_step_1(self):
        self.assert_test_case('step_1')

    def test_step_2(self):
        self.assert_test_case('step_2')

    def test_step_3(self):
        self.assert_test_case('step_3')

    def test_step_4(self):
        self.assert_test_case('step_4')

    def test_step_5(self):
        self.assert_test_case('step_5')

    def test_step_6(self):
        self.assert_test_case('step_6')

    def test_step_7(self):
        self.assert_test_case('step_7')

    def assert_test_case(self, test_step):
        test_case = get_test_case(test_step)
        output = self.parser.parse_chat(test_case['input'])
        self.assertEqual(test_case['output'], output)
