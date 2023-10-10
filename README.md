
<br />
<div align="center">

<h1 align="center">Projet 11 - GudLft</h1>
<h2 align="center">Improving a Python web application through testing and debugging </h2>
  <p align="center">
Güdlft, a digital platform to coordinate strength competitions in North America and Australia.   
<br /></p>
</div>
<img align="center" src="https://thumbs.dreamstime.com/b/weightlifting-vecteur-de-sport-silhouette-d-illustration-bodybuilder-119340954.jpg"
<h6> Credit : ID 119340954©  [Iland](https://fr.dreamstime.com/iland_info)| Dreamstime.com</small></h6>




<!-- ABOUT THE PROJECT -->

## Project Overview

Debug and add tests to a Python web application (https://github.com/OpenClassrooms-Student-Center/Python_Testing).
Generate a test coverage report and a performance report using Pytest and  Locust.


## Built With

* Python
* Pytest
* Pytest Mock
* Pytest Coverage
* Locust




<!-- GETTING STARTED -->

## Getting Started

#### Clone the repo
   ```sh
   git clone https://github.com/EdwinLRT/P11-GUDLFT/
   ```
#### Install venv 
   ```sh
   pip install venv
   ```
#### Create a virtual environment
   ```sh
   python -m venv env
   ```
#### Activate the virtual environment
   ```sh
   source env/bin/activate
   ```
#### Install the packages using requirements.txt
   ```sh
   pip install -r requirements.txt
   ```

#### Run the application

   ```sh
   export FLASK_APP=server.py
   flask run
   ```

#### Access the app: http://127.0.0.1:5000
   
---

## Run tests and generate coverage report
#### Run tests
   ```sh
   pytest
   ```
#### Generate coverage report
   ```sh
    coverage run -m pytest 
    coverage html  
    open htmlcov/index.html
   ```
<img src="https://i.ibb.co/gMLMCTX/LAURENT-EDWIN-2-rapport-test-102023.png">
---

## Run Locust performance test
#### Run Locust
   ```sh
   cd tests
   cd perf
   locust
   ```
<img src="https://i.ibb.co/4mXK5mM/Capture-d-e-cran-2023-10-10-a-20-44-34.png">