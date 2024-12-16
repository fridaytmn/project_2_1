import dash
import utils.styles.themes
import utils.styles.icons
from pydantic import ValidationError

app = dash.Dash(
    __name__,
    external_stylesheets=[utils.styles.themes.BOOTSTRAP, utils.styles.icons.BOOTSTRAP],
)
app.config["suppress_callback_exceptions"] = True
app.logger.propagate = False


@app.server.errorhandler(500)
def handle_error():
    return {
        "response": {
            "base-error": {
                "header": "Ошибка сервера",
                "is_open": True,
                "icon": "danger",
                "children": "Мы знаем об этой ошибке и уже принимаем меры по её устранению",
            }
        },
        "multi": True,
    }


@app.server.errorhandler(ValidationError)
def handle_validation_error(error):
    error_field = str(error).split("\n")[1]
    return {
        "response": {
            "base-error": {
                "header": "Предупреждение",
                "is_open": True,
                "icon": "warning",
                "children": f"Неверно заполненное поле: " f"{error_field}",
            }
        },
        "multi": True,
    }
