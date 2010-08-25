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

import cssutils

class BaseReplacementRule(object):
    vendor_prefixes = ['webkit', 'moz']

    def __init__(self, prop):
        self.prop = prop

    def get_prefixed_props(self):
        props = []
        for prefix in self.vendor_prefixes:
            props += [cssutils.css.Property(
                name='-%s-%s' % (prefix, self.prop.name),
                value=self.prop.value,
                priority=self.prop.priority
                )]
        return props

    def pure_css_hook(self):
        """
        Must return a string to add to the *stylesheet*.
        """
        return ''

class FullReplacementRule(BaseReplacementRule):
    """
    IE9 implements CSS3 without vendor prefixes,
    so this is base + Opera.
    """

    vendor_prefixes = BaseReplacementRule.vendor_prefixes + ['o']

rules = {
    'border-radius': BaseReplacementRule,
    'box-shadow': BaseReplacementRule,
    'transition': FullReplacementRule,
    'transform': FullReplacementRule,
}
