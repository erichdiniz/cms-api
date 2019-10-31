import urllib

from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
from flask_pymongo import PyMongo, MongoClient
from mongoengine import *


app = Flask(__name__)
mongo = PyMongo(app)

# Connect to MongoDB instance running on localhost
username1 = "admin"
password = "password"
host = "localhost"

client = MongoClient('localhost', 27017)

connString = client
connection = MongoClient(connString)
db = connection.query

lojas = {'loja1': 'Marisa', 'loja2': 'Extra', 'loja3': 'Itaú'}

spots = {'spot1': 'Logo','spot2': 'Banner Home', 'spot3': 'Banner Dashboard'}

# result_lojas = lojas_db.insert_one(lojas)
# result_spot = spots_db.insert_one(spots)
#

dblist = db.list_database_names()
if "query" in dblist:
  print("The database exists.")

@app.context_processor
def inject_lojas_in_all_templates():
    return dict(lojas=lojas)


@app.context_processor
def inject_spots_in_all_templates():
    return dict(spots=spots)


@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        return 'uai'
    else:
        return render_template('index.html')


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        # filename = secure_filename(f.filename)
        print(f)
        # select = request.form.get('comp_select')
        # return (str(select))
        f.save(secure_filename(f.filename))

        file_selected = f.filename
        loja_selected = request.form.get('loja_select')
        spot_selected = request.form.get('spot_select')

               
        result_query = {"file_selected": file_selected,
                 'loja_selected': loja_selected,
                 'spot_selected': spot_selected}

        mongo.save_file(f.filename, f)
        result = db.insert_one(result_query)
        
        print(result)

        # args1 = request.args[file_selected]
        # args2 = request.args[loja_selected]
        # args3 = request.args[spot_selected]
        # print(args1, args2, args3)
        # print(mongo.db.users)

        print(str(file_selected))
        print(str(loja_selected))
        print(str(spot_selected))

        # return '''<h1>The Query String are...{}:{}:{}</h1>'''.format(args1, args2, args3)
        return 'kkk'

# @app.route("/uploads/<path:filename>", methods=["POST"])
# def save_upload(filename):
#     return mongo.save_file(filename, request.files["file"])

if __name__ == '__main__':
    app.run(debug=True)
else:
    app.config.update(
        SERVER_NAME='snip.snip.com:80',
        APPLICATION_ROOT='/',
    )