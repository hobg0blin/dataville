# The script of the game goes in this file.

# Declare characters used by this game. The color argument colorizes the
# name of the character.
# Timer stuff from https://www.reddit.com/r/RenPy/comments/olfuk8/making_a_timer/  

define e = Character("Eileen")
define gui.frame_borders = Borders(15, 15, 15, 15)
image alien_human_family = "alien_human_family.png"
init python:
  import random
  store.drags = {}
  # text box template:
  # set "order" to final correct order of boxes
  # name doesn't matter, just used internally to reference each box
  # can manually set y pos if you want to for some reason
  text_boxes = [{'name': 'sweetie', 'text': "I enjoy eating apples with my sweetie.",
  'ypos': 0, 'order': 1}, {'name': "baking", 'text': " I enjoy baking an apple pie in my human kitchen.",
  'ypos': 0, 'order': 2}, {'name': "zzxnarf", 'text': "I enjoy eating Zzxnarf with my brain-mate.", 'ypos': 0, 'order': 3}]
  image_boxes = [{'src': 'alien_1.png', 'value' : True}, {'src': 'alien_2.png', 'value' : True}, {'src': 'alien_3.png', 'value' : True}, {'src': 'human_1.png', 'value' : False}, {'src': 'human_2.png', 'value' : False}, {'src': 'human_3.png', 'value' : False}, {'src': 'human_4.png', 'value' : False}]
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
      for d in text_boxes:
      #  print('d: ', d)
        if d['name'] == drags[0].drag_name: 
          d['ypos'] = drags[0].y
      #print('text boxes: ', text_boxes)

# TIMER STUFF
transform alpha_dissolve:
  alpha 0.0
  linear 0.5 alpha 1.0
  on hide:
    linear 0.5 alpha 0

screen timer:
  zorder 10
  vbox:
    xalign 0.9 
    yalign 0.275
    timer 0.01 repeat True action If(time > 0, true=SetVariable('time', time - 0.01))
    bar value time range timer_range xalign 0.5 yalign 0.9 xmaximum 300 at alpha_dissolve



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
# }

screen overlay(streak_text, feed_text, instructions, status, button_text=False):
  window id 'content':
    ymaximum 1200
    xmaximum 1600
    frame id 'streak':
      xsize 300
      ysize 300
      xalign 1.0
      yalign 0
      text 'PROGRESS TRACKER'
      text '\n\n{size=-5}' + streak_text 
    frame id 'feed':
      xsize 300
      ysize 300
      xalign 1.0
      yalign 0.5
      text 'NEWS'
      text '\n{size=-5}' + feed_text
    frame id 'instructions':
      xsize 300
      ysize 300
      xalign 0.0
      yalign 0.0
      text 'INSTRUCTIONS'
      text '\n{size=-5}' + instructions
    frame id 'status':
      xsize 300
      ysize 300
      xalign 0.0
      ypos 0.5
      text 'PERSONAL'
      text '\n{size=-5}' + status
    if (button_text):
      frame id 'overlay_button':
        xsize 300
        xalign 0.5
        yalign 0.95
        textbutton button_text action Return(True)
#
# SELECT DA IMAGES
screen image_gui(image_boxes, button_text):
  zorder 1 
  # $ random.shuffle(image_boxes)
  window id 'labeler':
      style "window_nobox"
      xmaximum 900
      ymaximum 900
      xalign 0.5
      yalign 0.0
      grid 3 4:
        xmaximum 250
        ymaximum 250
        for (i, box) in enumerate(image_boxes): 
          imagebutton:
            xfill True
            yfill True
            idle Transform(f"{box['src']}", size=(150, 150))
            hover Transform(f"{box['src']}", size=(200, 200))
            action Function(select_image, box) 
  frame id 'done':
    xsize 300
    xalign 0.5
    yalign 0.9
    textbutton button_text action Return(True)



# ORDER THE TEXT

