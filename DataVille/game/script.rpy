# The script of the game goes in this file.

# Declare characters used by this game. The color argument colorizes the
# name of the character.
# Timer stuff from https://www.reddit.com/r/RenPy/comments/olfuk8/making_a_timer/
#
# TODOS:0
# Overall state - in progress
# Saving/saved state - in progress
# highlight "selected" images
# "Hot or Not" RLHF GUI
# General GUI updates per figma file
# Probably use labels for each section/loop/etc.?
# Arnab - CSV prototyping
# Brent - incorporate CSV into data management
# Brent - structural reorg per Figma

#Set global variables
define e = Character("Eileen")
default task = {}
define gui.frame_borders = Borders(15, 15, 15, 15)
image alien_human_family = "alien_human_family.png"
##ALL THE PYTHON SETUP GOES HERE
init python:
  import random
  import csv
  from types import SimpleNamespace
  import re
  import operator

  store.drags = {}
  store.loop = {}
  # set default image ordering for testign
  store.order = [3,2,1]
  # search for a string, assign that as its order/ID within its text labeling
  # task
  def get_order(label):
    num_match = re.search(r'[0-9]+', label)
    num_str = num_match.group()
    return num_str

 # FIXME: make this smarter
  def get_assign_loop(filename, loop):
      with open(renpy.loader.transfn(filename), 'r') as current_loop:
          reader = csv.DictReader(current_loop)
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
                elif 'outcome' in k:
                    #HANDLE ANY CUSTOM OUTCOMES
                    print('k: ', k)
                    print('v: ', v)
                    order = get_order(k)
                    out_key = 'outcome_' + str(order) + '_'
                    strp_key = k.replace(out_key, '')
                    if not loop[row['task_id']].has_key('outcomes'):
                        loop[row['task_id']]['outcomes'] = {}
                    if not loop[row['task_id']]['outcomes'].has_key(order):
                        loop[row['task_id']]['outcomes'][order] = {}
                    if 'ui' in k:
                        if not loop[row['task_id']]['outcomes'][order].has_key('ui'):
                            loop[row['task_id']]['outcomes'][order]['ui'] = {}
                        strp_ui = strp_key.replace('ui_', '')
                        loop[row['task_id']]['outcomes'][order]['ui'][strp_ui] = v
                    elif 'counter' in k:
                        if not loop[row['task_id']]['outcomes'][order].has_key('counters'):
                            loop[row['task_id']]['outcomes'][order]['counters'] = {}
                        strp_counter = strp_key.replace('counter_', '')
                        loop[row['task_id']]['outcomes'][order]['counters'][strp_counter] = v
                    else:
                        loop[row['task_id']]['outcomes'][order][strp_key] = v
                    print('outcomes: ', loop[row['task_id']]['outcomes'])
                else:
                    loop[row['task_id']][k] = v


  get_assign_loop('game_files/loop_1.csv', store.loop)
  print('loops!', loop)

  #FIXME: would like this to be using RenPy's default store functionality but I think I'm not understanding how that works properly
  #Basically I am being forced into using object["attribute"] instead of dot notation and that feels dumb and wrong to me
  game_state = {}
  game_state.counters = {
        "current_day": 0,
        "current_task": 0,
        "employer_opinion": 0,
        "alien_player_opinion": 0,
        "alien_public_opinion": 0,
        "bank_account": 0,
    }
  game_state.ui = {
        "news_headline": "",
        "news_body":"",
        "past_news_stories": [],
        "budget": 0,
        "performance": "",
        "instructions": "Place the sentences in order of how human they sound."
      }


  def update_state(state, case, current_task, reward):
    outcomes = current_task['outcomes'][str(case)]
    print("outcomes", outcomes)
    if "news_headline" in outcomes["ui"].keys():
        state.ui["past_news_stories"].append({"headline": state.ui["news_headline"], "body": state.ui["news_body"]})
    for counter in state.counters.keys():
      if outcomes.has_key("counters") and counter in outcomes["counters"].keys():
        # if it's a counter, increment it
        state.counters[counter] += outcomes["counters"][counter]
    for ui_element in state.ui.keys():
      if ui_element in outcomes["ui"].keys():
        state.ui[ui_element] = outcomes["ui"][ui_element]
    state.ui['budget'] += reward
    print('next task: ', loop[current_task['next_task']])
    return loop[current_task['next_task']]
 # text box template:
  # set "order" to final correct order of boxes
  # name doesn't matter, just used internally to reference each box
  # can manually set y pos if you want to for some reason

