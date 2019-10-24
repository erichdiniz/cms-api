from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
from flask_pymongo import PyMongo

app = Flask(__name__)


app.debug = True
app.secret_key = 'development key'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/myDatabase'
mongo = PyMongo(app)

databases = {
    'loja': mongo.cx['loja'],
    'spot': mongo.cx['spot'],
}

lojas = {
    "loja": 'Marisa',
    "loja": 'Extra',
    "loja": 'Itaú'
}

spots = {
    'spot': 'Logo',
    'spot': 'Banner Home',
    'spot': 'Banner Dashboard',
}
@app.route('/')
def hello_world(loja, spot):
    loja = loja
    spot = spot
    return render_template('index.html', lojas=loja, spots=spot)


@app.route("/<database>/foo1")
def foo1(database):
    db = databases[database]  # fetch the appropriate DB
    # data = db.tar.find_one({'metadata.grid': {'$eq': '5000'}})
    print(database)
    return 'foo1 ' + database


@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        filename = secure_filename(f.filename)
        mongo.save_file(f.filename, f)
        mongo.db.users.insert({'f_name': f.filename})
        print(mongo.db.users)
        print(f)
        # f.save(secure_filename(f.filename))
        return 'Tudo salvo meu parceirinho'


@app.route("/uploads/<path:filename>", methods=["POST"])
def save_upload(filename):
    mongo.save_file(filename, request.files["file"])

