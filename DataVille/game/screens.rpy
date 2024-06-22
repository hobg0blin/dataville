################################################################################
## Initialization ############################################################################### init offset = -1

################################################################################
## Styles
################################################################################

style default:
    properties gui.text_properties()
    language gui.language

style input:
    properties gui.text_properties("input", accent=True)
    adjust_spacing False

style hyperlink_text:
    properties gui.text_properties("hyperlink", accent=True)
    hover_underline True

style gui_text:
    properties gui.text_properties("interface")


style button:
    properties gui.button_properties("button")

style button_text is gui_text:
    properties gui.text_properties("button")
    yalign 0.5


style label_text is gui_text:
    properties gui.text_properties("label", accent=True)

style prompt_text is gui_text:
    properties gui.text_properties("prompt")


style bar:
    ysize gui.bar_size
    left_bar Frame("gui/bar/left.png", gui.bar_borders, tile=gui.bar_tile)
    right_bar Frame("gui/bar/right.png", gui.bar_borders, tile=gui.bar_tile)

style vbar:
    xsize gui.bar_size
    top_bar Frame("gui/bar/top.png", gui.vbar_borders, tile=gui.bar_tile)
    bottom_bar Frame("gui/bar/bottom.png", gui.vbar_borders, tile=gui.bar_tile)

style scrollbar:
    ysize gui.scrollbar_size
    base_bar Frame("gui/scrollbar/horizontal_[prefix_]bar.png", gui.scrollbar_borders, tile=gui.scrollbar_tile)
    thumb Frame("gui/scrollbar/horizontal_[prefix_]thumb.png", gui.scrollbar_borders, tile=gui.scrollbar_tile)

style vscrollbar:
    xsize gui.scrollbar_size
    base_bar Frame("gui/scrollbar/vertical_[prefix_]bar.png", gui.vscrollbar_borders, tile=gui.scrollbar_tile)
    thumb Frame("gui/scrollbar/vertical_[prefix_]thumb.png", gui.vscrollbar_borders, tile=gui.scrollbar_tile)

style slider:
    ysize gui.slider_size
    base_bar Frame("gui/slider/horizontal_[prefix_]bar.png", gui.slider_borders, tile=gui.slider_tile)
    thumb "gui/slider/horizontal_[prefix_]thumb.png"

style vslider:
    xsize gui.slider_size
    base_bar Frame("gui/slider/vertical_[prefix_]bar.png", gui.vslider_borders, tile=gui.slider_tile)
    thumb "gui/slider/vertical_[prefix_]thumb.png"

style frame:
    padding gui.frame_borders.padding
    background Frame("gui/frame.png", gui.frame_borders, tile=gui.frame_tile)

style prompt_frame is frame:
    background Frame("gui/prompt_frame.png", gui.frame_borders, tile=gui.frame_tile)

style default_button:
    padding gui.frame_borders.padding
    background Frame("gui/prompt_frame.png", gui.frame_borders, tile=gui.frame_tile)
    activate_sound "click.wav"

################################################################################
## In-game screens
################################################################################


## Say screen ##################################################################
##
## The say screen is used to display dialogue to the player. It takes two
## parameters, who and what, which are the name of the speaking character and
## the text to be displayed, respectively. (The who parameter can be None if no
## name is given.)
##
## This screen must create a text displayable with id "what", as Ren'Py uses
## this to manage text display. It can also create displayables with id "who"
## and id "window" to apply style properties.
##
## https://www.renpy.org/doc/html/screen_special.html#say

screen say(who, what):
    style_prefix "say"

    window:
        id "window"
        if who is not None:

            window:
                id "namebox"
                style "namebox"
                text who id "who"

        text what id "what"


    ## If there's a side image, display it above the text. Do not display on the
    ## phone variant - there's no room.
    if not renpy.variant("small"):
        add SideImage() xalign 0.0 yalign 1.0


## Make the namebox available for styling through the Character object.
init python:
    config.character_id_prefixes.append('namebox')

style window is default
style say_label is default
style say_dialogue is default
style say_thought is say_dialogue

style namebox is default
style namebox_label is say_label

style window:
    xalign 0.5
    xfill True
    yalign gui.textbox_yalign
    ysize gui.textbox_height
    background None

style window_wbox:
    xalign 0.5
    xfill True
    yalign gui.textbox_yalign
    ysize gui.textbox_height
    background Image("gui/textbox.png", xalign=0.5, yalign=1.0)

style interview_dialogue:
    xalign 0.5
    xfill True
    yalign 0.2
    ysize gui.textbox_height
    background None

style namebox:
    xpos gui.name_xpos
    xanchor gui.name_xalign
    xsize gui.namebox_width
    ypos gui.name_ypos
    ysize gui.namebox_height

    background Frame("gui/namebox.png", gui.namebox_borders, tile=gui.namebox_tile, xalign=gui.name_xalign)
    padding gui.namebox_borders.padding

style interview_namebox is namebox:
    yalign 0.15

style say_label:
    properties gui.text_properties("name", accent=True)
    xalign gui.name_xalign
    yalign 0.5

style say_dialogue:
    properties gui.text_properties("dialogue")

    xpos gui.dialogue_xpos
    xsize gui.dialogue_width
    ypos gui.dialogue_ypos

    adjust_spacing False


## Input screen ################################################################
##
## This screen is used to display renpy.input. The prompt parameter is used to
## pass a text prompt in.
##
## This screen must create an input displayable with id "input" to accept the
## various input parameters.
##
## https://www.renpy.org/doc/html/screen_special.html#input

screen input(prompt):
    style_prefix "input"

    window:

        vbox:
            xanchor gui.dialogue_text_xalign
            xpos gui.dialogue_xpos
            xsize gui.dialogue_width
            ypos gui.dialogue_ypos

            text prompt style "input_prompt"
            input id "input"

style input_prompt is default

style input_prompt:
    xalign gui.dialogue_text_xalign
    properties gui.text_properties("input_prompt")

style input:
    xalign gui.dialogue_text_xalign
    xmaximum gui.dialogue_width


## Choice screen ###############################################################
##
## This screen is used to display the in-game choices presented by the menu
## statement. The one parameter, items, is a list of objects, each with caption
## and action fields.
##
## https://www.renpy.org/doc/html/screen_special.html#choice

screen choice(items):
    style_prefix "choice"

    vbox:
        for i in items:
            textbutton i.caption action i.action


style choice_vbox is vbox
style choice_button is button
style choice_button_text is button_text

style choice_vbox:
    xalign 0.5
    ypos 405
    yanchor 0.5

    spacing gui.choice_spacing

style choice_button is default:
    properties gui.button_properties("choice_button")

style choice_button_text is default:
    properties gui.button_text_properties("choice_button")


## Quick Menu screen ###########################################################
##
## The quick menu is displayed in-game to provide easy access to the out-of-game
## menus.

screen quick_menu():

    ## Ensure this appears on top of other screens.
    zorder 100

    if quick_menu:

        hbox:
            style_prefix "quick"

            xalign 0.5
            yalign 1.0

            textbutton _("Back") action Rollback()
            textbutton _("History") action ShowMenu('history')
            textbutton _("Skip") action Skip() alternate Skip(fast=True, confirm=True)
            textbutton _("Auto") action Preference("auto-forward", "toggle")
            textbutton _("Save") action ShowMenu('save')
            textbutton _("Q.Save") action QuickSave()
            textbutton _("Q.Load") action QuickLoad()
            textbutton _("Prefs") action ShowMenu('preferences')


## This code ensures that the quick_menu screen is displayed in-game, whenever
## the player has not explicitly hidden the interface.
# we're not doing that now
# init python:
#     config.overlay_screens.append("quick_menu")

default quick_menu = True

style quick_button is default
style quick_button_text is button_text

style quick_button:
    properties gui.button_properties("quick_button")

style quick_button_text:
    properties gui.button_text_properties("quick_button")


################################################################################
## Main and Game Menu Screens
################################################################################

## Navigation screen ###########################################################
##
## This screen is included in the main and game menus, and provides navigation
## to other menus, and to start the game.


