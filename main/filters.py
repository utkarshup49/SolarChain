from main import app

@app.template_filter('formatdatetime')
def format_datetime(value, format='%d %b %Y %H:%M:%S'):
    """Convert a datetime to a different format."""
    if value is None:
        return ""
    return value.strftime(format)

app.jinja_env.filters['formatdatetime'] = format_datetime