screen text_gui(text_boxes, button_text):
  zorder 1
  # this animates random shuffle??? is that supposed to be happening? either renpy.random or regular random does it
  #ok so use traditional python random library for actual randomization
  $ random.shuffle(text_boxes)
  # # does not return a list but changes an existing one, generates same numbers every time
  # $ renpy.random.shuffle(text_boxes)
  window id 'labeler':
    style "window_nobox"
    xmaximum 900
    ymaximum 900
    xalign 0.5
    yalign 0.0
    vbox:
      for (i, box) in enumerate(text_boxes): 
          drag:
              draggable True
              drag_name box['name']
              xpos start_x_text ypos start_y_text
              dragged drag_log
              frame:
                text '{size=-3}'+ box['text']
          python: 
            box['xpos'] = start_x_text
            box['ypos'] = start_y_text + (50*i)
            # for some reason if i increase start_y in here it loops when the timer is repeating. this seems insane to me and i would like to find out why (e.g if put start_y += 50 here)
  frame id 'done':
    xsize 300
    xalign 0.5
    yalign 0.9
    textbutton button_text action Return(True)
    
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
    e "Welcome to Anthropic Solutions."
    e "We're pleased that you've taken the opportunity to join the fast-growing field of human identification software."
    e "Your pay will correspond directly to your performance: your speed and accuracy are crucial to keeping our systems human first."
    e "For your first day, we'll keep things simple."
    e "Let's start with text identification."
    e "Order the lines of text based on how human they are."
    $ time = 3
    $ timer_range = 3
    #$ timer_jump = 'start'
    
    show screen timer
    show screen overlay("You're averaging 10 seconds faster than expected! Woohoo!", 'No major news happening today.', 'Put the phrases in order of how human they are.', 'Rent is due tomorrow.')
    
    label task:
      call screen text_gui(text_boxes, 'Done!')
      $ text_boxes.sort(key = lambda x: x['ypos'])
      # $ print('ordered text boxes: ', text_boxes)
      # These display lines of dialogue.
      python:
        get_order = [x['order'] for x in text_boxes]
      # order is a map object, so have to turn it into a list
        #order = map(lambda x, y: x['ypos'], text_boxes)
        order = list(get_order)
        if order == [1, 2, 3]:
          case = 1
        elif order == [2, 1, 3]:
          case = 2
        else:
          case = 3

      if case == 1:
        call screen overlay("Well done! Your input is 95% compatible with that of other labelers.", "Alien terrorists caught in disguise at American University.", "", "You're 1/3rd of the way to making this month's rent", "Continue")
      elif case == 2:
        call screen overlay("Your input is marked as 'partially correct' in comparison to other labelers.", "Alien terrorists caught in disguise at American University.", "", "You're 1/3rd of the way to making this month's rent", "Continue")
      else:
        call screen overlay("Your input is marked as incorrect in comparison to other labelers.", "Alien terrorists caught in disguise at American University.", "", "You're 1/3rd of the way to making this month's rent", "Continue")
      e "Great start. Now, for your second task, we'd like you to identify the aliens in an image."
      e "Aliens and humans have begun to cohabitate and even interbreed, which can make it hard to tell the difference."
      e "For your first task, though, it should be easy enough. Just look for the *obviously* non-human beings in this photo: gray or purple skin, or perhaps an unusual amount of teeth."
      show alien_human_family
      e "Take a look, and when you're ready to start labeling, continue."
      hide alien_human_family
      show screen overlay("You're averaging 10 seconds faster than expected! Woohoo!", 'No major news happening today.', 'Click on the images that are not human.', 'Rent is due tomorrow.')
      call screen image_gui(image_boxes, "Done!")
      python:
        images_correct = check_images(images_selected, image_boxes)
      if images_correct:
        e "Well done! You're ready to begin the job in earnest. But be warned, it only gets harder from here on out."
      else:
        e "You may not be a great fit for this position. We'll give you one last chance, but be warned, the work only gets harder from here."


    # This ends the game.

    return
