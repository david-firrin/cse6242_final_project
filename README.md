# Auto Advisor Description

Autoadvisor provides users not only with a price prediction for their car, but also offers specific context as to how the valuation decision was reached. Currently, determining the price of a used car involves manual research and may not consider all factors. Our innovation will leverage machine learning models and provide transparent insights that not only lead to more accurate price predictions, but a more informed user.

# Auto Advisor Installation and Execution

1) Clone the repo, and now let's set up a local python environment by navigating to the directory with the app and in your terminal and enter: 

python3 -m venv env

2) In order to acivate that python environment, enter:

source env/bin/activate

3) Now let's go ahead and install all the necessary packages into that python environment in order to run the application:

pip install -r requirements.txt

4) Finally, in order to start up the local flask server and test out the application, enter:

python server.py

5) The page should open on your browser at:

http://localhost:5000

6) The application can also be tested on the following website, which is hosted directly from the latest git commit at the following url:

https://autoadvisor.pro/

# Auto Advisor Application Structure
The directory is structured specific for a Flask application. The basic elements consist of: 
- 'static' directory, which contains all the static pages for the web application from the application's images, css, and javascript files
- 'templates' directory, which contains all the html pages for the web application.
- 'data', which contains the majority of the data for the application.
- 'user_interface_utils_assets', which contains the pickle files for the GAM model the application uses. 

The python files that make up the backend server of the application consist of:
- Server_Analyze.py, which consists of the execution for the scripts that make up the applications' machine learning models.
- server.py, which consist of all the scripts for routing. 
- user_interface_models_utils.py, which consists of the scripts for the application's GAM model.

The javascript files that make up the interactivity of the application consist of: 
- analysis_functions.js, which make up all the functions that go into the creation of the analysis page template in the application.
- validator_functions.js, which make up the interactivity of the application's ability to go forward and backward through the form inputs. 
- plot_mileage_age_curve_exp.js, which makes up the chartjs plot in the application.
