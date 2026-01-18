"""Test coverage for import-time exception handlers.

This module provides tests to achieve 100% code coverage by testing
the exception handlers for optional dependencies.
"""

import subprocess
import sys


def test_fpdf_import_error_coverage():
    """Test that FPDF = None line is executed when fpdf is not available.
    
    This test covers lines 18-19 in plugins.py by importing the module
    in a subprocess where fpdf is blocked.
    """
    # Python code that blocks fpdf import and verifies the exception handler
    code = """
import sys
import builtins

# Save original import
_original_import = builtins.__import__

def custom_import(name, *args, **kwargs):
    if name == 'fpdf' or name.startswith('fpdf.'):
        raise ImportError(f"Blocked import of {name}")
    return _original_import(name, *args, **kwargs)

# Replace __import__ before any imports happen
builtins.__import__ = custom_import

try:
    # Now import plugins - this should hit the except ImportError block (lines 18-19)
    import minibook.plugins
    
    # Verify FPDF was set to None by the exception handler
    assert minibook.plugins.FPDF is None, f"FPDF should be None, got {minibook.plugins.FPDF}"
    print("PASS")
finally:
    builtins.__import__ = _original_import
"""
    
    result = subprocess.run(
        [sys.executable, "-c", code],
        capture_output=True,
        text=True,
        timeout=10
    )
    
    assert result.returncode == 0, f"Test failed: {result.stderr}"
    assert "PASS" in result.stdout


def test_ebooklib_import_error_coverage():
    """Test that epub = None line is executed when ebooklib is not available.
    
    This test covers lines 23-24 in plugins.py by importing the module
    in a subprocess where ebooklib is blocked.
    """
    # Python code that blocks ebooklib import and verifies the exception handler
    code = """
import sys
import builtins

# Save original import
_original_import = builtins.__import__

def custom_import(name, *args, **kwargs):
    if name == 'ebooklib' or name.startswith('ebooklib.'):
        raise ImportError(f"Blocked import of {name}")
    return _original_import(name, *args, **kwargs)

# Replace __import__ before any imports happen
builtins.__import__ = custom_import

try:
    # Now import plugins - this should hit the except ImportError block (lines 23-24)
    import minibook.plugins
    
    # Verify epub was set to None by the exception handler
    assert minibook.plugins.epub is None, f"epub should be None, got {minibook.plugins.epub}"
    print("PASS")
finally:
    builtins.__import__ = _original_import
"""
    
    result = subprocess.run(
        [sys.executable, "-c", code],
        capture_output=True,
        text=True,
        timeout=10
    )
    
    assert result.returncode == 0, f"Test failed: {result.stderr}"
    assert "PASS" in result.stdout
