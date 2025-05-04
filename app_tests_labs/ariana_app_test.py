import unittest
from unittest.mock import patch
from modules import display_activity_summary
'''
class TestDisplayActivitySummary(unittest.TestCase):
    """Mocked tests for display_activity_summary (only mocking UI)."""
    
    @patch("modules.create_component")
    def test_no_workouts(self, mock_create_component):
        workouts = []
        display_activity_summary(workouts)
        mock_create_component.assert_called()

    @patch("modules.create_component")
    def test_valid_single_workout(self, mock_create_component):
        workouts = [
            {
                "start_timestamp": "2025-03-08 07:00:00",
                "end_timestamp": "2025-03-08 07:45:00",
                "distance": 3.0,
                "steps": 5000,
                "calories_burned": 300,
            }
        ]
        display_activity_summary(workouts)
        mock_create_component.assert_called()

    @patch("modules.create_component")
    def test_multiple_workouts(self, mock_create_component):
        workouts = [
            {
                "start_timestamp": "2025-03-08 06:00:00",
                "end_timestamp": "2025-03-08 06:30:00",
                "distance": 2.0,
                "steps": 4000,
                "calories_burned": 250,
            },
            {
                "start_timestamp": "2025-03-08 18:00:00",
                "end_timestamp": "2025-03-08 18:45:00",
                "distance": 4.0,
                "steps": 7000,
                "calories_burned": 400,
            }
        ]
        display_activity_summary(workouts)
        mock_create_component.assert_called()

    @patch("modules.create_component")
    def test_invalid_workout_format(self, mock_create_component):
        # Should not raise an error — just render with default or no data
        display_activity_summary([{"invalid_key": "oops"}])
        mock_create_component.assert_called()
        



if __name__ == "__main__":
    unittest.main()
'''
