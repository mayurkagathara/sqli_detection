import flask as fl
from flask_restful import Resource, Api
from prediction_module import predict_class

app = fl.Flask(__name__)
api = Api(app)

#create post method to return the class of the query
class Predict(Resource):
	def post(self):
		data = fl.request.get_json(force=True, silent=True, cache=False)
		if data:
			query = data['query']
			return { "class" : str(predict_class(query))}
		else:
			return {'message': 'No data received'}, 400
	def get(self):
		return fl.redirect("/")

api.add_resource(Predict, '/predict')

#create get method to return documentation
class Docs(Resource):
	def get(self):
		msg = """<html><p>There is an endpoint named predict. <br>
				It takes a query as a parameter and returns the class of the query. <br>
				It accepts a json object with a query as a parameter. <br>
				The query is a string. <br>
				The response is a json string. class = 1 if query is sql injection, 0 otherwise. <br><br>
				Example: <br>
				curl -X POST http://127.0.0.1:5000/predict -H "Content-Type: application/json" -d '{"query": "Select * from Employee"}' <br>
				The response is: {"class": "0"}</p></html>
				"""
		return fl.Response(msg, mimetype='text/html')

api.add_resource(Docs, '/')

@app.errorhandler(404)
def own_404_page(error):
    return fl.Response("<html><p>404: Page not found. Goto <a href='/'>home</a></p></html>", status=404, mimetype='text/html')

if __name__ == '__main__':
	app.run()