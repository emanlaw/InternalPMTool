from app.utils.date_helpers import (
    get_due_date_class,
    get_due_date_text_class,
    get_due_date_status,
    get_comment_count
)

def register_template_filters(app):
    """Register template filters and globals"""
    app.jinja_env.globals.update(
        get_due_date_class=get_due_date_class,
        get_due_date_text_class=get_due_date_text_class,
        get_due_date_status=get_due_date_status,
        get_comment_count=get_comment_count
    )