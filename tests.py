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
                         'a{-moz-border-radius:1em;-webkit-border-radius:1em;border-radius:1em}')

    def test_common_and_opera(self):
        self.assertEqual(cssprefixer.process('a{transform: rotate(10deg)}', minify=True),
                         'a{-moz-transform:rotate(10deg);-ms-transform:rotate(10deg);-o-transform:rotate(10deg);-webkit-transform:rotate(10deg);transform:rotate(10deg)}')

    def test_undefined(self):
        #test prefixed styles that don't have a rule yet, we use a fake property
        #for this test becuase we will never have a rule for this
        self.assertEqual(cssprefixer.process('a{-webkit-faker: black}', minify=True),
                         'a{-webkit-faker:black}')

    def test_webkit(self):
        self.assertEqual(cssprefixer.process('a{background-clip: padding-box}', minify=True),
                         'a{-webkit-background-clip:padding-box;background-clip:padding-box}')

    def test_appearance(self):
        #test prefixed styles that don't have a rule yet, we use a fake property
        #for this test becuase we will never have a rule for this
        self.assertEqual(cssprefixer.process('a{-webkit-appearance: none;}', minify=True),
                         'a{-webkit-appearance:none;appearance:none}')

    def test_ie_and_opera(self):
        self.assertEqual(cssprefixer.process('a{text-overflow: ellipsis}', minify=True),
                         'a{-ms-text-overflow:ellipsis;-o-text-overflow:ellipsis;text-overflow:ellipsis}')

    def test_moz_border_radius(self):
        self.assertEqual(cssprefixer.process('a{border-top-left-radius: 1em;border-top-right-radius: 1em;border-bottom-right-radius: 1em;border-bottom-left-radius: 1em;}', minify=True),
                         'a{-webkit-border-top-left-radius:1em;-moz-border-radius-topleft:1em;border-top-left-radius:1em;-webkit-border-top-right-radius:1em;-moz-border-radius-topright:1em;border-top-right-radius:1em;-webkit-border-bottom-right-radius:1em;-moz-border-radius-bottomright:1em;border-bottom-right-radius:1em;-webkit-border-bottom-left-radius:1em;-moz-border-radius-bottomleft:1em;border-bottom-left-radius:1em}')

    def test_flexbox(self):
        self.assertEqual(cssprefixer.process('a{display: box;}', minify=True),
                         'a{display:-moz-box;display:-webkit-box;display:box}')

    def test_displaybox(self):
        self.assertEqual(cssprefixer.process('a{display: display;}', minify=True),
                         'a{display:display}')

    def test_mq(self):
        self.assertEqual(cssprefixer.process('@media screen and (min-width:480px){a{color:red}}', minify=True),
                         '@media screen and (min-width:480px){a{color:red}}')

    def test_mq_common(self):
        self.assertEqual(cssprefixer.process('@media screen and (min-width:480px){a{border-radius: 1em}}', minify=True),
                         '@media screen and (min-width:480px){a{-moz-border-radius:1em;-webkit-border-radius:1em;border-radius:1em}}')

    def test_duplicate_common(self):
        self.assertEqual(cssprefixer.process('a{border-radius: 1em;border-radius: 2em;border-radius: 3em}', minify=True),
                         'a{-moz-border-radius:1em;-webkit-border-radius:1em;border-radius:1em;-moz-border-radius:2em;-webkit-border-radius:2em;border-radius:2em;-moz-border-radius:3em;-webkit-border-radius:3em;border-radius:3em}')

    def test_mixed_common(self):
        self.assertEqual(cssprefixer.process('a{-moz-border-radius: 1em;border-radius: 2em;-webkit-border-radius: 3em}', minify=True),
                         'a{-moz-border-radius:1em;-webkit-border-radius:1em;border-radius:1em;-moz-border-radius:2em;-webkit-border-radius:2em;border-radius:2em;-moz-border-radius:3em;-webkit-border-radius:3em;border-radius:3em}')

    def test_mixed_duplicate(self):
        self.assertEqual(cssprefixer.process('a{-moz-border-radius: 1em;border-radius: 1em;-webkit-border-radius: 1em}', minify=True),
                         'a{-moz-border-radius:1em;-webkit-border-radius:1em;border-radius:1em}')

    def test_transition(self):
        self.assertEqual(cssprefixer.process('''div {
      -webkit-transition: color .25s linear, -webkit-transform .15s linear .1s;
    }''', minify=False), '''div {
    -moz-transition: color 0.25s linear, -moz-transform 0.15s linear 0.1s;
    -o-transition: color 0.25s linear, -o-transform 0.15s linear 0.1s;
    -webkit-transition: color 0.25s linear, -webkit-transform 0.15s linear 0.1s;
    transition: color 0.25s linear, transform 0.15s linear 0.1s
    }''')

    def test_multi_transition(self):
        self.assertEqual(cssprefixer.process('''div {
    transition: color .25s linear;
    transition: background-color .15s linear .1;
    }''', minify=False), '''div {
    -moz-transition: color 0.25s linear;
    -o-transition: color 0.25s linear;
    -webkit-transition: color 0.25s linear;
    transition: color 0.25s linear;
    -moz-transition: background-color 0.15s linear 0.1;
    -o-transition: background-color 0.15s linear 0.1;
    -webkit-transition: background-color 0.15s linear 0.1;
    transition: background-color 0.15s linear 0.1
    }''')

    def test_transition_property(self):
        self.assertEqual(cssprefixer.process('''div {
    -webkit-transition-property: -webkit-transform, opacity, left;
    -webkit-transition-duration: rotatey(45deg), 2s, 4s;
    }''', minify=False), '''div {
    -moz-transition-property: -moz-transform, opacity, left;
    -o-transition-property: -o-transform, opacity, left;
    -webkit-transition-property: -webkit-transform, opacity, left;
    transition-property: transform, opacity, left;
    -moz-transition-duration: rotatey(45deg), 2s, 4s;
    -o-transition-duration: rotatey(45deg), 2s, 4s;
    -webkit-transition-duration: rotatey(45deg), 2s, 4s;
    transition-duration: rotatey(45deg), 2s, 4s
    }''')

    def test_opacity(self):
        self.assertEqual(cssprefixer.process('''a {
    opacity: 0.25;
    }''', minify=False), '''a {
    -ms-filter: "progid:DXImageTransform.Microsoft.Alpha(Opacity=25)";
    filter: alpha(opacity=25);
    opacity: 0.25
    }''')

    def test_no_mini(self):
        self.assertEqual(cssprefixer.process('''.my-class, #my-id {
    border-radius: 1em;
    transition: all 1s ease;
    box-shadow: #123456 0 0 10px;
    display: box;
}''', minify=False), '''.my-class, #my-id {
    -moz-border-radius: 1em;
    -webkit-border-radius: 1em;
    border-radius: 1em;
    -moz-transition: all 1s ease;
    -o-transition: all 1s ease;
    -webkit-transition: all 1s ease;
    transition: all 1s ease;
    -moz-box-shadow: #123456 0 0 10px;
    -webkit-box-shadow: #123456 0 0 10px;
    box-shadow: #123456 0 0 10px;
    display: -moz-box;
    display: -webkit-box;
    display: box
    }''')

    def test_empty(self):
        self.assertEqual(cssprefixer.process('a{}', minify=True), '')
        self.assertEqual(cssprefixer.process('a{}', minify=False), '')

    def test_media_no_mini(self):
        self.assertEqual(cssprefixer.process('''@media screen and (max-device-width: 480px){
    #book{
        border-radius: 1em;
    }
}''', minify=False), '''@media screen and (max-device-width: 480px) {
    #book {
        -moz-border-radius: 1em;
        -webkit-border-radius: 1em;
        border-radius: 1em
        }
    }''')

    def test_comment(self):
        self.assertEqual(cssprefixer.process('''/* HTML5 display-role reset for older browsers */
article, aside, details, figcaption, figure, footer, header, hgroup, menu, nav, section {
    display: block
    }''', minify=False), '''/* HTML5 display-role reset for older browsers */
article, aside, details, figcaption, figure, footer, header, hgroup, menu, nav, section {
    display: block
    }''')

    def test_inline_comment(self):
        #TODO: it would be nice if comments on the same line remained there, but this may not be possible because
        #cssutils tears everything apart into objects and then we rebuild it.
        self.assertEqual(cssprefixer.process('''article, aside, details, figcaption, figure, footer, header, hgroup, menu, nav, section {
    display: block;/* HTML5 display-role reset for older browsers */
    }''', minify=False), '''article, aside, details, figcaption, figure, footer, header, hgroup, menu, nav, section {
    display: block;
    /* HTML5 display-role reset for older browsers */
    }''')
        self.assertEqual(cssprefixer.process('''article, aside, details, figcaption, figure, footer, header, hgroup, menu, nav, section {
    /* HTML5 display-role reset for older browsers */
    display: block;
    }''', minify=False), '''article, aside, details, figcaption, figure, footer, header, hgroup, menu, nav, section {
    /* HTML5 display-role reset for older browsers */
    display: block
    }''')

