# Headmouse
An opensource project developed in UTN-FRBA by Ramiro Fontalva

This project is part of a larger one called "Tecnoapoyos y Sociedad", which aims to level the opportunities of access to technologies for those who are impaired by some kind of disability, motor or neurological. The purpouse of this API is to use the webcam to detect the user's face and move the cursor according to the tilt of their head, it can also link the wink of the right eye to a mouse's click. 

I am looking for constructive criticism and suggestions to improve this project and make it the best tool it can be to help those with disabilities, so please write me at ramirofontalva@gmail.com if you have any comment about it.

Thank you!


## Install

```shell script
virtualenv -p $(which python3) venv  
source venv/bin/activate
pip install -r requirements.txt
```


## Run demo

```shell
source venv/bin/activate
python main.py
```
