# Copyright 2004-2010 PyTom <pytom@bishoujo.us>
# See LICENSE.txt for license details.

# This file contains a number of definitions of standard
# locations and transitions. We've moved them into the common
# directory so that it's easy for an updated version of all of these
# definitions.

init -1110:

    transform reset:
        alpha 1 rotate None zoom 1 xzoom 1 yzoom 1 align (0, 0) alignaround (0, 0) subpixel False size None crop None 
   
    # These are positions that can be used inside at clauses. We set
    # them up here so that they can be used throughout the program.
    transform left:
        xpos 0.0 xanchor 0.0 ypos 1.0 yanchor 1.0

    transform right:
        xpos 1.0 xanchor 1.0 ypos 1.0 yanchor 1.0

    transform center:
        xpos 0.5 xanchor 0.5 ypos 1.0 yanchor 1.0

    transform truecenter:
        xpos 0.5 xanchor 0.5 ypos 0.5 yanchor 0.5
        
    # Offscreen positions for use with the move transition. Images at
    # these positions are still shown (and consume
    # resources)... remember to hide the image after the transition.    
    transform offscreenleft:
        xpos 0.0 xanchor 1.0 ypos 1.0 yanchor 1.0

    transform offscreenright:
        xpos 1.0 xanchor 0.0 ypos 1.0 yanchor 1.0

    transform default:
        reset
        center

    python:
        config.default_transform = None
        

init -1110 python:

    _define = define = object()
        
    # Positions ##############################################################


    # Transitions ############################################################

    # Simple transitions.
    fade = Fade(.5, 0, .5) # Fade to black and back.
    dissolve = Dissolve(0.5)
    pixellate = Pixellate(1.0, 5)

    # Various uses of CropMove.    
    wiperight = CropMove(1.0, "wiperight")
    wipeleft = CropMove(1.0, "wipeleft")
    wipeup = CropMove(1.0, "wipeup")
    wipedown = CropMove(1.0, "wipedown")

    slideright = CropMove(1.0, "slideright")
    slideleft = CropMove(1.0, "slideleft")
    slideup = CropMove(1.0, "slideup")
    slidedown = CropMove(1.0, "slidedown")

    slideawayright = CropMove(1.0, "slideawayright")
    slideawayleft = CropMove(1.0, "slideawayleft")
    slideawayup = CropMove(1.0, "slideawayup")
    slideawaydown = CropMove(1.0, "slideawaydown")

    irisout = CropMove(1.0, "irisout")
    irisin = CropMove(1.0, "irisin")

    # Ease images around. These are basically cosine-warped moves.
    def _ease_out_time_warp(x):
        import math
        return 1.0 - math.cos(x * math.pi / 2.0)

    def _ease_in_time_warp(x):
        import math
        return math.cos((1.0 - x) * math.pi / 2.0)

    def _ease_time_warp(x):
        import math
        return .5 - math.cos(math.pi * x) / 2.0

    # This defines a family of move transitions.
    def move_transitions(prefix, delay, time_warp=None, in_time_warp=None, out_time_warp=None, old=False, layers=[ 'master' ], **kwargs):
        moves = {
            "" : MoveTransition(
                delay,
                old=old,
                layers=layers,
                factory=MoveFactory(time_warp=time_warp, **kwargs)),

            "inright" : MoveTransition(
                delay,
                old=old,
                layers=layers,
                factory=MoveFactory(time_warp=time_warp, **kwargs), 
                enter_factory=MoveIn((1.0, None, 0.0, None), time_warp=in_time_warp, **kwargs)),

            "inleft" : MoveTransition(
                delay,
                old=old,
                layers=layers,
                factory=MoveFactory(time_warp=time_warp, **kwargs), 
                enter_factory=MoveIn((0.0, None, 1.0, None), time_warp=in_time_warp, **kwargs)),

            "intop" : MoveTransition(
                delay,
                old=old,
                layers=layers,
                factory=MoveFactory(time_warp=time_warp, **kwargs), 
                enter_factory=MoveIn((None, 0.0, None, 1.0), time_warp=in_time_warp, **kwargs)),

            "inbottom" : MoveTransition(
                delay,
                old=old,
                layers=layers,
                factory=MoveFactory(time_warp=time_warp, **kwargs),
                enter_factory=MoveIn((None, 1.0, None, 0.0), time_warp=in_time_warp, **kwargs)),

            "outright" : MoveTransition(
                delay,
                old=old,
                layers=layers,
                factory=MoveFactory(time_warp=time_warp, **kwargs), 
                leave_factory=MoveOut((1.0, None, 0.0, None), time_warp=out_time_warp, **kwargs)),

            "outleft" : MoveTransition(
                delay,
                old=old,
                layers=layers,
                factory=MoveFactory(time_warp=time_warp, **kwargs), 
                leave_factory=MoveOut((0.0, None, 1.0, None), time_warp=out_time_warp, **kwargs)),

            "outtop" : MoveTransition(
                delay,
                old=old,
                layers=layers,
                factory=MoveFactory(time_warp=time_warp, **kwargs), 
                leave_factory=MoveOut((None, 0.0, None, 1.0), time_warp=out_time_warp, **kwargs)),

            "outbottom" : MoveTransition(
                delay,
                old=old,
                layers=layers,
                factory=MoveFactory(time_warp=time_warp, **kwargs), 
                leave_factory=MoveOut((None, 1.0, None, 0.0), time_warp=time_warp, **kwargs)),
            }

        for k, v in moves.iteritems():
            setattr(store, prefix + k, v)

    define.move_transitions = move_transitions
    del move_transitions

    define.move_transitions("move", 0.5)
    define.move_transitions("ease", 0.5, _ease_time_warp, _ease_in_time_warp, _ease_out_time_warp) 

    # Zoom-based transitions.
    zoomin = MoveTransition(0.5, enter_factory=ZoomInOut(0.01, 1.0))
    zoomout = MoveTransition(0.5, leave_factory=ZoomInOut(1.0, 0.01))
    zoominout = MoveTransition(0.5, enter_factory=ZoomInOut(0.01, 1.0), leave_factory=ZoomInOut(1.0, 0.01))
    
    # These shake the screen up and down for a quarter second.
    # The delay needs to be an integer multiple of the period.
    vpunch = Move((0, 10), (0, -10), .10, bounce=True, repeat=True, delay=.275)
    hpunch = Move((15, 0), (-15, 0), .10, bounce=True, repeat=True, delay=.275)

    # These use the ImageDissolve to do some nifty effects.
    blinds = ImageDissolve(im.Tile("blindstile.png"), 1.0, 8)
    squares = ImageDissolve(im.Tile("squarestile.png"), 1.0, 256)


init -1110:
    image black = Solid("#000")

init 1110 python:
    if not hasattr(store, 'narrator'):
        narrator = Character(None, kind=adv, what_style='say_thought')

    if not hasattr(store, 'name_only'):
        name_only = adv

    if not hasattr(store, 'centered'):
        centered = Character(None, what_style="centered_text", window_style="centered_window")

    # This is necessary to ensure that config.default_transform works.
    if config.default_transform:
        config.default_transform.show()
