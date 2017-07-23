from flask import Flask, request, Response, render_template, flash
from rocanr import app
# http://flask.pocoo.org/docs/0.12/patterns/packages/
# => circular imports

@app.route('/')
def home_page():
    return render_template('home_page.html', counter=app.count)

@app.route('/q/nearest')
def q_nearest():
    word = request.args.get('w')
    if not word:
        return Response('arg "w" missing', mimetype='text/plain')
    if not word in app.model.wv.vocab:
        return Response('"%s" not in vocab' % word, mimetype='text/plain')
    topn = request.args.get('topn')
    topn = int(topn) if topn else 10
    result = app.model.most_similar(positive=[word], topn=topn)
    return Response(app.gen_output(request.args, result), mimetype='text/plain')

@app.route('/q/analogy')
def q_analogy():
    word1 = request.args.get('w1')
    word2 = request.args.get('w2')
    word3 = request.args.get('w3')
    if not word1:
        return Response('arg "w1" missing', mimetype='text/plain')
    if not word2:
        return Response('arg "w2" missing', mimetype='text/plain')
    if not word3:
        return Response('arg "w3" missing', mimetype='text/plain')
    if not word1 in app.model.wv.vocab:
        return Response('"%s" not in vocab' % word1, mimetype='text/plain')
    if not word2 in app.model.wv.vocab:
        return Response('"%s" not in vocab' % word2, mimetype='text/plain')
    if not word3 in app.model.wv.vocab:
        return Response('"%s" not in vocab' % word3, mimetype='text/plain')
    topn = request.args.get('topn')
    topn = int(topn) if topn else 10
    result = app.model.most_similar(positive=[word1,word3], negative=[word2], topn=topn)
    return Response(app.gen_output(request.args, result), mimetype='text/plain')
