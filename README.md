# CSSPrefixer #
A tool that rewrites your CSS files, adding vendor-prefixed versions of CSS3 rules. Keep your styles clean!
Requires cssutils.

## How to use ##
### From console ###
Like this
`cssprefixer.py my1.css my2.css --minify > result.css`

### From Python ###
    import cssprefixer
    cssprefixer.process(open('my.css').read(), debug=False, minify=True)

Django stuff (filters for django-assets and django-media-bundler) coming soon.
