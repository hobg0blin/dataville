﻿
# The script of the game goes in tcustom_feedbacup file performance.
# Declare characters used by this game. The color argument colorizes the
# name of the character.
# Timer stuff from https://www.reddit.com/r/RenPy/comments/olfuk8/making_a_timer/
#
#
# TODOS:
#-  Overall state - in progress
#-  Saving/saved state - in progress
#- General GUI updates per figma file - in progress
#-  Probably use labels for each section/loop/etc.?
# - Make timer display numbers, kill and check task if it hits zero
# - Debug scoring, not sure it's working properly
# - image caption image isn't showing at all for some reason



#Set global variables
define m = Character("Me")
define news = Character("NEWS")
default task = {}
default task_string = "start_task"
default day_string = ""
default time_string = ""
default performance_string = ""
default event_flag_string = ""
default latest_choice = ""
default latest_score = 0
define gui.frame_borders = Borders(15, 15, 15, 15)
default messages = []
default custom_feedback = ""
default custom_feedback_sender = ""
default has_custom_feedback = False

init:
  define show_window = True

  image alien_human_family = "alien_human_family.png"
  image dark_green = Solid("#136366")
  image bg black = Solid("#000000")

  # All images must be declared in the init block
  image cogni_sprite happy = "images/characters/cogni/cogni_happy.png"

  define supervisor = Character("Alex T.", image="images/characters/alex/alex_neutral.png", who_suffix = "Senior Manager @ Dataville", kind=email_message)
  # cogni defined in characters/cogni.rpy
  define stranger = Character("$(#@^%)$)(#)%$@^*$(*)", image="images/characters/stranger.png", who_suffix = "?*#$&#*@()%&@)%&$@^)($#)", kind=email_message)
  define union = Character("Tim", image="images/characters/union.png", who_suffix = "Union Rep. Section 18, Cohort 48", kind=email_message)
  define news_anchor = Character(
    "News Anchor", 
    image="images/news_anchor.jpg", 
    window_style="interview_dialogue", 
    what_text_align=1.0, 
    color="#b9b9b9", 
    namebox_style="interview_namebox",
    who_size=18,
    what_slow_cps=preferences.text_cps
    )
  define victor = Character(
    "Victor", 
    image="images/victor.avif", 
    window_style="interview_dialogue", 
    what_text_align=0.0, 
    color="#b9b9b9", 
    namebox_style="interview_namebox",
    who_size=18)

  define char_map = {
    "supervisor": {
      "obj": supervisor,
      "mood": {
        "default": "images/characters/alex/alex_neutral.png",
        "happy": "images/characters/alex/alex_happy.png",
        "angry": "images/characters/alex/alex_angry.png"
      }
    },
    "cogni": {
      "obj": cogni,
      "mood": {
        "default": "cogni_sprite happy",
        "quizzical": "images/characters/cogni/asst_quizzical.png",
        "angry": "images/characters/cogni/asst_angry.png",
        "surprised": "images/characters/cogni/asst_surprised.png"
      }
    },
    "stranger": {
      "obj": stranger,
      "mood": {
        "default": "images/characters/stranger.png"
      }
    },
    "tim": { # tim is a union man
      "obj": union,
      "mood": {
        "default": "images/characters/union.png"
      }
    },
  }

  define apartment_bg_map = {
    "apartment_1": "images/apartment/apartment3_1_overlay.png",
  }
  