class WebkitPrefixerTestCase(unittest.TestCase):
    def test_common(self):
        self.assertEqual(cssprefixer.process('a{-webkit-border-radius: 1em}', minify=True),
                         'a{-moz-border-radius:1em;-webkit-border-radius:1em;border-radius:1em}')

    def test_common_and_opera(self):
        self.assertEqual(cssprefixer.process('a{-webkit-transform: rotate(10deg)}', minify=True),
                         'a{-moz-transform:rotate(10deg);-ms-transform:rotate(10deg);-o-transform:rotate(10deg);-webkit-transform:rotate(10deg);transform:rotate(10deg)}')

    def test_webkit(self):
        self.assertEqual(cssprefixer.process('a{-webkit-background-clip: padding-box}', minify=True),
                         'a{-webkit-background-clip:padding-box;background-clip:padding-box}')

    def test_moz_border_radius(self):
        self.assertEqual(cssprefixer.process('a{-webkit-border-top-left-radius: 1em;-webkit-border-top-right-radius: 1em;-webkit-border-bottom-right-radius: 1em;-webkit-border-bottom-left-radius: 1em;}', minify=True),
                         'a{-webkit-border-top-left-radius:1em;-moz-border-radius-topleft:1em;border-top-left-radius:1em;-webkit-border-top-right-radius:1em;-moz-border-radius-topright:1em;border-top-right-radius:1em;-webkit-border-bottom-right-radius:1em;-moz-border-radius-bottomright:1em;border-bottom-right-radius:1em;-webkit-border-bottom-left-radius:1em;-moz-border-radius-bottomleft:1em;border-bottom-left-radius:1em}')

    def test_flexbox(self):
        self.assertEqual(cssprefixer.process('a{-webkit-display: box;}', minify=True),
                         'a{display:-moz-box;display:-webkit-box;display:box}')

    def test_mq_common(self):
        self.assertEqual(cssprefixer.process('@media screen and (min-width:480px){a{-webkit-border-radius: 1em}}', minify=True),
                         '@media screen and (min-width:480px){a{-moz-border-radius:1em;-webkit-border-radius:1em;border-radius:1em}}')

