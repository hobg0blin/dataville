style dream_text:
    size 52
    color "#FFFFFF"
    xmaximum 0.8
    xalign 0.5

style dream_button_text:
    color "#FFFFFF"
    hover_color "#FFFFFF"

style epilogue_text:
    yalign 0.5
    color "#FFFFFF"
    background "#000000"
    outlines [(8, "#000000FF", 0, 0)]
    size 46
    italic True
    xmaximum 0.8
    text_align 0.5
    slow_cps 40
    align (0.5, 0.5)

style epilogue_text_shadow:
    yalign 0.5
    color "#00000000"
    outlines [(8, "#00000000", 0, 0)]
    italic True
    size 46
    xmaximum 0.8
    text_align 0.5
    slow_cps 40
    yoffset -20
    align (0.5, 0.5)

style epilogue_button_text:
    color "#FFFFFF"
    hover_color "#FFFFFF"
    outlines [(7, "#000000", 0, 1)]
    size 50

style sticky_note:
    font "fonts/BrownBagLunch.ttf"
    color "#000000"
    size 105
    xsize 680
    ysize 645
    xalign 0.5
    yalign 0.5
    yoffset -45

style task_reward_text:
    xalign .50
    ypos 16
    color "#FFFFFF"

style task_reward_text:
    variant "small" 
    xalign .50
    ypos 16
    color "#FFFFFF"
    xoffset -175

style default_button:
    padding gui.frame_borders.padding
    xpadding 40
    background Frame("gui/button/custom/background.png")
    activate_sound "click.ogg"
    xminimum 300
    yminimum 50