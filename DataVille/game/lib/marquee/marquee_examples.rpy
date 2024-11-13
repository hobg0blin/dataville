################################################################################
##
## Marquee for Ren'Py by Feniks (feniksdev.itch.io / feniksdev.com)
##
################################################################################
## This file contains an example screen demonstrating how to use the marquee
## screen language statement. You are free to delete this file if you don't
## need the marquee examples; all the backend code is in 01_marquee.rpy.
##
## To see the example marquee screen, jump to the included test_marquee_label
## label e.g.
##
# label start:
#     jump test_marquee_label
##
## Leave a comment on the tool page on itch.io if you run into any issues.
################################################################################
screen test_marquee():

    add "#21212d"

    default songs = ["Sunflower", "Dance of the Sugar Plum Fairy", "One Summer Day"]
    default song_title = songs[0]
    default num_squares = 4

    frame:
        ## This frame is going around the marquee to give it a background and
        ## some positioning information.
        background "#f93c3e"
        left_margin 25 top_margin 25
        ## The marquee keyword lets you declare a marquee element.
        marquee:
            ## Here you'll declare the size of the marquee area. If the contents
            ## of the marquee are bigger than this, it'll use the marquee
            ## animation.
            xsize 400 ysize 70
            ## You can provide an animation to the marquee contents with
            ## the animation property. There are three transforms declared
            ## in 01_marquee.rpy: marquee_pan, marquee_scroll and
            ## marquee_shuffle. Feel free to declare your own!
            ## The 10.0 adjusts the loop speed.
            animation marquee_pan(10.0)
            ## This is an optional property that is False by default. If you set
            ## it to True like below, the marquee will always animate, even if
            ## its contents would fit in the marquee area.
            always_animate True
            ## You can put whatever sorts of contents you want in the marquee.
            ## Note the space at the end of the text; this is because the pan
            ## links the contents directly so the space allows there to be a
            ## gap between the end and the beginning of the looped text.
            text "BREAKING NEWS: This marquee looks like ticker tape that constantly repeats. ":
                ## In this case, to make sure the text doesn't wrap to the size
                ## of the marquee, we use the `nobreak` layout.
                ## You could also put it in a `fixed` with a size larger than
                ## xsize 200, or a variety of other solutions.
                layout 'nobreak'
                yalign 0.5 color "#fff"

    ## This marquee has text that changes. It will start scrolling if the
    ## text is too long. You can click it to change the text.
    button:
        background "#ff8335" hover_background "#ca5f1c"
        ycenter 0.5 xcenter 0.75
        action SetScreenVariable("song_title", songs[(songs.index(song_title)+1) % len(songs)])
        marquee:
            xysize (300, 80)
            ## This animation scrolls the marquee contents offscreen and then
            ## resets it to its initial position. The first number is how long
            ## it takes to scroll offscreen, and the second is the delay before
            ## it starts scrolling offscreen.
            animation marquee_scroll(5.0, 2.0)
            ## If you want to include multiple elements in the marquee that
            ## scroll, you may need to play around with fit properties
            ## like `yfit True` and `xfit True` like below, or use containers
            ## like hbox/vbox as seen in the next example.
            has fixed:
                ## This xalign 0.5 also makes it so that when the contents don't
                ## need to be scrolled, they're centered in the marquee area.
                yfit True xfit True xalign 0.5
            add "gui/window_icon.png" xysize (300, 80) fit "contain"
            text "[song_title]" color "#000" layout 'nobreak' yalign 0.5

    ## Lastly, this marquee is full of a variable number of squares in an hbox.
    ## It will start shuffling to the left and right if it fills up with
    ## too many squares.
    hbox:
        xcenter 0.5 ycenter 0.75 spacing 80
        vbox:
            textbutton "Add Square":
                action SetScreenVariable("num_squares", num_squares+1)
            textbutton "Remove Square":
                action SetScreenVariable("num_squares", max(0, num_squares-1))
        frame:
            background "#f7f7ed" padding (40, 40)
            marquee:
                xysize (800, 200)
                ## This animation shuffles the marquee contents between
                ## being left-aligned and being right-aligned. The first
                ## argument is how long it moves for, and the second is how
                ## long it waits at either end before moving back.
                animation marquee_shuffle(4.0, 2.0)
                ## You can put all sorts of contents in the marquee. In this
                ## case, we're putting a bunch of squares in an hbox.
                hbox:
                    spacing 40 xalign 0.5
                    for i in range(num_squares):
                        label "Square [i]":
                            text_color "#000" text_align (0.5, 0.5)
                            background "#ff8335"
                            xysize (200, 200)
                            yalign 0.5 xalign 0.5

    textbutton "Return" align (1.0, 1.0) action Return()


label test_marquee_label():
    call screen test_marquee()
    "End of test."
    return