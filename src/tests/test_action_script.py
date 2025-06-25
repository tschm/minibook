"""
Test for the minibook action script.
This test executes the test.sh script in the tests/resources directory.
"""

import os
import subprocess


def test_action_script(resource_dir, tmp_path):
    """Test the minibook action script."""

    # Path to the test.sh script
    test_script = resource_dir / "test.sh"

    # Check that the script exists
    assert test_script.exists(), f"Test script not found at {test_script}"

    # Make sure the script is executable
    os.chmod(test_script, 0o755)

    # Execute the script
    result = subprocess.run(
        [str(test_script)],
        capture_output=True,
        text=True,
        cwd=str(tmp_path)
    )

    # Print the output for debugging
    print(f"STDOUT: {result.stdout}")
    print(f"STDERR: {result.stderr}")

    # Check that the script executed successfully
    assert result.returncode == 0, f"Script execution failed with error: {result.stderr}"

    # Check that the output file was created
    output_file = tmp_path / "test-minibook.html"
    assert output_file.exists(), f"Output file not found at {output_file}"

