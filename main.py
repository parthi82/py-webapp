import os
import urllib
import jinja2
import webapp2
from google.appengine.ext import ndb


class Contents(ndb.Model):
    title = ndb.StringProperty()
    content = ndb.StringProperty()


class WritePost(webapp2.RequestHandler):

    def get(self):
        self.response.write('''
        <a href=/Posts>View Posts</a>
        <br>
        <br>
        <form method="POST" action="/Posts">
        title:<br>
        <input type="text" name="title">
        <br>
        content:<br>
        <input type="text" name="post_content">
        <br>
        <button type="submit">Post</button>
        </form>
        ''')


class Posts(webapp2.RequestHandler):

    def get(self):
        posts_content = Contents.query().fetch()
        self.response.write('<table>')
        for pst in posts_content:
            self.response.write('<tr> <td> title: {}     content: {} </td> </tr>'.format(pst.title, pst.content))
        self.response.write('</table>')

    def post(self):
        cnts = Contents(title=self.request.get('title'), content=self.request.get('post_content'))
        cnts.put()
        self.redirect('/Posts')

app = webapp2.WSGIApplication([
    ('/', WritePost),
    ('/Posts', Posts)
], debug=True)
