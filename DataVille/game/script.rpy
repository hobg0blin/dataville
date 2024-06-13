
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
  # image cogni_sprite = "images/characters/cogni/cogni_happy.png"

  define supervisor = Character("Alex T.", image="images/characters/alex/alex_neutral.png", who_suffix = "Senior Managaer @ Dataville", kind=email_message)
  # cogni defined in characters/cogni.rpy
  define stranger = Character("$(#@^%)$)(#)%$@^*$(*)", image="images/characters/stranger.png", who_suffix = "?*#$&#*@()%&@)%&$@^)($#)", kind=email_message)
  define union = Character("Tim", image="images/characters/union.png", who_suffix = "Union Rep. Section 18, Cohort 48", kind=email_message)
  define news_anchor = Character("News Anchor", image="images/news_anchor.jpg", window_style="window_wbox")
  define victor = Character("Victor", image="images/victor.avif", window_style="window_wbox") 

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
        "default": "images/characters/cogni/cogni_happy.png",
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
    "union": {
      "obj": union,
      "mood": {
        "default": "images/characters/union.png"
      }
    },
  }

transform blur:
  blur 30
    
transform unblur:
  blur 0

# The game starts here.
default skip_intro = True
default start_at_day_end = False
label start:
    if not skip_intro:
      play music "dataville_workspace_neutral.wav" fadein 2.0
      image bg start_screen = im.FactorScale("images/intro_desk.jpg", 1.5)
      image bg overlay_background = "images/screens/monitor/background.png"
      image bg black_bg = Solid('#FFFFFF')


      # v2 sequence
      image intro_01 = "images/screens/01-intro/intro-01.png"
      image intro_02 = "images/screens/01-intro/intro-02.png"
      image bg gray_bg = Solid('#464645')
      image bg news_bg = "images/news_bg.png"
      image bg apartment_bg = "images/apartment/apartment3_1.png"

      image zoom_seq:
        xoffset 205
        "images/screens/01-intro/title-into-trans.png"
        pause 1.2
        parallel:
          easeout_quad 3 xoffset 0
        # "images/screens/01-intro/intro-00.png"
        parallel:
          easeout_quad 3 zoom 1.5
        parallel:
          easeout_quad 3 yoffset config.screen_height/3.5

      scene bg gray_bg
      show zoom_seq
      $renpy.pause(4, hard=True)
      show intro_01 with Dissolve(1.0)
      pause
      show intro_02 with Dissolve(0.2)
      pause
      scene bg news_bg
      # show standard dialogue box - only for news chyrons
      # $ show_window = True
      news_anchor "Good evening, and welcome to our program."
      news_anchor "Tonight, hiding in the shadows. What the alien menace means for you and your family. I’m joined by Victor Willmington, founder and CEO of the Dataville Corporation. "
      news_anchor "Tell me Victor, how does your company see the ongoing alien migratory crisis?"
      victor "Where you see a crisis, we at Dataville see an opportunity. This is our chance to restore human society to a safer, simpler time."
      victor "With our patented alien identification AI technology, we’re able to accurately penetrate alien camouflage."
      news_anchor "And you’ve found active partners in the public sector?"
      victor "That’s right. Our clients include the Departments of Defense and State, as well as private enterprises looking to ensure their communities are 100 percent human."
      news_anchor "And what do you say to your critics who accuse the Dataville Corporation of exacerbating racial tensions with the aliens?"
      victor "Earth was meant for humans. If they have nothing to hide, why are they using camouflage?"
      $ blur_master()
      image job_page = "images/job_page.png"
      scene job_page
      call screen job_offer(1)
      call screen job_offer(2)
      scene bg gray_bg
      call screen dream("\n Looking for a job? Looking to make the world a better, more human place?", ["Take the quiz!"])
      call screen dream("Are you proud of your humanity?", ["Yes", "No"])
      call screen dream("Do you own a computer?", ["Yes", "No"])
      call screen dream("Are you interested in working from home?", ["Yes", "No"])
      call screen dream("Congratulations! We'd like to extend an offer of employment! Join the DataVille team now.", ["Let's get started."])
      $ unblur_master()

      label intro:
  #      manual stuff for game start
#        image bg apartment_1 = im.FactorScale("images/room/room/room_" + store.apartment_data["apartment_background"] + ".jpg", 1.5)
        # scene bg black_bg

