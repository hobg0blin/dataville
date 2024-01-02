# The s]cript of the game goes in this file performance.

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
default latest_choice = ""
default latest_score = 0
define gui.frame_borders = Borders(15, 15, 15, 15)
default messages = []

init: 
# switch to control showing dialogue box background
  default show_window = False

# in style window

  image alien_human_family = "alien_human_family.png"
  image dark_green = Solid("#136366")
  image bg black = Solid("#000000")
  image supervisor = "images/icons/supervisor.png"
  image side supervisor = "images/icons/supervisor.png"
  define e_big = Character("", image="supervisor", kind=bubble)
##ALL THE PYTHON SETUP GOES HERE
init python:
  import random
  import csv
  from types import SimpleNamespace
  import re
  import operator
  import os

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
        'earnings': 1200
        },
      'day_2': {
          'score': 70,
          'time': 8,
        'earnings': 1200
        },
      'day_3': {
          'score': 70,
          'time': 8,
        'earnings': 1200
        },
      'day_4': {
        'score': 70,
        'time': 8,
        'earnings': 1200
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

  store.apartment_data = {"apartment_background": "1", "sticky_note": [], "message": [], "news": [], "window_background": "images/window/city_scape.png", "button_text": "Go to work!"}

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
      print("task string: ", task_string)
      task = store.loop[task_string]
      set_ui_state(task, store.game_state)
    else:
        task = store.loop["start_task"]


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
                    loop[row['task_id']][k] = v.split(',')
                else:
                    #OTHERWISE, SET ATTRIBUTE ON MAIN LOOP OBJECT
                    loop[row['task_id']][k] = v

  def reset_performance(performance):
    for k in performance: performance[k] = 0
  
# PULL APARTMENT STATE FROM CSV
  def get_apartment_image(folder, file):
    return f"images/room/{folder}/{file}"

  def update_apartment_state(filename, apartment, game_state):
    messages = []
    store.apartment_data = {"apartment_background": "1", "sticky_note": [], "news": [], "message": [], "window_background": "images/window/city_scape.png", "button_text": "Go to work!"}
    with open(renpy.loader.transfn(filename), 'r') as current_file:
      reader = csv.DictReader(current_file)
      for row in reader:
        story_object = {}
        if row['TYPE'] == "":
          return
        story_object['performance'] = row['PERFORMANCE']
        story_object['time'] = row['TIME']
        if 'EVENT_FLAG' in row:
          story_object['event_flag'] = row['EVENT_FLAG']
        if row['TYPE'] == 'message':
          story_object['text'] = row['TEXT']
          story_object['sender'] = row['SENDER']
          if len(row['BUTTON_1_TEXT']) > 0:
            story_object['button_1_text'] = row['BUTTON_1_TEXT']
          if len(row['BUTTON_2_TEXT']):
            story_object['button_2_text'] = row['BUTTON_2_TEXT']
        elif row['TYPE'] == 'news':
          story_object['text'] = row['TEXT']
#          story_object['image'] = row['IMAGE']
#          #FIXME: PLACEHOLDER IMAGE
          if 'IMAGE_FOLDER' in row and len(row['IMAGE_FOLDER']) > 0:
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


#
# UPDATE STATE BASED ON TIME CHANGE
  def day_start():
    store.game_state.day += 1
    day = str(store.game_state.day)
    print('day: ', day)
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

  def set_performance_rating():

    if (store.game_state.performance['approval_rate'] > store.averages['day_' + str(store.game_state.day)]['score']):
      store.game_state.performance_rating = "good"
    elif (store.game_state.performance['approval_rate'] == store.averages['day_' + str(store.game_state.day)]['score']):
      store.game_state.performance_rating = "neutral"
    else:
      store.game_state.performance_rating = "bad"

# update task after it's scored, update state with scores
  def update_state(state, out, current_task):
    if (current_task['next_task'] == 'break'):
      set_performance_rating()
      next_task = 'break'
    else:
      next_task = store.loop[current_task['next_task']]
    #if event flag dependency isn't met, skip task
      if ('event_flag_dependency' in next_task):
        if next_task['event_flag_dependency'] not in store.event_flags:
          if next_task['next_task'] == 'break': 
            set_performance_rating()
            next_task = 'break'
          else:
              next_task = store.loop[next_task['next_task']]

  
    reward = int(current_task['payment'])/out

    performance = performance_feedback(out)
    performance_text = performance['text']
    is_ethical = check_ethical(store.latest_choice, current_task)
    if is_ethical and 'ethical_choice_event_flag' in current_task:
      store.event_flags.append(current_task['ethical_choice_event_flag'])
    if store.latest_score == 1 and 'correct_choice_event_flag' in current_task:
      store.event_flags.append(current_task['correct_choice_event_flag'])
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


# The game starts here.

label start:
    image bg start_screen = im.FactorScale("images/intro_desk.jpg", 1.5)
    scene bg start_screen
    pause
    # show standard dialogue box - only for news chyrons
    $ show_window = True
    label intro:
#      manual stuff for game start
#      image bg apartment_1 = im.FactorScale("images/room/room/room_" + store.apartment_data["apartment_background"] + ".jpg", 1.5)
      image bg apartment_1 = im.FactorScale("images/room/room/room.png", 0.3)
      
      scene bg apartment_1
      play music "dataville_apartment_neutral.wav"
      call screen apartment(clean(store.apartment_data), store.game_state.time)
      hide screen apartment
    # hide dialogue box
    $ show_window = False
    play music "dataville_workspace_neutral.wav" fadein 2.0
    if store.game_state.day == 0:
        show dataville_intro
        pause
        show hiring_detail
        pause
    image bg overlay_background = Solid('#EFF3E6')
    image bg black = Solid('#FFFFFF')
    scene bg overlay_background


# manually check messsages on first loop 
    $ cleaned = clean(store.apartment_data)
    label check_messages:
      while cleaned['message']:
        python:
          message = cleaned['message'].pop(0)
          text = message['text']
          buttons = None
          if 'button_1_text' in message:
            buttons = [message['button_1_text']]
          if 'button_2_text' in message:
            buttons.append(message['button_2_text'])
        show screen message(message['sender'], buttons)
        window hide
        e_big "[text]"
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
              text = message['text']
              buttons = None
              if 'button_1_text' in message:
                buttons = [message['button_1_text']]
              if 'button_2_text' in message:
                buttons.append(message['button_2_text'])
            show screen message(message['sender'], buttons)
            window hide
            e_big "[text]"
          hide screen message
          pause
      python:
        is_image = False
        print('task: ', task)
        if ('image' in task['type']):
          is_image = True
          images = get_images(task)
          time = int(task['time'])
          timer_range = time
      if 'custom_dialogue' in task:
        show screen message(task['custom_dialogue_sender'])
        $ custom_dialogue = task['custom_dialogue']
        e_big "[custom_dialogue]"
        hide screen message

      show screen instructions(store.game_state.ui)

      show screen timer
      show screen instructions(store.game_state.ui)
      if is_image:
        call screen expression(task['type']) pass (task, images)
      else: 
        call screen expression(task['type']) pass (task)
      python:
        if (task['type'] == 'captcha_image'):
          case = check_images(images_selected, task['correct_images'])
          store.latest_score = case
          task = update_state(store.game_state, case, task)
        elif (task['type'] == 'order_text'):
          case = check_order_text(task)
          store.latest_score = case
          task = update_state(store.game_state, case,  task)
        else:
          binary_correct = check_binary(store.latest_choice, task)
          store.latest_score = binary_correct
          task = update_state(store.game_state, binary_correct, task)
      hide screen instructions
      hide screen timer
      call screen overlay (store.game_state.ui, True, "Next!")
      if (task == 'break'):
        $ day_end()
        call interstitial
      else:
        call task_loop
      return

    # INTERSTITIAL
    label interstitial:
      hide screen instructions
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
            text = message['text']
            buttons = None
            if 'button_1_text' in message:
              buttons = [message['button_1_text']]
            if 'button_2_text' in message:
              buttons.append(message['button_2_text'])
          show screen message(message['sender'], buttons)
          window hide
          e_big "[text]"
          hide screen message
      else:
        "Waking up..."
      hide screen overlay
      scene bg apartment_1
      play music f"dataville_apartment_{store.game_state.performance_rating}.wav"
      $ show_window = True
      call screen apartment(clean(store.apartment_data), store.game_state.time)
      $ show_window = False
      if store.game_state.day < 4:
        if store.game_state.time == "end":
          python:
            reset_performance(store.game_state.performance)
            day_start()
          scene bg black
          "Sleeping, day [store.game_state.day]..."
          call interstitial
        elif store.game_state.time == "start":
          $ task = store.loop["start_task"]
          $ set_ui_state(task, store.game_state)
          $ cleaned = clean(store.apartment_data)
          play music f"dataville_workspace_{store.game_state.performance_rating}.wav" fadein 2.0
          call task_loop
        else:
          "game state is broken!!!"
      else:
        return

    # This ends the game.
    "game end!"
    return