screen navigation():

    vbox:
        style_prefix "navigation"

        xpos gui.navigation_xpos
        yalign 0.5

        spacing gui.navigation_spacing

        if main_menu:

            textbutton _("Start") action Start()

        else:

            textbutton _("History") action ShowMenu("history")

            textbutton _("Save") action ShowMenu("save")

        textbutton _("Load") action ShowMenu("load")

        textbutton _("Preferences") action ShowMenu("preferences")

        if _in_replay:

            textbutton _("End Replay") action EndReplay(confirm=True)

        elif not main_menu:

            textbutton _("Main Menu") action MainMenu()

        textbutton _("About") action ShowMenu("about")

        if renpy.variant("pc") or (renpy.variant("web") and not renpy.variant("mobile")):

            ## Help isn't necessary or relevant to mobile devices.
            textbutton _("Help") action ShowMenu("help")

        if renpy.variant("pc"):

            ## The quit button is banned on iOS and unnecessary on Android and
            ## Web.
            textbutton _("Quit") action Quit(confirm=not main_menu)


style navigation_button is gui_button
style navigation_button_text is gui_button_text

style navigation_button:
    size_group "navigation"
    properties gui.button_properties("navigation_button")

style navigation_button_text:
    properties gui.button_text_properties("navigation_button")


## Main Menu screen ############################################################
##
## Used to display the main menu when Ren'Py starts.
##
## https://www.renpy.org/doc/html/screen_special.html#main-menu

image attract_seq:
    # base offset is 410, 0
    xoffset 410
    "images/screens/00-title/title-00.png"
    zoom 1.0
    linear 5 xoffset 200 yoffset 50 zoom 1.1
    "images/screens/00-title/title-01.png"
    xoffset 410
    zoom 1.2
    linear 5 xoffset 400 yoffset 50 zoom 1.0
    "images/screens/00-title/title-02.png"
    xoffset 0
    yoffset 100
    zoom 1.3
    linear 5 xoffset 400 yoffset 50 zoom 1.0
    "images/screens/00-title/title-03.png"
    xoffset 410
    yoffset 0
    zoom 0.96
    linear 5 xoffset 500 yoffset 50 zoom 1.1
    repeat

image tv_hollow:
    "images/screens/00-title/tv_hollow.png"
    zoom 0.75
    xoffset -330
    yoffset -250

# this was used to help with position the tv screen
image top_pos = Solid("#ff0000", xpos = 0, ypos = 187, xsize = 1920, ysize = 5)
image bottom_pos = Solid("#ff0000", xpos = 0, ypos = 767, xsize = 1920, ysize = 5)
image left_pos = Solid("#ff0000", xpos = 738, ypos = 0, xsize = 5, ysize = 1080)
image right_pos = Solid("#ff0000", xpos = 1595, ypos = 0, xsize = 5, ysize = 1080)

screen main_menu():

    ## This ensures that any other menu screen is replaced.
    tag menu
    
    add "attract_seq" at VHS

    add "tv_hollow"

    ## This empty frame darkens the main menu.
    frame:
        style "main_menu_frame"

    ## The use statement includes another screen inside this one. The actual
    ## contents of the main menu are in the navigation screen.
    use navigation

    if gui.show_name:

        vbox:
            style "main_menu_vbox"

            text "[config.name!t]":
                style "main_menu_title"

            # text "[config.version]":
            #     style "main_menu_version"


style main_menu_frame is empty
style main_menu_vbox is vbox
style main_menu_text is gui_text
style main_menu_title is main_menu_text
style main_menu_version is main_menu_text

style main_menu_frame:
    xsize 420
    yfill True

    background Color("#b5b5b58e")

style main_menu_vbox:
    xalign 1.0
    xoffset -30
    xmaximum 1200
    yalign 1.0
    yoffset -30

style main_menu_text:
    properties gui.text_properties("main_menu", accent=True)

style main_menu_title:
    properties gui.text_properties("title")

style main_menu_version:
    properties gui.text_properties("version")


## Game Menu screen ############################################################
##
## This lays out the basic common structure of a game menu screen. It's called
## with the screen title, and displays the background, title, and navigation.
##
## The scroll parameter can be None, or one of "viewport" or "vpgrid".
## This screen is intended to be used with one or more children, which are
## transcluded (placed) inside it.

screen game_menu(title, scroll=None, yinitial=0.0):

    style_prefix "game_menu"

    if main_menu:
        add gui.main_menu_background
    else:
        add gui.game_menu_background

    frame:
        style "game_menu_outer_frame"

        hbox:

            ## Reserve space for the navigation section.
            frame:
                style "game_menu_navigation_frame"

            frame:
                style "game_menu_content_frame"

                if scroll == "viewport":

                    viewport:
                        yinitial yinitial
                        scrollbars "vertical"
                        mousewheel True
                        draggable True
                        pagekeys True

                        side_yfill True

                        vbox:
                            transclude

                elif scroll == "vpgrid":

                    vpgrid:
                        cols 1
                        yinitial yinitial

                        scrollbars "vertical"
                        mousewheel True
                        draggable True
                        pagekeys True

                        side_yfill True

                        transclude

                else:

                    transclude

    use navigation

    textbutton _("Return"):
        style "return_button"

        action Return()

    label title

    if main_menu:
        key "game_menu" action ShowMenu("main_menu")


style game_menu_outer_frame is empty
style game_menu_navigation_frame is empty
style game_menu_content_frame is empty
style game_menu_viewport is gui_viewport
style game_menu_side is gui_side
style game_menu_scrollbar is gui_vscrollbar

style game_menu_label is gui_label
style game_menu_label_text is gui_label_text

style return_button is navigation_button
style return_button_text is navigation_button_text

style game_menu_outer_frame:
    bottom_padding 45
    top_padding 180

    background "gui/overlay/game_menu.png"

style game_menu_navigation_frame:
    xsize 420
    yfill True

style game_menu_content_frame:
    left_margin 60
    right_margin 30
    top_margin 15

style game_menu_viewport:
    xsize 1380

style game_menu_vscrollbar:
    unscrollable gui.unscrollable

style game_menu_side:
    spacing 15

style game_menu_label:
    xpos 75
    ysize 180

style game_menu_label_text:
    size gui.title_text_size
    color gui.accent_color
    yalign 0.5

style return_button:
    xpos gui.navigation_xpos
    yalign 1.0
    yoffset -45


## About screen ################################################################
##
## This screen gives credit and copyright information about the game and Ren'Py.
##
## There's nothing special about this screen, and hence it also serves as an
## example of how to make a custom screen.

screen about():

    tag menu

    ## This use statement includes the game_menu screen inside this one. The
    ## vbox child is then included inside the viewport inside the game_menu
    ## screen.
    use game_menu(_("About"), scroll="viewport"):

        style_prefix "about"

        vbox:

            label "[config.name!t]"
            text _("Version [config.version!t]\n")

            ## gui.about is usually set in options.rpy.
            if gui.about:
                text "[gui.about!t]\n"

            text _("Made with {a=https://www.renpy.org/}Ren'Py{/a} [renpy.version_only].\n\n[renpy.license!t]")


style about_label is gui_label
style about_label_text is gui_label_text
style about_text is gui_text

style about_label_text:
    size gui.label_text_size


## Load and Save screens #######################################################
##
## These screens are responsible for letting the player save the game and load
## it again. Since they share nearly everything in common, both are implemented
## in terms of a third screen, file_slots.
##
## https://www.renpy.org/doc/html/screen_special.html#save https://
## www.renpy.org/doc/html/screen_special.html#load

screen save():

    tag menu

    use file_slots(_("Save"))


screen load():

    tag menu

    use file_slots(_("Load"))


