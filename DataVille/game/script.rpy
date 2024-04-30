# The s]cript of the game goes in tcustom_feedbacup file performance.

# Declare characters used by this game. The color argument colorizes the
# name of the character.
# Timer stuff from https://www.reddit.com/r/RenPy/comments/olfuk8/making_a_timer/
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
# switch to control showing dialogue box background
  default show_window = False

# in style window

  image alien_human_family = "alien_human_family.png"
  image dark_green = Solid("#136366")
  image bg black = Solid("#000000")
  image supervisor = "images/icons/supervisor.png"
  image cogni = "images/icons/asst_normal.png"
  image side supervisor = "images/icons/supervisor.png"
  define e_big = Character("", image="supervisor", kind=bubble)
  define custom_feedback_speaker = Character("", image="cogni", kind=bubble)
  define news_anchor = Character("News Anchor", image="images/news_anchor.jpg")
  define victor = Character("Victor", image="images/victor.avif")
##ALL THE PYTHON SETUP GOES HERE
init python:
  import random
  import csv
  from types import SimpleNamespace
  import re
  import operator
  import os
  from textwrap import wrap
  import re
  alphabets= "([A-Za-z])"
  prefixes = "(Mr|St|Mrs|Ms|Dr)[.]"
  suffixes = "(Inc|Ltd|Jr|Sr|Co)"
  starters = "(Mr|Mrs|Ms|Dr|Prof|Capt|Cpt|Lt|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)"
  acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
  websites = "[.](com|net|org|io|gov|edu|me)"
  digits = "([0-9])"
  multiple_dots = r'\.{2,}'

  def split_into_sentences(text: str) -> list[str]:
    """
    Split the text into sentences.

    If the text contains substrings "<prd>" or "<stop>", they would lead 
    to incorrect splitting because they are used as markers for splitting.

    :param text: text to be split into sentences
    :type text: str

    :return: list of sentences
    :rtype: list[str]
    """
    text = " " + text + "  "
    text = text.replace("\n"," ")
    text = re.sub(prefixes,"\\1<prd>",text)
    text = re.sub(websites,"<prd>\\1",text)
    text = re.sub(digits + "[.]" + digits,"\\1<prd>\\2",text)
    text = re.sub(multiple_dots, lambda match: "<prd>" * len(match.group(0)) + "<stop>", text)
    if "Ph.D" in text: text = text.replace("Ph.D.","Ph<prd>D<prd>")
    text = re.sub("\s" + alphabets + "[.] "," \\1<prd> ",text)
    text = re.sub(acronyms+" "+starters,"\\1<stop> \\2",text)
    text = re.sub(alphabets + "[.]" + alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>\\3<prd>",text)
    text = re.sub(alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>",text)
    text = re.sub(" "+suffixes+"[.] "+starters," \\1<stop> \\2",text)
    text = re.sub(" "+suffixes+"[.]"," \\1<prd>",text)
    text = re.sub(" " + alphabets + "[.]"," \\1<prd>",text)
    if "”" in text: text = text.replace(".”","”.")
    if "\"" in text: text = text.replace(".\"","\".")
    if "!" in text: text = text.replace("!\"","\"!")
    if "?" in text: text = text.replace("?\"","\"?")
    text = text.replace(".",".<stop>")
    text = text.replace("?","?<stop>")
    text = text.replace("!","!<stop>")
    text = text.replace("<prd>",".")
    sentences = text.split("<stop>")
    sentences = [s.strip() for s in sentences]
    if sentences and not sentences[-1]: sentences = sentences[:-1]
    return sentences

  store.drags = {}
  store.loop = {}
  # CONSTANTS FOR PERFORMANCE COMPARISON
  store.averages = {
      'day_0': {
        'score': 70,
        'time': 8,
        'earnings': 1200
        },
      'day_1': {
        'score': 70,
          'time': 8,
        'earnings': 2400
        },
      'day_2': {
          'score': 70,
          'time': 8,
        'earnings': 3600
        },
      'day_3': {
          'score': 70,
          'time': 8,
        'earnings': 4800
        },
      'day_4': {
        'score': 70,
        'time': 8,
        'earnings': 6000
        },
    }
# these should only be updated after a game loop
  store.game_state = {}
# STATE TRACKING VARIABLES
  store.event_flags = []
  store.game_state.time = 'start'
  store.game_state.day = -1
  store.game_state.performance_rating = 'neutral'
  store.game_state.task_count = 0
  store.apartment_file = ""


  store.game_state.ui = {
        "news_headline": "",
        "news_body":"",
        "past_news_stories": [],
        "earnings": 0,
        "performance": "",
        "instructions": "", 
        "timer": 10
      }
  store.game_state.performance = {
        "earnings": 0,
        "average_time": 0,
        "total_time": 0,
        "total_score": 0,
        "approval_rate": 0,
      }

  store.apartment_data = {"apartment_background": "1", "sticky_note": [], "message": [], "news": [], "window_background": "images/room/window_content/default_window_bg.jpg", "button_text": "Go to work!", "dream": []}

  # set default image ordering
  store.order = [3,2,1]
# DEFAULT TIMER VARIABLES
  timer_range = 0
  time = 0
  timer_jump = ''
  def update_from_state_menu():
    if (day_string and len(day_string) > 0):
      store.game_state.day = int(day_string) - 1
      day_start()
    if (task_string and len(task_string) > 0):
      task = store.loop[task_string]
      set_ui_state(task, store.game_state)
    else:
        task = store.loop["start_task"]
    if (time_string and len(time_string) > 0):
        store.game_state.time = time_string
    if (performance_string and len(performance_string) > 0):
        store.game_state.performance_rating = performance_string
    if (event_flag_string and len(event_flag_string) > 0) and event_flag_string not in store.event_flags:
        print('adding event flag: ', event_flag_string)
        store.event_flags.append(event_flag_string)


# CSV PARSING FOR TASK LOOPS AND APARTMENT STATE
  def get_order(label):
    num_match = re.search(r'[0-9]+', label)
    num_str = num_match.group()
    return num_str
# STATE FUNCTIONS
# set tasks from CSV
  def make_task_loop(filename, loop):
      with open(renpy.loader.transfn(filename), 'r') as current_loop:
          reader = csv.DictReader(current_loop)
          # each row in CSV becomes attribute in "loop" dict
          for row in reader:
            loop[row['task_id']] = {}
            for k,v in row.items():
                if not v or k == 'task_id':
                    continue;
                elif 'label' in k:
                    #HANDLE TEXT LABELING
                    order = get_order(k)
                    if not loop[row['task_id']].has_key('labels'):
                        loop[row['task_id']]['labels'] = {}
                    if not loop[row['task_id']]['labels'].has_key(order):
                        loop[row['task_id']]['labels'][order] = {}
                    if not loop[row['task_id']]['labels'][order].has_key('ypos'):
                        loop[row['task_id']]['labels'][order]['ypos'] = 0
                    if 'id' in k:
                        loop[row['task_id']]['labels'][order]['name'] = v
                    if 'text' in k:
                        loop[row['task_id']]['labels'][order]['text'] = v
                        
                elif 'correct_images' in k:
                    #SPLIT IMAGE LIST
                    correct_images = [x.strip(' ') for x in v.split(',')]
                    loop[row['task_id']][k] = correct_images 
                else:
                    #OTHERWISE, SET ATTRIBUTE ON MAIN LOOP OBJECT
                    loop[row['task_id']][k] = v

  def reset_performance(performance):
    for k in performance: performance[k] = 0
  
# PULL APARTMENT STATE FROM CSV
  def get_apartment_image(folder, file):
    return f"images/room/{folder}/{file}"

  def update_apartment_state(filename, apartment, game_state):
    store.apartment_data = {"apartment_background": "1", "sticky_note": [], "news": [], "message": [], "window_background": "images/room/window_content/default_window_bg.jpg", "button_text": "Go to work!", "dream": []}
    messages = []
    with open(renpy.loader.transfn(filename), 'r') as current_file:
      reader = csv.DictReader(current_file)
      for row in reader:
        story_object = {}
        if row['TYPE'] == "":
          return
        story_object['performance'] = row['PERFORMANCE']
        story_object['time'] = row['TIME']
        if len(row['BUTTON_1_TEXT']) > 0:
            story_object['buttons'] = [row['BUTTON_1_TEXT']]
        else:
            story_object['buttons'] = None
        if len(row['BUTTON_2_TEXT']) > 0:
            story_object['buttons'].append(row['BUTTON_2_TEXT'])
        if 'EVENT_FLAG' in row:
          story_object['event_flag'] = row['EVENT_FLAG']
        if row['TYPE'] == 'dream':
            story_object['text'] = row['TEXT']
        if row['TYPE'] == 'message':
          story_object['text'] = row['TEXT']
          story_object['sender'] = row['SENDER']
        elif row['TYPE'] == 'news':
          story_object['text'] = row['TEXT']
#          story_object['image'] = row['IMAGE']
#          #FIXME: PLACEHOLDER IMAGE
          if 'IMAGE' in row and len(row['IMAGE']) > 0:
            story_object['image'] = get_apartment_image(row['IMAGE_FOLDER'], row['IMAGE'])
          else:
            story_object['image'] = "images/placeholder.png"
        elif row['TYPE'] == 'sticky_note':
          story_object['text'] = row['TEXT']
        apartment_data[row['TYPE']].append(story_object) 

# remove items from apartment state when conditions aren't met (e.g. performance and event flags)
  def clean(apartment):
    output = {}
    for k in apartment:
      if isinstance(apartment[k], list):
        filtered = filter(filter_apartment, apartment[k])
        output[k] = list(filtered)
      else:
        output[k] = apartment[k]
    return output

  def filter_apartment(obj):
    if store.game_state.time != obj['time']:
      return False
    elif obj['performance'] == store.game_state.performance_rating:
      return True
    elif obj['performance'] == 'default':
      return True
    elif obj['performance'] == 'flag_dependent' and 'event_flag' in obj and obj['event_flag'] in store.event_flags:
      return True
    else:
      return False
    #SET TV NEWS ITEMS
  def setitem(data, index):
    length = len(data["news"])
    if index > length - 1:
        index = 0
    item = data["news"][index]
    if item["performance"] != "default" and item["performance"] != store.game_state.performance_rating and item["event_flag"] not in store.event_flags:
        index +=1
        return setitem(data, index)
    else:
        return [item, index]


#
# UPDATE STATE BASED ON TIME CHANGE
  def day_start():
    store.game_state.day += 1
    day = str(store.game_state.day)
    store.game_state.time = 'start'
    make_task_loop('game_files/tasks_day_' + day + '.csv', store.loop) 
    update_apartment_state('game_files/apt_day_' + day + '.csv', store.apartment_data, store.game_state)

  def day_end():
    store.game_state.time = 'end'
    day = str(store.game_state.day)

  day_start()
  task = store.loop['start_task']


 # update state with "outcomes" attribute from current loop, based on
 # performance. should always take the form of {1: (BEST OUTCOME), 2: (MEDIUM
 # OUTCOME), 3: (WORST OUTCOME)}
 # TODO: account for "ethical" vs. "correct" result
 # SCORING FUNCTIONS

  def performance_feedback(out):
      good = ["You’re really doing it!", "You’re labeling faster than 81% of DataVille Annotators!", "Great accuracy!", "Keep it up!", "Aim for that performance incentive!"]
      mid = ["Your performance is reasonable", "Your output is compatible with 70% of other labelers."]
      bad = ["Accuracy is important. Don’t be afraid to look carefully!", "Oof. Hope you do better next time.", "You’ll need to do better if you want the incentive bonus!", "Stay focused.", "That wasn’t great - do you need clearer instructions?"]
      if (out == 1):
        return {'text': random.choice(good), 'score': 100}
      elif (out == 2):
        return {'text': random.choice(mid), 'score': 66}
      else:
        return {'text': random.choice(bad), 'score': 33}
  def check_dependencies(dependencies, next_task):
    for dependency in dependencies:
        cleaned_dep = dependency.strip()
        if cleaned_dep not in store.event_flags:
            if next_task != 'break':
                if next_task['next_task'] == 'break': 
                    set_performance_rating()
                    next_task = 'break'
                else:
                    next_task = store.loop[next_task['next_task']]
                    if ('event_flag_dependency' in next_task):
                        next_task = check_dependencies(next_task['event_flag_dependency'].split(','), next_task)
        else:
            print("dependency in event flags: ", cleaned_dep)
            next_task = next_task
    return next_task

  def set_performance_rating():

    if (store.game_state.performance['approval_rate'] > store.averages['day_' + str(store.game_state.day)]['score']):
      store.game_state.performance_rating = "good"
    elif (store.game_state.performance['approval_rate'] == store.averages['day_' + str(store.game_state.day)]['score']):
      store.game_state.performance_rating = "neutral"
    else:
      store.game_state.performance_rating = "bad"

# update task after it's scored, update state with scores
  def update_state(state, out, current_task):
# ADD ANY EVENT FLAGS
    is_ethical = check_ethical(latest_choice, current_task)
    if is_ethical and 'ethical_choice_event_flag' in current_task:
      store.event_flags.append(current_task['ethical_choice_event_flag'])
    if store.latest_score == 1 and 'correct_choice_event_flag' in current_task:
      store.event_flags.append(current_task['correct_choice_event_flag'])
# HANDLE NEXT TASK LOGIC
    if (current_task['next_task'] == 'break'):
      set_performance_rating()
      next_task = 'break'
    else:
      next_task = store.loop[current_task['next_task']]
    #if event flag dependency isn't met, skip task
      if ('event_flag_dependency' in next_task):
        print('task has event flag dependency: ', next_task)
        print('current event flags: ', store.event_flags)
        dependencies = next_task['event_flag_dependency'].split(',')
        next_task = check_dependencies(dependencies, next_task)
        print('next task: ', next_task)
 # UPDATE UI VARIABLES 
    reward = int(current_task['payment'])/out

    performance = performance_feedback(out)
    performance_text = performance['text']
    #SCORING
    store.game_state.task_count += 1
    store.game_state.performance['total_score'] = (store.game_state.performance['total_score'] + performance['score'])
    store.game_state.performance['approval_rate'] = (store.game_state.performance['total_score']/store.game_state.task_count)
    # TIME TRACKER
    store.game_state.performance['total_time'] = (store.game_state.performance['total_time'] + (10 - time))    
    store.game_state.performance['average_time'] = (store.game_state.performance['total_time'] /store.game_state.task_count)    
    return set_ui_state(next_task, state, performance_text, reward)

  def set_ui_state( task, state, performance_text = '', reward = 0):
    print('task: ', task)
    state.ui['performance'] = performance_text
    state.ui['earnings'] += reward
    state.performance['earnings'] += reward
    if task == 'break':
      return task
    else:
      state.ui['instructions'] = task['instructions']
      state.ui['timer'] = int(task['time'])
      return task

  def get_epilogue():
    output = ""
    with open(renpy.loader.transfn('game_files/epilogues.csv'), 'r') as epilogues: 
        reader = csv.DictReader(epilogues)
        for epilogue in reader:
            if len(epilogue['event_flag']) <= 0:
                if epilogue['performance'] == store.game_state.performance_rating:
                    output = epilogue['text']
                    print('setting default event flag: ', output)
            else:
                for event_flag in store.event_flags: 
                    print('store event flag: ', event_flag)
                    print('epilogue event flag: ', event_flag)
                    if event_flag == epilogue['event_flag'] and epilogue['performance'] == store.game_state.performance_rating:
                        output = epilogue['text']
                        print('event flag based epilogue firing: ', epilogue)
    print('epilogue output: ', epilogue)

    return output


# IMAGE TASK FUNCTIONS
# default captcha image variables
  images_correct = False
  start_x_image = 100
  start_y_image = 300
  start_x_text = 100
  start_y_text = 300
  # timer stuff
  order = 1
  # could use periodic function to constantly update box position
  # also look at "cardgame" or "puzzle" templates, although they seem like overkill
  # easiest is slotting them into order in separate window, probably
  def get_images(task):
      images = []
      for imagepath in (renpy.list_files()):
         if imagepath.startswith("images/" + "set" + str(store.game_state.day) + "/" + task['image_folder']) :
            images.append(imagepath)
      return images

  images_selected = {'values': []}

  # TODO: highlight/frame selected images
  def select_image(image):
    if image not in images_selected['values']:
      images_selected['values'].append(image)
    else:
      images_selected['values'].remove(image)
    return None


  # dumb comparison of images that just returns true or false
  # should probably be percentile graded but we prototyping baby
  def check_images(selected, original):
    if sorted(selected['values']) == sorted(original):
      return 1
    else:
      return 3

  def check_binary(value, task):
      if value == task['correct_options']:
          return 1
      else:
          return 3

  def check_ethical(value, task):
    if 'ethical_options' in task:
      if value == task['ethical_options']:
        return True
      else:
        return False
    else:
      return False

# TEXT ORDERING FUNCTIONS (currently not in use because buggy)
  def drag_log(drags, drop):
    # needs to have droppable enabled, i guess?
    # if drop:
    for d in task['labels'].values():
        if d['name'] == drags[0].drag_name:
            d['ypos'] = drags[0].y

  def check_order_text(task):
    sort_labels = sorted(task['labels'].items(), key=lambda x: x[1]['ypos'])
    # set order defined in text_label_task object
    order = [int(i[0]) for i in sort_labels]
    if order == [1, 2, 3]:
      case = 1
    elif order == [2, 1, 3]:
      case = 2
    else:
      case = 3
    return case

  def blur_master():
    renpy.show_layer_at(blur)
    renpy.with_statement({'master' : Dissolve(0.15)})
  
  def unblur_master():
    renpy.show_layer_at(unblur)
    renpy.with_statement({'master' : Dissolve(0.15)})


transform blur:
  blur 30
    
transform unblur:
  blur 0

# The game starts here.
default skip_intro = False
default start_at_day_end = False
label start:
    if not skip_intro:
      play music "dataville_apartment_neutral.wav"
      image bg start_screen = im.FactorScale("images/intro_desk.jpg", 1.5)
      image bg overlay_background = Solid('#EFF3E6')
      image bg black_bg = Solid('#FFFFFF')


      # v2 sequence
      image intro_01 = "images/screens/01-intro/intro-01.png"
      image intro_02 = "images/screens/01-intro/intro-02.png"
      image bg gray_bg = Solid('#464645')
      image bg news_bg = "images/news_bg.png"

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
      $ show_window = True
      news_anchor "Good evening, and welcome to our program."
      news_anchor "Tonight, hiding in the shadows. What the alien menace means for you and your family. I’m joined by Victor Willmington, founder and CEO of the Dataville Corporation. "
      news_anchor "Tell me Victor, how does your company see the ongoing alien migratory crisis?"
      victor "Where you see a crisis, we at Dataville see an opportunity. This is our chance to restore human society to a safer, simpler time."
      victor "With our patented alien identification AI technology, we’re able to accurately penetrate alien camouflage."
      news_anchor "And you’ve found active partners in the public sector?"
      victor "That’s right. Our clients include the Departments of Defense and State, as well as private enterprises looking to ensure their communities are 100 percent human."
      news_anchor "And what do you say to your critics who accuse the Dataville Corporation of exacerbating racial tensions with the aliens?"
      victor "Earth was meant for humans. If they have nothing to hide, why are they using camouflage?"

      scene bg gray_bg with Dissolve(1.0)
      call screen dream("You have a message from the DataVille corporation. /n Looking for a job? Looking to make the world a better, more human place?", ["Take the quiz!"])
      call screen dream("Are you proud of your humanity?" ["Yes", "No"])
      call screen dream("Do you own a computer?" ["Yes", "No"])
      call screen dream("Are you interested in working from home?" ["Yes", "No"])
      call screen dream("Congratulations! We'd like to extend an offer of employment! Join the DataVille team now.", ["Let's get started."])

      label intro:
  #      manual stuff for game start
  #      image bg apartment_1 = im.FactorScale("images/room/room/room_" + store.apartment_data["apartment_background"] + ".jpg", 1.5)
        # scene bg black_bg
#
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

        image job_page = "images/job_page.png"
        scene job_page

        call screen job_offer(1)

        call screen job_offer(2)

        image bg apartment_1 = "images/apartment/apartment3_1.png"
        
        scene bg apartment_1
        call screen apartment(clean(store.apartment_data), store.game_state.time)
        hide screen apartment
      # hide dialogue box
      $ show_window = False
      scene bg gray_bg with Dissolve(1.0)

      call screen dream("Your first day at a new job", [])
      call screen dream("Try not to screw it up.", [])
      call screen dream("You really need the money.", [])
      call screen dream("Let's get started.", [])
    python:
      if start_at_day_end:
          day_end()
    if store.game_state.time == "end":
        jump interstitial

    play music "dataville_workspace_neutral.wav" fadein 2.0
    
    if store.game_state.day == 0:
        show dataville_intro
        pause
        # show hiring_detail
        # pause


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
            if count >= length - 2:
               buttons = message['buttons']
               second_sentence = ""
            else:
               buttons = []
               second_sentence = split[count+1]
          show screen message(message['sender'], buttons)
          $ text = f"{split[count]} {second_sentence}"
          e_big "[text]"
          $ count += 2
          window hide
          hide screen message
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
      $ show_window = False
      show screen overlay (store.game_state.ui)
      if store.game_state.day != 0 and len(cleaned['message'])>0:
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
              if count >= length - 2:
                 buttons = message['buttons']
                 second_sentence = ""
              else:
                 buttons = []
                 second_sentence = split[count+1]
            show screen message(message['sender'], buttons)
            $ text = f"{split[count]} {second_sentence}"
            e_big "[text]"
            $ count += 2
            window hide
            hide screen message
      python:
# CLEAR IMAGE VARIABLES
      # FIXME: should clean up variable resetting a bit better
        is_image = False
        images_selected = {'values': []}
        if ('image' in task['type']):
          is_image = True
          images = get_images(task)
          time = int(task['time'])
          timer_range = time
      if 'custom_dialogue' in task:
        show screen message(task['custom_dialogue_sender'], ["Next"])
        $ custom_dialogue = task['custom_dialogue']
        window hide
        custom_feedback_speaker "[custom_dialogue]"
        hide screen message


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
                        custom_feedback = task['custom_feedback_ethical'] 
                        custom_feedback_sender = task['custom_feedback_sender']
                        has_custom_feedback = True
                    if 'custom_feedback_correct' in task and latest_choice == correct:
                        custom_feedback = task['custom_feedback_correct'] 
                        custom_feedback_sender = task['custom_feedback_sender']
                        has_custom_feedback = True
                task = update_state(store.game_state, binary_correct, task)
        else:
            binary_correct = 1
            task = update_state(store.game_state, binary_correct, task)


      hide screen instructions
      hide screen timer
      hide screen task_type
      show screen overlay (store.game_state.ui)
      if has_custom_feedback:
        show screen message(custom_feedback_sender, ["Continue"])
        window hide
        custom_feedback_speaker "[custom_feedback]"
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
      if (store.game_state.time == "end"):
        show screen performance(store.game_state.performance, store.averages['day_' + str(store.game_state.day)])
        pause
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
            show screen message(message['sender'], buttons)
            $ text = f"{split[count]} {second_sentence}"
            e_big "[text]"
            $ count += 2
            window hide
            hide screen message
#      else:
      hide screen overlay
      scene bg apartment_1
      play music f"dataville_apartment_{store.game_state.performance_rating}.wav" fadein 2.0
      $ show_window = True
      call screen apartment(clean(store.apartment_data), store.game_state.time)
      $ show_window = False
      if store.game_state.day < 4:
        if store.game_state.time == "end":
            scene bg black_bg
            $ dream_counter = 0
            $ dream_len = len(store.apartment_data['dream'])
            while dream_counter < dream_len:
                $ dream = store.apartment_data['dream'][dream_counter]
                if dream['time'] != 'start':
                    hide screen apartment
                    scene bg gray_bg with Dissolve(1.0)
                    call screen dream(dream['text'], dream['buttons'])
                $ dream_counter += 1
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
      $ count = 0
      $ length = len(split)
      while count < length:
        python:
          if count <= length -2:
             additional_text = split[count+1]
          else:
             additional_text = ""
          epi_text = f"{split[count]} {additional_text}"
        
        call screen dream(epi_text, [])
        $ count += 2
      call screen dream('Thank you for playing DataVille!\na more human world\none click at a time', ['Restart'])
      # This ends the game.
      hide screen dream
      "game end!"
      return



