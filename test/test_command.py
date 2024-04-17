import unittest
from cmdcompass.models.Command import Command, Tag

class TestCommand(unittest.TestCase):
    def setUp(self):
        self.tag1 = Tag("Network", "blue")
        self.tag2 = Tag("Database", "green")
        self.command = Command(
            command_str="ping {{ host  }} -c {{count}}",
            description="Ping a host",
            tags=[self.tag1, self.tag2],
        )

    def test_parse_command_success(self):
        replacements = {"host": "google.com", "count": "4"}
        parsed_command = self.command.parse_command(replacements)
        self.assertEqual(parsed_command, "ping google.com -c 4")

    def test_parse_command_missing_variable(self):
        replacements = {"host": "google.com"}  # Missing 'count', so fail
        with self.assertRaises(ValueError) as context:
            self.command.parse_command(replacements)
        self.assertEqual(str(context.exception), "Variable 'count' not found in replacements")

    def test_parse_command_extra_spaces(self):
        replacements = {"host": "google.com", "count": "4"}
        command_with_spaces = Command(
            command_str="ping {{  host }} -c {{ count     }}", 
            description="Ping a host", 
            tags=[]
        )
        parsed_command = command_with_spaces.parse_command(replacements)
        self.assertEqual(parsed_command, "ping google.com -c 4")

if __name__ == "__main__":
    unittest.main()