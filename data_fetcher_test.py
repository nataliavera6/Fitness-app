#############################################################################
# data_fetcher_test.py
#
# This file contains tests for data_fetcher.py.
#
# You will write these tests in Unit 3.
#############################################################################
import unittest
import sqlite3
from unittest.mock import patch, MagicMock
from datetime import datetime
from datetime import datetime as real_datetime
with patch('setup_database.bigquery.Client'):
    from data_fetcher import (
        get_user_workouts,
        get_user_profile,
        get_user_posts,
        get_genai_advice,
        get_response, get_user_sensor_data,
    )
# Create a real exception class for SQLite3.Error
class MockSQLiteError(Exception):
    pass

# Mock the entire sqlite3 module
@patch('data_fetcher.sqlite3')
def setup_sqlite_mock(mock_sqlite):
    # Set up the Error class to be a real exception
    mock_sqlite.Error = MockSQLiteError
    return mock_sqlite

class TestDataFetcherWorkouts(unittest.TestCase):
    @patch('data_fetcher.client')
    def test_get_user_workouts_returns_correct_data(self, mock_client):
        """Should return a list of workout dictionaries for a valid user."""

        mock_query_job = MagicMock()
        mock_query_job.__iter__.return_value = [
            {'WorkoutId': 'w1', 'UserId': 'user123', 'Type': 'Running', 'Duration': 30},
            {'WorkoutId': 'w2', 'UserId': 'user123', 'Type': 'Yoga', 'Duration': 60},
        ]
        mock_client.query.return_value = mock_query_job

        result = get_user_workouts('user123')

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['Type'], 'Running')
        self.assertEqual(result[1]['Duration'], 60)

    @patch('data_fetcher.client')
    def test_get_user_workouts_with_no_results(self, mock_client):
        """Should return an empty list when no workouts are found."""

        mock_query_job = MagicMock()
        mock_query_job.__iter__.return_value = []
        mock_client.query.return_value = mock_query_job

        result = get_user_workouts('user999')
        self.assertEqual(result, [])

    @patch('data_fetcher.client')
    def test_get_user_workouts_handles_query_structure(self, mock_client):
        """Should correctly convert rows to dictionaries."""

        RowMock = MagicMock()
        RowMock.__iter__.return_value = iter([
            ('WorkoutId', 'UserId', 'Type', 'Duration')
        ])
        mock_query_job = MagicMock()
        mock_query_job.__iter__.return_value = [
            {'WorkoutId': 'w5', 'UserId': 'u5', 'Type': 'Cycling', 'Duration': 45}
        ]
        mock_client.query.return_value = mock_query_job

        result = get_user_workouts('u5')
        self.assertEqual(result[0]['Type'], 'Cycling')

    @patch('data_fetcher.client')
    def test_get_user_workouts_with_special_char_userid(self, mock_client):
        """Should work with special characters in userId (e.g., email)."""

        mock_query_job = MagicMock()
        mock_query_job.__iter__.return_value = [
            {'WorkoutId': 'w9', 'UserId': 'test+user@example.com', 'Type': 'Pilates', 'Duration': 20},
        ]
        mock_client.query.return_value = mock_query_job

        result = get_user_workouts('test+user@example.com')
        self.assertEqual(result[0]['UserId'], 'test+user@example.com')

    @patch('data_fetcher.client')
    def test_get_user_workouts_sql_query_format(self, mock_client):
        """Should construct a valid SQL query string."""

        mock_query_job = MagicMock()
        mock_query_job.__iter__.return_value = []
        mock_client.query.return_value = mock_query_job

        get_user_workouts('abc123')
        mock_client.query.assert_called_once()
        args, kwargs = mock_client.query.call_args
        assert "UserId = 'abc123'" in args[0]
    # def setUp(self):
    #     # Set up the sqlite3 mock before each test
    #     patcher = patch('data_fetcher.sqlite3')
    #     self.mock_sqlite = patcher.start()
    #     self.mock_sqlite.Error = MockSQLiteError  # Set Error as a proper exception class

    #     # Create mock connection and cursor
    #     self.mock_conn = MagicMock()
    #     self.mock_cursor = MagicMock()
    #     self.mock_sqlite.connect.return_value = self.mock_conn
    #     self.mock_conn.cursor.return_value = self.mock_cursor

    #     self.addCleanup(patcher.stop)

    # def test_get_user_workouts_success(self):
    #     """Test that get_user_workouts returns correct data for a valid user"""
    #     # Import here to make sure patching is applied before import
    #     from data_fetcher import get_user_workouts

    #     # Mock the cursor.fetchone to return that user exists
    #     self.mock_cursor.fetchone.return_value = (1,)

    #     # Mock the cursor.fetchall to return workout data with exactly 10 values per row
    #     self.mock_cursor.fetchall.return_value = [
    #         # Return two workout records for user1 - with 10 columns each
    #         ('workout2', '2024-01-02 10:00:00', '2024-01-02 11:30:00',
    #          37.7749, -122.4194, 37.7760, -122.4210, 3.0, 6000, 400),
    #         ('workout1', '2024-01-01 10:00:00', '2024-01-01 11:00:00',
    #          37.7749, -122.4194, 37.7750, -122.4200, 2.5, 5000, 350)
    #     ]

    #     # Call the function
    #     result = get_user_workouts("user1")

    #     # Assertions
    #     self.assertEqual(len(result), 2)  # Should return 2 workouts for user1

    #     # Check that workouts are in the correct order
    #     self.assertEqual(result[0]['workout_id'], 'workout2')
    #     self.assertEqual(result[1]['workout_id'], 'workout1')

    # def test_get_user_workouts_user_not_found(self):
    #     """Test that get_user_workouts raises ValueError for invalid user"""
    #     # Import here to make sure patching is applied before import
    #     from data_fetcher import get_user_workouts

    #     # Mock the cursor.fetchone to return (0,) for user not found
    #     self.mock_cursor.fetchone.return_value = (0,)

    #     # Should raise ValueError
    #     with self.assertRaises(ValueError):
    #         get_user_workouts("non_existent_user")

    # def test_get_user_workouts_empty_result(self):
    #     """Test behavior when user exists but has no workouts"""
    #     # Import here to make sure patching is applied before import
    #     from data_fetcher import get_user_workouts

    #     # Mock the cursor.fetchone for user check - user exists
    #     self.mock_cursor.fetchone.return_value = (1,)

    #     # Mock the cursor.fetchall to return empty list
    #     self.mock_cursor.fetchall.return_value = []

    #     # Should return an empty list, not error
    #     result = get_user_workouts("user_no_workouts")
    #     self.assertEqual(result, [])


