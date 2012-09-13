from moksha.common.lib.helpers import get_moksha_appconfig
from moksha.wsgi.middleware import make_moksha_middleware
from tw2.core.middleware import make_middleware

import datetime
import moksha.hub.api.producer
import moksha.wsgi.widgets.api
import tw2.jqplugins.gritter
import flask.templating

from flask import Flask
app = Flask(__name__)

simple_template = """
<html>
<head></head>
<body>
Really?
{{notification_widget.display()}}
{{moksha_socket.display()}}
</body>
</html>
"""


class PopupNotification(moksha.wsgi.widgets.api.LiveWidget):
    topic = "*"
    onmessage = "$.gritter.add({'title': 'Received', 'text': json});"
    resources = moksha.wsgi.widgets.api.LiveWidget.resources + \
            tw2.jqplugins.gritter.gritter_resources
    backend = "websocket"

    # Don't actually produce anything when you call .display() on this widget.
    inline_engine_name = "mako"
    template = ""


@app.route("/")
def hello():
    config = get_moksha_appconfig()
    socket = moksha.wsgi.widgets.api.get_moksha_socket(config)
    return flask.templating.render_template_string(
        simple_template,
        notification_widget=PopupNotification,
        moksha_socket=socket,
    )


class HelloWorldProducer(moksha.hub.api.producer.PollingProducer):
    frequency = datetime.timedelta(seconds=2)

    def poll(self):
        self.send_message('hello_world', "Hello World!")


if __name__ == "__main__":
    # Load development.ini
    config = get_moksha_appconfig()

    # Wrap the inner wsgi app with our middlewares
    app.wsgi_app = make_moksha_middleware(app.wsgi_app, config)
    app.wsgi_app = make_middleware(app.wsgi_app)

    app.run(debug=True)
