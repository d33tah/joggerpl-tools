#!/usr/bin/env python

"""
Imports Jogger.pl XML exported file to a Wordpress blog.

Sample usage:

./main.py http://localhost/xmlrpc.php user pass /tmp/20151220_1945_deetah.xml
"""

import lxml.etree
import wordpress_xmlrpc
import dateutil.parser
import sys

class Main(object):
    def main(self, url, login, password, path):
        self.client = wordpress_xmlrpc.Client(url, login, password)
        self.tree = lxml.etree.parse(path)
        entries = self.tree.xpath('//entry')
        for n, entry in enumerate(entries, 1):

            print("%d/%d" % (n, len(entries)))

            post = wordpress_xmlrpc.WordPressPost()

            post.title = entry.xpath('./subject')[0].text
            post.content = entry.xpath('./body')[0].text
            post.post_status = 'publish'
            post.comment_status = 'open'
            # TODO:
            # date
            # categories
            # comment_mode
            # level
            # tags
            # permalink
            # trackback
            # excerpt
            # geshi
            # self-linki

            post_id = self.client.call(wordpress_xmlrpc.methods.posts.NewPost(post))

            comments = entry.xpath('./comment')
            for n, comment_node in enumerate(comments, 1):
                print(">%d/%d" % (n, len(comments)))
                '''
                <comment>
                    <date>2008-03-13 22:11:11</date>
                    <nick>bobiko</nick>
                    <nick_url>http://bobiko.jogger.pl</nick_url>
                    <body>BODY</body>
                    <ip>IP</ip>
                    <trackback></trackback>
                </comment>
                '''
                comment = wordpress_xmlrpc.WordPressComment()
                comment.content = comment_node.xpath('./body')[0].text
                comment.date = dateutil.parser.parse(comment_node.xpath('./date')[0].text)
                try:
                    self.client.call(wordpress_xmlrpc.methods.comments.NewComment(post_id, comment))
                except Exception as e:
                    print(e)

if __name__ == '__main__':
    Main().main(*sys.argv[1:])
