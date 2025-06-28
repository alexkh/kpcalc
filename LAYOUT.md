# Project files layout

kpcalc/
|-------app.py           # main file
|-------fragments.py     # file containing sizes of window elements
|-------README.md        # general description of the project
|-------Requirements.txt # python requirements file
|-------LAYOUT.md        # this file
|-------doc/             # documentation directory
|-------img/             # directory containing images used by the software

The bulk of the code is in app.py, in the Canvas class, which is a subclass of
QWidget. It takes care of the calculator window.

There are two major modes of operation: scientific and hexadecimal. The state
of the mode is in mode class property. If it's 0 the mode is scientific, if it's
1 - the mod is hexadecimal.

Each of these modes has different background image displayed, while the mode is
active.

The window is split into the display on top and the keyboard, taking most of the
window. The display has the expression on top, which is stored in the class
property eval_str and the larger font-size number part right below it, which
value is stored in num_str property. Any time the screen is refreshed, those
two properties will be displayed.

Once a modifier key is activated, the mod property becomes non-zero. Depending
on the modifier key, the part of each key on the screen will be highlighted.
That functionality is mostly implemented in fragments.py, where all the numbers
are stored. There are two types of images for each mode: bright and dim, so
by overpainting bright on dim background, we can highlight certain areas of the
keyboard. Thus we need 4 images total (2 modes, dark and bright for each).
The difficult part was to figure out exact places where the highlights are to
be placed, which took a while to tweak. Those numbers were determined
experimentally.

Not all the functions that are displayed on the image are currently supported,
some need to be relocated. The layout is not final. It might take some testing
to figure out how to place all the trigonometric functions that might be useful.

