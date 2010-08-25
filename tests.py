#!/usr/bin/env python
import unittest
import cssprefixer

class PrefixerTestCase(unittest.TestCase):
    def test_common(self):
        self.assertEqual(cssprefixer.process('a{border-radius: 1em}', minify=True),
                         'a{border-radius:1em;-webkit-border-radius:1em;-moz-border-radius:1em}')

    def test_common_and_opera(self):
        self.assertEqual(cssprefixer.process('a{transform: rotate(10deg)}', minify=True),
                         'a{transform:rotate(10deg);-webkit-transform:rotate(10deg);-moz-transform:rotate(10deg);-o-transform:rotate(10deg)}')

if __name__ == '__main__':
    unittest.main()
