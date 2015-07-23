import os
import jinja2
import webapp2
from google.appengine.ext import ndb

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class Contents(ndb.Model):
    title = ndb.StringProperty()
    content = ndb.StringProperty()


class WritePost(webapp2.RequestHandler):

    def get(self):
        self.response.write('''
        <a href="/Posts">View Posts</a>
        <hr>
        <form method="POST" action="/Posts">
        title:<br>
        <textarea rows="2" cols="70" name="title">
        </textarea>
        <br>
        content:<br>
        <textarea rows="10" cols="70" name="post_content">
        </textarea>
        <br>
        <button type="submit">Post</button>
        </form>
        ''')


class Posts(webapp2.RequestHandler):
    # def get(self):
    #     posts_content = Contents.query().fetch()
    #     self.response.write('<table>')
    #     for pst in posts_content:
    #         self.response.write('<tr> <td> title: {}     content: {} </td> </tr>'.format(pst.title, pst.content))
    #     self.response.write('</table>')

    def get(self):
        contents = Contents.query().fetch()
        template_values = {
            'contents': contents
        }
        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))

    def post(self):
        cnts = Contents(title=self.request.get('title'), content=self.request.get('post_content'))
        cnts.put()
        self.redirect('/Posts')

    def delete(self, contents_id):
        content_key = ndb.Key(Contents, int(contents_id))
        content_key.delete()



class UpdatePost(webapp2.RequestHandler):

    def get(self, contents_id):
        content = Contents.get_by_id(int(contents_id))
        self.response.write('''
            <a href="/">Home</a>
            <a href="/Posts">View Posts</a>
            <hr>
            <form method="POST" action="/UpdatePosts/{0}">
            title:<br>
            <textarea rows="2" cols="70" name="title">{1}
            </textarea>
            <br>
            content:<br>
            <textarea rows="10" cols="70" name="post_content">{2}
            </textarea>
            <br>
            <button type="submit">Upade</button>
            </form>
        '''.format(contents_id, content.title, content.content))

    def post(self, contents_id):
        content = Contents.get_by_id(int(contents_id))
        title = self.request.get('title')
        post_content = self.request.get('post_content')
        if title and content:
            content.title = title
            content.content = post_content
        content.put()
        self.redirect('/Posts')


class Delete(webapp2.RequestHandler):

    def get(self, content_id):

        content_key = ndb.Key(Contents, int(content_id))
        content_key.delete()
        self.redirect('/Posts')


app = webapp2.WSGIApplication([
    ('/', WritePost),
    ('/Posts', Posts),
    (r'/Posts/(\d+)', Posts),
    (r'/UpdatePosts/(\d+)', UpdatePost)
], debug=True)
