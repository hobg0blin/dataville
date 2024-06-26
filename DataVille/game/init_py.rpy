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
  timer_range = 0
  time = 0
  timer_jump = ''
  store.timer_failed = False
  task = "start_task`"
  # default captcha image variables
  images_correct = False
  start_x_image = 100
  start_y_image = 300
  start_x_text = 100
  start_y_text = 300
  # timer stuff
  order = 1

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
#    text = text.replace("\n"," ")
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
#    if "\"" in text: text = text.replace(".\"","\".")
    if "!" in text: text = text.replace("!\"","\"!")
    if "?" in text: text = text.reSSplace("?\"","\"?")
    text = text.replace(".",".<stop>")
    text = text.replace("?","?<stop>")
    text = text.replace("!","!<stop>")
    text = text.replace("<prd>",".")
    sentences = text.split("<stop>")
    
    # hacky way to remove blank sentences at the end of the list
    if sentences[-1].isspace():
        sentences.pop()
    # if for some reason there are empty strings in the sentence list
    # besides at the end, we can use the filter function
    # sentences = list(filter(lambda s: not s.isspace(), sentences))
    
    sentences = [s.lstrip('\n.') for s in sentences]

    return sentences
  
  def set_initial_variables():
    store.drags = {}
    store.loop = {}
    # CONSTANTS FOR PERFORMANCE COMPARISON
    store.averages = {
        'day_0': {
          'score': 70,
          'time': 8,
          'earnings': 600
          },
        'day_1': {
          'score': 70,
            'time': 8,
          'earnings': 2200
          },
        'day_2': {
            'score': 70,
            'time': 8,
          'earnings': 5000
          },
        'day_3': {
            'score': 70,
            'time': 8,
          'earnings': 9000
          },
        'day_4': {
          'score': 70,
          'time': 8,
          'earnings': 15000
          },
      }
  # these should only be updated after a game loop
    store.game_state = {}
  # STATE TRACKING VARIABLES
    store.event_flags = []
    store.game_state.time = 'start'
    store.game_state.day = -1
    store.game_state.performance_rating = 'neutral'
    store.game_state.performance_count = {'good': 0, 'bad': 0, 'neutral': 0}
    store.game_state.task_count = 0
    store.apartment_file = ""
    store.daily_rent = 1500


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
          "earnings_minus_rent": 0
        }

    store.apartment_data = {"apartment_background": "1", "sticky_note": [], "message": [], "news": [], "window_background": "images/room/window_content/default_window_bg.jpg", "button_text": "Go to work!", "dream": []}

    # set default image ordering
    store.order = [3,2,1]
  # DEFAULT TIMER VARIABLES
    timer_range = 0
    time = 0
    timer_jump = ''
    store.timer_failed = False
    day_start()
    task = store.loop['start_task']
  # default captcha image variables
    images_correct = False
    start_x_image = 100
    start_y_image = 300
    start_x_text = 100
    start_y_text = 300
    # timer stuff
    order = 1

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
    length = len([x for x in data["news"] if x["time"] == store.game_state.time])
    print('length: ', length)
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


# update state with "outcomes" attribute from current loop, based on
# performance. should always take the form of {1: (BEST OUTCOME), 2: (MEDIUM
# OUTCOME), 3: (WORST OUTCOME)}
# TODO: account for "ethical" vs. "correct" result
# SCORING FUNCTIONS

  def performance_feedback(out):
      good = ["You’re really doing it!", "You’re labeling faster than 81% of DataVille Annotators!", "Great accuracy!", "Keep it up!", "Aim for that performance incentive!"]
      mid = ["Your performance is reasonable", "Your output is compatible with 70% of other labelers."]
      bad = ["Accuracy is important. Don’t be afraid to look carefully!", "Oof. Hope you do better next time.", "You’ll need to do better if you want the incentive bonus!", "Stay focused.", "That wasn’t great - do you need clearer instructions?"]
      if (out == "good" or out == 1):
        return {'text': random.choice(good), 'score': 100}
      elif (out == "neutral" or out == 2):
        return {'text': random.choice(mid), 'score': 66}
      else:
        return {'text': random.choice(bad), 'score': 33}
  def check_dependencies(dependencies, next_task):
      for dependency in dependencies:
        cleaned_dep = dependency.strip()
        new_task = ""
      
        if cleaned_dep not in store.event_flags:
            if next_task != 'break':
                if next_task['next_task'] == 'break': 
                    set_performance_rating()
                    new_task = 'break'
                else:
                    new_task = store.loop[next_task['next_task']]
                    if ('event_flag_dependency' in new_task):
                        new_task = check_dependencies(new_task['event_flag_dependency'].split(','), new_task)
        else:
            print("dependency in event flags: ", cleaned_dep)
            new_task = next_task
            break
      return new_task

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
    if store.timer_failed:
       print("Timer failed! Reducing reward.")
       reward = reward/2
       store.timer_failed = False

    performance = performance_feedback(out)
    performance_text = performance['text']
    #SCORING
    store.game_state.task_count += 1
    store.game_state.performance['total_score'] = (store.game_state.performance['total_score'] + performance['score'])
    store.game_state.performance['approval_rate'] = (store.game_state.performance['total_score']/store.game_state.task_count)
    # TIME TRACKER
    store.game_state.performance['total_time'] = (store.game_state.performance['total_time'] + (10 - (time/1000)))    
    store.game_state.performance['average_time'] = (store.game_state.performance['total_time'] /store.game_state.task_count)    
    return set_ui_state(next_task, state, performance_text, reward)

  def set_ui_state( task, state, performance_text = '', reward = 0):
    print('task: ', task)
    state.ui['performance'] = performance_text
    state.ui['earnings'] += reward
    state.performance['earnings'] += reward
    state.performance['earnings_minus_rent'] += reward
    if task == 'break':
      return task
    else:
      state.ui['instructions'] = task['instructions']
      state.ui['timer'] = float(task['time']) * 1000
      return task

  def get_epilogue():
    output = ""
    print('flags present: ', store.event_flags)
    with open(renpy.loader.transfn('game_files/epilogues.csv'), 'r') as epilogues: 
        reader = csv.DictReader(epilogues)
        has_event_flag = False
        for epilogue in reader:
            if len(epilogue['event_flag']) <= 0:
                if epilogue['performance'] == store.game_state.performance_rating:
                    output = epilogue['text']
                    print('setting default event flag: ', output)
            else:
                for event_flag in store.event_flags: 
                    output = epilogue['text']
                    if (event_flag == 'tutorial_fail' or event_flag == 'rent_fail' or event_flag == 'performance_fail') and event_flag == epilogue['event_flag']:
                        has_event_flag = True
                    if event_flag == epilogue['event_flag'] and epilogue['performance'] == store.game_state.performance_rating:
                        print('event flag based epilogue firing: ', epilogue)
                        has_event_flag = True
                if has_event_flag:
                      break
    print('epilogue output: ', epilogue)

    return output


# IMAGE TASK FUNCTIONS
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
  
  def render_message(who, who_suffix, what, mood, position = "center"):
    """
    Renders message style between emails or cogni from reading the CSV scripts.
    """
    if who != "Cogni":
      renpy.call_screen('email_message', who, who_suffix, what, mood)
    else:
      renpy.call_screen('cogni', what, mood, position)
  set_initial_variables() 