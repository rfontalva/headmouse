from HeadMouse import HeadMouse

if __name__ == '__main__':
    HeadMouse = HeadMouse()
    i = 0
    while True:
        HeadMouse.refresh()
        if i == 100:
            HeadMouse.calibrate()
        i += 1