screen file_slots(title):

    default page_name_value = FilePageNameInputValue(pattern=_("Page {}"), auto=_("Automatic saves"), quick=_("Quick saves"))

    use game_menu(title):

        fixed:

            ## This ensures the input will get the enter event before any of the
            ## buttons do.
            order_reverse True

            ## The page name, which can be edited by clicking on a button.
            button:
                style "page_label"

                key_events True
                xalign 0.5
                action page_name_value.Toggle()

                input:
                    style "page_label_text"
                    value page_name_value

            ## The grid of file slots.
            grid gui.file_slot_cols gui.file_slot_rows:
                style_prefix "slot"

                xalign 0.5
                yalign 0.5

                spacing gui.slot_spacing

                for i in range(gui.file_slot_cols * gui.file_slot_rows):

                    $ slot = i + 1

                    button:
                        action FileAction(slot)

                        has vbox

                        add FileScreenshot(slot) xalign 0.5

                        text FileTime(slot, format=_("{#file_time}%A, %B %d %Y, %H:%M"), empty=_("empty slot")):
                            style "slot_time_text"

                        text FileSaveName(slot):
                            style "slot_name_text"

                        key "save_delete" action FileDelete(slot)

            ## Buttons to access other pages.
            vbox:
                style_prefix "page"

                xalign 0.5
                yalign 1.0

                hbox:
                    xalign 0.5

                    spacing gui.page_spacing

                    textbutton _("<") action FilePagePrevious()

                    if config.has_autosave:
                        textbutton _("{#auto_page}A") action FilePage("auto")

                    if config.has_quicksave:
                        textbutton _("{#quick_page}Q") action FilePage("quick")

                    ## range(1, 10) gives the numbers from 1 to 9.
                    for page in range(1, 10):
                        textbutton "[page]" action FilePage(page)

                    textbutton _(">") action FilePageNext()

                if config.has_sync:
                    if CurrentScreenName() == "save":
                        textbutton _("Upload Sync"):
                            action UploadSync()
                            xalign 0.5
                    else:
                        textbutton _("Download Sync"):
                            action DownloadSync()
                            xalign 0.5


style page_label is gui_label
style page_label_text is gui_label_text
style page_button is gui_button
style page_button_text is gui_button_text

style slot_button is gui_button
style slot_button_text is gui_button_text
style slot_time_text is slot_button_text
style slot_name_text is slot_button_text

style page_label:
    xpadding 75
    ypadding 5

style page_label_text:
    textalign 0.5
    layout "subtitle"
    hover_color gui.hover_color

style page_button:
    properties gui.button_properties("page_button")

style page_button_text:
    properties gui.button_text_properties("page_button")

style slot_button:
    properties gui.button_properties("slot_button")

style slot_button_text:
    properties gui.button_text_properties("slot_button")


## Preferences screen ##########################################################
##
## The preferences screen allows the player to configure the game to better suit
## themselves.
##
## https://www.renpy.org/doc/html/screen_special.html#preferences

screen preferences():

    tag menu

    use game_menu(_("Preferences"), scroll="viewport"):

        vbox:

            hbox:
                box_wrap True

                if renpy.variant("pc") or renpy.variant("web"):

                    vbox:
                        style_prefix "radio"
                        label _("Display")
                        textbutton _("Window") action Preference("display", "window")
                        textbutton _("Fullscreen") action Preference("display", "fullscreen")

                vbox:
                    style_prefix "check"
                    label _("Skip")
                    textbutton _("Unseen Text") action Preference("skip", "toggle")
                    textbutton _("After Choices") action Preference("after choices", "toggle")
                    textbutton _("Transitions") action InvertSelected(Preference("transitions", "toggle"))

                ## Additional vboxes of type "radio_pref" or "check_pref" can be
                ## added here, to add additional creator-defined preferences.

            null height (4 * gui.pref_spacing)

            hbox:
                style_prefix "slider"
                box_wrap True

                vbox:

                    label _("Text Speed")

                    bar value Preference("text speed")

                    label _("Auto-Forward Time")

                    bar value Preference("auto-forward time")

                vbox:

                    if config.has_music:
                        label _("Music Volume")

                        hbox:
                            bar value Preference("music volume")

                    if config.has_sound:

                        label _("Sound Volume")

                        hbox:
                            bar value Preference("sound volume")

                            if config.sample_sound:
                                textbutton _("Test") action Play("sound", config.sample_sound)


                    if config.has_voice:
                        label _("Voice Volume")

                        hbox:
                            bar value Preference("voice volume")

                            if config.sample_voice:
                                textbutton _("Test") action Play("voice", config.sample_voice)

                    if config.has_music or config.has_sound or config.has_voice:
                        null height gui.pref_spacing

                        textbutton _("Mute All"):
                            action Preference("all mute", "toggle")
                            style "mute_all_button"


style pref_label is gui_label
style pref_label_text is gui_label_text
style pref_vbox is vbox

style radio_label is pref_label
style radio_label_text is pref_label_text
style radio_button is gui_button
style radio_button_text is gui_button_text
style radio_vbox is pref_vbox

style check_label is pref_label
style check_label_text is pref_label_text
style check_button is gui_button
style check_button_text is gui_button_text
style check_vbox is pref_vbox

style slider_label is pref_label
style slider_label_text is pref_label_text
style slider_slider is gui_slider
style slider_button is gui_button
style slider_button_text is gui_button_text
style slider_pref_vbox is pref_vbox

style mute_all_button is check_button
style mute_all_button_text is check_button_text

style pref_label:
    top_margin gui.pref_spacing
    bottom_margin 3

style pref_label_text:
    yalign 1.0

style pref_vbox:
    xsize 338

style radio_vbox:
    spacing gui.pref_button_spacing

style radio_button:
    properties gui.button_properties("radio_button")
    foreground "gui/button/radio_[prefix_]foreground.png"

style radio_button_text:
    properties gui.button_text_properties("radio_button")

style check_vbox:
    spacing gui.pref_button_spacing

style check_button:
    properties gui.button_properties("check_button")
    foreground "gui/button/check_[prefix_]foreground.png"

style check_button_text:
    properties gui.button_text_properties("check_button")

style slider_slider:
    xsize 525

style slider_button:
    properties gui.button_properties("slider_button")
    yalign 0.5
    left_margin 15

style slider_button_text:
    properties gui.button_text_properties("slider_button")

style slider_vbox:
    xsize 675


## History screen ##############################################################
##
## This is a screen that displays the dialogue history to the player. While
## there isn't anything special about this screen, it does have to access the
## dialogue history stored in _history_list.
##
## https://www.renpy.org/doc/html/history.html

screen history():

    tag menu

    ## Avoid predicting this screen, as it can be very large.
    predict False

    use game_menu(_("History"), scroll=("vpgrid" if gui.history_height else "viewport"), yinitial=1.0):

        style_prefix "history"

        for h in _history_list:

            window:

                ## This lays things out properly if history_height is None.
                has fixed:
                    yfit True

                if h.who:

                    label h.who:
                        style "history_name"
                        substitute False

                        ## Take the color of the who text from the Character, if
                        ## set.
                        if "color" in h.who_args:
                            text_color h.who_args["color"]

                $ what = renpy.filter_text_tags(h.what, allow=gui.history_allow_tags)
                text what:
                    substitute False

        if not _history_list:
            label _("The dialogue history is empty.")


## This determines what tags are allowed to be displayed on the history screen.

define gui.history_allow_tags = { "alt", "noalt", "rt", "rb", "art" }


style history_window is empty

style history_name is gui_label
style history_name_text is gui_label_text
style history_text is gui_text

style history_label is gui_label
style history_label_text is gui_label_text

style history_window:
    xfill True
    ysize gui.history_height

style history_name:
    xpos gui.history_name_xpos
    xanchor gui.history_name_xalign
    ypos gui.history_name_ypos
    xsize gui.history_name_width

style history_name_text:
    min_width gui.history_name_width
    textalign gui.history_name_xalign

style history_text:
    xpos gui.history_text_xpos
    ypos gui.history_text_ypos
    xanchor gui.history_text_xalign
    xsize gui.history_text_width
    min_width gui.history_text_width
    textalign gui.history_text_xalign
    layout ("subtitle" if gui.history_text_xalign else "tex")

style history_label:
    xfill True

style history_label_text:
    xalign 0.5


## Help screen #################################################################
##
## A screen that gives information about key and mouse bindings. It uses other
## screens (keyboard_help, mouse_help, and gamepad_help) to display the actual
## help.

