#!/usr/bin/env python

"""
Imports Jogger.pl XML exported file to a Wordpress blog.

Sample usage:

pip install -r requirements.txt  # first time only; might require sudo
./main.py http://localhost/xmlrpc.php wp_user wp_pass 20151220_1945_deetah.xml
"""

import lxml.etree
import wordpress_xmlrpc
import dateutil.parser
import sys
import re
import signal

PARSE_TIMEOUT = 2

class Main(object):

    def main(self, url, login, password, path):
        self.client = wordpress_xmlrpc.Client(url, login, password)
        # This is just to make sure that the credentials are OK before we jump
        # to XML parsing.
        self.client.call(wordpress_xmlrpc.methods.users.GetUsers())

        # Parse the XML. Give 2 seconds for parsing to prevent abuse.
        signal.alarm(PARSE_TIMEOUT)
        self.tree = lxml.etree.parse(path)
        signal.alarm(0)

        entries = self.tree.xpath('//entry')
        for n, entry in enumerate(entries, 1):

            print("%d/%d" % (n, len(entries)))
            self.handle_post(entry)

    def handle_post(self, entry):

        post = wordpress_xmlrpc.WordPressPost()

        post.title = entry.xpath('./subject')[0].text

        body = entry.xpath('./body')[0].text

        if '{geshi' in body:
            body = re.sub('{geshi lang=([^ ]+).*?}(.*?){/geshi}',
                          '<pre lang="\\1">\\2</pre>', body,
                          flags=re.DOTALL | re.MULTILINE)

        post.content = body
        if '<EXCERPT>' in body:
            post.excerpt = body[:body.find('<EXCERPT>')]

        if int(entry.xpath('./level_id')[0].text) == 0:
            post.post_status = 'publish'

        if entry.xpath('./trackback')[0].text:
            sys.stderr.write("trackback not empty!\n")

        post.comment_status = 'open'
        post.date = dateutil.parser.parse(entry.xpath('./date')[0].text)
        post.slug = entry.xpath('./permalink')[0].text

        categories = []
        for category in entry.xpath('./category'):
            categories += [category.text]
        post.terms_names = { 'category': categories }
        # TODO:
        # tags
        # comment_mode
        # self-linki

        post_id = self.client.call(wordpress_xmlrpc.methods.posts.NewPost(post))

        comments = entry.xpath('./comment')
        for n, comment_node in enumerate(comments, 1):
            print(">%d/%d" % (n, len(comments)))
            comment = wordpress_xmlrpc.WordPressComment()
            comment.content = comment_node.xpath('./body')[0].text
            comment.date = dateutil.parser.parse(comment_node.xpath('./date')[0].text)
            comment.author = comment_node.xpath('./nick')[0].text
            comment.author_url = comment_node.xpath('./nick_url')[0].text
            try:
                comment_id = self.client.call(wordpress_xmlrpc.methods.comments.NewComment(post_id, comment))
                self.client.call(wordpress_xmlrpc.methods.comments.EditComment(comment_id, comment))
            except Exception as e:
                print(repr(e))
        print("Done")


if __name__ == '__main__':
    if len(sys.argv) < 4:
        sys.exit(("Usage: %s http://localhost/xmlrpc.php "
                  "wordpress_username wordpress_password "
                  "jogger_exported.xml") % sys.argv[0])
    Main().main(*sys.argv[1:])
