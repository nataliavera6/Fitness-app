import unittest
from unittest.mock import patch
from modules import display_recent_workouts

class TestDisplayRecentWorkouts(unittest.TestCase):
    """Tests the display_recent_workouts function."""

    @patch("modules.create_component")
    def test_display_single_workout(self, mock_create_component):
        """Tests display_recent_workouts with a single workout entry."""
        # Define mock workout data
        mock_workout = [
            {
                "start_timestamp": "2025-03-06 08:00:00",
                "end_timestamp": "2025-03-06 08:30:00",
                "distance": 2.2,
                "steps": 6200,
                "calories_burned": 320,
                "start_lat_lng": (1.23, 4.56),
                "end_lat_lng": (1.25, 4.58),
            }
        ]
        
        # Call the function
        display_recent_workouts(mock_workout)
        
        # Verify create_component was called
        mock_create_component.assert_called_once()

    @patch("modules.create_component")
    def test_display_multiple_workouts(self, mock_create_component):
        """Tests display_recent_workouts with multiple workout entries."""
        # Define mock workouts data
        mock_workouts = [
            {
                "start_timestamp": "2025-03-06 08:00:00",
                "end_timestamp": "2025-03-06 08:30:00",
                "distance": 2.2,
                "steps": 6200,
                "calories_burned": 320,
                "start_lat_lng": (1.23, 4.56),
                "end_lat_lng": (1.25, 4.58),
            },
            {
                "start_timestamp": "2025-03-07 07:30:00",
                "end_timestamp": "2025-03-07 08:15:00",
                "distance": 3.0,
                "steps": 7500,
                "calories_burned": 400,
                "start_lat_lng": (1.30, 4.60),
                "end_lat_lng": (1.35, 4.65),
            }
        ]
        
        # Call the function
        display_recent_workouts(mock_workouts)
        
        # Verify create_component was called
        mock_create_component.assert_called_once()

    @patch("modules.create_component")
    def test_display_no_workouts(self, mock_create_component):
        """Tests display_recent_workouts with an empty list."""
        # Call the function with empty list
        display_recent_workouts([])
        
        # Verify create_component was called
        mock_create_component.assert_called_once()

    @patch("modules.create_component")
    def test_display_invalid_data(self, mock_create_component):
        """Tests display_recent_workouts with improperly formatted data."""
        # Test with invalid data
        workouts = [
            {
                "start_timestamp": "invalid_time",
                "end_timestamp": "another_invalid_time",
                "distance": "not_a_number",
                "steps": "also_not_a_number",
                "calories_burned": None,
                "start_lat_lng": "invalid_location",
                "end_lat_lng": "invalid_location",
            }
        ]
        
        # Call the function
        display_recent_workouts(workouts)
        
        # Verify create_component was called
        mock_create_component.assert_called_once()

if __name__ == "__main__":
    unittest.main()