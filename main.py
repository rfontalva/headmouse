from HeadMouseObj import HeadMouse

def myprint():
    print('wink wink')

if __name__ == '__main__':
    HeadMouse = HeadMouse()
    HeadMouse.on_eye_closed(myprint)
    i = 0
    while True:
        HeadMouse.refresh()
        if i == 100:
            print(HeadMouse.get_center())
            HeadMouse.calibrate()
            print(HeadMouse.get_center())
