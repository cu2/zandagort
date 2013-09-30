Zandagort
=========

[Zandagort](http://zandagort.com/) is/was a free massively multiplayer online sci-fi strategy game. It has been actively developed and running for 4 years, after which it went open source in 2012.

This is/will be/might become one day a simplified version of the original game (or its sequel *Zandagort II: Haven and Camelot*) with the following advantages:

- easy to install
- can be played as single player, multiplayer, massively multiplayer
- easy to reconfigure (change parameters, add new resources, etc.)
- readable code, so even new features are not hard to add

This is 100% a hobby project, with no intent to monetize and/or support it. I just feel distant enough from the original project to utilize all the experience gathered during that earlier period and have something fun for the long cold winter evenings coming.

# Dependencies

- Python 2.7 (note: for Python 3 it needs some rewrite)

# Usage

All config is available in `config.py`.

Launch server:

`python server.py`

You can access it via command line client:

`python client.py <HOST> <PORT>` (default: `python client.py localhost 3492`)

Or any web browser on this url:

`<HOST>:<PORT>` (default: `http://localhost:3492/`)

Or the test interface on this url:

`<HOST>:<PORT>/test` (default: `http://localhost:3492/test`)
