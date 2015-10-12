# Project 4 - Conference Organization App
### Udacity - Full Stack - Project 4 - Conference Organization App

By Jerry Wardlow for the Udacity [Full Stack Web Developer Nanodegree](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd004)

### About

This project is a continuation of the [Conference Central Application](https://github.com/udacity/ud858) from Udacity's Developing Scalable
Apps with Python course. Using the Google App Engine cloud hosting platform, a
highly scalable API server is implemented to handle the needs of our conference
application. This application uses Oauth2.0 to authenticate users through their
Google accounts.

### In This Repository

The core functionality of the project is contained within two files, `conference.py`
and `main.py`. These two files work together to build the App Engine project and
implement the required functionality. The class definitions for Profile, User,
Conference, and Session models and forms (among others) are defined in `models.py`.
Three YAML files are used to store configuration information. General application
configuration is contained within `app.yaml` along with route handlers and required
libraries. Indexes for datastore queries are generated and stored in `index.yaml`,
and cron configurations are placed in `cron.yaml`. Static files and templates for
the front end are stored in their respective folders.

### Using This Project

The API is hosted on Google App Engine as [Scale App 13602](https://scale-app-13602.appspot.com/)
and can be accessed directly via the [API Explorer](https://scale-app-13602.appspot.com/_ah/api/explorer). Alternatively,
this repository can be cloned and implemented locally, or configured and launched
on Google App Engine.

**Prerequisites**

* Python 2.7.x
* [Google App Engine SDK for Python](https://cloud.google.com/appengine/downloads?hl=en)

**Running and Testing This Project**

After cloning the repository, we need to create a new project through the [Google
Developers Console](https://console.developers.google.com/) and set up OAuth credentials.
Though a detailed tutorial for setting up OAuth credentials is outside the scope
of this project, in depth information can be found through [Google Identity
Platform](https://developers.google.com/identity/protocols/OAuth2?hl=en) guides.
After creating a new project through the Google Developers Console, we can
add new 'OAuth 2.0 client ID' credentials. Our application type is a 'Web
application'. 'Authorized JavaScript origins' are `http://localhost:8080` and
'Authorized redirect URIs' are `http://localhost:8080/oauth2callback`. We can now
use the generated Client ID to update `main.py` at line 31, `WEB_CLIENT_ID`. This
Client ID is also updated in `/static/js/app.js` at line 89, `CLIENT_ID`. Finally,
the application name is updated in `app.yaml`, line 1, `application:`.

Now that our project is updated, we can run it locally using the App Engine SDK
or deploy it to the Cloud Platform.
