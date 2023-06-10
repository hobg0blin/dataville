# The script of the game goes in this file.

# Declare characters used by this game. The color argument colorizes the
# name of the character.
# Timer stuff from https://www.reddit.com/r/RenPy/comments/olfuk8/making_a_timer/  
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


define e = Character("Eileen")
define gui.frame_borders = Borders(15, 15, 15, 15)
init python:
  store.drags = {}
  text_boxes = [{'name': 'sweetie', 'text': "I enjoy eating apples with my sweetie.",
  'ypos': 0, 'order': 1}, {'name': "baking", 'text': " I enjoy baking an apple pie in my human kitchen.",
  'ypos': 0, 'order': 2}, {'name': "zzxnarf", 'text': "I enjoy eating Zzxnarf with my brain-mate.", 'ypos': 0, 'order': 3}]
  start_x = 100
  start_y = 100
  # timer stuff
  timer_range = 0
  timer_jump = 0

  order = 1
  case = 0
  # could use periodic function to constantly update box position
  # also look at "cardgame" or "puzzle" templates, although they seem like overkill
  # easiest is slotting them into order in separate window, probably
  def drag_log(drags, drop):
    # needs to have droppable enabled, i guess?
    # if drop:
      print('dropped: ', drags[0].drag_name)
      for d in text_boxes:
        print('d: ', d)
        if d['name'] == drags[0].drag_name: 
          d['ypos'] = drags[0].y
      print('text boxes: ', text_boxes)


screen text_gui(text_boxes, streak_text, feed_text, instructions, status, button_text):
  zorder 1
  window id 'content':
    ymaximum 1200
    xmaximum 1600
    window id 'labeler':
      xmaximum 900
      ymaximum 900
      xalign 0.5
      yalign 0.0
      vbox:
        for (i, box) in enumerate(text_boxes): 
            drag:
                draggable True
                drag_name box['name']
                xpos start_x ypos start_y
                dragged drag_log
                frame:
                  text '{size=-3}'+ box['text']
            python: 
              box['xpos'] = start_x
              box['ypos'] = start_y + (50*i)
              # for some reason if i increase start_y in here it loops when the timer is repeating. this seems insane to me and i would like to find out why (e.g if put start_y += 50 here)
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
    frame id 'done':
      xsize 300
      xalign 0.5
      yalign 0.95
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
    
    label task:
      call screen text_gui(text_boxes, "You're averaging 10 seconds faster than expected! Woohoo!", 'No major news happening today.', 'Put the phrases in order of how human they are.', 'Rent is due tomorrow.', 'Done!')
      $ text_boxes.sort(key = lambda x: x['ypos'])
      # $ print('ordered text boxes: ', text_boxes)
      # These display lines of dialogue.
      python:
        order = map(lambda x, y: x['ypos'], text_boxes)
        print ('order: ', order)
        if order == [1, 2, 3]:
          case = 1
        elif order == [2, 1, 3]:
          case = 2
        else:
          case = 3

      if case == 1:
        call screen text_gui([], "Well done! Your input is 95% compatible with that of other labelers.", "Alien terrorists caught in disguise at American University.", "", "You're 1/3rd of the way to making this month's rent", "Continue")
      elif case == 2:
        call screen text_gui([], "Your input is marked as 'partially correct' in comparison to other labelers.", "Alien terrorists caught in disguise at American University.", "", "You're 1/3rd of the way to making this month's rent", "Continue")
      else:
        call screen text_gui([], "Your input is marked as incorrect in comparison to other labelers.", "Alien terrorists caught in disguise at American University.", "", "You're 1/3rd of the way to making this month's rent", "Continue")
      


    # This ends the game.

    return
