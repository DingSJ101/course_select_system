from app import app
from werkzeug.middleware.proxy_fix import ProxyFix
from app import db
if __name__ == "__main__":
    app.wsgi_app = ProxyFix(app.wsgi_app)
    # db.drop_all()
    # db.create_all()
    app.run(host='127.0.0.1', port=8000, debug=False)
