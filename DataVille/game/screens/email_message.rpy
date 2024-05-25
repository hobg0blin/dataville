# # *****************************
# # * Email Message Screen Type *
# # *****************************
# # Used for Alex T's character
# # that takes up majority of the screen.

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
    xsize 1920
    ysize 1080
    background Frame("gui/prompt_frame.png")

style email_message_window_nobox:
    xalign 0.5
    xfill True
    yalign gui.textbox_yalign
    ysize gui.textbox_height
    background None

style email_message_namebox:
    xpos gui.name_xpos
    xanchor gui.name_xalign
    xsize gui.namebox_width
    ypos gui.name_ypos
    ysize gui.namebox_height

    background Frame("gui/namebox.png", gui.namebox_borders, tile=gui.namebox_tile, xalign=gui.name_xalign)
    padding gui.namebox_borders.padding

style email_message_label:
    properties gui.text_properties("name", accent=True)
    xalign gui.name_xalign
    yalign 0.5

style email_message_dialogue:
    properties gui.text_properties("dialogue")

    xpos gui.dialogue_xpos
    xsize gui.dialogue_width
    ypos gui.dialogue_ypos

    adjust_spacing False

screen email_message(who, what):
    window:
        id "window"
        if who is not None:
            window:
                id "namebox"
                style "namebox"
                text who id "who"
        text what id "what"
        add SideImage() xalign 0.5 yalign 0.5
