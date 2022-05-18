from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class Model(db.Model):
    key = db.Column(db.String(100), primary_key=True)
    value = db.Column(db.String(100))

data_put_args = reqparse.RequestParser()
data_put_args.add_argument("key", type=str, help="key of data")
data_put_args.add_argument("value", type=str, help="value of data")

class Data(Resource):
    def post(self):
        args = data_put_args.parse_args()
        key = args['key']
        value = args['value']
        exist = Model.query.filter_by(key=key).count()
        if not exist:
            data = Model(key=key,value=value)
            db.session.add(data)
            db.session.commit()
            return '', 201
        else :
            return '', 400

    def get(self, key=None):
        if key != None:
            data = Model.query.filter_by(key=key).first()
            if data:
                data_json = {data.key: data.value}
                return data_json, 200
            else:
                return '', 404
        else :
            keys = [data.key for data in Model.query.all()]
            return keys, 200

    def put(self, key):
        args = data_put_args.parse_args()
        value = args['value']
        data = Model.query.filter_by(key=key)
        if data.count():
            data.first().value = value
            db.session.commit()
            return '', 200
        else :
            data = Model(key=key,value=value)
            db.session.add(data)
            db.session.commit()
            return '', 201

    def delete(self, key):
        Model.query.filter_by(key=key).delete()
        db.session.commit()
        return '', 200

api.add_resource(Data, "/key", "/key/<path:key>")
