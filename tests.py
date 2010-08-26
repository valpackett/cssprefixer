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

    def test_webkit(self):
        self.assertEqual(cssprefixer.process('a{background-clip: padding-box}', minify=True),
                         'a{background-clip:padding-box;-webkit-background-clip:padding-box}')

    def test_ie_and_opera(self):
        self.assertEqual(cssprefixer.process('a{text-overflow: ellipsis}', minify=True),
                         'a{text-overflow:ellipsis;-o-text-overflow:ellipsis;-ms-text-overflow:ellipsis}')

    def test_moz_border_radius(self):
        self.assertEqual(cssprefixer.process('a{border-top-left-radius: 1em;border-top-right-radius: 1em;border-bottom-right-radius: 1em;border-bottom-left-radius: 1em;}', minify=True),
                         'a{border-top-left-radius:1em;border-top-right-radius:1em;border-bottom-right-radius:1em;border-bottom-left-radius:1em;-webkit-border-top-left-radius:1em;-moz-border-radius-topleft:1em;-webkit-border-top-right-radius:1em;-moz-border-radius-topright:1em;-webkit-border-bottom-right-radius:1em;-moz-border-radius-bottomright:1em;-webkit-border-bottom-left-radius:1em;-moz-border-radius-bottomleft:1em}')

if __name__ == '__main__':
    unittest.main()
