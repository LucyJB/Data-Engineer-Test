from flask import Flask, request, jsonify, make_response
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy

#Create an instance of flask
app = Flask(__name__)

#Creating an API object
api = Api(app)

#Create database
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite://sam.db'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False

#SQLAlchemy mapper
db = SQLAlchemy(app)

#add a class
class Sample(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    productname= db.Column(db.String(80),nullable = False )
    creator = db.Column(db.String(80),nullable = False )
    location = db.Column(db.String(80),nullable = False )

    def __repr__(self):
        return f"{self.id} - {self.productName} - {self.creator} - {self.location}"

#For GET request to http://localhost:5000/ - returns 200 on completion
class GetSample(Resource):
    def get(self):
        samples = Sample.query.all()
        sam_list = []
        for sam in samples:
            sam_data = {'Id':sam.id, 'Productname':sam.productname, 'Creator':sam.creator,
             'Location': sam.location}
            sam_list.append(sam_data)
        return {"Samples":sam_list},200

#For POST request to http://localhost:5000/Sample - returns 201 on completion
class AddSample(Resource):
    def post(self):
        if request.is_json:
            sam = Sample(Productname=request.json['Productname'], Creator=request.json['Creator'],
            location = request.json['location'])
            db.session.add(sam)
            db.session.commit()

            #Return a json response
            return make_response(jsonify({'Id':sam.id, 'Productname':sam.productname,
            'Creator':sam.Creator, 'location':sam.location}),201)
        #returns 400 on error
        else:
            return {'error': 'Request must be JSON'},400

#For put request to http://localhost:5000/update/

class UpdateSample(Resource):
    def put(self, id):
        if request.is_json:
            sam = Sample.query.get(id)
            if sam is None:
                return{'error': 'not found'}, 404
            else:
                sam.Productname = request.json['Productname']
                sam.Creator = request.json['Creator']
                sam.location = request.json['location']
                db.session.commit()
                return 'Updated', 200
        else:
            return {'error': 'Request must be JSON'}, 400

#For delete request to http://localhost:5000/update/
class DeleteSample(Resource):
    def delete(self, id):
        sam = Sample.query.get(id)
        if sam is None:
            return {'error':'not found'}, 404
        db.session.delete(sam)
        db.session.commit()
        return f'{id} is deleted', 200

api.add_resource(GetSample, '/')
api.add_resource(AddSample, '/add')
api.add_resource(UpdateSample, '/update/<int:id>')
api.add_resource(DeleteSample, '/delete/<int:id>')

if __name__ == '__main__':
    app.run(debug=True)
