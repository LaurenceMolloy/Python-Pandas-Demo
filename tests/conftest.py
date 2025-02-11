import pytest

def pytest_configure(config):
    """Skip tests marked as 'fail' unless explicitly selected with '-m fail'."""
    config.addinivalue_line("markers", "fail: Mark test to run only when -m fail is used")
    
    # If no -m filter is provided, skip 'fail' tests
    if not config.option.markexpr:
        config.option.markexpr = "not fail"
    elif "fail" not in config.option.markexpr:
        config.option.markexpr = f"({config.option.markexpr}) and not fail"