#        $ blur_master()
#        
#        $ dream_counter = 0
#        $ dream_len = len(store.apartment_data['dream'])
#        while dream_counter < dream_len:
#          $ dream = store.apartment_data['dream'][dream_counter]
#          if dream['time'] == 'start':
#              call screen dream(dream['text'], dream['buttons'])
#          $ dream_counter += 1
#
#        $ unblur_master()
#
#        image desk_overhead = "images/desk_overhead.png"
#        scene desk_overhead
#        pause
#
#        
#
#
        image bg apartment_1 = "images/apartment/apartment3_1.png"
#        
        scene bg apartment_1
        play music "dataville_apartment_neutral.wav"
        call screen apartment(clean(store.apartment_data), store.game_state.time)
        hide screen apartment
      # hide dialogue box
      # $ show_window = False
      scene bg apartment_bg with Dissolve(1.0)

      $ blur_master()
      call screen dream("Your first day at a new job.", [])
      call screen dream("Try not to screw it up.", [])
      call screen dream("You really need the money.", [])
      call screen dream("Let's get started.", [])
      $ unblur_master()
    python:
      if start_at_day_end:
          day_end()
    if store.game_state.time == "end":
        jump interstitial

    play music "dataville_workspace_neutral.wav" fadein 2.0
    
    # if store.game_state.day == 0:
    #     show dataville_intro
    #     pause
    #     show hiring_detail
    #     pause


  # manually check messsages on first loop 
    $ cleaned = clean(store.apartment_data)
    show screen overlay (store.game_state.ui)
    scene bg overlay_background
    label check_messages:
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
            strip_message = split[count].strip()
            print('stripped message: ', strip_message)
            if count >= length - 1:
              buttons = message['buttons']
              second_sentence = ""
            else:
              buttons = []
              second_sentence = split[count+1]
          if strip_message != "" and strip_message != "\n":
            # show screen message(message['sender'], buttons)
            $ sender = char_map[message['sender']]
            # ONLY SHOWING ONE LINE DURING INTRO: I THINK THIS HAS THE LONGEST TEXT
            $ text =  f"{split[count]}"
            $ render_message(sender['obj'].name, sender['obj'].who_suffix, f"[text]", sender['mood']['default'])
          $ count += 1
  #manually set task & variables for first loop
    $ time = store.game_state.ui['timer']

    python:
      if len(task_string) > 0:
        task = store.loop[task_string]
      else:
        task = store.loop["start_task"]
      set_ui_state(task, store.game_state)


