duckbot
=======

This is a (currently) babby Discord bot written in Python 3.5

Usage
-----

To set up:

1.  `python3 -m venv env` in directory.
2.  `source env/bin/activate` to use virtual env
3.  `pip install -r requirements.py`
4.  Create a `app/config.py` file with the same format as `config.example.py`

    You can find or create your list of applications
    [here](https://discordapp.com/developers/applications/me).

To run:

1.  Use the start script `./start.sh -b [name]`
     
    Make sure the `name` is the name of a bot in `config.py`

    The bot will print out an OAuth URL that can be used to add the bot to your
    server.

License
-------

duckbot is licensed under the MIT license. See the LICENSE file.
