from flask import Flask, request
from flask_restful import Resource, Api
from recommender.service import Recommender

app = Flask(__name__)
api = Api(app)

r  = Recommender()
r_ = Recommender(model_path='data/GoogleNews-vectors-negative300.bin',embed_dimension=300,use_google=True)

class Recommendation(Resource):
    def get(self):
        r.updateuser()
        r.updaterecom()
        self.n = 10 if request.args.get("n") is None else int(request.args.get("n"))
        return r.getrecommendation(self.n)

class Recommendation_(Resource):
    def get(self):
        r_.updateuser()
        r_.updaterecom()
        self.n = 10 if request.args.get("n") is None else int(request.args.get("n"))
        return r_.getrecommendation(self.n)

api.add_resource(Recommendation,'/r')
api.add_resource(Recommendation_,'/r_')

if __name__ == '__main__':
    app.run(port=5002,host='0.0.0.0')
