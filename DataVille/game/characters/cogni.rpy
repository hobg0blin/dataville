define cogni = Character("Cogni", who_suffix="AI Assistant", image="images/characters/cogni/cogni_happy.png")

screen cogni(what, mood, position="center", overlay=False):
    layer "master"
    window:
        xalign position_map[position]["window"]["xalign"]
        yalign position_map[position]["window"]["yalign"]
    # two windows, one for the cogni sprite, the other for the bubble
        window: # sprite window
            image mood:
                fit "contain"
                xsize position_map[position]["sprite"]["xsize"]
                xpos position_map[position]["sprite"]["xpos"]
                ypos position_map[position]["sprite"]["ypos"]
                at still_aberate(position_map[position]["sprite"]["aberate"])
        if what:
            window: # bubble window
                style position_map[position]["style"]
                xpos position_map[position]["text"]["xpos"]
                ypos position_map[position]["text"]["ypos"]
                id "window"
                text what:
                    style "cogni_what"
                    id "what"
                    at still_aberate(position_map[position]["text"]["aberate"])
    # overlay signifies if cogni's dialogue pauses the game or not
    if not overlay: 
        button: # invisable full screen button to advance the dialogue
            xsize 1920
            ysize 1080
            pos (0, 0)
            action Return(True)
    
    image "scanlines_overlay" 

screen cogni_enter(mood, position="center", overlay=False, hide_bubble = False, hide_move = False):
    python:
        move1_time, move2_time, move3_time = (0.25, 0.1, 0.05)
        pop1_time, pop2_time, pop3_time = (0.09, 0.09, 0.09)
    default show_bubble = hide_move
    window:
        xalign position_map[position]["window"]["xalign"]
        yalign position_map[position]["window"]["yalign"]
    # two windows, one for the cogni sprite, the other for the bubble
        window: # sprite window
            image mood:
                fit "contain"
                xsize position_map[position]["sprite"]["xsize"]
                xpos position_map[position]["sprite"]["xpos"]
                ypos position_map[position]["sprite"]["ypos"]
                if not hide_move:
                    at l_to_pos_bounce(move1_time,move2_time, move3_time)
        if show_bubble:
            if not hide_bubble: # can't combine these two in renpy?
                window: # bubble window
                    style position_map[position]["style"]
                    xpos position_map[position]["text"]["xpos"]
                    ypos position_map[position]["text"]["ypos"]
                    at expand_bubble(pop1_time, pop2_time, pop3_time)
    # overlay signifies if cogni's dialogue pauses the game or not
    if not overlay: 
        button: # invisable full screen button to advance the dialogue
            xsize 1920
            ysize 1080
            pos (0, 0)
            action Return(True)

    image "scanlines_overlay"

    if not hide_move:
        timer move1_time + move2_time + move3_time action [ToggleScreenVariable("show_bubble")]
    if show_bubble:
        timer pop1_time + pop2_time + pop3_time action [Return(True)]

screen cogni_timeup(what, mood, position="center", overlay=False):
    layer "master"
    python:
        pop1_time, pop2_time, pop3_time = (0.09, 0.09, 0.09)
    default show_bubble = not timer_failed
    default show_text = False
    default hide_bubble = False

    window:
        xalign position_map[position]["window"]["xalign"]
        yalign position_map[position]["window"]["yalign"]
    # two windows, one for the cogni sprite, the other for the bubble
        window: # sprite window
            image mood:
                fit "contain"
                xsize position_map[position]["sprite"]["xsize"]
                xpos position_map[position]["sprite"]["xpos"]
                ypos position_map[position]["sprite"]["ypos"]
                at still_aberate(position_map[position]["sprite"]["aberate"])
        if timer_failed:
            window: # bubble window
                style position_map[position]["style"]
                xpos position_map[position]["text"]["xpos"]
                ypos position_map[position]["text"]["ypos"]
                id "window"
                if hide_bubble:
                    at min_bubble(pop1_time, pop2_time)
                elif show_text:
                    text what:
                        style "cogni_what"
                        id "what"
                        at still_aberate(position_map[position]["text"]["aberate"])
                else:
                    at expand_bubble(pop1_time, pop2_time, pop3_time)
    # overlay signifies if cogni's dialogue pauses the game or not
    if not overlay: 
        button: # invisable full screen button to advance the dialogue
            xsize 1920
            ysize 1080
            pos (0, 0)
            action Return(True)
    
    image "scanlines_overlay" 

    if hide_bubble:
        timer pop1_time + pop2_time
    elif show_text:
        timer 4 action [ToggleLocalVariable("hide_bubble")]
    elif timer_failed:
        timer pop1_time + pop2_time + pop3_time action [ToggleLocalVariable("show_text")]