screen help():

    tag menu

    default device = "keyboard"

    use game_menu(_("Help"), scroll="viewport"):

        style_prefix "help"

        vbox:
            spacing 23

            hbox:

                textbutton _("Keyboard") action SetScreenVariable("device", "keyboard")
                textbutton _("Mouse") action SetScreenVariable("device", "mouse")

                if GamepadExists():
                    textbutton _("Gamepad") action SetScreenVariable("device", "gamepad")

            if device == "keyboard":
                use keyboard_help
            elif device == "mouse":
                use mouse_help
            elif device == "gamepad":
                use gamepad_help


screen keyboard_help():

    hbox:
        label _("Enter")
        text _("Advances dialogue and activates the interface.")

    hbox:
        label _("Space")
        text _("Advances dialogue without selecting choices.")

    hbox:
        label _("Arrow Keys")
        text _("Navigate the interface.")

    hbox:
        label _("Escape")
        text _("Accesses the game menu.")

    hbox:
        label _("Ctrl")
        text _("Skips dialogue while held down.")

    hbox:
        label _("Tab")
        text _("Toggles dialogue skipping.")

    hbox:
        label _("Page Up")
        text _("Rolls back to earlier dialogue.")

    hbox:
        label _("Page Down")
        text _("Rolls forward to later dialogue.")

    hbox:
        label "H"
        text _("Hides the user interface.")

    hbox:
        label "S"
        text _("Takes a screenshot.")

    hbox:
        label "V"
        text _("Toggles assistive {a=https://www.renpy.org/l/voicing}self-voicing{/a}.")

    hbox:
        label "Shift+A"
        text _("Opens the accessibility menu.")


screen mouse_help():

    hbox:
        label _("Left Click")
        text _("Advances dialogue and activates the interface.")

    hbox:
        label _("Middle Click")
        text _("Hides the user interface.")

    hbox:
        label _("Right Click")
        text _("Accesses the game menu.")

    hbox:
        label _("Mouse Wheel Up\nClick Rollback Side")
        text _("Rolls back to earlier dialogue.")

    hbox:
        label _("Mouse Wheel Down")
        text _("Rolls forward to later dialogue.")


screen gamepad_help():

    hbox:
        label _("Right Trigger\nA/Bottom Button")
        text _("Advances dialogue and activates the interface.")

    hbox:
        label _("Left Trigger\nLeft Shoulder")
        text _("Rolls back to earlier dialogue.")

    hbox:
        label _("Right Shoulder")
        text _("Rolls forward to later dialogue.")


    hbox:
        label _("D-Pad, Sticks")
        text _("Navigate the interface.")

    hbox:
        label _("Start, Guide")
        text _("Accesses the game menu.")

    hbox:
        label _("Y/Top Button")
        text _("Hides the user interface.")

    textbutton _("Calibrate") action GamepadCalibrate()


style help_button is gui_button
style help_button_text is gui_button_text
style help_label is gui_label
style help_label_text is gui_label_text
style help_text is gui_text

style help_button:
    properties gui.button_properties("help_button")
    xmargin 12

style help_button_text:
    properties gui.button_text_properties("help_button")

style help_label:
    xsize 375
    right_padding 30

style help_label_text:
    size gui.text_size
    xalign 1.0
    textalign 1.0



################################################################################
## Additional screens
################################################################################


## Confirm screen ##############################################################
##
## The confirm screen is called when Ren'Py wants to ask the player a yes or no
## question.
##
## https://www.renpy.org/doc/html/screen_special.html#confirm

screen confirm(message, yes_action, no_action):

    ## Ensure other screens do not get input while this screen is displayed.
    modal True

    zorder 200

    style_prefix "confirm"

    add "gui/overlay/confirm_dark.png"

    frame:

        vbox:
            xalign .5
            yalign .5
            spacing 45

            label _(message):
                style "confirm_prompt"
                text_color "#ffffff"
                xalign 0.5

            hbox:
                xalign 0.5
                spacing 150

                textbutton _("Yes") action yes_action
                textbutton _("No") action no_action

    ## Right-click and escape answer "no".
    key "game_menu" action no_action


style confirm_frame is gui_frame
style confirm_prompt is gui_prompt
style confirm_prompt_text is gui_prompt_text
style confirm_button is gui_medium_button
style confirm_button_text is gui_medium_button_text

style confirm_frame:
    background Frame([ "gui/prompt_frame.png", "gui/frame.png"], gui.confirm_frame_borders, tile=gui.frame_tile)
    padding gui.confirm_frame_borders.padding
    xalign .5
    yalign .5

style confirm_prompt_text:
    textalign 0.5
    layout "subtitle"

style confirm_button:
    properties gui.button_properties("confirm_button")

style confirm_button_text:
    properties gui.button_text_properties("confirm_button")


## Skip indicator screen #######################################################
##
## The skip_indicator screen is displayed to indicate that skipping is in
## progress.
##
## https://www.renpy.org/doc/html/screen_special.html#skip-indicator

screen skip_indicator():

    zorder 100
    style_prefix "skip"

    frame:

        hbox:
            spacing 9

            text _("Skipping")

            text "▸" at delayed_blink(0.0, 1.0) style "skip_triangle"
            text "▸" at delayed_blink(0.2, 1.0) style "skip_triangle"
            text "▸" at delayed_blink(0.4, 1.0) style "skip_triangle"


## This transform is used to blink the arrows one after another.
transform delayed_blink(delay, cycle):
    alpha .5

    pause delay

    block:
        linear .2 alpha 1.0
        pause .2
        linear .2 alpha 0.5
        pause (cycle - .4)
        repeat


style skip_frame is empty
style skip_text is gui_text
style skip_triangle is skip_text

style skip_frame:
    ypos gui.skip_ypos
    background Frame("gui/skip.png", gui.skip_frame_borders, tile=gui.frame_tile)
    padding gui.skip_frame_borders.padding

style skip_text:
    size gui.notify_text_size

style skip_triangle:
    ## We have to use a font that has the BLACK RIGHT-POINTING SMALL TRIANGLE
    ## glyph in it.
    font "DejaVuSans.ttf"


## Notify screen ###############################################################
##
## The notify screen is used to show the player a message. (For example, when
## the game is quicksaved or a screenshot has been taken.)
##
## https://www.renpy.org/doc/html/screen_special.html#notify-screen

screen notify(message):

    zorder 100
    style_prefix "notify"

    frame at notify_appear:
        text "[message!tq]"

    timer 3.25 action Hide('notify')


transform notify_appear:
    on show:
        alpha 0
        linear .25 alpha 1.0
    on hide:
        linear .5 alpha 0.0


style notify_frame is empty
style notify_text is gui_text

style notify_frame:
    ypos gui.notify_ypos

    background Frame("gui/notify.png", gui.notify_frame_borders, tile=gui.frame_tile)
    padding gui.notify_frame_borders.padding

style notify_text:
    properties gui.text_properties("notify")


## NVL screen ##################################################################
##
## This screen is used for NVL-mode dialogue and menus.
##
## https://www.renpy.org/doc/html/screen_special.html#nvl


screen nvl(dialogue, items=None):

    window:
        style "nvl_window"

        has vbox:
            spacing gui.nvl_spacing

        ## Displays dialogue in either a vpgrid or the vbox.
        if gui.nvl_height:

            vpgrid:
                cols 1
                yinitial 1.0

                use nvl_dialogue(dialogue)

        else:

            use nvl_dialogue(dialogue)

        ## Displays the menu, if given. The menu may be displayed incorrectly if
        ## config.narrator_menu is set to True.
        for i in items:

            textbutton i.caption:
                action i.action
                style "nvl_button"

    add SideImage() xalign 0.0 yalign 1.0


screen nvl_dialogue(dialogue):

    for d in dialogue:

        window:
            id d.window_id

            fixed:
                yfit gui.nvl_height is None

                if d.who is not None:

                    text d.who:
                        id d.who_id

                text d.what:
                    id d.what_id


## This controls the maximum number of NVL-mode entries that can be displayed at
## once.
define config.nvl_list_length = gui.nvl_list_length

