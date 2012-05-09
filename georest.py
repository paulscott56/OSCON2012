import json
import bottle
from bottle import route, run, request, abort
from pymongo import Connection

from json import JSONEncoder
from pymongo.objectid import ObjectId

class MongoEncoder(JSONEncoder):
    def _iterencode(self, o, markers=None):
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
    entity = db['places'].find({'name':name})
    #print entity
    if not entity:
        abort(404, 'No document with name %s' % name)
    # Iterate over results
    res = []
    for e in entity:
         #print json.dumps(e, cls=MongoEncoder) 
         res.append([json.dumps(e, cls=MongoEncoder)])
    #print res
    return {"data": res}

@route('/loc', method='GET')
def get_documentlatlon():
    lat = request.GET.get('lat','').strip()
    lon = request.GET.get('lon','').strip()
    radius = request.GET.get('radius', 100)
    radius = int(radius)
    lat = float(lat)
    lon = float(lon)
    entity=db['places'].find({"loc": {"$within": {"$center": [[lat, lon], radius]}}}).limit(20)

    if not entity:
        abort(404, 'No document near %s' % latlon)
    res = []
    for e in entity:
#        print e
        res.append([json.dumps(e, cls=MongoEncoder)])
    return {"data": res}

run(host='localhost', port=8085)
