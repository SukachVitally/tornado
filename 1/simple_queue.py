#test  sdfsdf
import HTMLParser
from tornado import httpclient, gen, ioloop, queues

base_url = 'http://www.tornadoweb.org/en/stable/'

@gen.coroutine
def get_links_from_url(url):
    try:
        response = yield httpclient.AsyncHTTPClient.fetch(url)
        print response

    except Exception as e:
        print('Exception: %s %s' % (e, url))



@gen.coroutine
def main():
    q = queues.Queue()
    q.put(base_url)






if __name__ == '__main__':
    io_loop = ioloop.IOLoop.current()
    io_loop.run_sync(main)