from pymongo import MongoClient
import csv
import os
# import json
from flask import Flask, request, render_template, url_for, json

client = MongoClient("mongodb://localhost:27017/")
app = Flask(__name__)
db = client['cms-api-db']

user = db['users']
login = db['user_login']
# Issue the serverStatus command and print the results
print(db.list_collection_names())


@app.route('/loaduser', methods=['GET', 'POST'])
def upload_user():
    with open("data/users.csv", 'rt', encoding='utf-8-sig') as infile:
        csv.register_dialect('strip', skipinitialspace=True)
        reader = csv.DictReader(infile, dialect='strip')

        for i,row in enumerate(reader):
            # print(row)
            result = json.loads(json.dumps(row))
            print(result)
            login.insert_one(result)
            print(login)
            if (i >= 3):
                break
        return 'ok'

@app.route('/getlogin', methods=['GET', 'POST'])
def get_login():
    if request.method == 'POST':
        headers = {'Content-type': 'application/json'}
        data = request.form

        print(data['username'])
        print(data['password'])
        # cpf_data = request.args('cpf')
        # print(cpf_data)
        password = login.distinct('password')
        username = login.distinct('username')
        financeira = login.distinct('nome_financeira')

        if data['password'] in password or data['username'] in username:
            print('encontrado')
            print()
            user_selected = login.find_one({'username': data['username']})
            print(financeira)
            del user_selected['_id']
        else:
            print('nenhum valor encontrado')
        data_json = json.dumps(user_selected, indent=2)

        print('infos:',user)
        return data_json, 200


@app.route('/loadfile', methods=['GET', 'POST'])
def upload_file():
    with open("data/CargaNOFinanceiras.csv", 'rt') as infile:
        csv.register_dialect('strip', skipinitialspace=True)
        reader = csv.DictReader(infile, dialect='strip')

        for i,row in enumerate(reader):
            # print(row)
            result = json.loads(json.dumps(row))
            print(result)
            user.insert_one(result)
            if (i >= 5):
                break
        return render_template('index2.html', value=user.distinct('cpf'), value2=user.distinct('nome'))


@app.route('/getcpf', methods=['GET', 'POST'])
def get_file():
    if request.method == 'POST':
        headers = {'Content-type': 'application/json'}
        data = request.form

        print(data['cpf'])
        # print(data['nome_financeira'])
        # cpf_data = request.args('cpf')
        # print(cpf_data)
        cpf = user.distinct('cpf')
        if data['cpf'] in cpf:
            print('encontrado')
            user_selected = user.find_one({'cpf': data['cpf']})
            del user_selected['_id']
        else:
            print('nenhum valor encontrado')
        data_json = json.dumps(user_selected, indent=2)

        print('infos:',user)
        return data_json, 200




# print(db.collection_names())
# print(user.distinct('cpf'))

if __name__ == '__main__':
    app.run(debug=True)
else:
    app.config.update(
        SERVER_NAME='snip.snip.com:80',
        APPLICATION_ROOT='/')