# The game starts here.
default skip_intro = False
default no_fail = False
default start_at_day_end = False
label start:
    $ set_initial_variables()
    image overlay_background = "images/screens/monitor/background.png"
    image bg black_bg = Solid('#000000')
    image bg apartment_bg = "images/apartment/apartment3_1.png"
    image bg gray_bg = Solid('#464645')
    
    if not skip_intro:
      play music "dataville_workspace_neutral.ogg" loop fadein 2.0

      image tv_overlay:
        "images/screens/00-title/tv_hollow.png"

      # v2 sequence
      image interview:
        "images/screens/01-intro/interview.jpg"
        zoom 0.335
      # image bg news_bg = "images/news_bg.png"

      image interview_trans:
        "images/screens/01-intro/title-into-trans.png"
        tv_zoom_in_seq

      show tv_noise:
        pos (700, 145)
        xoffset 0
        yoffset 0
        zoom 1.1
      show tv_overlay:
        zoom 0.75
        xoffset -330
        yoffset -250
        pos (0, 0)
      pause 0.5
      hide tv_noise
      hide tv_overlay

      show interview_trans:
        pos (0,0)
        VHS
      show tv_overlay:
        pos (0, 0)  
        tv_zoom_in_seq
      $ renpy.pause(3.3)
      scene interview with Dissolve(1.0)
      pause 0.7

      news_anchor "{cps=30}Good evening, and welcome to our program.{/cps}"
      news_anchor "{cps=30}Tonight, *hiding in the shadows*: what the alien menace means for you and your family. I’m joined by Victor Willmington, founder and CEO of the Dataville Corporation.{/cps}"
      news_anchor "{cps=30}Tell me Victor, how does your company see the ongoing alien migratory crisis?{/cps}"
      victor "{cps=30}Where you see a crisis, we at Dataville see an opportunity. This is our chance to restore human society to a safer, simpler time.{/cps}"
      victor "{cps=30}With our patented alien identification AI technology, we’re able to accurately penetrate alien camouflage.{/cps}"
      news_anchor "{cps=30}And you’ve found active partners in the public sector?{/cps}"
      victor "{cps=30}That’s right. Our clients include the Departments of Defense and State, as well as private enterprises looking to ensure their communities are 100 percent human.{/cps}"
      news_anchor "{cps=30}And what do you say to critics who accuse the Dataville Corporation of exacerbating racial tensions with the aliens?{/cps}"
      victor "{cps=30}Earth was meant for humans. If they have nothing to hide, why are they using camouflage?{/cps}"
      
      image job_page = "images/job_page.png"
      image job_page_blur = "images/job_page_blur.png"
      scene job_page
      call screen job_offer(1) with Dissolve(1.0)
      call screen job_offer(2)
      call screen job_offer(3, "\n Looking for a job? Looking to make the world a better, more human place?", ["Take the quiz!"])
      call screen job_offer(3, "Are you proud of your humanity?", ["Yes", "No"])
      call screen job_offer(3, "Do you own a computer?", ["Yes", "No"])
      call screen job_offer(3, "Are you interested in working from home?", ["Yes", "No"])
      call screen job_offer(3, "Congratulations! We'd like to extend an offer of employment! Join the DataVille team now.", ["Let's get started."])    
      show job_page_blur

      $ fade_into_dream(2.5)
      call screen dream("Your first day at a new job.", ["I'm excited!", "I'm terrified."])
      call screen dream("Try not to screw it up.", ["I'm going to do my best!", "Let's hope this doesn't go like my last gig."])
      call screen dream("You really need the money.", ["Mittens really needs to see a vet..."])
      call screen dream("Let's get started.", [])
      $ fade_out_of_dream(0.5)

      label intro:
        play music "dataville_apartment_neutral.ogg"
        python:
          notes = shuffle_notes(clean(store.apartment_data)['sticky_note'])
          random_scribble_base = list(range(1, 9))[0:4]
          for i in range(0, 4):
            notes[i]['image'] = f"scribble_base_{random_scribble_base[i]}"
        call screen apartment(clean(store.apartment_data), store.game_state.time, apartment_bg_map['apartment_1'], notes)
        hide screen apartment

    python:
      if start_at_day_end:
          day_end()
    if store.game_state.time == "end":
        jump interstitial

    play music "dataville_workspace_neutral.ogg" loop fadein 2.0
    
    # manually check messsages on first loop 
    $ cleaned = clean(store.apartment_data)

    $ show_computer_screen(store.game_state.ui)

    label check_messages:
      python:
        prev_speaker = None
        next_message_set = {'sender': None}
      while cleaned['message']:
        python:
          message = cleaned['message'].pop(0)
          try:
            next_message_set = cleaned['message'][0]
          except IndexError:
            next_message_set = {'sender': None}
          n = 120 # character limit?
          text = message['text']
          split = split_into_sentences(text)
          length = len(split)
          count = 0
        while count < length:
          python:
            strip_message = split[count].strip()
            # print('stripped message: ', strip_message)
            if count >= length - 1:
              buttons = message['buttons']
              second_sentence = ""
            else:
              buttons = []
              second_sentence = split[count+1]
          if strip_message != "" and strip_message != "\n":
            $ sender = char_map[message['sender']]
            # ONLY SHOWING ONE LINE DURING INTRO: I THINK THIS HAS THE LONGEST TEXT
            $ text =  f"{split[count]}"
            $ start_speaker = (not count) and (prev_speaker != message['sender'])
            $ end_speaker = (count == length - 1) and (next_message_set['sender'] != message['sender'])
            # $ print('check_messages', sender['obj'].name, sender['obj'].who_suffix, text, sender['mood']['default'], start_speaker, end_speaker)
            $ render_message(sender['obj'].name, sender['obj'].who_suffix, text, sender['mood']['default'], start = start_speaker, end = end_speaker)
          $ count += 1
          $ prev_speaker = message['sender']
  #manually set task & variables for first loop
    $ time = store.game_state.ui['timer']

    python:
      if len(task_string) > 0:
        task = store.loop[task_string]
      else:
        task = store.loop["start_task"]
      set_ui_state(task, store.game_state)


