# Scanlines overlay needs to be added at the last element in screens that
# we want the led monitor effect
transform scroll_up:
    yoffset 0
    linear 0.4 yoffset -10
    repeat

image scanlines_overlay:
    "images/scanlines.png"
    size (1920, 1090)
    pos(0, 0)
    alpha 0.2
    scroll_up
# ----

transform fade_in(duration=0.5):
    alpha 0
    linear duration alpha 1.0

transform fade_out(duration=0.5):
    alpha 1.0
    linear duration alpha 0

transform dream_fade(duration=1):
    on show:
        fade_in(duration)
    on hide:
        fade_out(duration)

screen fade_to_black(duration=1.0):
    image Solid("#000000"):
        xsize 1920
        ysize 1080
        pos((0, 0))
        at dream_fade(duration)

image underline:
    Solid("#FFFFFF")
    ysize 4
    yoffset 60

image underline_blink:
    Solid("#FFFFFF")
    ysize 4
    yoffset 60
    blink

transform blink(duration=0.4, interval=0.05):
    block:
        alpha 1.0
        pause interval
        alpha 0.0
        pause interval
        repeat
    time duration
    alpha 0.0

transform wait_blur_and_fadeout(wait=1.0, duration=1.0):
    pause wait
    blur 0
    alpha 1.0
    linear duration blur 5 alpha 0.0

transform blur_and_fadeout(duration=1.0):
    blur 0
    alpha 1.0
    linear duration blur 5 alpha 0.0

transform dream_button(delay=1.0):
    alpha 0.0
    yoffset 20
    pause delay
    easein 0.8 alpha 1.0 yoffset 0
    on hide:
        fade_out(0.5)
        
transform alpha_dissolve:
    alpha 0.0
    linear 0.5 alpha 1.0
    on hide:
        linear 0.5 alpha 0

transform alpha_dissolve_quick:
    alpha 0.0
    linear 0.2 alpha 1.0
    on hide:
        linear 0.2 alpha 0

transform speech_bubble:
    xalign 0.3
    yalign 0.75

transform blur:
    blur 30
    
transform unblur:
    blur 0

transform tv_zoom_in_seq:
    zoom 0.75
    xoffset -330
    yoffset -250
    pause 0.5
    parallel:
        easeout_quad 3 xoffset -1400
    parallel:
        easeout_quad 3 zoom 1.19
    parallel:
        easeout_quad 3 yoffset -600

transform on_hide_fade_out:
    on hide:
        fade_out(0.5)