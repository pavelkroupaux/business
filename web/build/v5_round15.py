# Round 15 (5. 10. 2026): favicon (žlutý čtverec s černou fajfkou), vložený přímo do stránky.
import urllib.parse as _up
FAV_DIR = R + 'Career/07 Assets/favicon/'
_svg = open(FAV_DIR + 'favicon.svg').read()
_apple = base64.b64encode(open(FAV_DIR + 'apple-touch-icon.png', 'rb').read()).decode()
FAV_TAGS = ('<link rel="icon" type="image/svg+xml" href="data:image/svg+xml,' + _up.quote(_svg.replace('"', "'"), safe=" =:/'") + '">\n'
            '<link rel="apple-touch-icon" href="data:image/png;base64,' + _apple + '">\n'
            '<meta name="theme-color" content="#FFCE1B">\n')
def post_patch15(out):
    return rep(out, '<meta charset="utf-8">\n', '<meta charset="utf-8">\n' + FAV_TAGS)
