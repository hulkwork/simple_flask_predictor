from sklearn import datasets
import os
from sklearn.ensemble import RandomForestClassifier


# Iris data
iris = datasets.load_iris()
X = iris.data[:, :2]  # we only take the first two features.
Y = iris.target

#
import urllib
if 'smsspamcollection.zip' not in os.listdir('.'):
	url = "https://archive.ics.uci.edu/ml/machine-learning-databases/00228/smsspamcollection.zip"
	urllib.urlretrieve(url, "smsspamcollection.zip")
class Model(object):
	def __init__(self,path_data='/home'):
		self.path_data = path_data
		self.__train()
	def __train(self):
		self.model = RandomForestClassifier()
		self.model = self.model.fit(X,Y)
		
	def predictor(self,data):
		return self.model.predict(data)

class spam_Model(object):
	def __init__(self,path_data=''):
		self.path_data = path_data
		self.__train()
	def __train(self):
		self.model = RandomForestClassifier()
		self.model = self.model.fit(X,Y)
		
	def predictor(self,data):
		return self.model.predict(data)
	
