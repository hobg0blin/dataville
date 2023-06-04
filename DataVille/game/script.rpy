# The script of the game goes in this file.

# Declare characters used by this game. The color argument colorizes the
# name of the character.

define e = Character("Eileen")
define gui.frame_borders = Borders(15, 15, 15, 15)
init python:
  store.drags = {}
  text_boxes = [{'name': 'sweetie', 'text': "I enjoy eating apples with my sweetie.",
  'ypos': 0, 'order': 1}, {'name': "baking", 'text': " I enjoy baking an apple pie in my human kitchen.",
  'ypos': 0, 'order': 2}, {'name': "zzxnarf", 'text': "I enjoy eating Zzxnarf with my brain-mate.", 'ypos': 0, 'order': 3}]
  start_x = 100
  start_y = 100
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


screen test():
  window id 'content':
    ymaximum 1200
    xmaximum 1600
    window id 'labeler':
      xmaximum 900
      ymaximum 900
      xalign 0.5
      yalign 0.0
      vbox:
        for box in text_boxes: 
            drag:
                draggable True
                drag_name box['name']
                xpos start_x ypos start_y
                dragged drag_log
                frame:
                  textbutton box['text']
            python: 
              box['xpos'] = start_x
              box['ypos'] = start_y
              start_y += 50

    frame id 'streak':
      xmaximum 200
      xalign 1.0
      yalign 0
      text "You're averaging 10 seconds faster than expected! Woohoo!"
    frame id 'feed':
     xmaximum 200
     xalign 1.0
     yalign 0.5
     text 'No major news happening today.'

    frame id 'instructions':
      xmaximum 200
      xalign 0.0
      yalign 0.0
      text 'Put the phrases in order of how human they are.' 
    frame id 'status':
      xmaximum 200
      xalign 0.0
      ypos 0.5
      text 'Rent is due tomorrow.'

    frame id 'done':
      xmaximum 200
      xalign 0.5
      yalign 1.0
      textbutton "Done!" action Return(True)


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

    e "Order the lines of text based on how human they are."
    call screen test
    $ text_boxes.sort(key = lambda x: x['ypos'])
    $ print('ordered text boxes: ', text_boxes)
    # These display lines of dialogue.

    e "You've created a new Ren'Py game."

    e "Once you add a story, pictures, and music, you can release it to the world!"

    # This ends the game.

    return
