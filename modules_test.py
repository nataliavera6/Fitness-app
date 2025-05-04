import unittest
from datetime import datetime
from unittest.mock import patch
from modules import display_post, display_activity_summary, display_genai_advice, display_recent_workouts

class TestDisplayPost(unittest.TestCase):
    """Tests the display_post function with mocking."""

    @patch("modules.create_component")
    def test_display_with_image(self, mock_create):
        display_post("test_user", "test_user_image.jpg", "2023-11-15 12:00:00", "Test post with image", "test_post_image.jpg")
        mock_create.assert_called()

    @patch("modules.create_component")
    def test_display_without_image(self, mock_create):
        display_post("test_user2", "test_user2_image.jpg", "2023-11-16 14:30:00", "Test post without image", None)
        mock_create.assert_called()

    @patch("modules.create_component")
    def test_empty_content(self, mock_create):
        display_post("test_user3", "test_user3_image.jpg", "2023-11-17 16:00:00", "", "test_empty_content_image.jpg")
        mock_create.assert_called()

    @patch("modules.create_component")
    def test_long_content(self, mock_create):
        long_text = "This is a very long text " * 50
        display_post("test_user4", "test_user4_image.jpg", "2023-11-18 18:30:00", long_text, None)
        mock_create.assert_called()

    @patch("modules.create_component")
    def test_special_characters(self, mock_create):
        display_post("test_user5", "test_user5_image.jpg", "2023-11-19 20:00:00", "Content with special characters: !@#$%^&*()_+", None)
        mock_create.assert_called()

    @patch("modules.create_component")
    def test_timestamp_string(self, mock_create):
        display_post("test_user6", "test_user6_image.jpg", "2024-01-01 12:00:00", "test string timestamp", None)
        mock_create.assert_called()


class TestDisplayGenAiAdvice(unittest.TestCase):
    """Tests the display_genai_advice function with mocking."""

    @patch("modules.create_component")
    def test_display_with_image(self, mock_create):
        display_genai_advice("2025-03-09 12:00:00", "Test advice message with image", "https://example.com/test_image.jpg")
        mock_create.assert_called()

    @patch("modules.create_component")
    def test_display_without_image(self, mock_create):
        display_genai_advice("2025-03-09 12:00:00", "Test advice message without image", None)
        mock_create.assert_called()

    @patch("modules.create_component")
    def test_display_empty_content(self, mock_create):
        display_genai_advice("2025-03-09 12:00:00", "", "https://example.com/test_image.jpg")
        mock_create.assert_called()

    @patch("modules.create_component")
    def test_display_long_content(self, mock_create):
        long_content = "A" * 5000
        display_genai_advice("2025-03-09 12:00:00", long_content, "https://example.com/test_image.jpg")
        mock_create.assert_called()

    @patch("modules.create_component")
    def test_display_invalid_timestamp(self, mock_create):
        display_genai_advice("invalid_timestamp", "Test advice with invalid timestamp", None)
        mock_create.assert_called()

    @patch("modules.create_component")
    def test_display_none_timestamp(self, mock_create):
        display_genai_advice(None, "Test advice with None timestamp", "https://example.com/test_image.jpg")
        mock_create.assert_called()


class TestDisplayRecentWorkouts(unittest.TestCase):
    """Tests the display_recent_workouts function with mocking."""

    @patch("modules.create_component")
    def test_display_single_workout(self, mock_create):
        workouts = [{
            "start_timestamp": "2025-03-06 08:00:00",
            "end_timestamp": "2025-03-06 08:30:00",
            "distance": 2.2,
            "steps": 6200,
            "calories_burned": 320,
            "start_lat_lng": (1.23, 4.56),
            "end_lat_lng": (1.25, 4.58),
        }]
        display_recent_workouts(workouts)
        mock_create.assert_called()

    @patch("modules.create_component")
    def test_display_multiple_workouts(self, mock_create):
        workouts = [
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
        display_recent_workouts(workouts)
        mock_create.assert_called()

    @patch("modules.create_component")
    def test_display_no_workouts(self, mock_create):
        display_recent_workouts([])
        mock_create.assert_called()

    @patch("modules.create_component")
    def test_display_invalid_data(self, mock_create):
        workouts = [{
            "start_timestamp": "invalid_time",
            "end_timestamp": "invalid_time",
            "distance": "bad",
            "steps": "bad",
            "calories_burned": None,
            "start_lat_lng": "invalid",
            "end_lat_lng": "invalid",
        }]
        display_recent_workouts(workouts)
        mock_create.assert_called()

'''
class TestDisplayActivitySummary(unittest.TestCase):
    """Tests the display_activity_summary function with mocking."""

    @patch("modules.create_component")
    def test_empty_workouts(self, mock_create):
        display_activity_summary([])
        mock_create.assert_called()

    @patch("modules.create_component")
    def test_invalid_workout_entry(self, mock_create):
        invalid_workouts = [{"invalid_key": "some_value"}]
        display_activity_summary(invalid_workouts)

        mock_create.assert_called_with({
            "Total Steps": 0,
            "Total Distance (mi)": 0,
            "Total Calories Burned": 0
        }, "display_activity_summary")

    @patch("modules.create_component")
    def test_single_workout(self, mock_create):
        workouts = [{
            "start_timestamp": "2025-03-08 07:00:00",
            "end_timestamp": "2025-03-08 07:45:00",
            "distance": 3.0,
            "steps": 5000,
            "calories_burned": 300,
        }]
        display_activity_summary(workouts)
        mock_create.assert_called()

    @patch("modules.create_component")
    def test_multiple_workouts(self, mock_create):
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
        mock_create.assert_called()
'''

if __name__ == "__main__":
    unittest.main()