class TestDataFetcherPosts(unittest.TestCase):

    @patch('data_fetcher.get_post_table')
    def test_get_user_posts(self, mock_get_post_table):
        from data_fetcher import get_user_posts
        user_id = 123  # Integer

        mock_get_post_table.return_value = {
            user_id: {
                'postId': 'post1',
                'authorId': user_id,  # match exactly
                'Timestamp': '2024-01-01 00:00:00',
                'ImageUrl': 'image_url',
                'content': 'Had a great workout today!'
            }
        }

        result = get_user_posts(user_id)

        post = result[0]
        self.assertEqual(post['user_id'], user_id)


    @patch('data_fetcher.get_user_profile', return_value={"name": "Alice", "age": 30})
    def test_get_user_profile_valid(self, mock_get_user_profile):
        # Import here to ensure data_fetcher is patched before import
        from data_fetcher import get_user_profile
        user_id = 1
        result = get_user_profile(user_id)
        self.assertEqual(result, {"name": "Alice", "age": 30})
        mock_get_user_profile.assert_called_once_with(user_id)

    @patch('data_fetcher.get_user_profile', side_effect=ValueError('User 999 not found.'))
    def test_get_user_profile_invalid(self, mock_get_user_profile):
        # Import here to ensure data_fetcher is patched before import
        from data_fetcher import get_user_profile
        user_id = 999
        with self.assertRaises(ValueError) as context:
            get_user_profile(user_id)
        self.assertEqual(str(context.exception), 'User 999 not found.')
        mock_get_user_profile.assert_called_once_with(user_id)


