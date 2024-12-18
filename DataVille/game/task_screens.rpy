# SELECT DA IMAGES
screen captcha_image(task, images):
    python:
        blink_sec, blink_interval, exit_fade_secs = 0.3, 0.07, 0.5

    default exit_sequence = False
    default show_penalty = False

    if not exit_sequence:
        fixed:
            use instructions(task)
            at fade_in(blink_sec)
    else:
        fixed:
            use instructions(task)
            at fade_out(exit_fade_secs)
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
                    if exit_sequence:
                        at fade_out(exit_fade_secs)
                    else:
                        at fade_in(blink_sec)
    
    window id 'done':
        textbutton "Done":
            selected False
            style "default_button"
            text_xalign 0.5
            xsize 380
            xalign 0.5
            yalign 0.5
            if exit_sequence:
                at blink(blink_sec, blink_interval)
            action [SetScreenVariable('exit_sequence', True)]
    
    if exit_sequence:
        $ show_penalty = task_penalty(task['payment'], check_images(images_selected, task['correct_images']))

    use overlay_reward(task['payment'], show_penalty)

    use cogni_timeup("You ran out of time! Your earnings have been halved.", char_map['cogni']['mood']['default'], "bottom_left", True)

    if exit_sequence:
        timer max(blink_sec, exit_fade_secs) action Return(True)

screen comparison_image(task, images):
    python:
        blink_sec, blink_interval, exit_fade_secs = 0.3, 0.1, 0.5

    default exit_sequence = False
    default selected_button = None
    default show_penalty = False

    if not exit_sequence:
        fixed:
            use instructions(task)
            at fade_in(blink_sec)
    else:
        fixed:
            use instructions(task)
            at fade_out(exit_fade_secs)
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
                    if selected_button == img:
                        at fade_and_blink(blink_sec, blink_interval)
                    elif exit_sequence:
                        at fade_out(exit_fade_secs)
                    else:
                        at fade_in(blink_sec)
                    action [
                        SetVariable("latest_choice", strp), 
                        SetScreenVariable("selected_button", img),
                        SetScreenVariable('exit_sequence', True)]

    if selected_button:
        $ show_penalty = task_penalty(task['payment'], check_binary(latest_choice, task))

    use overlay_reward(task['payment'], show_penalty)

    use cogni_timeup("You ran out of time! Your earnings have been halved.", char_map['cogni']['mood']['default'], "bottom_left", True)

    if exit_sequence:
        timer max(blink_sec, exit_fade_secs) action Return(True)

# SAY YES OR NO TO DA IMAGES
screen binary_image(task, images):
    python:
        blink_sec, blink_interval, exit_fade_secs = 0.3, 0.07, 0.5

    default exit_sequence = False
    default selected_button = None
    default show_penalty = False

    if not exit_sequence:
        fixed:
            use instructions(task)
            at fade_in(blink_sec)
    else:
        fixed:
            use instructions(task)
            at fade_out(exit_fade_secs)

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
                image im.Scale(f"{img}", 614, 614):
                    if exit_sequence:
                        at fade_out(exit_fade_secs)
                    else:
                        at fade_in(blink_sec)

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
            if selected_button == 'Y':
                at blink(blink_sec, blink_interval)
            elif exit_sequence:
                at fade_out(exit_fade_secs)
            else:
                at fade_in(blink_sec)
            action [
                SetVariable("latest_choice", "Y"), 
                SetScreenVariable('selected_button', 'Y'),
                SetScreenVariable('exit_sequence', True)]
        textbutton 'No':
            style "default_button"
            xsize 380
            text_xalign 0.5
            selected False
            if selected_button == 'N':
                at blink(blink_sec, blink_interval)
            elif exit_sequence:
                at fade_out(exit_fade_secs)
            else:
                at fade_in(blink_sec)
            action [
                SetVariable("latest_choice", "N"), 
                SetScreenVariable('selected_button', 'N'), 
                SetScreenVariable('exit_sequence', True)]

    if selected_button:
        $ show_penalty = task_penalty(task['payment'], check_binary(latest_choice, task))
         
    use overlay_reward(task['payment'], show_penalty)

    use cogni_timeup("You ran out of time! Your earnings have been halved.", char_map['cogni']['mood']['default'], "bottom_left", True)

    if exit_sequence:
        timer max(blink_sec, exit_fade_secs) action Return(True)
    
