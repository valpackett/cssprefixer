#!/usr/bin/env python
# CSSPrefixer
# Copyright 2010 MyFreeWeb <me@myfreeweb.ru>

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

# http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import unittest
import cssprefixer

class PrefixerTestCase(unittest.TestCase):
    def test_common(self):
        self.assertEqual(cssprefixer.process('a{border-radius: 1em}', minify=True),
                         'a{-webkit-border-radius:1em;-moz-border-radius:1em;border-radius:1em}')

    def test_common_and_opera(self):
        self.assertEqual(cssprefixer.process('a{transform: rotate(10deg)}', minify=True),
                         'a{-webkit-transform:rotate(10deg);-moz-transform:rotate(10deg);-o-transform:rotate(10deg);transform:rotate(10deg)}')

    def test_webkit(self):
        self.assertEqual(cssprefixer.process('a{background-clip: padding-box}', minify=True),
                         'a{-webkit-background-clip:padding-box;background-clip:padding-box}')

    def test_ie_and_opera(self):
        self.assertEqual(cssprefixer.process('a{text-overflow: ellipsis}', minify=True),
                         'a{-o-text-overflow:ellipsis;-ms-text-overflow:ellipsis;text-overflow:ellipsis}')

    def test_moz_border_radius(self):
        self.assertEqual(cssprefixer.process('a{border-top-left-radius: 1em;border-top-right-radius: 1em;border-bottom-right-radius: 1em;border-bottom-left-radius: 1em;}', minify=True),
                         'a{-webkit-border-top-left-radius:1em;-moz-border-radius-topleft:1em;border-top-left-radius:1em;-webkit-border-top-right-radius:1em;-moz-border-radius-topright:1em;border-top-right-radius:1em;-webkit-border-bottom-right-radius:1em;-moz-border-radius-bottomright:1em;border-bottom-right-radius:1em;-webkit-border-bottom-left-radius:1em;-moz-border-radius-bottomleft:1em;border-bottom-left-radius:1em}')

    def test_flexbox(self):
        self.assertEqual(cssprefixer.process('a{display: box;}', minify=True),
                         'a{display:-webkit-box;display:-moz-box;display:box}')
                         
    def test_displaybox(self):
        self.assertEqual(cssprefixer.process('a{display: display;}', minify=True),
                         'a{display:display}')

    def test_mq(self):
        self.assertEqual(cssprefixer.process('@media screen and (min-width:480px){a{color:red}}', minify=True),
                         '@media screen and (min-width:480px){a{color:red}}')
                         
    def test_mq_common(self):
        self.assertEqual(cssprefixer.process('@media screen and (min-width:480px){a{border-radius: 1em}}', minify=True),
                         '@media screen and (min-width:480px){a{-webkit-border-radius:1em;-moz-border-radius:1em;border-radius:1em}}')
                         
    def test_duplicate_common(self):
        self.assertEqual(cssprefixer.process('a{border-radius: 1em;border-radius: 2em;border-radius: 3em}', minify=True),
                         'a{-webkit-border-radius:3em;-moz-border-radius:3em;border-radius:3em}')
                         
    def test_mixed_common(self):
        self.assertEqual(cssprefixer.process('a{-moz-border-radius: 1em;border-radius: 2em;-webkit-border-radius: 3em}', minify=True),
                         'a{-webkit-border-radius:3em;-moz-border-radius:3em;border-radius:3em}')
                         
    def test_no_mini(self):
        self.assertEqual(cssprefixer.process('''.my-class, #my-id {
    border-radius: 1em;
    transition: all 1s ease;
    box-shadow: #123456 0 0 10px;
    display: box;
}''', minify=False), '''.my-class, #my-id {
    -webkit-border-radius: 1em;
    -moz-border-radius: 1em;
    border-radius: 1em;
    -webkit-transition: all 1s ease;
    -moz-transition: all 1s ease;
    -o-transition: all 1s ease;
    transition: all 1s ease;
    -webkit-box-shadow: #123456 0 0 10px;
    -moz-box-shadow: #123456 0 0 10px;
    box-shadow: #123456 0 0 10px;
    display: -webkit-box;
    display: -moz-box;
    display: box;
}''')

    def test_empty(self):
        self.assertEqual(cssprefixer.process('a{}', minify=True), '')
        self.assertEqual(cssprefixer.process('a{}', minify=False), '')
                         
