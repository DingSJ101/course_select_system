from app import app
from werkzeug.middleware.proxy_fix import ProxyFix
from app import db
import os 
if __name__ == "__main__":
    app.wsgi_app = ProxyFix(app.wsgi_app)
    app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.realpath(__file__)),'upload/')
    # db.drop_all()
    # db.create_all()
    app.run(host='0.0.0.0', port=8000, debug=False)