style nvl_window is default
style nvl_entry is default

style nvl_label is say_label
style nvl_dialogue is say_dialogue

style nvl_button is button
style nvl_button_text is button_text

style nvl_window:
    xfill True
    yfill True

    background "gui/nvl.png"
    padding gui.nvl_borders.padding

style nvl_entry:
    xfill True
    ysize gui.nvl_height

style nvl_label:
    xpos gui.nvl_name_xpos
    xanchor gui.nvl_name_xalign
    ypos gui.nvl_name_ypos
    yanchor 0.0
    xsize gui.nvl_name_width
    min_width gui.nvl_name_width
    textalign gui.nvl_name_xalign

style nvl_dialogue:
    xpos gui.nvl_text_xpos
    xanchor gui.nvl_text_xalign
    ypos gui.nvl_text_ypos
    xsize gui.nvl_text_width
    min_width gui.nvl_text_width
    textalign gui.nvl_text_xalign
    layout ("subtitle" if gui.nvl_text_xalign else "tex")

style nvl_thought:
    xpos gui.nvl_thought_xpos
    xanchor gui.nvl_thought_xalign
    ypos gui.nvl_thought_ypos
    xsize gui.nvl_thought_width
    min_width gui.nvl_thought_width
    textalign gui.nvl_thought_xalign
    layout ("subtitle" if gui.nvl_text_xalign else "tex")

style nvl_button:
    properties gui.button_properties("nvl_button")
    xpos gui.nvl_button_xpos
    xanchor gui.nvl_button_xalign

style nvl_button_text:
    properties gui.button_text_properties("nvl_button")


## Bubble screen ###############################################################
##
## The bubble screen is used to display dialogue to the player when using speech
## bubbles. The bubble screen takes the same parameters as the say screen, must
## create a displayable with the id of "what", and can create displayables with
## the "namebox", "who", and "window" ids.
##
## https://www.renpy.org/doc/html/bubble.html#bubble-screen

screen bubble(who, what):
    style_prefix "bubble"

    window:
        id "window"

        if who is not None:

            window:
                id "namebox"
                style "bubble_namebox"

                text who:
                    id "who"

        text what:
            id "what"

style bubble_window is empty
style bubble_namebox is empty
style bubble_who is default
style bubble_what is default

style bubble_window:
    xpadding 30
    top_padding 5
    bottom_padding 5

style bubble_namebox:
    xalign 0.5

style bubble_who:
    xalign 0.5
    textalign 0.5
    color "#000"

style bubble_what:
    align (0.5, 0.5)
    text_align 0.5
    layout "subtitle"
    color "#000"

define bubble.frame = Frame("gui/bubble.png", 55, 55, 55, 95)
define bubble.thoughtframe = Frame("gui/thoughtbubble.png", 55, 55, 55, 55)

define bubble.properties = {
    "bottom_left" : {
        "window_background" : Transform(bubble.frame, xzoom=1, yzoom=1),
        "window_bottom_padding" : 27,
    },

    "bottom_right" : {
        "window_background" : Transform(bubble.frame, xzoom=-1, yzoom=1),
        "window_bottom_padding" : 27,
    },

    "top_left" : {
        "window_background" : Transform(bubble.frame, xzoom=1, yzoom=-1),
        "window_top_padding" : 27,
    },

    "top_right" : {
        "window_background" : Transform(bubble.frame, xzoom=-1, yzoom=-1),
        "window_top_padding" : 27,
    },

    "thought" : {
        "window_background" : bubble.thoughtframe,
    },
}

define bubble.expand_area = {
    "bottom_left" : (0, 0, 0, 22),
    "bottom_right" : (0, 0, 0, 22),
    "top_left" : (0, 22, 0, 0),
    "top_right" : (0, 22, 0, 0),
    "thought" : (0, 0, 0, 0),
}



################################################################################
## Mobile Variants
################################################################################

style pref_vbox:
    variant "medium"
    xsize 675

## Since a mouse may not be present, we replace the quick menu with a version
## that uses fewer and bigger buttons that are easier to touch.
screen quick_menu():
    variant "touch"

    zorder 100

    if quick_menu:

        hbox:
            style_prefix "quick"

            xalign 0.5
            yalign 1.0

            textbutton _("Back") action Rollback()
            textbutton _("Skip") action Skip() alternate Skip(fast=True, confirm=True)
            textbutton _("Auto") action Preference("auto-forward", "toggle")
            textbutton _("Menu") action ShowMenu()


style window:
    variant "small"
    background "gui/phone/textbox.png"

style radio_button:
    variant "small"
    foreground "gui/phone/button/radio_[prefix_]foreground.png"

style check_button:
    variant "small"
    foreground "gui/phone/button/check_[prefix_]foreground.png"

style nvl_window:
    variant "small"
    background "gui/phone/nvl.png"

style main_menu_frame:
    variant "small"
    background "gui/phone/overlay/main_menu.png"

style game_menu_outer_frame:
    variant "small"
    background "gui/phone/overlay/game_menu.png"

style game_menu_navigation_frame:
    variant "small"
    xsize 510

style game_menu_content_frame:
    variant "small"
    top_margin 0

style pref_vbox:
    variant "small"
    xsize 600

style bar:
    variant "small"
    ysize gui.bar_size
    left_bar Frame("gui/phone/bar/left.png", gui.bar_borders, tile=gui.bar_tile)
    right_bar Frame("gui/phone/bar/right.png", gui.bar_borders, tile=gui.bar_tile)

style vbar:
    variant "small"
    xsize gui.bar_size
    top_bar Frame("gui/phone/bar/top.png", gui.vbar_borders, tile=gui.bar_tile)
    bottom_bar Frame("gui/phone/bar/bottom.png", gui.vbar_borders, tile=gui.bar_tile)

style scrollbar:
    variant "small"
    ysize gui.scrollbar_size
    base_bar Frame("gui/phone/scrollbar/horizontal_[prefix_]bar.png", gui.scrollbar_borders, tile=gui.scrollbar_tile)
    thumb Frame("gui/phone/scrollbar/horizontal_[prefix_]thumb.png", gui.scrollbar_borders, tile=gui.scrollbar_tile)

style vscrollbar:
    variant "small"
    xsize gui.scrollbar_size
    base_bar Frame("gui/phone/scrollbar/vertical_[prefix_]bar.png", gui.vscrollbar_borders, tile=gui.scrollbar_tile)
    thumb Frame("gui/phone/scrollbar/vertical_[prefix_]thumb.png", gui.vscrollbar_borders, tile=gui.scrollbar_tile)

style slider:
    variant "small"
    ysize gui.slider_size
    base_bar Frame("gui/phone/slider/horizontal_[prefix_]bar.png", gui.slider_borders, tile=gui.slider_tile)
    thumb "gui/phone/slider/horizontal_[prefix_]thumb.png"

style vslider:
    variant "small"
    xsize gui.slider_size
    base_bar Frame("gui/phone/slider/vertical_[prefix_]bar.png", gui.vslider_borders, tile=gui.slider_tile)
    thumb "gui/phone/slider/vertical_[prefix_]thumb.png"

style slider_vbox:
    variant "small"
    xsize None

style slider_slider:
    variant "small"
    xsize 900

################################################################
#### CUSTOM SCREENS AND STYLING
#################################################################
# TIMER STUFF
#


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

style button_click:
    activate_sound "click.wav"



screen timer:
    zorder 10
    python:
        init_time = float(task['time']) * 1000
        timer_failed = False
    vbox:
        xalign 0.0
        yalign 1.0
        timer 0.03 repeat True action If(time > 0, true=SetVariable('time', time - 30), false=[SetVariable('timer_failed', True), Show("cogni", None, "You ran out of time! Your earnings have been halved.", char_map['cogni']['mood']['default'], "bottom_left", True)])
        bar: 
            value time 
            range timer_range 
            xmaximum 1920
            # hls (0, 41, 0) == #696969
            # if timer is still less than half way, keep saturation at 0
            # else, start increaing it by the time left
            # offset is included to treat the halfway point at 0.0 and timer end at 0.5
            left_bar Solid(Color(hls=(0.0, 0.41, 0.0 if ((init_time - time) / init_time) < 0.5 else (init_time - (time + (init_time * 0.5))) / init_time)))
            right_bar Solid("#D9D9D9")  
            at alpha_dissolve