screen cogni_leave(mood, position="center", overlay=False, hide_bubble = False, hide_move = False):
    python:
        move1_time, move2_time = (0.1, 0.25)
        pop1_time, pop2_time = (0.09, 0.09)
    default move_cogni = hide_bubble

    window:
        xalign position_map[position]["window"]["xalign"]
        yalign position_map[position]["window"]["yalign"]
    # two windows, one for the cogni sprite, the other for the bubble
        window: # sprite window
            image mood:
                fit "contain"
                xsize position_map[position]["sprite"]["xsize"]
                xpos position_map[position]["sprite"]["xpos"]
                ypos position_map[position]["sprite"]["ypos"]
                if move_cogni:
                    if not hide_move:
                        at pos_to_l_bounce(move1_time, move2_time)
        if not hide_bubble:
            window: # bubble window
                    style position_map[position]["style"]
                    xpos position_map[position]["text"]["xpos"]
                    ypos position_map[position]["text"]["ypos"]
                    at min_bubble(pop1_time, pop2_time)
    # overlay signifies if cogni's dialogue pauses the game or not
    if not overlay: 
        button: # invisable full screen button to advance the dialogue
            xsize 1920
            ysize 1080
            pos (0, 0)
            action Return(True)

    image "scanlines_overlay" 

    if move_cogni:
        timer move1_time + move2_time action [Return(True)]
    elif not hide_bubble:
        timer pop1_time + pop2_time action If(hide_move, true=[Return(True)], false=[ToggleScreenVariable("move_cogni")])

transform l_to_pos_bounce(move1_time=0.5, move2_time=0.1, move3_time=0.05):
    xoffset -1500
    parallel:
        easein move1_time xoffset 100
        easein move2_time xoffset -50
        easein move3_time xoffset 0
    parallel:
        still_aberate(5.0)

transform expand_bubble(pop1_time=0.09, pop2_time=0.09, pop3_time=0.09):
    zoom 0.0
    parallel:
        linear pop1_time zoom 1.2
        linear pop2_time zoom 0.9
        linear pop3_time zoom 1.0
    parallel:
        still_aberate(2.0)

transform pos_to_l_bounce(move1_time=0.1, move2_time=0.2):
    xoffset 0
    parallel:
        easein move1_time xoffset 100
        easein move2_time xoffset -1500
    parallel:
        still_aberate(5.0)

transform min_bubble(pop1_time=0.09, pop2_time=0.09):
    zoom 1.0
    parallel:
        linear pop1_time zoom 1.2
        linear pop2_time zoom 0.0
    parallel:
        still_aberate(2.0)


define position_map = {
    "center": {
        "style": "cogni_bubble_center",
        "window": {
            "xalign": 0.5,
            "yalign": 0.5,
        },
        "sprite": {
            "xpos": 600,
            "ypos": 100,
            "xsize": 250,
            "aberate": 5.0
        },
        "text": {
            "xpos": 800,
            "ypos": 100,
            "aberate": 3.0
        }
    },
    "bottom_left": {
        "style": "cogni_bubble_bottom_left",
        "window": {
            "xalign": 0.0,
            "yalign": 1.0,
        },
        "sprite": {
            "xpos": 100,
            "ypos": 0,
            "xsize": 150,
            "aberate": 5.0
        },
        "text": {
            "xpos": 100,
            "ypos": 0,
            "aberate": 3.0
        }
    },
}

style cogni_bubble:
    # xminimum 300
    anchor (0.0, 1.0)
    background Frame("images/characters/cogni/cogni_bubble.png")

style cogni_bubble_center is cogni_bubble:
    xsize 500
    ysize 300
    xpadding 30
    bottom_padding 50

style cogni_bubble_bottom_left is cogni_bubble:
    xsize 500
    ysize 300
    xpadding 30
    bottom_padding 50

style cogni_what:
    anchor (0.0,0.0)
    xalign 0.5
    yalign 0.5
    text_align 0.5
    color "#FFF"
    slow_cps 60

# style cogni_window is empty
# style cogni_namebox is empty
# style cogni_who is default
# style cogni_what is default

# style cogni_window:
#     xpadding 30
#     top_padding 5
#     bottom_padding 5

# style cogni_namebox:
#     xalign 0.5

# style cogni_who:
#     xalign 0.5
#     textalign 0.5
#     color "#000"

# style cogni_what:
#     align (0.5, 0.5)
#     text_align 0.5
#     layout "subtitle"
#     color "#000"

# define cogni.expand_area = {
#     "bottom_left" : (0, 0, 0, 22),
#     "bottom_right" : (0, 0, 0, 22),
#     "top_left" : (0, 22, 0, 0),
#     "top_right" : (0, 22, 0, 0),
# }