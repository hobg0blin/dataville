# Scanlines overlay needs to be added at the last element in screens that
# we want the led monitor effect
transform scroll_up:
    yoffset 0
    linear 0.7 yoffset -47
    repeat

transform scroll_up2:
    yoffset 0
    linear 0.7 yoffset -97
    repeat

image scanlines_overlay:
    "images/scanlines.png"
    size (1920, 10000)
    pos(0, 0)
    alpha 0.05
    scroll_up

image scanlines_overlay_tighter:
    "images/scanlines.png"
    size (1920, 20000)
    pos(0, 0)
    alpha 0.10
    scroll_up2
# ----

transform tv_aberate:
    still_aberate(5.0)
    pause 4.8
    fast_aberate(20.0, 20.0)
    pause 0.15
    still_aberate(5.0)
    pause 2.8
    fast_aberate(13.0, 10.0)
    pause 0.3
    still_aberate(5.0)
    pause 2.8
    fast_aberate(8.0, 15.0)
    pause 0.1
    still_aberate(5.0)
    pause 0.6
    fast_aberate(13.0, 10.0)
    pause 0.3
    still_aberate(5.0)
    pause 0.2
    fast_aberate(12.0, 20.0)
    pause 0.2
    repeat

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

transform fade_and_blink(duration=0.5, interval=0.05):
    parallel:
        linear duration alpha 0.0
    parallel:
        alpha 1.0
        pause interval
        alpha 0.0
        pause interval
        alpha 1.0
        pause interval
        alpha 0.0
        pause interval

transform wait_blur_and_fadeout(wait=0.7, duration=0.7, blur_amount=5):
    pause wait
    blur 0
    alpha 1.0
    linear duration blur blur_amount alpha 0.0

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

transform blur(amount = 30):
    blur amount
    
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

transform zoom_computer(duration = 1.0):
    easein duration zoom 2.4 xoffset -1500 yoffset -960

transform zoom_sticky_notes(x_trans, y_trans, duration = 1.0):
    easein duration zoom 2.4 xoffset x_trans yoffset y_trans

transform zoom_computer_tv(duration = 1.0):
    easein duration zoom 2.4 xoffset -1510 yoffset -200