# GENERAL 'ALWAYS-ON OVERLAY'
# TODO:
# add 'effects' map to gui input that then affects overlay, something like
# if (order == 1) {
#  {streak_text: 'nice',
#  feed_text: 'good',
#  status: 'hell yeah brother
# } elif (order == 2) {
# { streak_text: 'less nice'
# }
# etc.
# }j

# COMPUTER screens
screen message(sender, buttons=None):
    $ print('buttons: ', buttons)
    python:
        if sender == 'supervisor':
            avatar = "images/characters/alex/alex_nuetral.png"
        elif sender == 'stranger':
            avatar = "images/characters/cogni/asst_normal.png"
        elif sender == 'cogni':
            avatar = "images/characters/cogni/asst_normal.png"
        else:
            avatar = "images/characters/cogni/asst_normal.png"
    window id 'content':
        ysize 1080
        xsize 1920
        image avatar:
            xpos 625
            ypos 620
        if buttons != None:
            hbox id 'buttons':
                xpos 0.38
                ypos 0.80
                spacing 10
                for button_text in buttons:
                    textbutton button_text style "default_button" action Return(True)

# A helper to create borders for displayable but maybe not the best
# keeping it here in case I come across a use case for this - HAB
# init python:
#     class Border(renpy.Displayable):
#         def __init__(self, color = "#FFFFFF", border_width = 3):
#             super(Border, self).__init__()
#             self.color = color
#             self.border_width = border_width

#         def render(self, width, height, st, at):
#             render = renpy.Render(width, height)

#             print(render.get_size())

#             xsize, ysize = (int(num) - 1 for num in render.get_size())

#             # Draw the border
#             render.place(Solid(self.color, xsize = xsize, ysize = self.border_width))  # Top border
#             render.place(Solid(self.color, xsize = self.border_width, ysize = ysize), x = xsize - self.border_width - 1) # Right border
#             render.place(Solid(self.color, xsize = xsize, ysize = self.border_width), y = ysize - self.border_width)# Bottom border
#             render.place(Solid(self.color, xsize = self.border_width, ysize = ysize), x = - 1) # Right border

#             return render
    
#     def create_border(inner, color, border_width):
#         return Frame(image = Solid("#000000"), xpadding=10, ypadding=10, child = Frame(Solid(color, alpha = 0.5), xpadding=10, ypadding=10, child=inner))


screen dream(dream_text, buttons):
    python:
        if buttons == None or len(buttons) <= 0:
            buttons = ["Next"]
    image "images/dataville_logo_white.svg":
        xalign 0.5
        yalign 0.1
    frame id 'content':
        style "prompt_frame"
        xalign 0.5
        yalign 0.5
        xmaximum 1419
        ymaximum 619
        vbox id 'text':
            yalign 0.4
            xalign 0.5
            text dream_text: 
                color "#FFFFFF"
        hbox id 'buttons':
            yalign 0.8
            xalign 0.5
            spacing 15
            for button_text in buttons:
                button:
                    style "default_button"
                    text button_text:
                        color "#FFFFFF"
                    action Return(True)

screen job_offer(phase):
    if phase == 1:
        image "images/job_page.png"
 
        button:
            xsize 579
            ysize 94
            xpos 670
            ypos 792
            style "default_button"
            text "{b}{size=36}Apply":
                yalign 0.5
                xalign 0.5
                color "#FFFFFF"
            action Return(True)
    else:
        image "images/job_page_blur.png" at alpha_dissolve_quick
                
        frame:
            xpos 251
            ypos 76
            xsize 1418
            ysize 923
            style "prompt_frame"
            python:
                text_file = renpy.open_file('game_files/job_description.txt', 'utf-8')
                counter = 0
            for row in text_file:
                python:
                    cleaned = str(row).replace("b'", '').replace('\n', '')
                text '\n' * counter + cleaned:
                    color "#FFFFFF"
                $ counter += 1
            python:
                text_file.close()
                del text_file
            button:
                xsize 579
                ysize 94
                xalign 0.5
                yalign 0.9
                text "{b}{size=36}Get Started":
                    yalign 0.5
                    xalign 0.5
                    color "#FFFFFF"
                style "default_button"
                action Return(True)

screen assistant:
    window id 'content':
        ymaximum 1200
        xmaximum 1600
        frame id 'status_bar':
            background "#136366"
            has hbox
            xsize 1600
            image "images/logo_white.png"
        hbox id 'assistant':
            xalign 0.3
            yalign 0.75
            image "images/characters/cogni/asst_normal.png"

screen instructions(task, xalign_val=0.5, yalign_val=0.13):
    vbox id 'instructions':
        xalign xalign_val
        yalign yalign_val
        text task['instructions']

screen overlay(task, cogni=False, button_text=False):
# streak_text, feed_text, instructions, status, button_text=False):
    window id 'content':
        style "window_nobox"
        ymaximum 1200
        xmaximum 1920
        frame id 'status_bar':
            background "images/screens/monitor/overlay.png"
            has hbox
            xsize 1920
            #TODO: just track number of tasks here
            #      text 'Performance:' + '\n{size=-5}' + task['performance']
            text '{font=fonts/RussoOne-Regular.ttf}TOTAL EARNINGS: $ ' + "{:.2f}".format(float(task['earnings'])) + '{/font}' xalign .90 color "#FFFFFF" 
        hbox id 'cogni':
            xsize 400
            ysize 300
            yalign 0.75
            xalign 0.2
            #TODO: diff version of cogni based on performance
            if cogni:
                vbox:
                    spacing 15
                    xsize 500
                    text '\n{size=-5}' + task['performance']
                    image "images/characters/cogni/asst_normal.png"
        if (button_text):
            frame id 'overlay_button':
                xsize 300
                xalign 0.5
                yalign 0.55
                textbutton button_text style "button_click" action Return(True)
#
# SELECT DA IMAGES
screen captcha_image(task, images):
    use instructions(task)
    window id 'labeler': 
        style "window_nobox"
        xsize 619
        ysize 619
        xalign 0.5
        yalign 0.5
        grid 3 3:
            xmaximum 200
            ymaximum 200
            spacing 7
            for i, img in enumerate(images):
                default strp = ""
                default btn_selected=False
                python:
                    base = os.path.basename(img)
                    strp = os.path.splitext(base)[0]
                    selected_image = Transform(f"{img}", matrixcolor=SaturationMatrix(0))
                    hover_image = Transform(f"{img}", matrixcolor=SepiaMatrix(tint=Color("#464d8aa2")))
                    print('img: ', img)
                    def check_selected(img):
                        if img in images_selected['values']:
                            return True
                        else:
                            return False
                imagebutton:
                    style "button_click"
                    xfill True
                    yfill True 
                    idle Transform(f"{img}", size = (200, 200), xpos = 0, ypos = 0)
                    hover Transform(hover_image, size = (200,200), xpos = 0, ypos = 0)
                    selected_idle Transform(selected_image, size=(180,180), xpos = 10, ypos = 10)
                    selected_hover Transform(hover_image, size=(180,180), xpos = 10, ypos = 10)
                    action [Function(select_image, strp), SelectedIf(check_selected(strp))]
    window id 'done':
        textbutton "Done":
            style "default_button"
            text_xalign 0.5
            xsize 380
            xalign 0.5
            yalign 0.5
            action Return(True)

screen comparison_image(task, images):
    use instructions(task)
    # $ random.shuffle(task)
    window id 'labeler':
        style "window_nobox"
        xmaximum 1920
        ymaximum 1600
        xalign 0.5
        yalign 0.5
        hbox:
            xalign 0.5
            spacing 100
            for img in images:
                default strp = ""
                python:
                    base = os.path.basename(img)
                    strp = os.path.splitext(base)[0]
                imagebutton:
                    xysize (600,600)
                    # xfill True
                    # yfill True
                    idle Transform(img, size = (600, 600), xpos = 0, ypos = 0)
                    hover Transform(img, size = (625, 625), xpos = -12, ypos = -12)
                    action [SetVariable("latest_choice", strp), Return(True)]