class WebkitPrefixerTestCase(unittest.TestCase):
    def test_common(self):
        self.assertEqual(cssprefixer.process('a{-webkit-border-radius: 1em}', minify=True),
                         'a{-webkit-border-radius:1em;-moz-border-radius:1em;border-radius:1em}')
                         
    def test_common_and_opera(self):
        self.assertEqual(cssprefixer.process('a{-webkit-transform: rotate(10deg)}', minify=True),
                         'a{-webkit-transform:rotate(10deg);-moz-transform:rotate(10deg);-o-transform:rotate(10deg);transform:rotate(10deg)}')
                         
    def test_webkit(self):
        self.assertEqual(cssprefixer.process('a{-webkit-background-clip: padding-box}', minify=True),
                         'a{-webkit-background-clip:padding-box;background-clip:padding-box}')

    def test_moz_border_radius(self):
        self.assertEqual(cssprefixer.process('a{-webkit-border-top-left-radius: 1em;-webkit-border-top-right-radius: 1em;-webkit-border-bottom-right-radius: 1em;-webkit-border-bottom-left-radius: 1em;}', minify=True),
                         'a{-webkit-border-top-left-radius:1em;-moz-border-radius-topleft:1em;border-top-left-radius:1em;-webkit-border-top-right-radius:1em;-moz-border-radius-topright:1em;border-top-right-radius:1em;-webkit-border-bottom-right-radius:1em;-moz-border-radius-bottomright:1em;border-bottom-right-radius:1em;-webkit-border-bottom-left-radius:1em;-moz-border-radius-bottomleft:1em;border-bottom-left-radius:1em}')
                         
    def test_flexbox(self):
        self.assertEqual(cssprefixer.process('a{-webkit-display: box;}', minify=True),
                         'a{display:-webkit-box;display:-moz-box;display:box}')
                         
    def test_mq_common(self):
        self.assertEqual(cssprefixer.process('@media screen and (min-width:480px){a{-webkit-border-radius: 1em}}', minify=True),
                         '@media screen and (min-width:480px){a{-webkit-border-radius:1em;-moz-border-radius:1em;border-radius:1em}}')                           
                         
class MozPrefixerTestCase(unittest.TestCase):
    def test_common(self):
        self.assertEqual(cssprefixer.process('a{-moz-border-radius: 1em}', minify=True),
                         'a{-webkit-border-radius:1em;-moz-border-radius:1em;border-radius:1em}')
                         
    def test_common_and_opera(self):
        self.assertEqual(cssprefixer.process('a{-moz-transform: rotate(10deg)}', minify=True),
                         'a{-webkit-transform:rotate(10deg);-moz-transform:rotate(10deg);-o-transform:rotate(10deg);transform:rotate(10deg)}')
                         
    def test_moz_border_radius(self):
        self.assertEqual(cssprefixer.process('a{-moz-border-top-left-radius: 1em;-moz-border-top-right-radius: 1em;-moz-border-bottom-right-radius: 1em;-moz-border-bottom-left-radius: 1em;}', minify=True),
                         'a{-webkit-border-top-left-radius:1em;-moz-border-radius-topleft:1em;border-top-left-radius:1em;-webkit-border-top-right-radius:1em;-moz-border-radius-topright:1em;border-top-right-radius:1em;-webkit-border-bottom-right-radius:1em;-moz-border-radius-bottomright:1em;border-bottom-right-radius:1em;-webkit-border-bottom-left-radius:1em;-moz-border-radius-bottomleft:1em;border-bottom-left-radius:1em}')
                         
    def test_flexbox(self):
        self.assertEqual(cssprefixer.process('a{-moz-display: box;}', minify=True),
                         'a{display:-webkit-box;display:-moz-box;display:box}')  
                         
    def test_mq_common(self):
        self.assertEqual(cssprefixer.process('@media screen and (min-width:480px){a{-moz-border-radius: 1em}}', minify=True),
                         '@media screen and (min-width:480px){a{-webkit-border-radius:1em;-moz-border-radius:1em;border-radius:1em}}')                        
                         
class OperaPrefixerTestCase(unittest.TestCase):
    def test_common_and_opera(self):
        self.assertEqual(cssprefixer.process('a{-o-transform: rotate(10deg)}', minify=True),
                         'a{-webkit-transform:rotate(10deg);-moz-transform:rotate(10deg);-o-transform:rotate(10deg);transform:rotate(10deg)}')
                         
    def test_ie_and_opera(self):
        self.assertEqual(cssprefixer.process('a{-o-text-overflow: ellipsis}', minify=True),
                         'a{-o-text-overflow:ellipsis;-ms-text-overflow:ellipsis;text-overflow:ellipsis}')                         

class IePrefixerTestCase(unittest.TestCase):
    def test_ie_and_opera(self):
        self.assertEqual(cssprefixer.process('a{-ms-text-overflow: ellipsis}', minify=True),
                         'a{-o-text-overflow:ellipsis;-ms-text-overflow:ellipsis;text-overflow:ellipsis}')   
                         
if __name__ == '__main__':
    unittest.main()
