# Setting up Python Development Environment


## 1 Install Python

If Python is not already installed on your system, you'll need to install it. Visit the Python website and follow the instructions to download and install the latest version of Python.

## Clone the repo into Visual Studio Code (ide of choice)
the directory for your application where you'll running the project
---
## Create a virtual Environment:
It's recommended to use a virtual environment to isolate your Python dependencies. In your project directory, open a terminal or command prompt and run the following command:
`python3 -m venv venv`
this command creates a new virtual environment names 'venv' in your the project directory

## Activate the virtual Enfironment:
- on mcOs and Linus, use the following command:
`source venv/bin/activate`

- on windows:
`venv\Scripts\activate`

## install the required python packages
run this command -> `pip install flask` in your terminal (under the project directory)
`pip install flask`
`pip install math`
`pip install uuid`

## start the flask development server
- start the server by running the app through this command in the terminal
`python3 app.py`

## assuming you have Docker installed, 
build the docker image by running this command: `docker build -t receipt-processor .`

## run the container based on the image
`docker run -p 5000:5000 receipt-processor`