# SAY YES OR NO TO DA IMAGES
screen binary_image(task, images):
    use instructions(task)
    window id 'labeler':
        style "window_nobox"
        xalign 0.5
        yalign 0.5
        hbox:
            spacing 10
            for i, img in enumerate(images):
                default strp = ""
                python:
                    base = os.path.basename(img)
                    strp = os.path.splitext(base)[0]
                image im.Scale(f"{img}", 614, 614)

    hbox id 'done':
        xmaximum 1920
        xalign 0.5
        yalign 0.9
        spacing 20
        # Selected False prevents previous prompt selection from carrying over
        textbutton 'Yes':
            style "default_button"
            xsize 380
            text_xalign 0.5
            selected False
            action [SetVariable("latest_choice", "Y"), Return(True)]
        textbutton 'No':
            style "default_button"
            xsize 380
            text_xalign 0.5
            selected False
            action [SetVariable("latest_choice", "N"), Return(True)]

screen binary_text(task):
    use instructions(task)
    window id 'labeler':
        style "window_nobox"
        xmaximum 1920
        ymaximum 1080
        xalign 0.5
        yalign 0.5
        vbox id 'text_block':
            text '{size=+15}{i}'+ task['text_block'] + '{/i}{/size}'
    hbox id 'done':
        xmaximum 1920
        xalign 0.5
        yalign 0.9
        spacing 20
        # Selected False prevents previous prompt selection from carrying over
        textbutton 'Yes':
            style "default_button"
            xsize 380
            text_xalign 0.5
            selected False
            action [SetVariable("latest_choice", "Y"), Return(True)]
        textbutton 'No':
            style "default_button"
            xsize 380
            text_xalign 0.5
            selected False
            action [SetVariable("latest_choice", "N"), Return(True)]

screen task_error():
    # $ random.shuffle(task)
    window id 'labeler':
        style "window_nobox"
        xmaximum 900
        ymaximum 900
        xalign 0.75
        yalign 0.4
        vbox id 'text_block':
            text 'This task is missing something in the CSV!'
    hbox id 'done':
        xmaximum 900
        xalign 0.45
        yalign 0.7
        spacing 20
        frame:
            textbutton 'Next task' style "button_click" action [SetVariable("latest_choice", "Y"), Return(True)]

screen comparison_text(task, button_text='Done!'):
    use instructions(task)
    window id 'labeler':
        style "window_nobox"
        xalign 0.5
        yalign 0.5
        vbox:
            hbox:
                spacing 30
                for i in task['labels']:
                    vbox:
                        xsize 700
                        text '{size=+4}{i}'+ task['labels'][i]['text'] + '{/i}{/size}'
                            # xpos start_x_text ypos start_y_text
                            # action [SetVariable("latest_choice", i), Return(True)]
            hbox:
                xalign 0.5
                spacing 350
                for i in task['labels']:
                    textbutton "Option " + i:
                        style "default_button"
                        ypos 200
                        xsize 380
                        text_xalign 0.5
                        action [SetVariable("latest_choice", i), Return(True)]
                # python:
                #     box['xpos'] = start_x_text
                #     box['ypos'] = int(start_y_text) + (50*idx)
            # for some reason if i increase start_y in here it loops when the timer is repeating. this seems insane to me and i would like to find out why (e.g if put start_y += 50 here)
#  frame id 'done':
#    xsize 300
#    xalign 0.5
#    yalign 0.9
#    textbutton button_text action Return(True)

screen caption_image(task, images):
    use instructions(task)
    # Note: this shuffles because of the timer recalls the screen, which inturn reshuffles the labels
    # If we want the labels to shuffle, then the tasks need to be shuffled and stored sperately and
    # outside of the screen, so when the screne is called, the order isn't shuffled again
    # python:
    #     from random import shuffle
    #     shuffled_labels = list(task['labels'])
    #     shuffle(shuffled_labels)
    window id 'labeler':
        style "window_nobox"
        xmaximum 900
        ymaximum 900
        xalign 0.5
        yalign 0.5
        image im.Scale(f"{images[0]}", 614, 614)

    hbox:
        xmaximum 1920
        xalign 0.5
        yalign 0.9
        spacing 20
        for id in task['labels']:
            textbutton task['labels'][id]['text']:
                style "default_button" 
                xsize 380
                text_xalign 0.5
                selected False
                action [SetVariable("latest_choice", task['labels'][id]['name']), Return(True)]

screen sentiment_text(task):
    use instructions(task)
    window id 'labeler':
        style "window_nobox"
        xsize 700
        xalign 0.5
        yalign 0.5
        text "{size=+4}{i}" + task['text_block'] + "{/i}{/size}"

    hbox:
        xalign 0.5
        yalign 0.9
        spacing 30
        for id in task['labels']:
            textbutton task['labels'][id]['text']:
                style "default_button" 
                xminimum 350
                selected False
                xalign 0.5
                yalign 0.1
                action [SetVariable("latest_choice", task['labels'][id]['name']), Return(True)]




# ORDER THE TEXT

screen order_text(task, button_text='Done!'):
    zorder 1
    # this animates random shuffle??? is that supposed to be happening? either renpy.random or regular random does it
    #ok so use traditional python random library for actual randomization
    default label_order = []
    default box = {}
    python:
        import random
        label_count = len(task['labels'].values())
        label_order = []
        for x in range(1, label_count + 1):
            label_order.append(str(x))
        # disabling random for now because it keeps causing an animation, i don't know why
        # could just set a random position for them, I guess? Or have them side by side
            # random.shuffle(label_order)
    # # does not return a list but changes an existing one, generates same numbers every time
    # $ renpy.random.shuffle(task)

    window id 'labeler':
        style "window_nobox"
        xmaximum 900
        ymaximum 900
        xalign 0.5
        yalign 0.0
        vbox:
            for idx, i in enumerate(label_order):
                $ box = task['labels'][i]
                drag:
                    draggable True
                    drag_name box['name']
                    xpos start_x_text ypos start_y_text
                    dragged drag_log
                frame:
                    text '{size=-3}'+ box['text']
                python:
                    box['xpos'] = start_x_text
                    box['ypos'] = int(start_y_text) + (50*idx)
                    # for some reason if i increase start_y in here it loops when the timer is repeating. this seems insane to me and i would like to find out why (e.g if put start_y += 50 here)
    frame id 'done':
        xsize 300
        xalign 0.5
        yalign 0.9
        textbutton button_text style "button_click" action Return(True)

screen performance(state, average):
    $ print('state: ', state)
    $ print('average: ', average)
    python:
        positive_emoji = ["thumbs_up", "star_struck", "heart_eyes"]
        neutral_emoji = ["not_so_great", "ok", "neutral"]
        bad_emoji = ["angry", "vomit", "poo"]
        approval = "neutral"
        time = "neutral"
        money = "neutral"

        if state["approval_rate"] > average["score"] + 10:
            approval = positive_emoji[0]
            positive_emoji.pop(0)
        elif state["approval_rate"] <= average["score"] + 10 and state["approval_rate"] >= average["score"] - 10:
            approval = neutral_emoji[0]
            neutral_emoji.pop(0)
        else:
            approval = bad_emoji[0]
            neutral_emoji.pop(0)

        if state["average_time"] < average["time"] + 2:
            time = positive_emoji[0]
            positive_emoji.pop(0)
        elif state["average_time"] >= average["time"] + 2 and state["average_time"] <= average["time"] - 2:
            time = neutral_emoji[0]
            neutral_emoji.pop(0)
        else:
            time = bad_emoji[0]
            bad_emoji.pop(0)
    
        if state["earnings"] > average["earnings"] + (average["earnings"] / 10):
            earnings = positive_emoji[0]
            positive_emoji.pop(0)
        elif state["earnings"] <= average["earnings"] + (average["earnings"] / 10) and state["earnings"] <= average["earnings"] - (average["earnings"] / 10):
            earnings = neutral_emoji[0]
            neutral_emoji.pop(0)
        else:
            earnings = bad_emoji[0]
            bad_emoji.pop(0)

            
    frame:
        style "prompt_frame"
        xalign 0.5
        yalign 0.2
        xsize 600
        xpadding 50
        has vbox
        hbox:
            xsize 525
            text(f"Approval rating: {round(state['approval_rate'], 2)}%"):
                xsize 550
                yalign 0.5
            image f"icons/emoji/{approval}.png":
                xalign 1.0
        hbox:
            xsize 525
            text(f"Average time: {round(state['average_time'], 1)} seconds"):
                xsize 550
                yalign 0.5
            image f"icons/emoji/{time}.png":
                xalign 1.0

        hbox:
            xsize 525
            text(f"Earnings: ${round(state['earnings'], 2)}"):
                xsize 550
                yalign 0.5
            image f"icons/emoji/{earnings}.png":
                xalign 1.0

