# v0.3 (first verison)

- features:
  - can read quizes from specially formatted files.

## commit `dda9f18` (6/20/2022)

- added:
  - tried to add "return to title" button, it didn't worked;
  - also separated default ~~meme~~ questions from the code into `questions/default.txt` so they can still be loaded, if necessary.

## commit `7397c4f` (6/27/2022)

- due separating the default questions from the program, now it's impossible to start a quiz without a file (todo line removed).

- added:
  - quiz ending line is now using fstrings to reduce clutter in the code.

# v0.4

- changes:
  - slightly improved source code because of fstrings.

- added:
  - now the app is using `.yaml` configuration file. It's not doing much right now but it will have more uses later on.