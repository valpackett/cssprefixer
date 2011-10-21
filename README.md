# CSSPrefixer #
A tool that rewrites your CSS files, adding vendor-prefixed versions of (popular) CSS3 rules. It also can combine and minify your stylesheets. **Keep your styles clean!**

It supports many CSS3 stuff including keyframe animations, Flexbox and gradients.

For example, this
    #wrapper {
        border-radius: 1em;
        transform: rotate(45deg)
    }

becomes this:
    #wrapper {
        -moz-border-radius: 1em;
        -webkit-border-radius: 1em;
        border-radius: 1em;
        -o-transform: rotate(45deg);
        -moz-transform: rotate(45deg);
        -webkit-transform: rotate(45deg);
        transform: rotate(45deg)
    }

Requires [cssutils](http://cthedot.de/cssutils/).

## Contributors ##
- [InScopeApps](https://github.com/InScopeApps)
- you?

## How to install ##
    $ easy_install cssutils #or 'pip install cssutils' if you have pip
    $ sudo python setup.py install

## How to use ##
### From console ###
Like this:
`cssprefixer my1.css my2.css --minify > result.css`

### From Python ###
    import cssprefixer
    cssprefixer.process(open('my.css').read(), debug=False, minify=True)

### With Django or Flask ###
or any other Python web framework — latest git version of [webassets](http://github.com/miracle2k/webassets) has a filter for cssprefixer.