#THIS AUTOMATES GOING THROUGH TASKS WHEN INSTRUCTIONS/ETC. ARE UNNECESSARY
    $ starting_earnings = store.game_state.performance['earnings_minus_rent']
    label task_loop:
      # hide screen overlay
      # show screen overlay(task)
      # $ show_computer_screen_with_cogni_enter(store.game_state.ui)
      python:
        if not renpy.get_screen('cogni'):
          renpy.call_screen('cogni_enter', char_map['cogni']['mood']['default'], "bottom_left", hide_bubble = True)
      python:
        prev_speaker = None
        next_message_set = {'sender': None}

      if store.game_state.day != 0 and len(cleaned['message'])>0:
        while cleaned['message']:
          python:
            message = cleaned['message'].pop(0)
            try:
              next_message_set = cleaned['message'][0]
            except IndexError:
              next_message_set = {'sender': None}
            text = message['text']
            split = split_into_sentences(text)
            length = len(split)
            count = 0
          while count < length:
            python:
              strip_message == split[count].strip()
              if count >= length - 1:
                buttons = message['buttons']
                second_sentence = ""
              else:
                buttons = []
                second_sentence = split[count+1]
            if strip_message != "" and strip_message !="\n":
              $ text = f"{split[count]}"
              $ sender = char_map[message['sender']]
              $ start_speaker = (not count) and (prev_speaker != message['sender'])
              $ end_speaker = (count == length - 1) and (next_message_set['sender'] != message['sender'])
              # $ print('task_loop', sender['obj'].name, sender['obj'].who_suffix, text, sender['mood']['default'], start_speaker, end_speaker)
              $ render_message(sender['obj'].name, sender['obj'].who_suffix, text, sender['mood']['default'], position = "bottom_left", start = start_speaker, end = end_speaker)
            $ count += 1
            $ prev_speaker = message['sender']
      python:
