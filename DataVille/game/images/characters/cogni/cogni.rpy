define cogni = Character("Cogni", who_suffix="AI Assistant", image="images/characters/cogni/cogni_happy.png")

screen cogni(what, mood, position="center", overlay=False):
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
        window: # bubble window
            style position_map[position]["style"]
            xpos position_map[position]["text"]["xpos"]
            ypos position_map[position]["text"]["ypos"]
            id "window"
            text what:
                style "cogni_what"
                id "what"
    # overlay signifies if cogni's dialogue pauses the game or not
    if not overlay: 
        button: # invisable full screen button to advance the dialogue
            xsize 1920
            ysize 1080
            pos (0, 0)
            action Return(True)

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
        },
        "text": {
            "xpos": 800,
            "ypos": 100
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
            "xsize": 150
        },
        "text": {
            "xpos": 225,
            "ypos": 0
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
    top_padding 10
    bottom_padding 44

style cogni_bubble_bottom_left is cogni_bubble:
    xsize 500
    ysize 300
    xpadding 30
    top_padding 10
    bottom_padding 44

style cogni_what:
    yoffset -50
    xalign 0.5
    yalign 0.5
    text_align 0.5
    color "#FFF"

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