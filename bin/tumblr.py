#!/usr/local/bin/python

import json
import os
import pytumblr

import basics
import imglib
import render
import useful

TUMBLR_PHOTO = 'P'
TUMBLR_TEXT = 'T'
TUMBLR_QUOTE = 'Q'
TUMBLR_LINK = 'L'
TUMBLR_CHAT = 'C'
TUMBLR_AUDIO = 'A'
TUMBLR_VIDEO = 'V'


class Tumblr(object):
    '''Class for throwing stuff onto Tumblr.
    We only care about writing so that's all I've implemented here.'''

    def __init__(self, pif, name='bamca.tumblr.com'):
        pif.secure.set_config('tumblr')
        self.pif = pif
        self.name = name
        self.client = pytumblr.TumblrRestClient(pif.secure.oauth, pif.secure.secret, pif.secure.key, pif.secure.value)

    # All of these have: state tags tweet date format slug, plus...

    def create_photo(self, **kwargs):
        # kwargs['source'] = kwargs['source'].replace('https:', 'http:')  no longer necessary
        kwargs['link'] = kwargs.get('link', '').replace('beta', 'www')
        fn = kwargs['source'][kwargs['source'].find('/pic') + 1:]
        x, y = imglib.get_size(fn)
        # caption link source data

        content = [
            {"type": "image", "media": [{"type": "image/jpeg", "url": kwargs['source'], "width": x, "height": y}]},
            {"type": "text", "text": kwargs['caption'], "formatting": [
                {"start": 0, "end": len(kwargs['caption']), "type": "link", "url": kwargs['link']}]}
        ]
        response = self.client.create_post(self.name, content=content)
        self.post(TUMBLR_PHOTO, response, **kwargs)

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
            self.pif.dbh.insert_tumblr(ty_post, json.dumps(response), json.dumps(kwargs))
        return response

    def redo(self, post):
        ty_post = post['post_type']
        kwargs = json.loads(post['payload'].replace("'", '"').replace('https:', 'http:').replace('/beta.', '/www.'))
        kwargs['state'] = 'published'
        print(kwargs)
        for tries in range(20):
            if ty_post == TUMBLR_PHOTO:

                kwargs['link'] = kwargs.get('link', '').replace('beta', 'www')
                fn = kwargs['source'][kwargs['source'].find('/pic') + 1:]
                x, y = imglib.get_size(fn)
                # caption link source data

                content = [
                    {"type": "image", "media": [{"type": "image/jpeg", "url": kwargs['source'], "width": x, "height": y}]},
                    {"type": "text", "text": kwargs['caption'], "formatting": [
                        {"start": 0, "end": len(kwargs['caption']), "type": "link", "url": kwargs['link']}]}
                ]
                response = self.client.create_post(self.name, content=content)

                if response.get('state') == 'published':
                    useful.write_message(f'removing from spool ({tries + 1})')
                    self.pif.dbh.delete_tumblr(post['id'])
                    break

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
        print(response)
        print()
        return response


# ---- ---------------------------------------


@basics.web_page
def tumblr_main(pif):
    pif.ren.print_html()
    pif.restrict('a')

    def make_ent(row):
        blob = json.loads(row['payload'].replace("'", '"'))
        resp = json.loads(row['response'].replace("'", '"'))
        ret = {
            'id': f'<a href="{pif.dbh.get_editor_link("tumblr", id=row["id"])}">{row["id"]}</a>',
            'caption': blob['caption'],
            'source': pif.ren.format_link(blob['source'], blob['source'][blob['source'].rfind('/') + 1:]),
            'status': resp['meta']['status'],
            'msg': resp['meta']['msg'],
            'errors': '<br>'.join(resp['response']['errors']),
            'size': os.stat(blob['source'][blob['source'].find('/pic') + 1:]).st_size,
        }
        if blob.get('link'):
            ret['link'] = pif.ren.format_link(blob['link'], blob['link'][blob['link'].rfind('/') + 1:])
        return ret

    cols = ['id', 'caption', 'source', 'link', 'status', 'msg', 'errors', 'size']
    llist = render.Listix(id='tumblr', section=[render.Section(
        id='t', name='', colist=cols, headers=cols,
        range=[render.Range(entry=[make_ent(x) for x in pif.dbh.fetch_tumblr_posts()])])])
    return pif.ren.format_template('simplelistix.html', llineup=llist)


# ---- ---------------------------------------


def post_picture(pif, title, url, link):
    # url = 'http://www.bamca.org/' + largest
    # link = 'http://www.bamca.org/cgi-bin/vars.cgi?mod=%s&var=%s' % (self.man, self.var)
    pass
    useful.write_message('Post to Tumblr: ', Tumblr(pif).create_photo(caption=title, source=url, link=link))


def check_table(pif):
    for post in pif.dbh.fetch_tumblr_posts():
        print(post)


def redo_posts(pif, *args):
    args = [int(x) for x in args]
    posts = pif.dbh.fetch_tumblr_posts()
    print(len(posts), 'posts waiting')
    for post in posts:
        if not args or post['id'] in args:
            response = Tumblr(pif).redo(post)
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
