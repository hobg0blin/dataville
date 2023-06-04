# The script of the game goes in this file.

# Declare characters used by this game. The color argument colorizes the
# name of the character.

define e = Character("Eileen")

init python:
  store.drags = {}
  text_boxes = [{'name': 'sweetie', 'text': "I enjoy eating apples with my sweetie.",
  'ypos': 0}, {'name': "baking", 'text': " I enjoy baking an apple pie in my human kitchen.",
  'ypos': 0}, {'name': "zzxnarf", 'text': "I enjoy eating Zzxnarf with my brain-mate.", 'ypos': 0}]
  start_x = 100
  start_y = 100
  # could use periodic function to constantly update box position
  def drag_log(drags, drop):
    for d in text_boxes:
      if d['ypos'] > drags[0].y:
        get_child_by_name[d['name']].snap(drags[0].y + 50)
      if d['ypos'] < drags[0].y:
        get_child_by_name[d['name']].snap(drags[0].y - 50)


screen test():
    for box in text_boxes: 
        drag:
            draggable True
            drag_name box['name']
            xpos start_x ypos start_y
            dragged drag_log
            vbox:
              textbutton box['text']
        python: 
          box['xpos'] = start_x
          box['ypos'] = start_y
          start_y += 50

    window id 'done':
      vbox:
        textbutton "Done!" action Return(True)


# The game starts here.

label start:

    # Show a background. This uses a placeholder by default, but you can
    # add a file (named either "bg room.png" or "bg room.jpg") to the
    # images directory to show it.

    scene bg room

    # This shows a character sprite. A placeholder is used, but you can
    # replace it by adding a file named "eileen happy.png" to the images
    # directory.

    show eileen happy

    e "Order the lines of text based on how human they are."
    call screen test
    # These display lines of dialogue.

    e "You've created a new Ren'Py game."

    e "Once you add a story, pictures, and music, you can release it to the world!"

    # This ends the game.

    return
