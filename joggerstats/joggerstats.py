#!/usr/bin/python -i

from lxml import html
import pickle
try:
    from urllib import urlopen
except ImportError:
    from urllib.request import urlopen

try:
    unicode
except NameError:
    unicode = str


def fetch_users():
    i = 1
    ret = []
    while True:
        url = "http://jogger.pl/users/?page=%d&ord=desc" % i
        print("Pobieram %s" % url)
        body = urlopen(url).read()
        body = body.decode('utf-8')
        t = html.fromstring(body)
        rows = t.xpath('//tr/td[1]/..')
        if rows == []:
            break
        i += 1
        for row in rows:
            data = {}
            data['username'] = unicode(row[0].text_content())
            data['url'] = unicode(row[0][0].get('href'))
            data['xmpp_status'] = unicode(row[1].text_content())
            data['registered'] = unicode(row[2].text_content())
            data['num_entries'] = int(row[3].text_content())
            data['num_comments'] = int(row[4].text_content())
            data['online'] = row.get('class') == 'online'
            ret += [data]
    return ret


if __name__ == "__main__":
    # Feel free to comment the next two lines after first fetching.
    users = fetch_users()
    pickle.dump(users, open('users.pickle', 'wb'))
    users = pickle.load(open('users.pickle', 'rb'))
