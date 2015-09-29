import webapp2

from google.appengine.api import app_identity # Collects information about app
from google.appengine.api import mail         # Send e-mail from app

from conference import ConferenceApi          # Main class from conference.py


class SetAnnouncementHandler(webapp2.RequestHandler):
    def get(self):
        """Set Announcement in Memcache."""
        ConferenceApi._cacheAnnouncement()
        self.response.set_status(204)


class SendConfirmationEmailHandler(webapp2.RequestHandler):
    def post(self):
        """Send an email confirming Conference creation."""
        mail.send_mail(
            'noreply@%s.appspotmail.com' % (
                app_identity.get_application_id()),     # From
            self.request.get('email'),                  # To
            'You created a new Conference!',            # Subject
            'Hi, you have created the following '       # Body
            'conference:\r\n\r\n%s' % self.request.get(
                'conferenceInfo')
        )

class SetFeatureSessionHandler(webapp2.RequestHandler):
    def post(self):
        """Set Announcement in Memcache."""
        ConferenceApi._cacheFeatureSessions(
            self.request.get('speaker'),
            self.request.get('conferenceKey'))
        self.response.set_status(204)

app = webapp2.WSGIApplication([
    ('/crons/set_announcement', SetAnnouncementHandler),
    ('/tasks/send_confirmation_email', SendConfirmationEmailHandler),
    ('/tasks/get_featured_speaker', SetFeatureSessionHandler),
], debug=True)
