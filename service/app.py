from flask import Flask, request, jsonify, make_response
from flask_restplus import Api, Resource, fields
import scipy
from absl import logging
from sklearn.metrics.pairwise import cosine_similarity

import tensorflow as tf
import tensorflow_hub as hub
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import re
import seaborn as sns

#STS Benchmark imports
import pandas
import scipy
import math
import csv
from sklearn.externals import joblib

flask_app = Flask(__name__)
app = Api(app = flask_app, 
		  version = "1.0", 
		  title = "ML React App", 
		  description = "Predict results using a trained model")

name_space = app.namespace('prediction', description='Prediction APIs')

model = app.model('Prediction params',
				  {'textField1': fields.String(required = True,
				  							   description="Text Field 1",
    					  				 	   help="Text Field 1 cannot be blank"),
				  'textField2': fields.String(required = True,
				  							   description="Text Field 2",
    					  				 	   help="Text Field 2 cannot be blank"),
				  'select1': fields.Integer(required = True,
				  							description="Select 1",
    					  				 	help="Select 1 cannot be blank"),
				  'select2': fields.Integer(required = True,
				  							description="Select 2",
    					  				 	help="Select 2 cannot be blank"),
				  'select3': fields.Integer(required = True,
				  							description="Select 3",
    					  				 	help="Select 3 cannot be blank")})

# classifier = joblib.load('classifier.joblib')




@name_space.route("/")
class MainClass(Resource):

	#######################################################

	def embed(self, input):
		module_url = "https://tfhub.dev/google/universal-sentence-encoder/4"
		# @param ["https://tfhub.dev/google/universal-sentence-encoder/4",
		# "https://tfhub.dev/google/universal-sentence-encoder-large/5"]

		model = hub.load(module_url)
		print("module %s loaded" % module_url)
		return model(input)

	def plot_similarity(self, labels, features, rotation):
		corr = np.inner(features, features)
		sns.set(font_scale=1.2)
		g = sns.heatmap(
			corr,
			xticklabels=labels,
			yticklabels=labels,
			vmin=0,
			vmax=1,
			cmap="YlOrRd")
		g.set_xticklabels(labels, rotation=rotation)
		g.set_title("Semantic Textual Similarity")

	def run_and_plot(self, messages_):
		message_embeddings_ = self.embed(messages_)
		self.plot_similarity(messages_, message_embeddings_, 90)

	########################################################

	def options(self):
		response = make_response()
		response.headers.add("Access-Control-Allow-Origin", "*")
		response.headers.add('Access-Control-Allow-Headers', "*")
		response.headers.add('Access-Control-Allow-Methods', "*")
		return response

	@app.expect(model)		
	def post(self):
		try:

			formData = request.json
			data = [val for val in formData.values()]
			# prediction = classifier.predict(data)
			data = []


			# @title Compute a representation for each message, showing various lengths supported.
			word = "Plagiarisma"
			sentence = "Best plagiarism detector for you."
			paragraph = ("French to Dutch translation results for 'plagiat' designed for tablets and mobile devices."
						 "Possible languages include English, Dutch, German, French, Spanish.")
			messages = [word, sentence, paragraph]

			word1 = "Elephant"
			sentence1 = "Best plagiarism detector for you."
			paragraph1 = (
				"English is a West Germanic language that was first spoken in early medieval England,"
				" eventually became a global lingua franca."
				"It is named after the Angles."
			)
			messages1 = [word1, sentence1, paragraph1]

			# Reduce logging output.
			logging.set_verbosity(logging.ERROR)

			message_embeddings1 = self.embed(messages)
			message_embeddings2 = self.embed(messages1)

			# Similarity matrix
			similarity_matrix = cosine_similarity(message_embeddings1, message_embeddings2)
			num_similar_sentences = 0

			for i in range(len(similarity_matrix)):
				for j in range(len(similarity_matrix[i])):
					if similarity_matrix[i][j] > 0.90:
						num_similar_sentences = num_similar_sentences + 1

			print(num_similar_sentences)
			print(len(similarity_matrix))
			if ((num_similar_sentences / len(similarity_matrix)) > 0.5):
				data = ['PLAGIAT!']
			else:
				data = ['NOT PLAGIAT.']

			response = jsonify({
				"statusCode": 200,
				"status": "Prediction made",
				"result": "Prediction: " + str(data)
				})
			response.headers.add('Access-Control-Allow-Origin', '*')
			return response
		except Exception as error:
			return jsonify({
				"statusCode": 500,
				"status": "Could not make prediction",
				"error": str(error)
			})