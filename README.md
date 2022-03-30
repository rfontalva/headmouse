# Headmouse

The HeadMouse module provides an interface by opening the web camera anddetecting the user's face to control the mouse by tilting the head, 
using the tip of the nose as reference point.
It can also be customized to trigger different functions instead of a mouse click when the user winks.
To use the module it\'s necessary to have the file shape_predictor_68_face_landmarks.dat.

Compressed:
<http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2>

Uncompressed:
<https://github.com/rfontalva/dlib_shape_predictor_68_face_landmarks/tree/master>'

This project is part of a larger one called "Tecnoapoyos y Sociedad", which aims to level the opportunities of access to technologies for those who are impaired by some kind of disability, motor or neurological.

An opensource project developed in UTN-FRBA by Ramiro Fontalva.

## Run demo

```python
from headmouse import Headmouse
import cv2

if __name__ == "__main__":
    predictor_path = "/path/to/shape_predictor_68_face_landmarks.dat"
    h = Headmouse(predictor_path=predictor_path)
    h.update_threshold(10, 5)
    while True:
        h.refresh()
        h.show_image()
        key = cv2.waitKey(1)
        if key == 27: #press escape
            h.destroy_window()
            h.quit()
            break
        if key == 32: #press spacebar
            h.calibrate()
            print("calibrated")
```
