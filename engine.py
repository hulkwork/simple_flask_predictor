from sklearn import datasets
from sklearn.ensemble import RandomForestClassifier
iris = datasets.load_iris()
X = iris.data[:, :2]  # we only take the first two features.
Y = iris.target

class Model(object):
	def __init__(self,path_data='/home'):
		self.path_data = path_data
		self.__train()
	def __train(self):
		self.model = RandomForestClassifier()
		self.model = self.model.fit(X,Y)
		
	def predictor(self,data):
		return self.model.predict(data)


#m = Model()
#print m.predictor([[0,2] for i in xrange(3)])
