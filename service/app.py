from comtypes.safearray import numpy
from flask import Flask, request, jsonify, make_response
from flask_restplus import Api, Resource, fields
from sklearn.metrics.pairwise import cosine_similarity
import logging
import scipy
from absl import logging

import numpy as np
import tensorflow_hub as hub
import seaborn as sns
import tensorflow as tf
import matplotlib.pyplot as plt

import os
import pandas as pd
import seaborn as sns

# #STS Benchmark imports
# import pandas
# import scipy
# import math
# import csv
# from sklearn.externals import joblib

flask_app = Flask(__name__)
app = Api(app = flask_app,
		  version = "1.0",
		  title = "ML React App",
		  description = "Predict results using a trained model")

name_space = app.namespace('prediction', description='Prediction APIs')

#inputModel = app.model('Prediction params',
#				  {'textField1': fields.String(required = True,
#				  							   description="Text Field 1",
 #   					  				 	   help="Text Field 1 cannot be blank"),
#				  'textField2': fields.String(required = True,
#				  							   description="Text Field 2",
 #   					  				 	   help="Text Field 2 cannot be blank"),
#				  'select1': fields.Integer(required = True,
#				  							description="Select 1",
 #   					  				 	help="Select 1 cannot be blank"),
#				  'select2': fields.Integer(required = True,
#				  							description="Select 2",
 #   					  				 	help="Select 2 cannot be blank"),
#				  'select3': fields.Integer(required = True,
#				  							description="Select 3",
 #   					  				 	help="Select 3 cannot be blank")})'''

# classifier = joblib.load('classifier.joblib')

#Model Loading
module_url = "https://tfhub.dev/google/universal-sentence-encoder/4"
		# @param ["https://tfhub.dev/google/universal-sentence-encoder/4",
		# "https://tfhub.dev/google/universal-sentence-encoder-large/5"]

model = hub.load(module_url)


@name_space.route("/")
class MainClass(Resource):

	sentencePercentPlagiat= [[]]

	def embed(self, input):
		print("module %s loaded" % module_url)
		return model(input)

	def plot_similarity(self, labels, features, rotation):
		corr = np.inner(features, features)
		self.sentencePercentPlagiat = corr
		sns.set(font_scale=1.0)
		plt.figure(figsize=(16,9))
		g = sns.heatmap(
			corr,
			annot=True,
			fmt=".2%",
			annot_kws={"size": 6},
			xticklabels=labels,
			yticklabels=labels,
			vmin=0,
			vmax=1,
			cmap="YlOrRd")
		g.set_xticklabels(labels, rotation=rotation)
		g.set_title("Semantic Textual Similarity")
		#g.set_size(20,15)
		#fig = g.get_figure()
		plt.savefig("static/img/output.png")

	def run_and_plot(self, messages1,messages2):
		messages = []
		for i in range(len(messages1)):
			s = messages1[i]
			messages.append(s[0:10] + "...[1." + str(i) + "]")
		for i in range(len(messages2)):
			s = messages2[i]
			messages.append(s[0:10]+"...[2." + str(i) + "]")
		plotingMessages = messages1+ messages2
		message_embeddings_ = self.embed(plotingMessages)
		print (messages)
		self.plot_similarity(messages, message_embeddings_, 90)

	def options(self):
		response = make_response()
		response.headers.add("Access-Control-Allow-Origin", "*")
		response.headers.add('Access-Control-Allow-Headers', "*")
		response.headers.add('Access-Control-Allow-Methods', "*")
		return response

	#@app.expect(inputModel)
	def post(self):
		try:
			formData = request.json
			text1 = formData.get('fileupload1')
			text2 = formData.get('fileupload2')
			messages = []
			messages1 = []
			linesText1 = text1.split('\n')
			for line in linesText1:
				messages.append(line.rstrip())
			print(messages)

			linesText2 = text2.split('\n')
			for line in linesText2:
				messages1.append(line.rstrip())
			print(messages1)

			#data = [val for val in formData.values()]
			# prediction = classifier.predict(data)
			data = []

			# @title Compute a representation for each message, showing various lengths supported.
			# word = "Plagiarisma"
			# sentence = "Best plagiarism detector for you."
			# paragraph = ("French to Dutch translation results for 'plagiat' designed for tablets and mobile devices."
			# 			 "Possible languages include English, Dutch, German, French, Spanish.")
			# messages = [word, sentence, paragraph]

			# Reduce logging output.
			#logging.set_verbosity(logging.ERROR)

			message_embeddings1 = self.embed(messages)
			message_embeddings2 = self.embed(messages1)

			# Similarity matrix
			similarity_matrix = cosine_similarity(message_embeddings1, message_embeddings2)
			num_similar_sentences = 0

			for i in range(len(similarity_matrix)):
				for j in range(len(similarity_matrix[i])):
					if similarity_matrix[i][j] > 0.80:
						num_similar_sentences = num_similar_sentences + 1


			print(num_similar_sentences)
			print(len(similarity_matrix))

			ratio = (num_similar_sentences / len(similarity_matrix))
			outputStr = "{0:.2f}".format(ratio *100)

			if (ratio > 0.5):
				data = ['PLAGIAT!']
			else:
				data = ['Not Plagiat.']

			#data.append(outputStr)
			#data.append('%')

			print(data)
			#Run Plot HeatMap

			plotingMessages = messages + messages1
			self.run_and_plot(messages,messages1)

			#Find Sentence Max Percent Plagiat
			maxPercent = -100.00
			maxSentencePercentPlagiat = []

			for row in range(len(self.sentencePercentPlagiat)):
				for cell in range(len(self.sentencePercentPlagiat[row])):
					if row != cell:
						if self.sentencePercentPlagiat[row][cell] > maxPercent:
							maxPercent =self.sentencePercentPlagiat[row][cell]
				maxSentencePercentPlagiat.append("{0:.2f}".format(maxPercent *100))
				maxPercent = -100.00

			print(maxSentencePercentPlagiat)

			response = jsonify({
				"statusCode": 200,
				"status": "Prediction made",
				"result": "Prediction: " + str(data),
				"maxSentencePercentPlagiat": str(maxSentencePercentPlagiat)
				})
			response.headers.add('Access-Control-Allow-Origin', '*')
			return response
		except Exception as error:
			return jsonify({
				"statusCode": 500,
				"status": "Could not make prediction",
				"error": str(error)
			})