# apartment screens
# sticky notes zoom
# tv zoom
# window zoom
# MAYBE: CAT?

style sticky_note is default:
    font "fonts/BrownBagLunch.ttf"
    color "#000000"
    size 30
    xalign 0.5
    yalign 0.5

screen apartment(data, time):
    python:
        computer_sound = "computer.ogg"
        if time == "end":
            btn = "Go to sleep"
        else:
            btn = "Back to work"
        note_positions = [(730, 826), (1104, 828), (1458, 650), (1458, 462)]
    fixed:
        # We're not doing note clickables anymore, right? - HAB
        # imagebutton:
        #   xpos 1200 ypos 300
        #   activate_sound "audio/rustle.wav"
        #   idle Transform("images/room/room/note.png", size=(480, 270)) 
        #   hover Transform("images/room/room/note.png", size=(500, 290)) 
        #   action Show("zoomed_note", None, store.apartment_data)

        # Notes
        python:
            random.shuffle(data["sticky_note"])
        for i, note in enumerate(data["sticky_note"]):
            if i > 3:
                break
            if note["performance"] == "default" or note["performance"] == store.game_state.performance_rating or (note["event_flag"] in store.event_flags):
                hbox:
                    xsize 125 ysize 132
                    xpos note_positions[i][0] ypos note_positions[i][1]
                    text note["text"]:
                        style "sticky_note"

        # TV Hover button
        imagebutton:
            xpos 50 ypos 567
            xsize 539 ysize 433
            activate_sound "audio/tv_2.wav"
            idle Solid("#00000000")
            hover Solid("#d3a95620")
            action Show("zoomed_tv", None, store.apartment_data)
        
        # Same with windows as notes? - HAB
        # imagebutton:
        #   xpos 0 ypos 0
        #   activate_sound "audio/window.mp3"
        #   idle Transform("images/room/room/window_with_bg.png", size=(768, 432)) 
        #   hover Transform("images/room/room/window_with_bg.png", size=(788, 455)) 
        #   action Show("zoomed_window", None, store.apartment_data)
        
        # Computer Screen Hovor Button
        imagebutton:
            xpos 614 ypos 404
            xsize 837 ysize 456
            activate_sound "audio/tv_2.wav"
            idle Solid("#00000000")
            hover Solid("#d3a95620")
            action Return(True)

    # frame:
    #     xalign 0.1
    #     yalign 0.9
    #     textbutton "Set State" action Show("set_state", None)

# No longer zooming into the notes
screen zoomed_note(data):
    modal True
    vbox:
        xalign 0.5
        yalign 0
        image Transform("images/room/room/note.png", size=(1200, 1000)) 
    vbox:
        xalign 0.5
        yalign 0.2
        for note in data["sticky_note"]:
            if note["performance"] == "default" or note["performance"] == store.game_state.performance_rating or (note["event_flag"] in store.event_flags):
                text note["text"]
    frame:
        textbutton "X" activate_sound "rustle.wav" action Hide("zoomed_note", None)

screen zoomed_tv(data, index=0):
    modal True
    python:
        if store.game_state.day == 0 and store.game_state.time == "end":
            index = data["news"].index(next(filter(lambda n: n.get('time') == 'end', data['news'])))
    # advance through news items
        result = setitem(data, index)
        print('result: ', result)
        item = result[0]
        index = result[1]
        index +=1

    image item["image"] xsize 1920 ysize 1080
    # window:
    imagebutton:
        xpos 483 ypos 108
        xsize 1092 ysize 870
        activate_sound "remote.ogg"
        idle Solid("#00000000")
        hover Solid("#d3a95620")
        action Show("zoomed_tv", None, data, index)
    frame:
        style "intro_prompt"
        textbutton "X" activate_sound "tv_2.wav" action Hide("zoomed_tv", None)

screen zoomed_window(data):
    modal True
    frame:
        xalign 0
        yalign 0
    vbox:
        xalign 0.2
        image Transform(data["window_background"], size=(1000, 1000))
    image Transform("images/room/room/window.png", size=(2500, 1200))
    textbutton "X" action Hide("zoomed_window", None)

screen set_state():
    modal True
# streak_text, feed_text, instructions, status, button_text=False):
    frame id 'content':
        xalign 0
        yalign 0
        background "#136366"
        yfill 1200
        xfill 1800
        vbox:
            spacing 10
            frame:
                textbutton "Set day" action Show("set_day", None)
            frame:
                textbutton "Set task" action Show("set_task", None)
            frame:
                textbutton "Set performance" action Show("set_performance", None)
            frame:
                textbutton "Set time" action Show("set_time", None)
            frame:
                textbutton "Add event flag" action Show("add_event_flag", None)
            frame:
                textbutton "Close" action Hide("set_state", None)
#
# TODO: refactor so these are one screen that takes a variable

screen set_performance():
    modal True
# streak_text, feed_text, instructions, status, button_text=False):
    frame id 'content':
        xalign 0
        yalign 0
        background "#136366"
        yfill 1200
        xfill 1800
        vbox:
            text "set your performance (bad/good/neutral):"
            input default "":
                value VariableInputValue("performance_string")
            frame:
                textbutton "Set" action [Function(update_from_state_menu), Hide("set_performance", None), Show("set_state", None)]

screen set_time():
    modal True
# streak_text, feed_text, instructions, status, button_text=False):
    frame id 'content':
        xalign 0
        yalign 0
        background "#136366"
        yfill 1200
        xfill 1800
        vbox:
            text "set the time of day (start/end):"
            input default "":
                value VariableInputValue("time_string")
            frame:
                textbutton "Set" action [Function(update_from_state_menu), Hide("set_time", None), Show("set_state", None)]

screen set_day():
    modal True
# streak_text, feed_text, instructions, status, button_text=False):
    frame id 'content':
        xalign 0
        yalign 0
        background "#136366"
        yfill 1200
        xfill 1800
        vbox:
            text "set the day:"
            input default "":
                value VariableInputValue("day_string")
            frame:
                textbutton "Set" action [Function(update_from_state_menu), Hide("set_day", None), Show("set_state", None)]

screen set_task():
    modal True
# streak_text, feed_text, instructions, status, button_text=False):
    frame id 'content':
        xalign 0
        yalign 0
        background "#136366"
        yfill 1200
        xfill 1800
        vbox:
            text "set the task ID: "
            input default "":
                value VariableInputValue("task_string")
            frame:
                textbutton "Set" action [Function(update_from_state_menu), Hide("set_task", None), Show("set_state", None)]

screen add_event_flag():
    modal True
# streak_text, feed_text, instructions, status, button_text=False):
    frame id 'content':
        xalign 0
        yalign 0
        background "#136366"
        yfill 1200
        xfill 1800
        vbox:
            text "add an event flag: "
            input default "":
                value VariableInputValue("event_flag_string")
            frame:
                textbutton "Set" action [Function(update_from_state_menu), Hide("add_event_flag", None), Show("set_state", None)]

screen effect_overlay():
    zorder 100
    vbox:
        xsize 1920
        ysize 1080
        image Solid("#FF00FF44", xsize=1920, ysize=1080)