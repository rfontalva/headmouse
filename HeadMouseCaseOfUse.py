from HeadMouseObj import HeadMouse

def myprint():
    print('wink wink')

HeadMouse=HeadMouse()
HeadMouse.onRightEye_closed(myprint)

while True:
    HeadMouse.refresh()