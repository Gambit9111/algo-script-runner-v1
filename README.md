Introduction

This Flask application is a web application that uses blueprints to manage different functionalities. It uses Flask-Login for user authentication and Flask-Session for session management. The application also reads from and writes to a JSON file to manage the status of two scripts.
Installation

To install the application, follow these steps:

    Clone the repository to your local machine.
    Navigate to the directory of the cloned repository.
    Install the required packages using pip:

pip install -r requirements.txt

This command will install all the dependencies listed in the requirements.txt file 1.
Usage

To run the application, use the following command in the terminal:

python app.py

The application will start running on your local server. You can access it by navigating to http://localhost:5000 in your web browser.

The application has three routes:

    /script1: This route is used to manage the first script.
    /script2: This route is used to manage the second script.
    /auth: This route is used for user authentication.

The application also has a home route (/) that displays the status of the two scripts and their arguments.
Features

    User Authentication: The application uses Flask-Login for user authentication. Users can log in and log out.
    Session Management: The application uses Flask-Session for session management. It stores the arguments of the two scripts in the session.
    JSON File Management: The application reads from and writes to a JSON file to manage the status of the two scripts.
