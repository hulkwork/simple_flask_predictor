from sklearn import datasets
import pandas as pd
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline

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
	def __init__(self,path_data='smsspamcollection.zip'):
		self.path_data = path_data
		import zipfile
		archive = zipfile.ZipFile('smsspamcollection.zip', 'r')
		self.raw_data = archive.open('SMSSpamCollection')
		self._dataFrame = pd.read_csv(self.raw_data,delimiter = '\t',names = ["label", "message"])		
		self.Y = self._dataFrame["label"]
		self.X = self._dataFrame["message"]
		self.__train()
	

	def __train(self):
		self.model = RandomForestClassifier(n_estimators = 20)
		self.transformer = TfidfVectorizer(max_features=200)
		self.X_train = self.transformer.fit_transform(self.X).toarray()
		self.model = self.model.fit(self.X_train,self.Y)
		self.pipeline = Pipeline([('tfidf', self.transformer), ('rfr', self.model)])
		
	def predictor(self,data):
		self.x_test = self.transformer.transform(data).toarray()
		return self.model.predict(self.x_test)
	
# Test
#spam = spam_Model()
#print spam._dataFrame.head()
#print spam.predictor(["i am happy",'Free entry in 2 a wkly comp to win FA Cup fina'])
