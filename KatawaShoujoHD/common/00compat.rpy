# Copyright 2004-2010 PyTom <pytom@bishoujo.us>
# See LICENSE.txt for license details.

init -1210 python:

    # This is called when script_version is set, to immediately
    # run code in response to a script_version change.        
    def _set_script_version(version):

        if version is None:
            return

        if version <= (5, 6, 0):
            config.check_properties = False

        if version <= (6, 5, 0):
            layout.compat()

        if version <= (6, 9, 1):
            store.library = store.config

        if version <= (6, 9, 3):

            # Before 6.10, these were positions, rather than transforms.
            store.left = Position(xalign=0.0)
            store.center = Position(xalign=0.5)
            store.truecenter = Position(xalign=0.5, yalign=0.5)
            store.right = Position(xalign=1.0)
            store.offscreenleft = Position(xpos=0.0, xanchor=1.0)
            store.offscreenright = Position(xpos=1.0, xanchor=0.0)

            
            
init 1210 python hide::

    # This returns true if the script_version is <= the
    # script_version supplied. Give it the last script version
    # where an old version was used.
    def compat(x, y, z):
        return config.script_version and config.script_version <= (x, y, z)

    # Compat for changes to with-callback.
    if compat(5, 4, 5):
        if config.with_callback:
            def compat_with_function(trans, paired, old=config.with_callback):
                old(trans)
                return trans

            config.with_callback = compat_with_function

    if not config.sound:
        config.has_sound = False
        config.has_music = False
        config.has_voice = False
        
    # Compat for SFont recoloring.
    if compat(5, 1, 1):
        config.recolor_sfonts = False

    if compat(5, 5, 4):
        config.implicit_with_none = False

    # Compat for changes to button look.
    if compat(5, 5, 4):            
        style.button.setdefault(xpos=0.5, xanchor=0.5)
        style.menu_button.clear()
        style.menu_button_text.clear()

    if compat(5, 6, 6):
        config.reject_midi = False

    if compat(6, 2, 0):
        config.reject_backslash = False

    if compat(6, 9, 0):
        style.motion.clear()
        
    if "Fullscreen" in config.translations:
        fs = _("Fullscreen")
        config.translations.setdefault("Fullscreen 4:3", fs + " 4:3")
        config.translations.setdefault("Fullscreen 16:9", fs + " 16:9")
        config.translations.setdefault("Fullscreen 16:10", fs + " 16:10")
            
    for i in layout.compat_funcs:
        i()
