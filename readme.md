# Vision2 - the emojifier #
by Mateusz Cyraniak

This small web app uses google's vision API to analyse uploaded pictures, and if it finds any faces, it adds an emoji
(corresponding with person's detected emotion) in their place.

Application uses free emoji by [EmojiOne](https://www.emojione.com).

##Installation
__Virtualenv is recommended.__

1. Install project and all requirements with `python setup.py install` (or `.venv/bin/python setup.py install` if virtualenv is used)
1. Generate an empty database with `alembic upgrade head` (if venv is used, see point 1)
1. Copy service key project's directory, as *key.json*
1. If environment variable is prefered, comment out *vision2.service_key_path* line from config ini file. 
1. Run server with `pserve production.ini`
1. Open server in browser, and upload an image.