# SynthEdge
Machine Learning tool for creative music applications. Inspired by WEKINATOR (https://github.com/fiebrink1/wekinator), but written in Python and on a more modern tech stack

## under development
This is an initial commit. The project is still under development. Current functionality:
- OSC Input and output
- save and load training data
- train and predict with the following models:
	- Classifiers:
		- MLP
		- RandomForest
		- Support Vector Machine
		- K-Nearest Neighbour
	- Regressors:
		- RandomForest Regressor
		- Linear / Polynomial Regression
		- MLP Regressor
		- Support Vector Regressor
- basic model selection over GUI
		
## To do
- dynamic time warping
	


## How to develop
Git clone the repository
Create virtual environment:
```
python3 -m venv .env
source .env/bin/activate
```

install requirements:
```
pip install -r requirements.txt
```

## how to build
create virtual environment and source it(see above)
build with 
`pyinstaller --onefile main.py`