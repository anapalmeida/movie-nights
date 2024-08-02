from flask import Flask

def create_app():
    app = Flask(__name__)

    from api.routes import configure_routes
    configure_routes(app)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