screen binary_text(task):
    python:
        blink_sec, blink_interval, exit_fade_secs = 0.3, 0.07, 0.5

    default exit_sequence = False
    default selected_button = None
    default show_penalty = False

    if not exit_sequence:
        fixed:
            use instructions(task)
            at fade_in(blink_sec)
    else:
        fixed:
            use instructions(task)
            at fade_out(exit_fade_secs)

    window id 'labeler':
        style "window_nobox"
        xmaximum 1920
        ymaximum 1080
        xalign 0.5
        yalign 0.5
        vbox id 'text_block':
            text '{size=+15}{i}'+ task['text_block'] + '{/i}{/size}':
                if exit_sequence:
                    at fade_out(exit_fade_secs)
                else:
                    at fade_in(blink_sec)

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
            if selected_button == 'Y':
                at blink(blink_sec, blink_interval)
            elif exit_sequence:
                at fade_out(exit_fade_secs)
            else:
                at fade_in(blink_sec)
            action [
                SetVariable("latest_choice", "Y"), 
                SetScreenVariable('selected_button', 'Y'),
                SetScreenVariable('show_penalty', task_penalty(task['payment'], check_binary(latest_choice, task))),  
                SetScreenVariable('exit_sequence', True)]
        textbutton 'No':
            style "default_button"
            xsize 380
            text_xalign 0.5
            selected False
            if selected_button == 'N':
                at blink(blink_sec, blink_interval)
            elif exit_sequence:
                at fade_out(exit_fade_secs)
            else:
                at fade_in(blink_sec)
            action [
                SetVariable("latest_choice", "N"), 
                SetScreenVariable('selected_button', 'N'), 
                SetScreenVariable('show_penalty', task_penalty(task['payment'], check_binary(latest_choice, task))), 
                SetScreenVariable('exit_sequence', True)]

    if selected_button:
        $ show_penalty = task_penalty(task['payment'], check_binary(latest_choice, task))
         
    use overlay_reward(task['payment'], show_penalty)

    use cogni_timeup("You ran out of time! Your earnings have been halved.", char_map['cogni']['mood']['default'], "bottom_left", True)

    if exit_sequence:
        timer max(blink_sec, exit_fade_secs) action Return(True)

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
    python:
        blink_sec, blink_interval, exit_fade_secs = 0.3, 0.07, 0.5

    default exit_sequence = False
    default selected_button = None
    default show_penalty = False

    if not exit_sequence:
        fixed:
            use instructions(task)
            at fade_in(blink_sec)
    else:
        fixed:
            use instructions(task)
            at fade_out(exit_fade_secs)
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
                        text '{size=+4}{i}'+ task['labels'][i]['text'] + '{/i}{/size}':
                            if exit_sequence:
                                at fade_out(exit_fade_secs)
                            else:
                                at fade_in(blink_sec)
                            # xpos start_x_text ypos start_y_text
                            # action [SetVariable("latest_choice", i), Return(True)]
            hbox:
                xalign 0.5
                spacing 350
                for i in task['labels']:
                    textbutton "Option " + i:
                        style "default_button"
                        selected False
                        ypos 200
                        xsize 380
                        text_xalign 0.5
                        if selected_button == i:
                            at blink(blink_sec, blink_interval)
                        elif exit_sequence:
                            at fade_out(exit_fade_secs)
                        else:
                            at fade_in(blink_sec)
                        action [
                            SetVariable("latest_choice", i),
                            SetScreenVariable('selected_button', i),
                            SetScreenVariable('show_penalty', task_penalty(task['payment'], check_binary(latest_choice, task))), 
                            SetScreenVariable('exit_sequence', True)]
                # python:
                #     box['xpos'] = start_x_text
                #     box['ypos'] = int(start_y_text) + (50*idx)
            # for some reason if i increase start_y in here it loops when the timer is repeating. this seems insane to me and i would like to find out why (e.g if put start_y += 50 here)
