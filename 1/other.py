from tornado import ioloop, web, httpclient, escape, httpserver


class MainHandler(web.RequestHandler):
    @web.asynchronous
    def get(self):
        http = httpclient.AsyncHTTPClient()
        http.fetch("http://friendfeed-api.com/v2/feed/bret", callback=self.on_response)

    def on_response(self, response):
        if response.error: raise web.HTTPError(500)
        json = escape.json_decode(response.body)
        self.write("Fetched " + str(len(json["entries"])) + " entries from the FriendFeed API")
        self.finish()


class StoryHandler(web.RequestHandler):
    def get(self, story_id):
        self.write("You requested the story " + story_id)


class MyFormHandler(web.RequestHandler):
    def get(self):
        self.write('''<html><body><form action="/myform" method="post">
            <input type="text" name="message">
            <input type="submit" value="Submit">
            </form></body></html>''')

    def post(self):
        self.set_header("Content-Type", "text/plain")
        self.write("You wrote " + self.get_argument("message"))


class ErrorHandler(web.RequestHandler):
    def get(self):
        raise web.HTTPError(403)


class RedirectHandler(web.RequestHandler):
    def get(self):
        self.redirect('/myform')



application = web.Application([
    (r"/", MainHandler),
    (r"/myform", MyFormHandler),
    (r"/story/([0-9]+)", StoryHandler),
    (r"/er", ErrorHandler),
    (r"/redirect", RedirectHandler),
])

if __name__ == "__main__":
    http_server = httpserver.HTTPServer(application)
    http_server.bind(8888)
    http_server.start(0)
    ioloop.IOLoop.instance().start()
