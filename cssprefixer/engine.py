import cssutils

from rules import rules as tr_rules

def process(string):
    parser = cssutils.CSSParser()
    sheet = parser.parseString(string)
    for ruleset in sheet.cssRules:
        for rule in ruleset.style.children():
            try:
                processor = tr_rules[rule.name](rule)
                [ruleset.style.setProperty(prop) for prop in processor.get_prefixed_props()]
                sheet.cssText += processor.pure_css_hook()
            except KeyError:
                pass

    return sheet
