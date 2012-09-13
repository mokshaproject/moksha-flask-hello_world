from moksha.common.lib.helpers import get_moksha_appconfig
from moksha.wsgi.middleware import make_moksha_middleware
from tw2.core.middleware import make_middleware

import datetime
import moksha.hub.api.producer


from flask import Flask
app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World!"


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

    app.run()
