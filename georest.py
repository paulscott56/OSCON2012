import json
import bottle
from bottle import route, run, request, abort, response
from pymongo import Connection
import urllib
from json import JSONEncoder
from pymongo.objectid import ObjectId

class MongoEncoder(JSONEncoder):
    def _iterencode(self, o, markers=None):
        o = ''
        if isinstance(o, ObjectId):
            return """ObjectId("%s")""" % str(o)
        else:
            return JSONEncoder._iterencode(self, o, markers)

connection = Connection('localhost', 27017)
db = connection.geopoints

@route('/documents', method='PUT')
def put_document():
    data = request.body.readline()
    if not data:
        abort(400, 'No data received')
    entity = json.loads(data)
    if not entity.has_key('_id'):
        abort(400, 'No _id specified')
    try:
        db['userplaces'].save(entity)
    except ValidationError as ve:
        abort(400, str(ve))

@route('/documents/:name', method='GET')
def get_document(name):
    name = urllib.unquote_plus(name)
    name = name.title()
    response.content_type = 'application/json'
    entity = db['places'].find({'name':name}, {'_id' : 0})
    if not entity:  
        abort(404, 'No document with name %s' % name)
    # Iterate over results
    entries = [entry for entry in entity]
    return MongoEncoder().encode(entries) 

@route('/loc', method='GET')
def get_documentlatlon():
    response.content_type = 'application/json'
    lat = request.GET.get('lat','').strip()
    lon = request.GET.get('lon','').strip()
    radius = request.GET.get('radius', 100)
    radius = int(radius)
    lat = float(lat)
    lon = float(lon)
    entity=db['places'].find({"loc": {"$within": {"$center": [[lat, lon], radius]}}}, {'_id':0}).limit(20)
    if not entity:
        abort(404, 'No document with name %s' % name)
    # Iterate over results
    entries = [entry for entry in entity]
    return MongoEncoder().encode(entries)

run(host='geo.chisimba.com', port=8080)
