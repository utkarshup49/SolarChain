"""
This module adds custom Jinja2 filters for use in the Flask application.
Specifically, it provides a datetime formatting filter to render datetime objects
in templates with a specified format.
"""
from time import strftime

from main import app  # Import the Flask application instance

@app.template_filter('formatdatetime')
def format_datetime(value: strftime, time_format:str = '%d %b %Y %H:%M:%S'):
    """
    Custom Jinja2 filter to format datetime objects for template rendering.

    Args:
        value (datetime): The datetime object to format. If None, returns an empty string.
        time_format (str): The format string for strftime. Defaults to '%d %b %Y %H:%M:%S'.

    Returns:
        str: The formatted datetime as a string, or an empty string if the input is None.

    Example Usage:
        {{ some_datetime_variable|formatdatetime('%Y-%m-%d') }}
    """
    if value is None:  # Handle cases where the datetime value is missing
        return ""
    return value.strftime(time_format)  # Format the datetime using the provided format

# Explicitly register the filter in the Jinja environment
app.jinja_env.filters['formatdatetime'] = format_datetime
