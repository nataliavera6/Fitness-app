import unittest
from unittest.mock import patch
from datetime import datetime
from modules import display_genai_advice
from modules import create_component




class TestDisplayGenAIAdvice(unittest.TestCase):
    """Tests the display_genai_advice function."""

    @patch("modules.create_component")
    def test_display_with_image(self, mock_create_component):
        """Tests display_genai_advice with an image."""
        # Define mock input data
        mock_data = {
            'TIME': datetime(2025, 3, 9, 12, 0, 0).strftime('%Y-%m-%d %H:%M:%S'),
            'CONTENT': 'Test advice message with image',
            'IMAGE': 'https://example.com/test_image.jpg'
        }

        # Call the function
        display_genai_advice(mock_data['TIME'], mock_data['CONTENT'], mock_data['IMAGE'])
        
        # Verify create_component was called
        mock_create_component.assert_called_once()

    @patch("modules.create_component")
    def test_display_without_image(self, mock_create_component):
        """Tests display_genai_advice without an image."""
        # Define mock input data
        mock_data = {
            'TIME': datetime(2025, 3, 9, 12, 0, 0).strftime('%Y-%m-%d %H:%M:%S'),
            'CONTENT': 'Test advice message without image',
            'IMAGE': None
        }

        # Call the function
        display_genai_advice(mock_data['TIME'], mock_data['CONTENT'], mock_data['IMAGE'])
        
        # Verify create_component was called
        mock_create_component.assert_called_once()

    @patch("modules.create_component")
    def test_display_empty_content(self, mock_create_component):
        """Tests display_genai_advice with empty content."""
        # Define mock input data
        mock_data = {
            'TIME': datetime(2025, 3, 9, 12, 0, 0).strftime('%Y-%m-%d %H:%M:%S'),
            'CONTENT': '',
            'IMAGE': 'https://example.com/test_image.jpg'
        }

        # Call the function
        display_genai_advice(mock_data['TIME'], mock_data['CONTENT'], mock_data['IMAGE'])
        
        # Verify create_component was called
        mock_create_component.assert_called_once()

    @patch("modules.create_component")
    def test_display_long_content(self, mock_create_component):
        """Tests display_genai_advice with a very long content string."""
        # Define mock input data with long content
        mock_data = {
            'TIME': datetime(2025, 3, 9, 12, 0, 0).strftime('%Y-%m-%d %H:%M:%S'),
            'CONTENT': "A" * 5000,  # 5000 characters long
            'IMAGE': 'https://example.com/test_image.jpg'
        }

        # Call the function
        display_genai_advice(mock_data['TIME'], mock_data['CONTENT'], mock_data['IMAGE'])
        
        # Verify create_component was called
        mock_create_component.assert_called_once()

    @patch("modules.create_component")
    def test_display_invalid_timestamp(self, mock_create_component):
        """Tests display_genai_advice with an invalid timestamp."""
        # Define mock input data with invalid timestamp
        mock_data = {
            'TIME': "invalid_timestamp",
            'CONTENT': 'Test advice with invalid timestamp',
            'IMAGE': None
        }

        # Call the function
        display_genai_advice(mock_data['TIME'], mock_data['CONTENT'], mock_data['IMAGE'])
        
        # Verify create_component was called
        mock_create_component.assert_called_once()

    @patch("modules.create_component")
    def test_display_none_timestamp(self, mock_create_component):
        """Tests display_genai_advice with None as timestamp."""
        # Define mock input data with None as timestamp
        mock_data = {
            'TIME': None,
            'CONTENT': 'Test advice with None timestamp',
            'IMAGE': 'https://example.com/test_image.jpg'
        }

        # Call the function
        display_genai_advice(mock_data['TIME'], mock_data['CONTENT'], mock_data['IMAGE'])
        
        # Verify create_component was called
        mock_create_component.assert_called_once()

if __name__ == "__main__":
    unittest.main()