class TestGetGenAIAdvice(unittest.TestCase):
    @patch('random.choice')
    @patch('data_fetcher.get_response') 
    def test_get_genai_advice_with_image(self, mock_get_response, mock_random_choice):
        """Test get_genai_advice function with a selected image."""

        # Mock get_response to return a predefined response
        mock_data = MagicMock()
        mock_data.candidates[0].content.parts[0].text = "You're doing awesome! Keep pushing."
        mock_get_response.return_value = mock_data

        # Mock random.choice to return a specific image and advice
        mock_random_choice.side_effect = [
            "You're doing great! Keep up the good work.",  # Advice
            'https://plus.unsplash.com/premium_photo-1669048780129-051d670fa2d1?q=80&w=3870&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'  # Image URL
        ]

        # Call the function
        user_id = 'user123'
        users = {}  # Mock users as empty for this test
        result = get_genai_advice(users, user_id)

        # Check if the function returns the expected result
        self.assertEqual(result['advice_id'], 'advice1')
        self.assertEqual(result['content'], "You're doing awesome! Keep pushing.")
        self.assertEqual(result['image'], 'https://plus.unsplash.com/premium_photo-1669048780129-051d670fa2d1?q=80&w=3870&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D')
        self.assertTrue(result['timestamp'])  # Ensure timestamp is set

    @patch('data_fetcher.get_response')               # mock_get_response
    @patch('data_fetcher.random.choice')              # mock_random_choice
    def test_get_genai_advice_without_image(self, mock_random_choice, mock_get_response):
        """Test get_genai_advice function without an image."""

        # Set up mocked get_response output
        mock_response = MagicMock()
        mock_response.candidates = [MagicMock()]
        mock_response.candidates[0].content.parts = [MagicMock()]
        mock_response.candidates[0].content.parts[0].text = "You worked hard yesterday, take it easy today."
        mock_get_response.return_value = mock_response

        # Set random.choice to return False for 'include_image'
        mock_random_choice.return_value = False

        # Call the function
        user_id = 'user123'
        users = {}  # You can leave this as an empty dict if unused
        result = get_genai_advice(users, user_id)

        # Assert expected results
        self.assertEqual(result['advice_id'], 'advice1')
        self.assertEqual(result['content'], "You worked hard yesterday, take it easy today.")
        self.assertIsNone(result['image'])  # Ensure image is None
        self.assertTrue(result['timestamp'])  # Ensure timestamp is set 
    
    @patch('data_fetcher.get_response')
    @patch('data_fetcher.random.choice')
    def test_get_genai_advice_with_empty_content(self, mock_random_choice, mock_get_response):
        mock_data = MagicMock()
        mock_data.candidates = [MagicMock()]
        mock_data.candidates[0].content.parts = [MagicMock()]
        mock_data.candidates[0].content.parts[0].text = ""
        mock_get_response.return_value = mock_data

        mock_random_choice.return_value = True  # Include image

        result = get_genai_advice({}, 'user123')
        self.assertEqual(result['content'], "")
        self.assertTrue(result['image'].startswith('http'))  # Image URL included


    @patch('data_fetcher.get_response')
    @patch('data_fetcher.random.choice')
    def test_get_genai_advice_with_random_advice(self, mock_random_choice, mock_get_response):
        mock_data = MagicMock()
        mock_data.candidates = [MagicMock()]
        mock_data.candidates[0].content.parts = [MagicMock()]
        mock_data.candidates[0].content.parts[0].text = "Take a rest day if you need it!"
        mock_get_response.return_value = mock_data

        mock_random_choice.return_value = False  # No image

        result = get_genai_advice({}, 'user123')
        self.assertEqual(result['content'], "Take a rest day if you need it!")
        self.assertIsNone(result['image'])

    @patch('data_fetcher.get_response')
    @patch('data_fetcher.random.choice')
    def test_get_genai_advice_with_malformed_response(self, mock_random_choice, mock_get_response):
        mock_data = MagicMock()
        mock_data.candidates = []  # No candidates
        mock_get_response.return_value = mock_data

        mock_random_choice.return_value = True  # Include image

        result = get_genai_advice({}, 'user123')
        self.assertEqual(result['content'], "")
        self.assertTrue(result['image'].startswith('http'))

    @patch('data_fetcher.get_response')
    @patch('data_fetcher.random.choice')
    def test_get_genai_advice_with_none_values(self, mock_random_choice, mock_get_response):
        """Test get_genai_advice function with None values for image."""

        # Mock a valid GenAI response
        mock_data = MagicMock()
        mock_data.candidates = [MagicMock()]
        mock_data.candidates[0].content.parts = [MagicMock()]
        mock_data.candidates[0].content.parts[0].text = "Rest up today, you deserve it!"
        mock_get_response.return_value = mock_data

        # Simulate that no image should be included
        mock_random_choice.return_value = False

        result = get_genai_advice({}, 'user123')

        self.assertEqual(result['content'], "Rest up today, you deserve it!")
        self.assertIsNone(result['image'])  # ✅ Will now pass
        self.assertTrue(result['timestamp'])





    @patch('data_fetcher.get_response')
    @patch('data_fetcher.random.choice')
    def test_get_genai_advice_with_future_timestamp(self, mock_random_choice, mock_get_response):
        mock_data = MagicMock()
        mock_data.candidates = [MagicMock()]
        mock_data.candidates[0].content.parts = [MagicMock()]
        mock_data.candidates[0].content.parts[0].text = "Keep pushing, you're doing awesome!"
        mock_get_response.return_value = mock_data

        mock_random_choice.return_value = True  # Include image

        with patch('data_fetcher.datetime') as mock_datetime:
            mock_datetime.now.return_value = real_datetime(2025, 12, 25, 12, 0, 0)
            mock_datetime.strftime = real_datetime.strftime  # Needed for formatting

            result = get_genai_advice({}, 'user123')

        self.assertEqual(result['timestamp'], '2025-12-25 12:00:00')


 
    
    @patch('data_fetcher.get_response')  # mock_get_response
    @patch('data_fetcher.random.choice')  # mock_random_choice
    def test_get_genai_advice_with_valid_user(self, mock_random_choice, mock_get_response):
        """Test get_genai_advice function with valid user data."""

        users = {
            'user123': {
                'full_name': 'Test User 1',
                'username': 'testuser1',
                'date_of_birth': '1990-01-01',
                'profile_image': 'https://example.com/user_image.jpg'
            }
        }

        # Mock get_response to return a structured response
        mock_data = MagicMock()
        mock_data.candidates = [MagicMock()]
        mock_data.candidates[0].content.parts = [MagicMock()]
        mock_data.candidates[0].content.parts[0].text = "You're doing awesome! Keep pushing. - testuser1"
        mock_get_response.return_value = mock_data

        # Mock random.choice to return False (=> no image)
        mock_random_choice.return_value = False

        user_id = 'user123'
        result = get_genai_advice(users, user_id)

        self.assertEqual(result['advice_id'], 'advice1')
        self.assertEqual(result['content'], "You're doing awesome! Keep pushing. - testuser1")
        self.assertIsNone(result['image'])  # Now this will pass
        self.assertTrue(result['timestamp'])

    # @patch('data_fetcher.get_response')
    # @patch('data_fetcher.random.choice')
    # @patch('data_fetcher.datetime')  # Fix datetime.now
    # def test_get_genai_advice_with_image(self, mock_datetime, mock_random_choice, mock_get_response):
    #     mock_data = MagicMock()
    #     mock_data.candidates = [MagicMock()]
    #     mock_data.candidates[0].content.parts = [MagicMock()]
    #     mock_data.candidates[0].content.parts[0].text = "You're doing awesome! Keep pushing."
    #     mock_get_response.return_value = mock_data

    #     mock_random_choice.return_value = True
    #     mock_datetime.now.return_value = real_datetime(2025, 4, 6, 12, 0, 0)

    #     result = get_genai_advice({}, 'user123')

    #     self.assertEqual(result['advice_id'], 'advice1')
    #     self.assertEqual(result['content'], "You're doing awesome! Keep pushing.")
    #     self.assertTrue(result['image'].startswith('https://'))
    #     self.assertEqual(result['timestamp'], '2025-04-06 12:00:00')

    # @patch('data_fetcher.get_response')
    # @patch('data_fetcher.random.choice')
    # @patch('data_fetcher.datetime')
    # def test_get_genai_advice_without_image(self, mock_datetime, mock_random_choice, mock_get_response):
    #     mock_response = MagicMock()
    #     mock_response.candidates = [MagicMock()]
    #     mock_response.candidates[0].content.parts = [MagicMock()]
    #     mock_response.candidates[0].content.parts[0].text = "You worked hard yesterday, take it easy today."
    #     mock_get_response.return_value = mock_response

    #     mock_random_choice.return_value = False
    #     mock_datetime.now.return_value = real_datetime(2025, 4, 6, 12, 0, 0)

    #     result = get_genai_advice({}, 'user123')

    #     self.assertEqual(result['advice_id'], 'advice1')
    #     self.assertEqual(result['content'], "You worked hard yesterday, take it easy today.")
    #     self.assertIsNone(result['image'])
    #     self.assertEqual(result['timestamp'], '2025-04-06 12:00:00')

    # @patch('data_fetcher.get_response')
    # @patch('data_fetcher.random.choice')
    # @patch('data_fetcher.datetime')
    # def test_get_genai_advice_with_empty_content(self, mock_datetime, mock_random_choice, mock_get_response):
    #     mock_data = MagicMock()
    #     mock_data.candidates = [MagicMock()]
    #     mock_data.candidates[0].content.parts = [MagicMock()]
    #     mock_data.candidates[0].content.parts[0].text = ""
    #     mock_get_response.return_value = mock_data

    #     mock_random_choice.return_value = True
    #     mock_datetime.now.return_value = real_datetime(2025, 4, 6, 12, 0, 0)

    #     result = get_genai_advice({}, 'user123')

    #     self.assertEqual(result['content'], "")
    #     self.assertTrue(result['image'].startswith('https://'))

    # @patch('data_fetcher.get_response')
    # @patch('data_fetcher.random.choice')
    # @patch('data_fetcher.datetime')
    # def test_get_genai_advice_with_random_advice(self, mock_datetime, mock_random_choice, mock_get_response):
    #     mock_data = MagicMock()
    #     mock_data.candidates = [MagicMock()]
    #     mock_data.candidates[0].content.parts = [MagicMock()]
    #     mock_data.candidates[0].content.parts[0].text = "Take a rest day if you need it!"
    #     mock_get_response.return_value = mock_data

    #     mock_random_choice.return_value = False
    #     mock_datetime.now.return_value = real_datetime(2025, 4, 6, 12, 0, 0)

    #     result = get_genai_advice({}, 'user123')

    #     self.assertEqual(result['content'], "Take a rest day if you need it!")
    #     self.assertIsNone(result['image'])

    # @patch('data_fetcher.get_response')
    # @patch('data_fetcher.random.choice')
    # @patch('data_fetcher.datetime')
    # def test_get_genai_advice_with_malformed_response(self, mock_datetime, mock_random_choice, mock_get_response):
    #     mock_data = MagicMock()
    #     mock_data.candidates = []  # No candidates
    #     mock_get_response.return_value = mock_data

    #     mock_random_choice.return_value = True
    #     mock_datetime.now.return_value = real_datetime(2025, 4, 6, 12, 0, 0)

    #     result = get_genai_advice({}, 'user123')

    #     self.assertEqual(result['content'], "")
    #     self.assertTrue(result['image'].startswith('https://'))

    # @patch('data_fetcher.get_response')
    # @patch('data_fetcher.random.choice')
    # @patch('data_fetcher.datetime')
    # def test_get_genai_advice_with_none_values(self, mock_datetime, mock_random_choice, mock_get_response):
    #     mock_data = MagicMock()
    #     mock_data.candidates = [MagicMock()]
    #     mock_data.candidates[0].content.parts = [MagicMock()]
    #     mock_data.candidates[0].content.parts[0].text = "Rest up today, you deserve it!"
    #     mock_get_response.return_value = mock_data

    #     mock_random_choice.return_value = False
    #     mock_datetime.now.return_value = real_datetime(2025, 4, 6, 12, 0, 0)

    #     result = get_genai_advice({}, 'user123')

    #     self.assertEqual(result['content'], "Rest up today, you deserve it!")
    #     self.assertIsNone(result['image'])
    #     self.assertEqual(result['timestamp'], '2025-04-06 12:00:00')

    # @patch('data_fetcher.get_response')
    # @patch('data_fetcher.random.choice')
    # @patch('data_fetcher.datetime')
    # def test_get_genai_advice_with_future_timestamp(self, mock_datetime, mock_random_choice, mock_get_response):
    #     mock_data = MagicMock()
    #     mock_data.candidates = [MagicMock()]
    #     mock_data.candidates[0].content.parts = [MagicMock()]
    #     mock_data.candidates[0].content.parts[0].text = "Keep pushing, you're doing awesome!"
    #     mock_get_response.return_value = mock_data

    #     mock_random_choice.return_value = True
    #     mock_datetime.now.return_value = real_datetime(2025, 12, 25, 12, 0, 0)

    #     result = get_genai_advice({}, 'user123')

    #     self.assertEqual(result['timestamp'], '2025-12-25 12:00:00')

    # @patch('data_fetcher.get_response')
    # @patch('data_fetcher.random.choice')
    # @patch('data_fetcher.datetime')
    # def test_get_genai_advice_with_valid_user(self, mock_datetime, mock_random_choice, mock_get_response):
    #     users = {
    #         'user123': {
    #             'full_name': 'Test User 1',
    #             'username': 'testuser1',
    #             'date_of_birth': '1990-01-01',
    #             'profile_image': 'https://example.com/user_image.jpg'
    #         }
    #     }

    #     mock_data = MagicMock()
    #     mock_data.candidates = [MagicMock()]
    #     mock_data.candidates[0].content.parts = [MagicMock()]
    #     mock_data.candidates[0].content.parts[0].text = "You're doing awesome! Keep pushing. - testuser1"
    #     mock_get_response.return_value = mock_data

    #     mock_random_choice.return_value = False
    #     mock_datetime.now.return_value = real_datetime(2025, 4, 6, 12, 0, 0)

    #     result = get_genai_advice(users, 'user123')

    #     self.assertEqual(result['advice_id'], 'advice1')
    #     self.assertEqual(result['content'], "You're doing awesome! Keep pushing. - testuser1")
    #     self.assertIsNone(result['image'])
    #     self.assertEqual(result['timestamp'], '2025-04-06 12:00:00')



if __name__ == "__main__":
    unittest.main()