from functools import wraps

from flask import current_app
from flask_login import current_user, login_required


def isAdmin(func):
    @wraps(func)
    def test_if_user_admin(*args, **kwargs):
        if current_app.config.get("LOGIN_DISABLED"):
            pass
        elif not current_user.is_authenticated or not current_user.is_admin:
            return current_app.login_manager.unauthorized()

        if callable(getattr(current_app, "ensure_sync", None)):
            return current_app.ensure_sync(func)(*args, **kwargs)
        return func(*args, **kwargs)

    return test_if_user_admin