#THIS AUTOMATES GOING THROUGH TASKS WHEN INSTRUCTIONS/ETC. ARE UNNECESSARY
    label task_loop:
      scene bg overlay_background
      # $ show_window = False
      show screen overlay (store.game_state.ui)
      if store.game_state.day != 0 and len(cleaned['message'])>0:
        while cleaned['message']:
          python:
            message = cleaned['message'].pop(0)
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
            $ render_message(sender['obj'].name, sender['obj'].who_suffix, f"[text]", sender['mood']['default'])
            $ count += 1
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
        $ render_message(sender['obj'].name, sender['obj'].who_suffix, custom_dialogue, sender['mood']['default'])
        # show screen message(task['custom_dialogue_sender'], ["Next"])
        # window hide
        # cogni "[custom_dialogue]"
        # hide screen message


      show screen timer
      show screen instructions(store.game_state.ui)
      $ custom_feedback = ""
      $ custom_feedback_sender = ""
      $ has_custom_feedback = False
      $ task_type = task['type']
      $ task_error = False
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
                if 'ethical_options' in task:
                    print('hit ethical task: ', task)
                    ethical = task['ethical_options']
                    if 'custom_feedback_ethical' in task and latest_choice == ethical:
                        print('should be showing ethical custom feedback')
                        custom_feedback = task['custom_feedback_ethical'] 
                    if 'custom_feedback_correct' in task and latest_choice == correct:
                        print('should be showing correct custom feedback')
                        custom_feedback = task['custom_feedback_correct'] 
                    custom_feedback_sender = char_map[task['custom_feedback_sender']]
                    has_custom_feedback = True
                task = update_state(store.game_state, binary_correct, task)
        else:
            binary_correct = 1
            task = update_state(store.game_state, binary_correct, task)


      hide screen instructions
      hide screen timer
      hide screen task_type
      hide screen cogni
      show screen overlay (store.game_state.ui)
      if has_custom_feedback:
        $ print('has custom feedback')
        $ render_message(custom_feedback_sender['obj'].name, custom_feedback_sender['obj'].who_suffix, custom_feedback, custom_feedback_sender['mood']['default'])
        # show screen message(custom_feedback_sender, [f"{custom_feedback_sender}"])
        # window hide
        hide screen message 
      #show screen overlay (store.game_state.ui, True)
      if (task == 'break'):
        $ day_end()
        call interstitial from _call_interstitial
      else:
        call task_loop from _call_task_loop
      return

    # INTERSTITIAL
    label interstitial:
      hide screen instructions
      scene bg overlay_background
      show screen overlay (store.game_state.ui)
      # fail states for not making rent, failing the tutorial, or being bad at the game
      $ store.game_state.performance_count[store.game_state.performance_rating] += 1
      if store.game_state.performance_count['bad'] >= 3:
        $ store.event_flags.append('performance_fail')
        jump end
      if (store.game_state.day == 0) and store.game_state.time == 'end' and store.game_state.performance['earnings'] < 600:
        $ store.event_flags.append('tutorial_fail')
        jump end
      if (store.game_state.time == "end"):
        show screen performance(store.game_state.performance, store.averages['day_' + str(store.game_state.day)])
        show screen cogni(performance_feedback(store.game_state.performance_rating)['text'], char_map['cogni']['mood']['default'], "bottom_left") 
        pause
        python:
          print('earnings: ', store.game_state.performance['earnings_minus_rent'])
          if (store.game_state.day != 0):
            store.game_state.performance['earnings_minus_rent'] -= (store.daily_rent * store.game_state.day)
          print('earnings minus rent: ', store.game_state.performance['earnings_minus_rent'])
          if store.game_state.performance['earnings_minus_rent'] <= 0:
            store.event_flags.append('rent_fail')
        if 'rent_fail' in store.event_flags:
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
              if count >= length - 2:
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
            $ render_message(sender['obj'].name, sender['obj'].who_suffix, f"[text]", sender['mood']['default'])
            $ count += 2
            # window hide
            # hide screen message
#      else:
      hide screen overlay
      scene bg apartment_1
      play music f"dataville_apartment_{store.game_state.performance_rating}.wav" fadein 2.0
      # $ show_window = True
      call screen apartment(clean(store.apartment_data), store.game_state.time)
      # $ show_window = False
      if store.game_state.day < 4:
        if store.game_state.time == "end":
            scene bg black_bg
            $ dream_counter = 0
            $ dream_len = len(store.apartment_data['dream'])
            hide screen apartment
            scene bg apartment_bg with Dissolve(1.0)
            $ blur_master()
            while dream_counter < dream_len:
                $ dream = store.apartment_data['dream'][dream_counter]
                if dream['time'] != 'start':
                    call screen dream(dream['text'], dream['buttons'])
                $ dream_counter += 1
            $ unblur_master()
            python:
                # reset_performance(store.game_state.performance)
                day_start()
            if store.game_state.performance_rating != 'bad':
                play music f"dataville_workspace_{store.game_state.performance_rating}.wav" fadein 2.0
            else:
                play music f"dataville_workspace_neutral.wav" fadein 2.0
            $ task = store.loop["start_task"]
            $ set_ui_state(task, store.game_state)
            $ cleaned = clean(store.apartment_data)

            call task_loop from _call_task_loop_1
        else:
          "game state is broken!!!"
      else:
        jump end
    label end:
      scene bg gray_bg with Dissolve(1.0)
      $ epilogue = get_epilogue()
      $ split = split_into_sentences(epilogue)
      $ print('epilogue variable: ', epilogue)
      $ print('split text: ', split)
      $ count = 0
      $ length = len(split)
      scene bg apartment_bg with Dissolve(1.0) 
      $ blur_master()

      while count < length:
        python:
          if count <= length -2:
            additional_text = split[count+1]
          else:
            additional_text = ""
          print('epilogue text: ', split[count])
        call screen dream(f"{split[count]} {additional_text}", [])
        $ count += 2
      call screen dream('Thank you for playing DataVille!\na more human world\none click at a time', ['Restart'])
      # This ends the game.
      hide screen dream
      # clear store and return to start
      $ set_initial_variables() 
      # if we want to send them to the main menu:
      #MainMenu(confirm=False)

      jump start
      #return