#  frame id 'done':
#    xsize 300
#    xalign 0.5
#    yalign 0.9
#    textbutton button_text action Return(True)
    if selected_button:
        $ show_penalty = task_penalty(task['payment'], check_binary(latest_choice, task))
         
    use overlay_reward(task['payment'], show_penalty)
    
    use cogni_timeup("You ran out of time! Your earnings have been halved.", char_map['cogni']['mood']['default'], "bottom_left", True)

    if exit_sequence:
        timer max(blink_sec, exit_fade_secs) action Return(True)


screen caption_image(task, images):
    python:
        blink_sec, blink_interval, exit_fade_secs = 0.3, 0.07, 0.5

    default exit_sequence = False
    default selected_button = None
    default show_penalty = False

    if not exit_sequence:
        fixed:
            use instructions(task)
            at fade_in(blink_sec)
    else:
        fixed:
            use instructions(task)
            at fade_out(exit_fade_secs)
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
        image im.Scale(f"{images[0]}", 614, 614):
            if exit_sequence:
                at fade_out(exit_fade_secs)
            else:
                at fade_in(blink_sec)

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
                if selected_button == task['labels'][id]['name']:
                    at blink(blink_sec, blink_interval)
                elif exit_sequence:
                    at fade_out(exit_fade_secs)
                else:
                    at fade_in(blink_sec)
                action [
                    SetVariable("latest_choice", task['labels'][id]['name']),
                    SetScreenVariable('selected_button', task['labels'][id]['name']),
                    SetScreenVariable('show_penalty', task_penalty(task['payment'], check_binary(latest_choice, task))), 
                    SetScreenVariable('exit_sequence', True)]
    
    if selected_button:
        $ show_penalty = task_penalty(task['payment'], check_binary(latest_choice, task))
         
    use overlay_reward(task['payment'], show_penalty)
    
    use cogni_timeup("You ran out of time! Your earnings have been halved.", char_map['cogni']['mood']['default'], "bottom_left", True)

    if exit_sequence:
        timer max(blink_sec, exit_fade_secs) action Return(True)

screen sentiment_text(task):
    python:
        blink_sec, blink_interval, exit_fade_secs = 0.3, 0.07, 0.5

    default exit_sequence = False
    default selected_button = None
    default show_penalty = False

    if not exit_sequence:
        fixed:
            use instructions(task)
            at fade_in(blink_sec)
    else:
        fixed:
            use instructions(task)
            at fade_out(exit_fade_secs)

    window id 'labeler':
        style "window_nobox"
        xsize 700
        xalign 0.5
        yalign 0.5
        text "{size=+4}{i}" + task['text_block'] + "{/i}{/size}":
            if exit_sequence:
                at fade_out(exit_fade_secs)
            else:
                at fade_in(blink_sec)

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
                text_xalign 0.5
                if selected_button == task['labels'][id]['name']:
                    at blink(blink_sec, blink_interval)
                elif exit_sequence:
                    at fade_out(exit_fade_secs)
                else:
                    at fade_in(blink_sec)
                action [
                    SetVariable("latest_choice", task['labels'][id]['name']),
                    SetScreenVariable('selected_button', task['labels'][id]['name']),
                    SetScreenVariable('show_penalty', task_penalty(task['payment'], check_binary(latest_choice, task))), 
                    SetScreenVariable('exit_sequence', True)]

    if selected_button:
        $ show_penalty = task_penalty(task['payment'], check_binary(latest_choice, task))
         
    use overlay_reward(task['payment'], show_penalty)
    
    use cogni_timeup("You ran out of time! Your earnings have been halved.", char_map['cogni']['mood']['default'], "bottom_left", True)

    if exit_sequence:
        timer max(blink_sec, exit_fade_secs) action Return(True)

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
    
    use cogni_timeup("You ran out of time! Your earnings have been halved.", char_map['cogni']['mood']['default'], "bottom_left", True)