class MozPrefixerTestCase(unittest.TestCase):
    def test_common(self):
        self.assertEqual(cssprefixer.process('a{-moz-border-radius: 1em}', minify=True),
                         'a{-moz-border-radius:1em;-webkit-border-radius:1em;border-radius:1em}')

    def test_common_and_opera(self):
        self.assertEqual(cssprefixer.process('a{-moz-transform: rotate(10deg)}', minify=True),
                         'a{-moz-transform:rotate(10deg);-ms-transform:rotate(10deg);-o-transform:rotate(10deg);-webkit-transform:rotate(10deg);transform:rotate(10deg)}')

    def test_moz_border_radius(self):
        self.assertEqual(cssprefixer.process('a{-moz-border-top-left-radius: 1em;-moz-border-top-right-radius: 1em;-moz-border-bottom-right-radius: 1em;-moz-border-bottom-left-radius: 1em;}', minify=True),
                         'a{-webkit-border-top-left-radius:1em;-moz-border-radius-topleft:1em;border-top-left-radius:1em;-webkit-border-top-right-radius:1em;-moz-border-radius-topright:1em;border-top-right-radius:1em;-webkit-border-bottom-right-radius:1em;-moz-border-radius-bottomright:1em;border-bottom-right-radius:1em;-webkit-border-bottom-left-radius:1em;-moz-border-radius-bottomleft:1em;border-bottom-left-radius:1em}')

    def test_flexbox(self):
        self.assertEqual(cssprefixer.process('a{-moz-display: box;}', minify=True),
                         'a{display:-moz-box;display:-webkit-box;display:box}')

    def test_mq_common(self):
        self.assertEqual(cssprefixer.process('@media screen and (min-width:480px){a{-moz-border-radius: 1em}}', minify=True),
                         '@media screen and (min-width:480px){a{-moz-border-radius:1em;-webkit-border-radius:1em;border-radius:1em}}')