#  text_label_task_1 = { 'labels': [{'name': 'sweetie', 'text': "I enjoy eating apples with my sweetie.",
#      'ypos': 0, 'order': 1}, {'name': "baking", 'text': " I enjoy baking an apple pie in my human kitchen.",
#      'ypos': 0, 'order': 2}, {'name': "zzxnarf", 'text': "I enjoy eating Zzxnarf with my brain-mate.", 'ypos': 0, 'order': 3}],
#    'outcomes': {
#      1: {
#           "ui_state": {
#             "labeling_performance" : "Well done! Your input is 95% compatible with that of other labelers.",
#              "current_news_story": {
#                "headline": "Alien terrorists Caught in Disguise at New Terra University", "body": "TK"
#             },
#             "budget": "Nice! You're 1/3rd of the way to making today's rent!",
#            },
#            "counters": {
#             "bank_account": 200,
#            }
#         },
#      2: {
#           "ui_state": {
#             "labeling_performance" : "Your input is marked as 'partially correct' in comparison to other labelers.",
#              "current_news_story": {
#                "headline": "Alien terrorists Caught in Disguise at New Terra University - but Leader Escapes", "body": "TK"
#             },
#             "budget": "You're 1/6th of the way to making today's rent!",
#           },
#            "counters": {
#             "bank_account": 100,
#           }
#         },
#        3: {
#           "ui_state": {
#             "labeling_performance" : "Your input is marked as incorrect in comparison to other labelers.",
#              "current_news_story": {
#                "headline": "Alien Terrorists Attack Research Center At New Terra University", "body": "TK"
#             },
#             "budget": "You're 1/12 of the way to making today's rent!",
#            },
#            "counters": {
#             "bank_account": 50,
#           }
#       }
#      }
#    }
#  text_label_task_1 = SimpleNamespace(**text_label_task_1)
#  # image label template:
#  # src comes from `images` folder
#  # True: should be clicked
#  # False: should not be clicked
#  image_label_task_1 = [{'src': 'alien_1.png', 'value' : True}, {'src': 'alien_2.png', 'value' : True}, {'src': 'alien_3.png', 'value' : True}, {'src': 'human_1.png', 'value' : False}, {'src': 'human_2.png', 'value' : False}, {'src': 'human_3.png', 'value' : False}, {'src': 'human_4.png', 'value' : False}]
#
  images_correct = False
  start_x_image = 100
  start_y_image = 100
  start_x_text = 100
  start_y_text = 100
  # timer stuff
  timer_range = 0
  timer_jump = 0

  order = 1
  case = 0
  # could use periodic function to constantly update box position
  # also look at "cardgame" or "puzzle" templates, although they seem like overkill
  # easiest is slotting them into order in separate window, probably
  # TODO: make image buttons unselectable - just doing it quick and dirty right now
  images_selected = {'ids': [], 'values': []}
  def select_image(image):
    if image['src'] not in images_selected['ids']:
      images_selected['ids'].append(image['src'])
      images_selected['values'].append(image['value'])


  # dumb comparison of images that just returns true or false
  # should probably be percentile graded but we prototyping baby
  def check_images(selected, original):
    correct_values = list(filter(lambda x: x['value'] == True, original))
    if selected['values'] == [x['value'] for x in correct_values]:
      return True
    else:
      return False


  def drag_log(drags, drop):
    # needs to have droppable enabled, i guess?
    # if drop:
      #print('dropped: ', drags[0].drag_name)
      for d in task['labels']:
      #  print('d: ', d)
        if d['name'] == drags[0].drag_name:
          d['ypos'] = drags[0].y
      #print('text boxes: ', text_label_task_1)


# The game starts here.

label start:

    # Show a background. This uses a placeholder by default, but you can
    # add a file (named either "bg room.png" or "bg room.jpg") to the
    # images directory to show it.

    scene bg xp

    # This shows a character sprite. A placeholder is used, but you can
    # replace it by adding a file named "eileen happy.png" to the images
    # directory.

    # show eileen happy
    # FIRST TEXT LOOP
#    e "Welcome to Anthropic Solutions."
#    e "We're pleased that you've taken the opportunity to join the fast-growing field of human identification software."
#    e "Your pay will correspond directly to your performance: your speed and accuracy are crucial to keeping our systems human first."
#    e "For your first day, we'll keep things simple."
#    e "Let's start with text identification."
#    e "Order the lines of text based on how human they are."

    ## SET TIMER FOR TASK - WIP
    # TODO: set timers on individual task object?
    $ time = 3
    $ timer_range = 3
    #$ timer_jump = 'start'

    show screen timer
    show screen overlay(game_state.ui)

    label task_1:
      call screen text_gui(store.loop['text_task_1'], 'Done!')
      python:
        task = loop['text_task_1']
        sort_labels = sorted(task['labels'].items(), key=lambda x: x[1]['ypos'])
        # set order defined in text_label_task object
        order = dict(sort_labels).keys()
        if order == [1, 2, 3]:
          case = 1
        elif order == [2, 1, 3]:
          case = 2
        else:
          case = 3
        task = update_state(game_state, case,  task, int(task['payment'])/case)

      call screen overlay (game_state.ui, "Next")

      # FIRST IMAGE LOOP
      #
      e "Great start. Now, for your second task, we'd like you to identify the aliens in an image."
      e "Aliens and humans have begun to cohabitate and even interbreed, which can make it hard to tell the difference."
      e "For your first task, though, it should be easy enough. Just look for the *obviously* non-human beings in this photo: gray or purple skin, or perhaps an unusual amount of teeth."
      show alien_human_family
      e "Take a look, and when you're ready to start labeling, continue."
      hide alien_human_family
      show screen overlay(game_state.ui)
      call screen image_gui(task, "Done!")
      python:
        images_correct = check_images(images_selected, image_label_task_1)
      if images_correct:
        e "Well done! You're ready to begin the job in earnest. But be warned, it only gets harder from here on out."
      else:
        e "You may not be a great fit for this position. We'll give you one last chance, but be warned, the work only gets harder from here."


    # This ends the game.

    return
