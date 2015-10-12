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

### Design Tasks

**Task 1: Add Sessions to a Conference**

As outlined in the project guidelines, the following four endpoint methods were defined:

* `getConferenceSessions`: Given a conference, return all sessions
* `getConferenceSessionsByType`: Given a conference, return all sessions of a specified type
* `getSessionsBySpeaker`: Return all sessions by a given speaker, across all conferences.
* `createSession`: Creates a new session in a conference (only open to organizer of said conference.)

The `Session` model was created with the same basic structure as `Conference` with the following attributes:

**Property** | **Type**
- | -
name | String
highlights | String
speaker | String
duration | Integer
typeOfSession | String
startDate | Date
startTime | Integer
conference | Key (Kind: Conference)

Sessions are linked to a Conference using it's datastore key, stored in the `conference` attribute and created with the `createSession` endpoint using the
`websafeConferenceKey`. Before creation of a new Session, the User is checked for authorization and then to see if they match the `organizerUserId` of the specified Conference. This will isolate creation of new Session's to only the organizer of the original Conference.

Speaker is implemented as a plain string field within the Session model for
simplicity. By not tying the Speaker to a User, we are granted more flexibility
by not requiring a Conference organizer to verify that the Speaker has an account,
requiring creation of one if not.

Session highlights are modeled as a repeatable string field which allows a Session
to have more than one focus and allow for more information to be represented.

Session `startTime` is represented by an integer in 24 hour format to allow for
ease of sorting.

**Task 2: Add Sessions to User Wishlist**

To store a wishlist of sessions in a Users profile, the `Profile` model was
modified to add a property `sessionWishlist`. This is a repeated string field which
stores the `websafeSessionKey` of each Session the User wishes to add. Adding
to and retrieving from the wishlist is accomplished with the introduction of two
new endpoint methods:

* `addSessionToWishlist`: adds Session to User's wishlist using `websafeSessionKey`
* `getSessionsInWishlist`: returns the Session's which have been stored in a User's wishlist

**Task 3: Indexes and Queries**

Two additional endpoint methods for queries were added.

* `getSessionsByHighlight`: Returns all sessions with a matching highlight
attribute. This allows a quick and concise way for a user or conference organizer
to quickly find out what sessions match a specific highlight. This will allow
a simple method to discover sessions which are similar to ones in a users
wishlist, or to find if a conference is becoming over-saturated with a certain
highlight ('Free Donuts For Showing Up!').
* `getSessionsByStartTime`: Returns sessions which start at a specific time. This
allows for discovery of scheduling conflicts or to find sessions to fill a gap in
a users daily schedule. An automated process can use this endpoint to automatically
notify a conference organizer if too many sessions are planned at one time, or to
notify a user of other sessions at the same time as a canceled session.

For the complex query problem (finding non-workshop sessions before 7pm), NDB
queries are not allowed more than one inequality filter. Executing a query as
described would result in a `BadRequestError` with no result. To work around this
limitation, a primary query of sessions before 7pm can be issued and returned.
This result can be post-processed in Python to eliminate any entries which feature
a `typeOfSession` of 'workshop', leaving us with only those sessions before 7pm
that are not workshops. This unfortunate limitation of Datastore can easily be
countered with Python, though we are still forced to work with a potentially
large data set returned by the query. Carefully considering the response when
constructing our query to minimize the returned set before post-processing is a
necessity in these cases..


**Task 4: Add a Task**

Implementing the "Featured Speaker" functionality was accomplished through the
definition of a new endpoint `getFeaturedSpeaker` as well as modifcation of the
`createSession` endpoint. During the creation of a new session, a check is made
on the speaker to see if their number of sessions is greater than one, per project
guidelines. If so, a new memcache entry is made which contains the name of the
speaker as well as the names of all sessions they are associated with.
