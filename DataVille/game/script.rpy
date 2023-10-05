# The script of the game goes in this file.

# Declare characters used by this game. The color argument colorizes the
# name of the character.
# Timer stuff from https://www.reddit.com/r/RenPy/comments/olfuk8/making_a_timer/
#
# TODOS:
# Overall state - in progress
# Saving/saved state - in progress
# "Hot or Not" RLHF GUI
# General GUI updates per figma file
# Probably use labels for each section/loop/etc.?
# Brent - structural reorg per Figma
# In UI update, automaticallly pull "UI performance" from array of random text
# based on outcome, e.g. {1: ['Great!'], 2:[ 'Not so great'], 3: ['Bad!']}
# Could just do 2 outcomes (good or bad) and periodically update UI based on
# expected score to this point vs. actual score - only tasks that could
# potentially have 3 outcomes anyway are text ordering, image captcha, image
# caption, and sentiment - and thinking of keeping image captcha to 2 outcomes
# to simplify scoring, at least for now

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
  def set_timer(range):
      timer_range = range
  def get_order(label):
    num_match = re.search(r'[0-9]+', label)
    num_str = num_match.group()
    return num_str

 # FIXME: make this smarter
  def get_assign_loop(filename, loop):
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
                elif 'outcome' in k:
                    #HANDLE ANY CUSTOM OUTCOMES - in loop[id][outcomes][ui/counters]
                    #counters are game state/counting tasks
                    #ui stuff updates visible UI boxes
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
                else:
                    #OTHERWISE, SET ATTRIBUTE ON MAIN LOOP OBJECT
                    loop[row['task_id']][k] = v


  get_assign_loop('game_files/loop.csv', store.loop)
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

 # update state with "outcomes" attribute from current loop, based on
 # performance. should always take the form of {1: (BEST OUTCOME), 2: (MEDIUM
 # OUTCOME), 3: (WORST OUTCOME)}
 # TODO: account for "ethical" vs. "correct" result
  def performance_feedback(case):
      good = ["Great work!", "Your output is compatible with 95% of labelers!", "Well done!"]
      mid = ["Your performance is reasonable", "Your output is compatible with 70% of other labelers."]
      bad = ["Not so great!", "Your output is incompatible with that of other labelers. Please try to pay attention."]
      if (case == 1):
        return random.choice(good)
      elif (case == 2):
        return random.choice(mid)
      else:
        return random.choice(bad)

  def update_state(state, case, current_task):
    reward = int[task['payment']]/case
    outcomes = current_task['outcomes'][str(case)]
    performance = performance_feedback(case)
    # put past news articles in archive (if needed)
    if "news_headline" in outcomes["ui"].keys():
        state.ui["past_news_stories"].append({"headline": state.ui["news_headline"], "body": state.ui["news_body"]})
    for counter in state.counters.keys():
      if outcomes.has_key("counters") and counter in outcomes["counters"].keys():
        # if it's a counter, increment it
        state.counters[counter] += outcomes["counters"][counter]
    for ui_element in state.ui.keys():
      if ui_element in outcomes["ui"].keys():
        state.ui[ui_element] = outcomes["ui"][ui_element]
    state.ui['performance'] = performance
    state.ui['budget'] += reward
    return loop[current_task['next_task']]

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
  images_selected = {'values': []}
  def select_image(image):
    if image not in images_selected['values']:
      print('selecting: ', image)
      images_selected['values'].append(image)
    else:
      print('unselecting: ', image)
      images_selected.remove(image)


  # dumb comparison of images that just returns true or false
  # should probably be percentile graded but we prototyping baby
  def check_images(selected, original):
    correct_values = list(filter(lambda x: x['value'] == True, original))
    if selected['values'] == [x['value'] for x in correct_values]:
      return 1
    else:
      return 3


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
    #$ timer_jump = 'start'
    python:
        task = loop['text_task_1']
        set_timer(task.time)

    show screen timer
    show screen overlay(game_state.ui)

    label task_1:
      call screen expression store.loop['text_task_1']['type'] pass (store.loop['text_task_1'], 'Done!')
      python:
        task = loop['text_task_1']
        sort_labels = sorted(task['labels'].items(), key=lambda x: x[1]['ypos'])
        # set order defined in text_label_task object
        # have to turn it into a list so renpy will pickle it
        order = list(dict(sort_labels).keys())
        if order == [1, 2, 3]:
          case = 1
        elif order == [2, 1, 3]:
          case = 2
        else:
          case = 3
        task = update_state(game_state, case,  task)

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
      #TODO pick screen to call based on task type
      # call screen image_gui(task, "Done!")
      call screen expression(task['type']) pass (task, 'Done!')

      python:
        images_correct = check_images(images_selected, image_label_task_1['correct_images'])
      update_state(game_state, images_correct, task)


    # This ends the game.

    return


# old version of state for reference:
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

