import os
from flask import Flask, request, Response, render_template, flash
from flask_cors import CORS, cross_origin
from gensim.models import KeyedVectors

class rocanr(Flask):

    def __init__(self):
        Flask.__init__(self, __name__)
        self.config.from_object(__name__)
        path = os.path.dirname(os.path.realpath(__file__))
        self.config.update(dict(
            VECTOR_FILE = path + '/GoogleNews-vectors.txt'
        ))
        self.config.from_envvar('ROCANR_SETTINGS', silent=True)
        self.count = 0
        self.model = KeyedVectors.load_word2vec_format(self.config['VECTOR_FILE'], binary=False)

    def gen_output(self, request_args, result):
        dim = request_args.get('dim')
        dim = int(dim) if dim else 0
        if dim > self.model.vector_size:
            dim = self.model.vector_size 
        header = request_args.get('hd')
        if header:
            output = 'word,prob'
            if dim > 0:
                output += ',' + ','.join(['d%03d' % (x) for x in range(dim)])
            output += '\n'
        else:
            output = ''
        for (w, p) in result:
            if w.find('"')<0:
                output += '"%s",%0.6f' % (w,p)
                if dim > 0:
                    v = self.model.word_vec(w)[:dim]
                    output += ',' + ','.join(['%0.6f' % (x) for x in v])
                output += '\n'
        return output

app = rocanr()
CORS(app)

import rocanr.views

# http://flask.pocoo.org/docs/0.12/patterns/packages/
# => circular imports

# https://stackoverflow.com/questions/19098295/flask-setting-application-and-request-specific-attributes
# https://kronosapiens.github.io/blog/2014/08/14/understanding-contexts-in-flask.html
# https://stackoverflow.com/questions/35309042/python-how-to-set-global-variables-in-flask
# https://stackoverflow.com/questions/1977362/how-to-create-module-wide-variables-in-python
# https://blog.lerner.co.il/python-attributes/
