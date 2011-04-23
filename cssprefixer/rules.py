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

import re
import cssutils

prefixRegex = re.compile('^(-o-|-ms-|-moz-|-webkit-)')

class BaseReplacementRule(object):
    vendor_prefixes = ['webkit', 'moz']

    def __init__(self, prop):
        self.prop = prop

    def get_prefixed_props(self):
        props = []
        for prefix in self.vendor_prefixes:
            props.append(cssutils.css.Property(
                name='-%s-%s' % (prefix, self.prop.name),
                value=self.prop.value,
                priority=self.prop.priority
                ))
        return props


class FullReplacementRule(BaseReplacementRule):
    """
    IE9 implements CSS3 without vendor prefixes,
    so this is base + Opera.
    """

    vendor_prefixes = BaseReplacementRule.vendor_prefixes + ['o']

class WebkitReplacementRule(BaseReplacementRule):
    vendor_prefixes = ['webkit']

class OperaAndIEReplacementRule(BaseReplacementRule):
    vendor_prefixes = ['o', 'ms']

class BorderRadiusReplacementRule(BaseReplacementRule):
    """
    Mozilla's Gecko engine uses different syntax for rounded corners.
    """
    vendor_prefixes = ['webkit']

    def get_prefixed_props(self):
        props = BaseReplacementRule.get_prefixed_props(self)
        name = '-moz-' + self.prop.name.replace('top-left-radius', 'radius-topleft') \
               .replace('top-right-radius', 'radius-topright') \
               .replace('bottom-right-radius', 'radius-bottomright') \
               .replace('bottom-left-radius', 'radius-bottomleft')
        props.append(cssutils.css.Property(
            name=name,
            value=self.prop.value,
            priority=self.prop.priority
            ))
        return props

class DisplayReplacementRule(BaseReplacementRule):
    """
    Flexible Box Model stuff.
    CSSUtils parser doesn't support duplicate properties, so that's dirty.
    """
    def get_prefixed_props(self):
        props = []
        if self.prop.value == 'box':#only add prefixes if the value is box
            for prefix in self.vendor_prefixes:
                props.append(cssutils.css.Property(
                    name='display', 
                    value='-%s-box' % prefix, 
                    priority=self.prop.priority
                    ))
        return props

class TransitionReplacementRule(BaseReplacementRule):
    vendor_prefixes = ['webkit', 'moz', 'o']
    
    def __get_prefixed_prop(self, prefix=None):
        #transition-property is the easy one...
        name = self.prop.name
        if prefix:
            name = '-%s-%s' % (prefix, self.prop.name)        
        if self.prop.name == 'transition-property':
            values = self.prop.value.split(',')
            newValues = []
            for value in values:
                value = prefixRegex.sub('', value.strip())
                if value in rules and prefix:
                    newValues.append('-%s-%s' % (prefix, value))
                else:
                    newValues.append(value)
            return cssutils.css.Property(
                    name=name,
                    value=', '.join(newValues),
                    priority=self.prop.priority
                    )
        return cssutils.css.Property(
            name=name,
            value=self.prop.value,
            priority=self.prop.priority
            )
    
    def get_prefixed_props(self):
        props = []
        for prefix in self.vendor_prefixes:
            props.append(self.__get_prefixed_prop(prefix))
        return props
        
    def get_base_prop(self):
        return self.__get_prefixed_prop()

rules = {
    'border-radius': BaseReplacementRule,
    'border-top-left-radius': BorderRadiusReplacementRule,
    'border-top-right-radius': BorderRadiusReplacementRule,
    'border-bottom-right-radius': BorderRadiusReplacementRule,
    'border-bottom-left-radius': BorderRadiusReplacementRule,
    'border-image': FullReplacementRule,
    'box-shadow': BaseReplacementRule,
    'box-sizing': BaseReplacementRule,
    'box-orient': BaseReplacementRule,
    'box-direction': BaseReplacementRule,
    'box-ordinal-group': BaseReplacementRule,
    'box-align': BaseReplacementRule,
    'box-flex': BaseReplacementRule,
    'box-flex-group': BaseReplacementRule,
    'box-pack': BaseReplacementRule,
    'box-lines': BaseReplacementRule,
    'user-select': BaseReplacementRule,
    'user-modify': BaseReplacementRule,
    'margin-start': BaseReplacementRule,
    'margin-end': BaseReplacementRule,
    'padding-start': BaseReplacementRule,
    'padding-end': BaseReplacementRule,
    'column-count': BaseReplacementRule,
    'column-gap': BaseReplacementRule,
    'column-rule': BaseReplacementRule,
    'column-rule-color': BaseReplacementRule,
    'column-rule-style': BaseReplacementRule,
    'column-rule-width': BaseReplacementRule,
    'column-width': BaseReplacementRule,

    'background-clip': WebkitReplacementRule,
    'background-origin': WebkitReplacementRule,
    'background-size': WebkitReplacementRule,

    'text-overflow': OperaAndIEReplacementRule,

    'transition': TransitionReplacementRule,
    'transition-delay': FullReplacementRule,
    'transition-duration': FullReplacementRule,
    'transition-property': TransitionReplacementRule,
    'transition-timing-function': FullReplacementRule,
    'transform': FullReplacementRule,
    'transform-origin': FullReplacementRule,

    'display': DisplayReplacementRule,
}
