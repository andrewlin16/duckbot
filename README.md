duckbot
=======

This is a (currently) babby Discord bot written in Python 3.

Usage
-----

To set up:

1.  `python3 -m venv env` in directory.
2.  `python3 -m pip install discord.py`
3.  Create a `app/config.py` file with the following contents:

    ```
    CLIENT_ID = '<your Discord app Client ID>'
    TOKEN = '<yout Discord app Token>'
    ```

    You can find or create your list of applications
    [here](https://discordapp.com/developers/applications/me).

To run:

1.  `source env/bin/activate`
2.  `python3 app/duckbot.py`

Or run the start script:

1.  `./start.sh`

    The bot will print out an OAuth URL that can be used to add the bot to your
    server.

License
-------

duckbot is licensed under the MIT license. See the LICENSE file.