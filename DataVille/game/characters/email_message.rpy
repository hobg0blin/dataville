# ***********************************************
# * Renpy Character Template for Email Messages *
# ***********************************************
# Used for Alex T's character

define email_message = Character(
    screen = "email_message", 
    window_style = "email_message_window", 
    window_nobox_style = "email_message_window_nobox", 
    namebox_style = "email_message_namebox", 
    # namebox_label_style = "email_message_namebox_label", 
    label_style = "email_message_label", 
    dialogue_style = "email_message_dialogue", 
    thought_style = "email_message_dialogue")

style email_message_window is window_nobox
style email_message_label is say_label
style email_message_dialogue is say_dialogue
style email_message_thought is email_message_dialogue

style email_message_namebox is namebox
style email_message_namebox_label is say_label

style email_message_window:
    xalign 0.5
    yalign 0.42
    xsize 1500
    ymaximum 600
    yfill True
    padding (100, 50)
    background Frame("gui/prompt_frame.png")

style email_message_window_nobox:
    xalign 0.5
    xfill True
    yalign 0.5
    ysize gui.textbox_height
    background None

style email_message_namebox:
    padding (0, 0)
    xalign 0.0
    yalign 0.0

transform expand(duration=0.5):
    linear duration zoom 1.0
    pause(duration)

transform minimize(duration=0.5):
    linear duration zoom 0.0
    pause(duration)

default expand_time = 0.35

image expand_prompt_frame:
    "gui/prompt_frame_empty.png"
    zoom 0.0
    xalign 0.5
    yalign 0.42
    xsize 1500
    ysize 600
    parallel:
        expand(expand_time)
    parallel:
        # blink duration and ending pause should be the same as expand duration
        blink(expand_time, 0.05)
    parallel:
        LightAberate

image close_prompt_frame:
    "gui/prompt_frame_empty.png"
    zoom 1.0
    xalign 0.5
    yalign 0.42
    xsize 1500
    ysize 600
    parallel:
        minimize(expand_time)
    parallel:
        # blink duration and ending pause should be the same as expand duration
        blink(expand_time, 0.05)


screen expand_message(expand_time = 0.35, blink_interval = 0.05):
    add "expand_prompt_frame"
    timer expand_time action [Return(True)]

screen email_message(who, who_suffix, what, show_intro = False, image_path = None, buttons = ["Continue"]):  
    style_prefix "email_message"
    window:
        id "window"
        if who is not None:
            window:
                id "namebox"
                style "email_message_namebox"

                if image_path:
                    image image_path:
                        xsize 150
                        ysize 150
                        xalign 0.0
                        yalign 0.0
                        at still_aberate(15)
                text who id "who":
                    color "#FFFFFF"
                    size 72
                    if image_path:
                        xpos 200
                    else:
                        xpos 0
                    at still_aberate(5.0)
                if who_suffix is not None:
                    text who_suffix id "who_suffix":
                        color "#d2d2d2"
                        size 42
                        ypos 100
                        if image_path:
                            xpos 200
                        else:
                            xpos 0
                        at still_aberate(2.0)
        text what id "what":
            color "#FFFFFF"
            size 30
            ypos 200
            at still_aberate(2.8)
            slow_cps 35
        at still_aberate(1.0)
        
    hbox id 'buttons':
        xalign 0.5
        ypos 900
        spacing 10
        for button_text in buttons:
            button:
                style "default_button"
                xsize 300
                at still_aberate(1.0)
                action Return(True)
                text button_text:
                    style "default_button_text"
                    xalign 0.5
                    at still_aberate(10.0)
    
    image "scanlines_overlay"