# CLEAR IMAGE VARIABLES
      # FIXME: should clean up variable resetting a bit better
        is_image = False
        images_selected = {'values': []}
        if ('image' in task['type']):
          is_image = True
          images = get_images(task)
        time = float(task['time']) * 1000
        timer_range = time
      if 'custom_dialogue' in task:
        $ sender = char_map[task['custom_dialogue_sender']]
        $ custom_dialogue = task['custom_dialogue']
        $ start_speaker = sender['obj'].name != "cogni"
        $ end_speaker = sender['obj'].name != "cogni"
        # $ print('custom_dialogue', sender['obj'].name, sender['obj'].who_suffix, custom_dialogue, sender['mood']['default'], start_speaker, end_speaker)
        $ render_message(sender['obj'].name, sender['obj'].who_suffix, custom_dialogue, sender['mood']['default'], position = "bottom_left", start = start_speaker, end = end_speaker, overlay = True)

      $ custom_feedback = ""
      $ custom_feedback_sender = ""
      $ has_custom_feedback = False
      $ task_type = task['type']
      $ task_error = False

      show screen timer

      $ aberate_layer('all', 10)
      
      if (task['type'] == 'sentiment_text' and not 'labels' in task) or task['type'] == 'captcha_image' and not 'correct_images' in task:
        call screen task_error 
        $ task_error = True
      elif is_image:
        call screen expression(task['type']) pass (task, images)
      else:
        call screen expression(task['type']) pass (task)
      
      python:
        if not task_error:
            if (task['type'] == 'captcha_image'):
                case = check_images(images_selected, task['correct_images'])
                store.latest_score = case
                task = update_state(store.game_state, case, task)
            elif (task['type'] == 'order_text'):
                case = check_order_text(task)
                store.latest_score = case
                task = update_state(store.game_state, case,  task)
            else:
                binary_correct = check_binary(latest_choice, task)
                store.latest_score = binary_correct
                correct = task['correct_options']
                if 'custom_feedback_sender' in task:
                #if there's an ethical option AND specific feedback, show that
                    # print('hit ethical task: ', task)
                    # print('choice:', latest_choice)
                    # print('correct option: ', correct)
                    custom_feedback_sender = char_map[task['custom_feedback_sender']]
                    if 'ethical_options' in task:
                      ethical = task['ethical_options']
                      # print('ethical option: ', ethical)
                      if 'custom_feedback_ethical' in task and latest_choice == ethical:
                          # print('should be showing ethical custom feedback')
                          custom_feedback = task['custom_feedback_ethical'] 
                          has_custom_feedback = True
                    # if choice is correct and there's feedback for that, show it
                    if 'custom_feedback_correct' in task and latest_choice == correct:
                        # print('should be showing correct custom feedback')
                        # print('correct custom feedback: ', task['custom_feedback_correct'])
                        custom_feedback = task['custom_feedback_correct'] 
                        has_custom_feedback = True
                task = update_state(store.game_state, binary_correct, task)
                has_custom_feedback = custom_feedback != ""
        else:
            binary_correct = 1
            task = update_state(store.game_state, binary_correct, task)

      hide screen instructions
      hide screen timer
      hide screen empty_timer
      hide screen cogni_timeup
      hide screen task_type

      hide screen overlay_earnings
      $ show_green = starting_earnings != store.game_state.performance['earnings_minus_rent']
      show screen overlay_earnings(earning_flag = show_green)

      if has_custom_feedback:
        # need to hide and show cogni again due to some odd behavior with CPS text.
        hide screen cogni
        show screen cogni(None, char_map['cogni']['mood']['default'], position = "bottom_left")
        $ start_speaker = custom_feedback_sender['obj'].name != "cogni"
        $ end_speaker = custom_feedback_sender['obj'].name != "cogni" 
        # $ print('custom_feedback', custom_feedback_sender['obj'].name, custom_feedback_sender['obj'].who_suffix, custom_feedback, custom_feedback_sender['mood']['default'], start_speaker, end_speaker)    
        $ render_message(custom_feedback_sender['obj'].name, custom_feedback_sender['obj'].who_suffix, custom_feedback, custom_feedback_sender['mood']['default'], position = "bottom_left", start = start_speaker, end = end_speaker, overlay = True)
        hide screen message 

      if (task == 'break'):
        $ day_end()
        call interstitial from _call_interstitial
      else:
        call task_loop from _call_task_loop
      return

    # INTERSTITIAL
    label interstitial:
      hide screen instructions
      # $ show_computer_screen(store.game_state.ui)
      # fail states for not making rent, failing the tutorial, or being bad at the game
      $ store.game_state.performance_count[store.game_state.performance_rating] += 1
      #if store.game_state.performance_count['bad'] >= 3 and not no_fail:
      #  $ print('three bad states')
      #  $ store.event_flags.append('performance_fail')
      #  jump end
      # To get less than $500 on the first day, you need to get 3 incorrect tasks.
      if (store.game_state.day == 0) and store.game_state.time == 'end' and store.game_state.performance['earnings'] <= 500 and not no_fail:
        $ store.event_flags.append('tutorial_fail')
        jump end
      if (store.game_state.time == "end"):
        python:
          # Deduct rent from earnings
          if (store.game_state.day != 0):
            store.game_state.performance['earnings_minus_rent'] -= (store.daily_rent * store.game_state.day)
            renpy.hide_screen('overlay_earnings')
            renpy.show_screen('overlay_earnings', rent_loss_flag = True)
          # print('earnings minus rent: ', store.game_state.performance['earnings_minus_rent'])
          # Bank acount is in the red
          if store.game_state.performance['earnings_minus_rent'] <= 0 and store.game_state.day < 4:
            store.event_flags.append('rent_fail')
        $ emojis = emoji_selection(store.game_state.performance, store.averages['day_' + str(store.game_state.day)])
        show screen performance(store.game_state.performance, store.averages['day_' + str(store.game_state.day)], emojis)
        # $ print('interstitial_performance_feedback', performance_feedback(store.game_state.performance_rating)['text'])
        # hide and showing cogni again due to CPS text behavior
        hide screen cogni
        show screen cogni(None, char_map['cogni']['mood']['default'], position = "bottom_left")
        $ render_message(char_map['cogni']['obj'].name, char_map['cogni']['obj'].who_suffix, performance_feedback(store.game_state.performance_rating)['text'], char_map['cogni']['mood']['default'], position = "bottom_left", overlay=True)
        hide screen cogni
        call screen cogni_leave(char_map['cogni']['mood']['default'], "bottom_left", hide_bubble = True)
        if 'rent_fail' in store.event_flags and not no_fail:
          # $ print('hitting rent fail state')
          jump end 
      
        hide screen performance
      # FEEDBACK FROM MANAGER
        #NEW UI STATE
        $ cleaned = clean(store.apartment_data)
        while cleaned['message']:
          python:
            message = cleaned['message'].pop(0)
            n = 120
            text = message['text']
            split = split_into_sentences(text)
            length = len(split)
            count = 0
          while count < length:
            python:
              buttons = None
              if count >= length - 1:
                if 'button_1_text' in message:
                  buttons = [message['button_1_text']]
                if 'button_2_text' in message:
                  buttons.append(message['button_2_text'])
                second_sentence = ""
              else:
                buttons = []
                second_sentence = split[count+1]
            # show screen message(message['sender'], buttons)
            $ text = f"{split[count]} {second_sentence}"
            $ sender = char_map[message['sender']]  
            $ start_speaker = (not count) and (prev_speaker != message['sender'])
            $ end_speaker = (count == length - 1) and (next_message_set['sender'] != message['sender'])
            # $ print('interstitial_message', sender['obj'].name, sender['obj'].who_suffix, text, sender['mood']['default'], start_speaker, end_speaker)
            $ render_message(sender['obj'].name, sender['obj'].who_suffix, text, sender['mood']['default'], start = start_speaker, end = end_speaker)
            $ count += 2
      
      hide screen overlay
      hide screen overlay_earnings
      $ aberate_layer('all', 0)

      if store.game_state.day < 4:
        if store.game_state.time == "end":
            $ fade_into_dream(2.0)
            $ dream_counter = 0
            $ dream_data = filter_dreams(store.apartment_data['dream'])
            $ dream_len = len(dream_data)
            while dream_counter < dream_len:
                $ dream = dream_data[dream_counter]
                if dream['time'] != 'start':
                    call screen dream(dream['text'], dream['buttons'])
                $ dream_counter += 1
            $ fade_out_of_dream(0.5)
      
      #this is where the next day should start

      if store.game_state.day < 4:
        if store.game_state.time == "end":
          $ day_start()
          python:
            notes = shuffle_notes(clean(store.apartment_data)['sticky_note'])
            random_scribble_base = list(range(1, 9))[0:4]
            for i in range(0, 4):
              notes[i]['image'] = f"scribble_base_{random_scribble_base[i]}"
          if store.game_state.performance_rating != 'bad':
              play music f"dataville_apartment_{store.game_state.performance_rating}.ogg" loop
          else:
              play music f"dataville_apartment_bad.ogg" loop fadein 2.0
          call screen apartment(clean(store.apartment_data), store.game_state.time, apartment_bg_map['apartment_1'], notes)
          if store.game_state.performance_rating != 'bad':
              play music f"dataville_workspace_{store.game_state.performance_rating}.ogg" loop
          else:
              play music f"dataville_workspace_bad.ogg" loop fadein 2.0
          $ task = store.loop["start_task"]
          $ set_ui_state(task, store.game_state)
          $ cleaned = clean(store.apartment_data)
          $ show_computer_screen(store.game_state.ui)
          $ fee_text = f"Your combined fees and rent are ${store.daily_rent * store.game_state.day}. Make sure your earnings exceed this number!"
          # $ print('interstitial_fee_text', fee_text)
          $ render_message(char_map['cogni']['obj'].name, char_map['cogni']['obj'].who_suffix, fee_text, char_map['cogni']['mood']['default'], position = "center", start= True, end = True)
          call task_loop from _call_task_loop_1
        else:
          "game state is broken!!!"
      else:
        jump end
    label end:
      hide screen overlay
      hide screen overlay_earnings
      hide screen performance
      hide screen cogni
      $ aberate_layer('all', 0)
      play music "datavilleoutro.ogg" loop
      scene bg black_bg with Dissolve(3.0)
      
      # testing purposes / tests all epilogue screens
      # $ epilogues = test_all_epilogues()
      # $ epi_len = len(epilogues)
      # $ epi_counter = 0
      # while epi_counter < epi_len:
      #   $ split = split_into_sentences(epilogues[epi_counter]["text"])
      #   $ count = 0
      #   $ length = len(split)
      #   hide screen dream
      #   $ renpy.show(epilogues[epi_counter]["image"], layer="master", at_list=[fade_in(1.0)])
      #   pause 1.0
      #   while count < length:
      #     python:
      #       if count <= length -2:
      #         additional_text = split[count+1]
      #       else:
      #         additional_text = ""
      #     call screen epilogue(f"{split[count]} {additional_text}")
      #     $ count += 2
      #   call screen epilogue('Thank you for playing DataVille!\na more human world\none click at a time', ['Restart'])
      #   $ epi_counter += 1
      # call screen epilogue('End of Tests', ['Restart'])
      # jump start

      $ epilogue = get_epilogue()
      $ split = split_into_sentences(epilogue["text"])
      # $ print('epilogue variable: ', epilogue)
      # $ print('split text: ', split)
      $ count = 0
      $ length = len(split)
      # scene bg apartment_bg with Dissolve(1.0) 
      # $ blur_master()
      hide screen dream
      $ renpy.show(epilogue["image"], layer="master", at_list=[fade_in(1.0)])
      pause 1.0
      while count < length:
        python:
          if count <= length -2:
            additional_text = split[count+1]
          else:
            additional_text = ""
          # print('epilogue text: ', split[count])
        call screen epilogue(f"{split[count]} {additional_text}")
        $ count += 2
      call screen epilogue('Thank you for playing DataVille!\na more human world\none click at a time', ['Return to Main Menu'])
      hide screen epilogue
      $ MainMenu(confirm=False)()
      # This ends the game.
      # clear store and return to start
      # if we want to send them to the main menu
      # jump start