class OperaPrefixerTestCase(unittest.TestCase):
    def test_common_and_opera(self):
        self.assertEqual(cssprefixer.process('a{-o-transform: rotate(10deg)}', minify=True),
                         'a{-moz-transform:rotate(10deg);-ms-transform:rotate(10deg);-o-transform:rotate(10deg);-webkit-transform:rotate(10deg);transform:rotate(10deg)}')

    def test_ie_and_opera(self):
        self.assertEqual(cssprefixer.process('a{-o-text-overflow: ellipsis}', minify=True),
                         'a{-ms-text-overflow:ellipsis;-o-text-overflow:ellipsis;text-overflow:ellipsis}')

class IePrefixerTestCase(unittest.TestCase):
    def test_ie_and_opera(self):
        self.assertEqual(cssprefixer.process('a{-ms-text-overflow: ellipsis}', minify=True),
                         'a{-ms-text-overflow:ellipsis;-o-text-overflow:ellipsis;text-overflow:ellipsis}')

class GradientTestCase(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(cssprefixer.process('''.box_gradient {
    background-image: linear-gradient(top, #444444, #999999);
    }''', minify=False), '''.box_gradient {
    background-image: -moz-linear-gradient(top, #444, #999);
    background-image: -o-linear-gradient(top, #444, #999);
    background-image: -webkit-linear-gradient(top, #444, #999);
    background-image: -webkit-gradient(linear, left top, left bottom, color-stop(0, #444), color-stop(1, #999));
    filter: "progid:DXImageTransform.Microsoft.gradient(startColorStr=#444, EndColorStr=#999)";
    background-image: linear-gradient(top, #444, #999)
    }''')

    def test_linear_no_pos(self):
        self.assertEqual(cssprefixer.process('''.box_gradient {
    background-image: linear-gradient(#444444, #999999);
    }''', minify=False), '''.box_gradient {
    background-image: -moz-linear-gradient(#444, #999);
    background-image: -o-linear-gradient(#444, #999);
    background-image: -webkit-linear-gradient(#444, #999);
    background-image: -webkit-gradient(linear, left top, left bottom, color-stop(0, #444), color-stop(1, #999));
    filter: "progid:DXImageTransform.Microsoft.gradient(startColorStr=#444, EndColorStr=#999)";
    background-image: linear-gradient(#444, #999)
    }''')

    def test_webkit(self):
        self.assertEqual(cssprefixer.process('''.box_gradient {
    background-image: -webkit-linear-gradient(top, #444444, #999999);
    }''', minify=False), '''.box_gradient {
    background-image: -moz-linear-gradient(top, #444, #999);
    background-image: -o-linear-gradient(top, #444, #999);
    background-image: -webkit-linear-gradient(top, #444, #999);
    background-image: -webkit-gradient(linear, left top, left bottom, color-stop(0, #444), color-stop(1, #999));
    filter: "progid:DXImageTransform.Microsoft.gradient(startColorStr=#444, EndColorStr=#999)";
    background-image: linear-gradient(top, #444, #999)
    }''')

    def test_webkit_mixed(self):
        self.assertEqual(cssprefixer.process('''.box_gradient {
    background-image: -webkit-linear-gradient(top, #444444, #999999), linear-gradient(top, black, white);
    }''', minify=False), '''.box_gradient {
    background-image: -moz-linear-gradient(top, #444, #999), -moz-linear-gradient(top, black, white);
    background-image: -o-linear-gradient(top, #444, #999), -o-linear-gradient(top, black, white);
    background-image: -webkit-linear-gradient(top, #444, #999), -webkit-linear-gradient(top, black, white);
    background-image: -webkit-gradient(linear, left top, left bottom, color-stop(0, #444), color-stop(1, #999)), -webkit-gradient(linear, left top, left bottom, color-stop(0, black), color-stop(1, white));
    filter: "progid:DXImageTransform.Microsoft.gradient(startColorStr=#444, EndColorStr=#999)";
    background-image: linear-gradient(top, #444, #999), linear-gradient(top, black, white)
    }''')

    def test_moz(self):
        self.assertEqual(cssprefixer.process('''.box_gradient {
    background-image: -moz-linear-gradient(top, #444444, #999999);
    }''', minify=False), '''.box_gradient {
    background-image: -moz-linear-gradient(top, #444, #999);
    background-image: -o-linear-gradient(top, #444, #999);
    background-image: -webkit-linear-gradient(top, #444, #999);
    background-image: -webkit-gradient(linear, left top, left bottom, color-stop(0, #444), color-stop(1, #999));
    filter: "progid:DXImageTransform.Microsoft.gradient(startColorStr=#444, EndColorStr=#999)";
    background-image: linear-gradient(top, #444, #999)
    }''')

    def test_o(self):
        self.assertEqual(cssprefixer.process('''.box_gradient {
    background-image: -o-linear-gradient(top, #444444, #999999);
    }''', minify=False), '''.box_gradient {
    background-image: -moz-linear-gradient(top, #444, #999);
    background-image: -o-linear-gradient(top, #444, #999);
    background-image: -webkit-linear-gradient(top, #444, #999);
    background-image: -webkit-gradient(linear, left top, left bottom, color-stop(0, #444), color-stop(1, #999));
    filter: "progid:DXImageTransform.Microsoft.gradient(startColorStr=#444, EndColorStr=#999)";
    background-image: linear-gradient(top, #444, #999)
    }''')

    def test_webkit_gradient(self):
        self.assertEqual(cssprefixer.process('''.box_gradient {
    background-image: -webkit-gradient(linear, left top, left bottom, color-stop(0, #444), color-stop(1, #999));
    }''', minify=False), '''.box_gradient {
    background-image: -moz-linear-gradient(#444, #999);
    background-image: -o-linear-gradient(#444, #999);
    background-image: -webkit-linear-gradient(#444, #999);
    background-image: -webkit-gradient(linear, left top, left bottom, color-stop(0, #444), color-stop(1, #999));
    filter: "progid:DXImageTransform.Microsoft.gradient(startColorStr=#444, EndColorStr=#999)";
    background-image: linear-gradient(#444, #999)
    }''')

    def test_webkit_gradient_mixed(self):
        self.assertEqual(cssprefixer.process('''.box_gradient {
    background-image: -webkit-gradient(linear, left top, left bottom, color-stop(0, #444), color-stop(1, #999)), -webkit-linear-gradient(top, black, white);
    }''', minify=False), '''.box_gradient {
    background-image: -moz-linear-gradient(#444, #999), -moz-linear-gradient(top, black, white);
    background-image: -o-linear-gradient(#444, #999), -o-linear-gradient(top, black, white);
    background-image: -webkit-linear-gradient(#444, #999), -webkit-linear-gradient(top, black, white);
    background-image: -webkit-gradient(linear, left top, left bottom, color-stop(0, #444), color-stop(1, #999)), -webkit-gradient(linear, left top, left bottom, color-stop(0, black), color-stop(1, white));
    filter: "progid:DXImageTransform.Microsoft.gradient(startColorStr=#444, EndColorStr=#999)";
    background-image: linear-gradient(#444, #999), linear-gradient(top, black, white)
    }''')

    def test_image(self):
        #I don't think this test produces valid css but it shows that data and order is being preserved.
        self.assertEqual(cssprefixer.process('''.box_gradient {
    background-image: url(images/background.png), linear-gradient(top, black, white);
    }''', minify=False), '''.box_gradient {
    background-image: url(images/background.png), -moz-linear-gradient(top, black, white);
    background-image: url(images/background.png), -o-linear-gradient(top, black, white);
    background-image: url(images/background.png), -webkit-linear-gradient(top, black, white);
    background-image: url(images/background.png), -webkit-gradient(linear, left top, left bottom, color-stop(0, black), color-stop(1, white));
    filter: "progid:DXImageTransform.Microsoft.gradient(startColorStr=black, EndColorStr=white)";
    background-image: url(images/background.png), linear-gradient(top, black, white)
    }''')

    def test_background_multiple_images(self):
        self.assertEqual(cssprefixer.process('''.box_gradient {
    background: url(images/cross.png), url(images/gradient.png) top center no-repeat, url(images/background.png);
    }''', minify=False), '''.box_gradient {
    background: url(images/cross.png), url(images/gradient.png) top center no-repeat, url(images/background.png)
    }''')

    def test_background_multiple_images_and_gradient(self):
        self.assertEqual(cssprefixer.process('''.box_gradient {
    background: linear-gradient(top, black, white), url(images/gradient.png) top center no-repeat, url(images/background.png);
    }''', minify=False), '''.box_gradient {
    background: -moz-linear-gradient(top, black, white), url(images/gradient.png) top center no-repeat, url(images/background.png);
    background: -o-linear-gradient(top, black, white), url(images/gradient.png) top center no-repeat, url(images/background.png);
    background: -webkit-linear-gradient(top, black, white), url(images/gradient.png) top center no-repeat, url(images/background.png);
    background: -webkit-gradient(linear, left top, left bottom, color-stop(0, black), color-stop(1, white)), url(images/gradient.png) top center no-repeat, url(images/background.png);
    filter: "progid:DXImageTransform.Microsoft.gradient(startColorStr=black, EndColorStr=white)";
    background: linear-gradient(top, black, white), url(images/gradient.png) top center no-repeat, url(images/background.png)
    }''')

    def test_background_multiple_images_and_gradients(self):
        self.assertEqual(cssprefixer.process('''.box_gradient {
    background: linear-gradient(top, black, white), url(images/gradient.png) top center no-repeat, url(images/background.png), -moz-linear-gradient(top, #444444, #999999);
    }''', minify=False), '''.box_gradient {
    background: -moz-linear-gradient(top, black, white), url(images/gradient.png) top center no-repeat, url(images/background.png), -moz-linear-gradient(top, #444, #999);
    background: -o-linear-gradient(top, black, white), url(images/gradient.png) top center no-repeat, url(images/background.png), -o-linear-gradient(top, #444, #999);
    background: -webkit-linear-gradient(top, black, white), url(images/gradient.png) top center no-repeat, url(images/background.png), -webkit-linear-gradient(top, #444, #999);
    background: -webkit-gradient(linear, left top, left bottom, color-stop(0, black), color-stop(1, white)), url(images/gradient.png) top center no-repeat, url(images/background.png), -webkit-gradient(linear, left top, left bottom, color-stop(0, #444), color-stop(1, #999));
    filter: "progid:DXImageTransform.Microsoft.gradient(startColorStr=black, EndColorStr=white)";
    background: linear-gradient(top, black, white), url(images/gradient.png) top center no-repeat, url(images/background.png), linear-gradient(top, #444, #999)
    }''')

    #cssutils cannot parse this rule
    def _test_background_multiple_images_and_gradients(self):
        self.assertEqual(cssprefixer.process('''.box_gradient {
    background-image:
        url('../img/arrow.png'),
        -webkit-gradient(
        linear,
        left top,
        left bottom,
        from(rgb(240, 240, 240)),
        to(rgb(210, 210, 210))
    )}''', minify=False), '''.box_gradient {
    }''')

    def test_keyframes(self):
        self.assertEqual(cssprefixer.process('''@keyframes round {
    from {border-radius: 2px}
    to {border-radius: 10px}
    }''', minify=False), "@-webkit-keyframes round {\nfrom {\n    -webkit-border-radius: 2px;\n    border-radius: 2px\n    }\nto {\n    -webkit-border-radius: 10px;\n    border-radius: 10px\n    }\n}\n@-moz-keyframes round {\nfrom {\n    -moz-border-radius: 2px;\n    border-radius: 2px\n    }\nto {\n    -moz-border-radius: 10px;\n    border-radius: 10px\n    }\n}\n@keyframes round {\n    from {\n        border-radius: 2px\n        } to {\n        border-radius: 10px\n        }\n    }")

        self.assertEqual(cssprefixer.process('''@keyframes round {
    0% {border-radius: 2px}
    100% {border-radius: 10px}
    }''', minify=False), "@-webkit-keyframes round {\nfrom {\n    -webkit-border-radius: 2px;\n    border-radius: 2px\n    }\nto {\n    -webkit-border-radius: 10px;\n    border-radius: 10px\n    }\n}\n@-moz-keyframes round {\nfrom {\n    -moz-border-radius: 2px;\n    border-radius: 2px\n    }\nto {\n    -moz-border-radius: 10px;\n    border-radius: 10px\n    }\n}\n@keyframes round {\n    from {\n        border-radius: 2px\n        } to {\n        border-radius: 10px\n        }\n    }")

        self.assertEqual(cssprefixer.process('''@-webkit-keyframes round {
    0% {border-radius: 2px}
    100% {border-radius: 10px}
    }''', minify=False), "@-webkit-keyframes round {\nfrom {\n    -webkit-border-radius: 2px;\n    border-radius: 2px\n    }\nto {\n    -webkit-border-radius: 10px;\n    border-radius: 10px\n    }\n}\n@-moz-keyframes round {\nfrom {\n    -moz-border-radius: 2px;\n    border-radius: 2px\n    }\nto {\n    -moz-border-radius: 10px;\n    border-radius: 10px\n    }\n}\n@keyframes round {\n    from {\n        border-radius: 2px\n        } to {\n        border-radius: 10px\n        }\n    }")

    def test_animation(self):
        self.assertEqual(cssprefixer.process('a{animation: foo 1s}', minify=True),
                         'a{-moz-animation:foo 1s;-ms-animation:foo 1s;-o-animation:foo 1s;-webkit-animation:foo 1s;animation:foo 1s}')


if __name__ == '__main__':
    unittest.main()
