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

screen email_message(who, who_suffix, what, image_path = None, buttons = ["Continue"]):
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
                text who id "who":
                    size 72
                    if image_path:
                        xpos 200
                    else:
                        xpos 0
                if who_suffix is not None:
                    text who_suffix id "who_suffix":
                        size 42
                        ypos 100
                        if image_path:
                            xpos 200
                        else:
                            xpos 0
        text what id "what":
            size 30
            ypos 200
        
    hbox id 'buttons':
        xalign 0.5
        ypos 900
        spacing 10
        for button_text in buttons:
            textbutton button_text:
                style "default_button"
                xsize 300
                text_xalign 0.5
                action Return(True)
