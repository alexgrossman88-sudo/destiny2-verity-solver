A tool for solving the 4th encounter of raid "Salvation's Edge" in Destiny 2.

# Features

- Can solve both solo rooms and dissection.
- Can make a solution which meets encounter triumph "Equal Distribution"
  and challenge "Varied Geometry" requirements.
    - The resulting solution can meet triumph and challenge requirements
      simultaneously or separately depending on configuration.

# Installation

1. Clone this project.
2. Install [Python 3.12.4](https://www.python.org/downloads/release/python-3124/)
   or higher version of Python 3.12.
3. Copy `config-template.toml` as `config.toml`.
4. I suggest to delete all comments in `config.toml` once you have read them.

# Usage

1. Open PowerShell in the root of the project you cloned.
2. There is a way to make the same 2 people always enter solo rooms.
   Follow [this guide](https://www.reddit.com/r/raidsecrets/comments/1duz6qp/manipulating_who_goes_top_and_bottom_in_the/)
   on how to accomplish that.
3. Decide who are these 2 people and write their nicknames as aliases
   for `player1` and `player2` in the config file `config.toml`.
4. The 3rd solo player is always random, so use "The third" as the alias for `player3`.
5. If you are doing the triumph, set `is_doing_triumph` to `true`.
6. If you are doing the challenge,
   on the 1st phase set `key_set` to `mixed`,
   on the 2nd phase - to `double`
   and on the 3rd phase - back to `mixed`.
7. Position your team according to the guide from step 2.
8. You are ready to start the encounter.

Then, for every phase:

1. Player 1 must tell 2D shapes held by statues in solo rooms from left to right.
   Fill `shades` respectively.
2. Player 1 must tell their shape (i.e. the shape their statue holds)
   and other shape on the wall. Complete `player1`.
3. Player 2 and player 3 must do the same. Complete `player2` and `player3` respectively.
4. Meanwhile, someone in the main room must tell shapes held by the statues from left to right.
   Fill `3d_shapes`.
5. Decide who is dissecting in the main room and fill `dissector_alias` with their nickname.
6. Fill `helper1_alias` and `helper2_alias`
   with the nicknames of other player in the main room.
7. In opened PowerShell window type `python -m solve both` and press Enter.
8. Follow the steps printed in the console window.
9. Once all steps are completed:
    1. Kill champions, resque each other.
    2. Position you team according to the guide mentioned previously.
    3. If you are doing the triumph,
       in config set `last_position` to the last position mentioned in the steps.
    4. If you are doing the challenge, switch key set.
    5. Return to the step 1.

Run `python -m solve --help` to see more options.

- For example, instead of `both` you can use `solo-rooms` to get steps only for solo rooms.
- Option `-i` pauses output after every step. Press Enter to proceed to the next step.

# Development

## Running tests

1. Open terminal in the root of this project.
2. Run `python -m unittest discover tests "test_*.py" .` to run all tests.
