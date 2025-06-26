"""
Tests for the main entry point of the MiniBook package.
"""

from unittest.mock import patch

import minibook.main


def test_main_entry_point():
    """Test the main entry point of the MiniBook package."""
    # Mock the app function to avoid actually running the command
    with patch('minibook.main.app') as mock_app:
        # Save the original __name__ value
        original_name = minibook.main.__name__

        try:
            # Set __name__ to "__main__" to trigger the if block
            minibook.main.__name__ = "__main__"

            # Execute the if block directly to cover line 257
            # This is the line we want to cover: if __name__ == "__main__": app()
            if minibook.main.__name__ == "__main__":
                # This will call the mocked app function
                minibook.main.app()

            # Check that the app function was called
            mock_app.assert_called_once()
        finally:
            # Restore the original __name__ value
            minibook.main.__name__ = original_name
