import io
import unittest
from unittest import mock
from unittest.mock import patch
import json

from PSSController import *

input_read_set1 = ["8", "Set1.json"]
input_delete_intern = ["6", "Intern Interview"]
input_add_intern = ["1", "Intern Interview", "Appointment", "17", "2.5", "20200427", "", "", ""]
input_add_movie = ["1", "Watch a movie", "Movie", "21.5", "2", "20200429", "", "", ""]
input_add_movie2 = ["1", "Watch a movie", "Visit", "18.5", "2", "20200430", "", "",  ""]
input_read_set2 = ["8", "Set2.json"]
input_exit = ["0"]

# Input for only Scenario 1.1
input_1_1_1 = input_read_set1 + input_exit
# Input for Scenario 1.1 to 1.2
input_1_1_2 = input_1_1_1[:-1] + input_delete_intern + input_exit
# Input for Scenario 1.1 to 1.3
input_1_1_3 = input_1_1_2[:-1] + input_add_intern + input_exit
# Input for Scenario 1.1 to 1.4
input_1_1_4 = input_1_1_3[:-1] + input_add_movie + input_exit
# Input for Scenario 1.1 to 1.5
input_1_1_5 = input_1_1_4[:-1] + input_add_movie2 + input_exit
# Input for Scenario 1.1 to 1.6
input_1_1_6 = input_1_1_5[:-1] + input_read_set2 + input_exit


class TestPSSController(unittest.TestCase):
    def setUp(self) -> None:
        self.controller = PSSController()

    @staticmethod
    def set1_json_length():
        with open("Set1.json") as set1_json:
            set1 = json.load(set1_json)
            return len(set1)

    def current_task_list_length(self):
        return len(self.controller.schedule.tasks)

    @patch('builtins.input', side_effect=input_1_1_1)
    def testScenario1_1(self, mock_inputs):
        """Test Scenario1.txt up to 1.1, Read file"""
        with mock.patch('sys.stdout', new=io.StringIO()) as std_out:
            self.controller.menu_and_act_loop()

        # Verify Set1 JSON is loaded
        with open("Set1.json") as set1_json:
            # Manually load json file
            set1 = json.load(set1_json)
            # Check actual loaded tasks
            set2 = [json.loads(task.to_json()) for task in self.controller.schedule.tasks]
            # JSON file and added task should be the same
            self.assertEqual(set1, set2)

        self.assertIn("Schedule loaded from file successfully", std_out.getvalue())

    @patch('builtins.input', side_effect=input_1_1_2)
    def testScenario1_2(self, mock_inputs):
        """Test Scenario1.txt up to 1.2, Delete Task"""
        with mock.patch('sys.stdout', new=io.StringIO()) as std_out:
            self.controller.menu_and_act_loop()

        # Schedule should be 1 less in length
        self.assertEqual(self.current_task_list_length(), self.set1_json_length() - 1)

        self.assertIn("Task deleted successfully!", std_out.getvalue())

    @patch('builtins.input', side_effect=input_1_1_3)
    def testScenario1_3(self, mock_inputs):
        """Test Scenario1.txt up to 1.3, Add new Task"""
        with mock.patch('sys.stdout', new=io.StringIO()) as std_out:
            self.controller.menu_and_act_loop()

        # Schedule should be same length again (remove 1, added 1)
        self.assertEqual(self.current_task_list_length(), self.set1_json_length())

        # Test success notification
        self.assertIn("Task deleted successfully!", std_out.getvalue())

    @patch('builtins.input', side_effect=input_1_1_4)
    def testScenario1_4(self, mock_inputs):
        """Test Scenario1.txt up to 1.4, Add new Task fail"""
        with mock.patch('sys.stdout', new=io.StringIO()) as std_out:
            self.controller.menu_and_act_loop()

        # Schedule should be same length again (remove 1, added 1, fail to add 1)
        self.assertEqual(self.current_task_list_length(), self.set1_json_length())

        self.assertIn("Failed to add task", std_out.getvalue())

    @patch('builtins.input', side_effect=input_1_1_5)
    def testScenario1_5(self, mock_inputs):
        """Test Scenario1.txt up to 1.5, Add new Task fail"""
        with mock.patch('sys.stdout', new=io.StringIO()) as std_out:
            self.controller.menu_and_act_loop()

        # Schedule should be same length again (remove 1 added 1, fail to add 2 times)
        self.assertEqual(self.current_task_list_length(), self.set1_json_length())

        # By step 5 we have failed to add tasks twice
        self.assertEqual(2, std_out.getvalue().count("Failed to add task to the schedule"))

    @patch('builtins.input', side_effect=input_1_1_6)
    def testScenario1_6(self, mock_inputs):
        """Test Scenario1.txt up to 1.6, Fail to read Set2"""
        with mock.patch('sys.stdout', new=io.StringIO()) as std_out:
            self.controller.menu_and_act_loop()

        # Schedule should be same length again (remove 1 added 1, fail to add 2, failed to read Set2)
        self.assertEqual(self.current_task_list_length(), self.set1_json_length())

        # TODO PSS crashes with TaskOverlapException, once handled update this test!
        # Test success notification
        self.assertTrue(False)  # TODO Remove this when a fail message is added
        # Currently there is no fail message, This always fails
        self.assertIn("Fail Message For Reading File", std_out.getvalue())


if __name__ == '__main__':
    unittest.main()
