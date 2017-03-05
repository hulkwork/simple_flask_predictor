# simple_flask_predictor

This is a simple flask server to predict spam or iris

# Requirement
	- Flask
	- urllib
# Usage
	-	launch iris : python app.py
	- 	launch spam : python app.py spam
# Get prediction:
	-	Iris : curl -X POST http://localhost:5000/randomForest -d '[[0,1],[0,5]]'
	- 	spam : curl -X POST http://localhost:5000/randomForest -d '[["year"],["hello world !"]]'
