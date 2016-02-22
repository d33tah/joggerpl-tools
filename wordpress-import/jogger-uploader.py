#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, request, redirect, url_for, send_from_directory
from werkzeug import secure_filename

import os
import subprocess
import uuid
import resource
import time

MAIN_PY_PATH = '/home/d33tah/workspace/joggerpl-tools/wordpress-import/main.py'
UPLOAD_FOLDER = '/var/tmp/'
ALLOWED_EXTENSIONS = set(['xml'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024

BOOTSTRAP_BOILERPLATE = """<!DOCTYPE html>
<html lang="pl">

<head>

<meta charset="utf-8">
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%(title)s - joggerpl-wordpress-import</title>

<link
href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css"
integrity="sha384-1q8mTJOASx8j1Au+a5WDVnPi2lkFfwwEAa8hDDdjZlpLegxhjVME1fgjWPGmkzs7"
crossorigin="anonymous"
rel="stylesheet">

<link
rel="stylesheet"
href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap-theme.min.css"
integrity="sha384-fLW2N01lMqjakBkx3l/M9EahuwpSfeNvV63J5ezn3uZzapT0u7EYsXMjQV+0En5r"
crossorigin="anonymous">

<!--[if lt IE 9]>
<script src="https://oss.maxcdn.com/html5shiv/3.7.2/html5shiv.min.js">
</script>
<script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js">
</script>
<![endif]-->

</head>

<body>

<div class="container">

<div class="page-header"><h1>joggerpl-wordpress-import</h1></div>

<div class="panel panel-primary">
<div class="panel-heading"><h3 class="panel-title">%(title)s</h3></div>
<div class="panel-body">%(content)s</div>
</div>

<footer>
<em>Autor: Jacek "d33tah" Wielemborek. Kod źródłowy:
<a href="https://github.com/d33tah/joggerpl-tools/tree/master/wordpress-import"
>https://github.com/d33tah/joggerpl-tools/tree/master/wordpress-import</a></em>
</footer>
</div>

<script
src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js">
</script>

<script
src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/js/bootstrap.min.js"
integrity="sha384-0mSbJDEHialfmuBBQP6A4Qrprq5OVfW37PRR3j5ELqxss1yVqOtnepnHVP9aJ7xS"
crossorigin="anonymous">
</script>

</body>
</html>"""

@app.route("/", methods=['GET', 'POST'])
def index():
    index_content = """
        %(error)s
        <form action="" method=post enctype=multipart/form-data>
            <div class="form-group">
                <label for="url">Adres bloga Wordpress:</label>
                <input id="url" name="url" type="url" class="form-control"
                    placeholder="http://blog.example.com/xmlrpc.php">
            </div>
            <div class="form-group">
                <label for="login">Nazwa użytkownika bloga Wordpress:</label>
                <input id="login" name="login" class="form-control"
                    placeholder="admin">
            </div>
            <div class="form-group">
                <label for="pass">Hasło użytkownika bloga Wordpress:</label>
                <input id="pass" name="pass" type="password"
                    class="form-control" placeholder="haslo">
            </div>

            <div class="form-group">
                <label for="file">Plik wyeksportowany przez jogger.pl:</label>
                <input id="file" type="file" name="file">
            </div>
            <p>
            <strong>Uwaga:</strong>
            <ul>
                <li>Plik XML ze wpisami może zawierać też wpisy prywatne
                    (poziom 1 i powyżej). Jeżeli nie chcesz ich przesyłać na
                    ten serwer, użyj terminalowej wersji tej strony,</li>
                <li>Po zaimportowaniu wpisów należy
                    <strong>zmienić hasło</strong> do Wordpressa.</li>
            </ul>
            </p>

            <button type="submit"class="btn btn-default">Wyślij</button>
        </form>
    """
    error_msg = ''

    if request.method == 'GET':
        return BOOTSTRAP_BOILERPLATE % {'title': 'Podaj dane bloga',
                                        'content':
                                            index_content % {'error': ''}}

    file = request.files['file']
    if not file.filename.endswith('.xml'):
        error_msg = ('Podany plik nie jest plikiem .xml stworzonym'
                     ' przez jogger.pl.')

    if error_msg:
        error = '''
            <div class="alert alert-danger" role="alert">
              <span class="glyphicon glyphicon-exclamation-sign"
                  aria-hidden="true"></span>
              <span class="sr-only">Błąd:</span>
                  %s
            </div>
        ''' % error_msg
        return BOOTSTRAP_BOILERPLATE % {'title': 'Podaj dane bloga',
                                        'content':
                                            index_content % {'error': error}}

    fuuid = str(uuid.uuid4())
    filename = os.path.join(app.config['UPLOAD_FOLDER'], fuuid + '.xml')
    file.save(filename)

    logfuuid = str(uuid.uuid4())
    logfname = os.path.join(app.config['UPLOAD_FOLDER'], logfuuid + '.txt')
    logf = open(logfname, 'w')

    subprocess_environment = dict(os.environ)
    subprocess_environment['REMOVE_ON_EXIT'] = '1'
    def pfn():
        # this function will be called before subprocess Python is run.
        # the limit is there to prevent denial of service by using all memory
        max_memory = 256 * 1024 * 1024  # 128 MiB
        resource.setrlimit(resource.RLIMIT_AS, (max_memory, max_memory))
    subprocess.Popen([
            'python', '-u', MAIN_PY_PATH,
            request.form['url'], request.form['login'], request.form['pass'],
            filename
        ], bufsize=1, stderr=subprocess.STDOUT, stdout=logf, preexec_fn=pfn,
        env=subprocess_environment)
    # sleep for three seconds so we have a change of showing something in a log
    time.sleep(3.0)
    return redirect('/show/%s.txt' % logfuuid)

@app.route('/show/<path:path>')
def show(path):
    response = send_from_directory(app.config['UPLOAD_FOLDER'], path,
                                   cache_timeout=0)
    response.headers['Refresh'] = '2; /show/%s' % path
    return response

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001)
