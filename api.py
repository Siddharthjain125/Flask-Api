from flask import Flask,jsonify,request
from flask_pymongo import PyMongo,pymongo
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config['MONGO_DBNAME'] = 'api_data'
app.config['MONGO_URI'] = 'mongodb://siddharth:jain@ds223760.mlab.com:23760/api_data'

mongo = PyMongo(app)

@app.route('/api')
def get_all():
	photos = mongo.db.photos
	output = []

	offset = int(request.args['offset'])
	limit = int(request.args['limit'])

	start = photos.find().sort('_id', pymongo.ASCENDING)
	last = start[offset]['_id']

	pid = photos.find({'_id' : {'$gte' : last}}).sort('_id', pymongo.ASCENDING).limit(limit)

	for q in pid:
		output.append({'title' : q['title'], 'url' : q['url'] })

	next_url = '/api?limit=' +str(limit)+ '&offset=' +str(offset+limit)
	prev_url = '/api?limit=' +str(limit)+ '&offset=' +str(offset-limit)

	return jsonify({'result' : output , 'prev_url' : prev_url , 'next_url' : next_url })

@app.route('/api/photos/<title>')
def get_one(title):
	photos = mongo.db.photos
	q = photos.find_one({'title' : title})
	if q:
		output = {'title' : q['title'] , 'url' : q['url']}
	else:
		output = 'No result Found'  
	return jsonify({'result' : output})

@app.route('/api/photos' , methods = ['POST'])
def add():
	photos = mongo.db.photos
	title = request.json['title']
	url = request.json['url']

	pid = photos.insert({'title' : title , 'url' : url})
	new_photo = photos.find_one({'_id' : pid})

	output = {'title' : new_photo['title'] , 'url' : new_photo['url']}
	return jsonify({'result' : output})

@app.route('/api' , methods = ['POST'])
def del_one():
	photos = mongo.db.photos
	title = request.json['title']
	q = photos.find_one({'title' : title})
	if q:
		photos.remove({'title' : q['title']})
		output =  'Item Deleted'
	else:
		output = 'No result Found'  
	return jsonify({'result' : output})



if __name__ == '__main__':
	app.run(debug = True)