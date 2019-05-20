from flask import Flask, request
from flask_restful import Resource, Api
from recommender.service import Recommender

app = Flask(__name__)
api = Api(app)

r  = Recommender(
                 user_path = 'data/allnews/user_all.json',
                 title_path  ='data/allnews/title_all.json',
                 recom_path ='data/allnews/recom_all.json',
                 ids_path   ='data/allnews/ids_all.json',
                 summary_path = 'data/allnews/summary_all.json')#for all the summary

r_ = Recommender(model_path='data/GoogleNews-vectors-negative300.bin',
                 user_path = 'data/allnews/user_all.json',
                 title_path  ='data/allnews/title_all.json',#news path is for title only
                 recom_path ='data/allnews/recom_all.json',
                 ids_path   ='data/allnews/ids_all.json',
                 summary_path = 'data/allnews/summary_all.json',#for all the summary
                 embed_dimension=300,
                 use_google=True)

class Recommendation(Resource):
    def get(self):

        self.title = 0 if request.args.get("s") is None else 1

        if self.title:
            r.use_title()
        else:
            r.use_summary()

        r.updateuser()
        r.updaterecom()
        self.n = 10 if request.args.get("n") is None else int(request.args.get("n"))
        return r.getrecommendation(self.n)

class Recommendation_(Resource):
    def get(self):

        self.title = 0 if request.args.get("s") is None else 1

        if self.title:
            r_.use_title()
        else:
            r_.use_summary()

        r_.updateuser()
        r_.updaterecom()
        self.n = 10 if request.args.get("n") is None else int(request.args.get("n"))
        return r_.getrecommendation(self.n)

api.add_resource(Recommendation,'/r')
api.add_resource(Recommendation_,'/r_')


if __name__ == '__main__':
    app.run(port=5002,host='0.0.0.0')
