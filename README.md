# SynthEdge
Machine Learning tool for creative music applications. Inspired by WEKINATOR (https://github.com/fiebrink1/wekinator), but written in Python and on a more modern tech stack

## under development
This project is under development. Use it at your own risk. Current functionality:
- OSC Input and output
- save and load projects
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
- model selection and OSC configurationover GUI
		
## To do
- dynamic time warping
- configuration of models
- probability
- docs


## How to use the tools
- Docs will follow soon.
- for now, check osc_example.pd file


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
`pyinstaller main.py --onefile --noconsole --icon=synthedge.ico --add-data "synthedge.ico;."`