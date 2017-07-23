import unittest, rocanr, os, re
from gensim.models import KeyedVectors

class RocanrTestCase(unittest.TestCase):

    def setUp(self):
        self.model = KeyedVectors.load_word2vec_format(rocanr.app.config['VECTOR_FILE'], binary=False)
        rocanr.app.testing = True
        self.app = rocanr.app.test_client()

    def tearDown(self):
        '''no file or database to close'''
        pass

    def test_404(self):
        rv = self.app.get('/no_such_page', follow_redirects=True)
        assert 'not found' in rv.data

    def test_nearest(self):
        rv = self.app.get('/q/nearest?dim=5&w=said&top=10', follow_redirects=True)
        lines = filter(lambda x:x, rv.data.split('\n'))
        assert 10==len(lines)
        for line in lines:
            line = re.sub(r'[^",]', '', line)
            assert re.match(r'^"",{6}$', line)


if __name__ == '__main__':
    unittest.main()

