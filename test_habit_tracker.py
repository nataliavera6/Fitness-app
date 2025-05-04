import unittest
from unittest.mock import patch
import habit_tracker
import habit_tracker
from datetime import date, timedelta
import streamlit as st


class TestHabitTracker(unittest.TestCase):
    user = "user1"

    #Implemented using GenAI
    def setUp(self):
        # Reset habit data before each test
        # Access the globals directly from the habit_tracker module
        habit_tracker.user_habits_data = {}
        habit_tracker.next_habit_id = 1
    #Implemented using GenAI
    def tearDown(self):
        # Clean up any habits created during the test
        habits = habit_tracker.get_habits(self.user)
        if habits:
            for habit in habits:
                habit_tracker.delete_habit(self.user, habit['habit_id'])

    # Testing Basic Functionality
    def test_add_habit(self):
        result = habit_tracker.add_habit(self.user, "Exercise", "30 minute workout", "daily")
        self.assertTrue(result)
        self.assertEqual(len(habit_tracker.get_habits(self.user)), 1)
        self.assertEqual(habit_tracker.get_habits(self.user)[0]['name'], "Exercise")
        self.assertEqual(habit_tracker.get_habits(self.user)[0]['description'], "30 minute workout")
        self.assertEqual(habit_tracker.get_habits(self.user)[0]['frequency'], "daily")

    def test_edit_habit(self):
        habit_tracker.add_habit(self.user, "Exercise", "30 minute workout", "daily")
        result = habit_tracker.edit_habit(self.user, 1, "Swimming", "20 Minutes", "Daily")
        self.assertTrue(result)
        self.assertEqual(habit_tracker.get_habits(self.user)[0]['name'], "Swimming")
        self.assertEqual(habit_tracker.get_habits(self.user)[0]['description'], "20 Minutes")
        self.assertEqual(habit_tracker.get_habits(self.user)[0]['frequency'], "Daily")

    def test_delete_habit(self):
        habit_tracker.add_habit(self.user, "Exercise", "30 minute workout", "daily")
        result = habit_tracker.delete_habit(self.user, 1)
        self.assertTrue(result)
        self.assertEqual(len(habit_tracker.get_habits(self.user)),0)

    def test_get_habits(self):
        habit_tracker.add_habit(self.user, "Exercise", "30 minute workout", "daily")
        result = habit_tracker.get_habits(self.user)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['name'], "Exercise")
        self.assertEqual(result[0]['description'], "30 minute workout")
        self.assertEqual(result[0]['frequency'], "daily")

    @patch('habit_tracker.st')
    def test_complete_habit(self, mock_st):
        habit_tracker.add_habit(self.user, "Exercise", "30 minute workout", "daily")
        today_str = str(date.today())
        result = habit_tracker.complete_habit(self.user, 1, today_str)
        self.assertTrue(result)

    def test_get_habit_completions(self):
        habit_tracker.add_habit(self.user, "Exercise", "30 minute workout", "daily")
        today_str = str(date.today())
        habit_tracker.complete_habit(self.user, 1, today_str)
        result = habit_tracker.get_habit_completions(self.user, 1)
        self.assertEqual(result, [today_str])
    #Implemented using GenAI
    def test_current_streak(self):
        habit_tracker.add_habit(self.user, "Exercise", "30 minute workout", "daily")
        today = date.today()
        yesterday = today - timedelta(days=1)
        two_days_ago = today - timedelta(days=2)
        habit_tracker.complete_habit(self.user, 1, str(today))
        habit_tracker.complete_habit(self.user, 1, str(yesterday))
        habit_tracker.complete_habit(self.user, 1, str(two_days_ago))
        streak = habit_tracker.get_current_streak(self.user, 1)
        self.assertEqual(streak, 3)
    #Implemented using GenAI
    def test_longest_streak(self):
        habit_tracker.add_habit(self.user, "Exercise", "30 minute workout", "daily")
        today = date.today()
        yesterday = today - timedelta(days=1)
        two_days_ago = today - timedelta(days=2)
        four_days_ago = today - timedelta(days=4)
        five_days_ago = today - timedelta(days=5)
        habit_tracker.complete_habit(self.user, 1, str(today))
        habit_tracker.complete_habit(self.user, 1, str(yesterday))
        habit_tracker.complete_habit(self.user, 1, str(two_days_ago))
        habit_tracker.complete_habit(self.user, 1, str(four_days_ago))
        habit_tracker.complete_habit(self.user, 1, str(five_days_ago))
        longest_streak = habit_tracker.get_longest_streak(self.user, 1)
        self.assertEqual(longest_streak, 3)

    def test_add_duplicate_habit(self):
        habit_tracker.add_habit(self.user, "Exercise", "30 minute workout", "daily")
        result = habit_tracker.add_habit(self.user, "Exercise", "Another workout", "weekly")
        self.assertFalse(result)
        self.assertEqual(len(habit_tracker.get_habits(self.user)), 1)

    def test_edit_non_existent_habit(self):
        result = habit_tracker.edit_habit(self.user, 99, "Swimming", "20 Minutes", "Daily")
        self.assertFalse(result)

    def test_edit_duplicate_habit_name(self):
        habit_tracker.add_habit(self.user, "Exercise", "30 minute workout", "daily")
        habit_tracker.add_habit(self.user, "Swimming", "20 Minutes", "Daily")
        result = habit_tracker.edit_habit(self.user, 1, "Swimming", "New Description", "Weekly")
        self.assertFalse(result)
        self.assertEqual(habit_tracker.get_habits(self.user)[0]['name'], "Exercise")

    def test_delete_nonexistent_habit(self):
        result = habit_tracker.delete_habit(self.user, 99)
        self.assertFalse(result)

    def test_get_habits_no_habits(self):
        result = habit_tracker.get_habits(self.user)
        self.assertEqual(result, [])

    @patch('habit_tracker.st')
    def test_complete_nonexistent_habit(self, mock_st):
        today_str = str(date.today())
        result = habit_tracker.complete_habit(self.user, 99, today_str)
        self.assertFalse(result)

    def test_is_habit_completed(self):
        habit_tracker.add_habit(self.user, "Exercise", "30 minute workout", "daily")
        today_str = str(date.today())
        self.assertFalse(habit_tracker.is_habit_completed(self.user, 1, today_str))
        habit_tracker.complete_habit(self.user, 1, today_str)
        self.assertTrue(habit_tracker.is_habit_completed(self.user, 1, today_str))

    def test_get_habit_completions_no_completions(self):
        habit_tracker.add_habit(self.user, "Exercise", "30 minute workout", "daily")
        result = habit_tracker.get_habit_completions(self.user, 1)
        self.assertEqual(result, [])

    def test_current_streak_no_completions(self):
        habit_tracker.add_habit(self.user, "Exercise", "30 minute workout", "daily")
        streak = habit_tracker.get_current_streak(self.user, 1)
        self.assertEqual(streak, 0)

    def test_longest_streak_no_completions(self):
        habit_tracker.add_habit(self.user, "Exercise", "30 minute workout", "daily")
        longest_streak = habit_tracker.get_longest_streak(self.user, 1)
        self.assertEqual(longest_streak, 0)
    
    @patch('habit_tracker.st')
    def test_complete_habit_already_completed(self, mock_st):
        habit_tracker.add_habit(self.user, "Exercise", "30 minute workout", "daily")
        today_str = str(date.today())
        habit_tracker.complete_habit(self.user, 1, today_str)
        result = habit_tracker.complete_habit(self.user, 1, today_str)
        self.assertFalse(result)

if __name__ == "__main__":
    unittest.main()
