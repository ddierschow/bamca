#!/usr/local/bin/python

from sprint import sprint as print
import pytumblr

import basics
import useful

TUMBLR_PHOTO = 'P'
TUMBLR_TEXT = 'T'
TUMBLR_QUOTE = 'Q'
TUMBLR_LINK = 'L'
TUMBLR_CHAT = 'C'
TUMBLR_AUDIO = 'A'
TUMBLR_VIDEO = 'V'


class Client(object):
    def __init__(self, oauth_key, oauth_secret, client_key, client_secret):
        self.oauth_key = oauth_key
        self.oauth_secret = oauth_secret
        self.client_key = client_key
        self.client_secret = client_secret
        self.url = 'https://api.tumblr.com/'

    def create_photo(self, **kwargs):
        url = self.url + '/v2/blog/bamca.tumblr.com/posts'
        return {}


class Tumblr(object):
    '''Class for throwing stuff onto Tumblr.
    We only care about writing so that's all I've implemented here.'''

    def __init__(self, pif, name='bamca.tumblr.com'):
        pif.secure.set_config('tumblr')
        self.pif = pif
        self.name = name
        self.client = pytumblr.TumblrRestClient(pif.secure.oauth, pif.secure.secret, pif.secure.key, pif.secure.value)
        # self.client = Client(pif.secure.oauth, pif.secure.secret, pif.secure.key, pif.secure.value)

    # All of these have: state tags tweet date format slug, plus...

    def create_photo(self, **kwargs):
        kwargs['source'] = kwargs['source'].replace('https:', 'http:')
        # caption link source data
        return self.post(TUMBLR_PHOTO, self.client.create_photo(self.name, **kwargs), **kwargs)

    # def create_text(self, **kwargs):
    #     # title body
    #     return self.post(TUMBLR_TEXT, self.client.create_text(self.name, **kwargs), **kwargs)

    # def create_quote(self, **kwargs):
    #     # quote source
    #     return self.post(TUMBLR_QUOTE, self.client.create_quote(self.name, **kwargs), **kwargs)

    # def create_link(self, **kwargs):
    #     # title url description
    #     return self.post(TUMBLR_LINK, self.client.create_link(self.name, **kwargs), **kwargs)

    # def create_chat(self, **kwargs):
    #     # title conversation
    #     return self.post(TUMBLR_CHAT, self.client.create_chat(self.name, **kwargs), **kwargs)

    # def create_audio(self, **kwargs):
    #     # caption external_url data
    #     return self.post(TUMBLR_AUDIO, self.client.create_audio(self.name, **kwargs), **kwargs)

    # def create_video(self, **kwargs):
    #     # caption embed data
    #     return self.post(TUMBLR_VIDEO, self.client.create_video(self.name, **kwargs), **kwargs)

    def post(self, ty_post, response, **kwargs):
        if response.get('state') != 'published':
            useful.write_message('spooling for later')
            self.pif.dbh.insert_tumblr(ty_post, str(response), str(kwargs))
        return response

    def redo(self, post):
        useful.write_message('removing from spool')
        self.pif.dbh.delete_tumblr(post.id)
        ty_post = post.post_type
        kwargs = eval(post.payload)
        print(kwargs)
        if ty_post == TUMBLR_PHOTO:
            response = self.create_photo(**kwargs)
        # elif ty_post == TUMBLR_TEXT:
        #     response = self.create_text(**kwargs)
        # elif ty_post == TUMBLR_QUOTE:
        #     response = self.create_quote(**kwargs)
        # elif ty_post == TUMBLR_LINK:
        #     response = self.create_link(**kwargs)
        # elif ty_post == TUMBLR_CHAT:
        #     response = self.create_chat(**kwargs)
        # elif ty_post == TUMBLR_AUDIO:
        #     response = self.create_audio(**kwargs)
        # elif ty_post == TUMBLR_VIDEO:
        #     response = self.create_video(**kwargs)
        else:
            response = {'state': 'published'}
        return response


# ---- ---------------------------------------


def post_picture(pif, title, link):
    # url = 'http://www.bamca.org/' + largest
    # link = 'http://www.bamca.org/cgi-bin/vars.cgi?mod=%s&var=%s' % (self.man, self.var)
    pass
    # useful.write_message('Post to Tumblr: ', Tumblr(pif).create_photo(caption=title, source=url, link=link))


def check_table(pif):
    for post in pif.dbh.fetch_tumblr_posts():
        print(post)


def redo_posts(pif):
    posts = pif.dbh.fetch_tumblr_posts()
    print(len(posts), 'posts waiting')
    for post in posts:
        print(post)
        response = Tumblr(pif).redo(post)
        print(response)
        if response.get('state') != 'published':
            break


cmds = {
    ('p', post_picture, "picture"),
    ('c', check_table, "check"),
    ('r', redo_posts, "redo"),
}


# ---- ---------------------------------------


if __name__ == '__main__':  # pragma: no cover
    basics.process_command_list(cmds=cmds, dbedit='')
