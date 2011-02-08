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

from rules import rules as tr_rules

def magic(ruleset, debug):
    added = ''
    if hasattr(ruleset, 'style'): # Comments don't
        for rule in ruleset.style.children():
            try:
                processor = tr_rules[rule.name](rule)
                [ruleset.style.setProperty(prop) for prop in processor.get_prefixed_props()]
                added += processor.add_to_sheet
                if hasattr(processor, 'replace_hook'):
                    ruleset.cssText = processor.replace_hook(ruleset.cssText)
            except:
                if debug:
                    print 'warning with ' + str(rule)
    elif hasattr(ruleset, 'cssRules'):
        for subruleset in ruleset:
            magic(subruleset, debug)
    return unicode(ruleset.cssText) + added

def process(string, debug=False, minify=False):
    if debug:
        loglevel = 'info'
    else:
        loglevel = 'error'
    parser = cssutils.CSSParser(loglevel=loglevel)
    if minify:
        cssutils.ser.prefs.useMinified()
    else:
        cssutils.ser.prefs.useDefaults()
    sheet = parser.parseString(string)
    result = ''
    for ruleset in sheet.cssRules:
        result += magic(ruleset, debug)

    # Not using sheet.cssText - it's buggy:
    # it skips some prefixed properties.
    return result

__all__ = ('process')





