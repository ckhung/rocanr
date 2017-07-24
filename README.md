# rocanr
vocabulary-in-R^n server: a query-only minimal RESTful interface to gensim.models.keyedvectors

This project is experimental.
It is not for production use.
**Do not expose the service to the outside world.**

## Background

- [Semantic Word Embeddings](http://www.offconvex.org/2015/12/12/word-embeddings-1/)
- [Word2Vec](https://deeplearning4j.org/word2vec)
- [Deep Learning, NLP, and Representations](https://colah.github.io/posts/2014-07-NLP-RNNs-Representations/)

## Running Rocanr

Clone or download this repo.
In the repo's top level directory, do the following:
```
pushd rocanr ; ln -s GoogleNews-vectors-1k.txt GoogleNews-vectors.txt ; popd
virtualenv .env
source .env/bin/activate
pip install --editable .
export FLASK_APP=rocanr
export FLASK_DEBUG=true
flask run --port=5006
```

In your browser, visit http://localhost:5006/q/nearest?w=years
You should see some words and their "probabilities"
being neighbors of the word "years".

Here are a few more example queries:
- ```/q/nearest?w=years&hd=1``` also show a header row
- ```/q/nearest?w=years&topn=20``` show top 20 matches instead of top 10
- ```/q/nearest?w=years&dim=5``` show the first 5 dimensions
  of the word vectors (only meaningful if the pre-trained model
  has been processed by PCA and the dimensions are sorted)
- ```/q/nearest?w=years&dim=9999``` show all available dimensions of the word vectors

For word analogy queries, try:
- ```/q/analogy?w1=he&w2=she&w3=him```
- ```/q/analogy?w1=Friday&w2=week&w3=June```

## The Google News Pre-trained Model File

1. Get Google’s pre-trained Word2Vec model from
[here](http://mccormickml.com/2016/04/12/googles-pretrained-word2vec-model-in-python/). Uncompress the file: ```gunzip GoogleNews-vectors-negative300.bin.gz```
2. Compile the bin-to-txt converter program misc/gw2v-txt.c :
```gcc -Wall misc/gw2v-txt.c -lm -o misc/gw2v-txt```
3. Generate a text version containing "only" the first 60k words for gensim :
```./misc/gw2v-txt -1 -n 60000 /path/to/GoogleNews-vectors-negative300.bin > /path/to/GoogleNews-vectors-60k.txt```
4. Change the symlink: ```ln -sf /path/to/GoogleNews-vectors-60k.txt rocanr/GoogleNews-vectors.txt```

Now you can kill flask and restart it again to use this
larger, more interesting model than the sample one shipped with rocanr.

Note: You can also generate a 1k model from the 60k model like this:
```(echo '1000 300' ; tail -n +2 GoogleNews-vectors-60k.txt | head -n 1000) > GoogleNews-vectors-1k.txt```

## Visualizing the Results with t-sne-lab

See [t-sne-lab](https://ckhung.github.io/t-sne-lab/)
and use misc/rocanr-for-t-sne.json as a configuration file for t-sne-lab.

