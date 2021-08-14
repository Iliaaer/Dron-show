import requests
session = requests.session()

def led_on(ip:str, red:int=255, green:int=255, blue:int=255):
    try:
        session.get('http://' + ip + '/?led_2_off_{}_{}_{}'.format(red, green, blue))
    except:
       pass 

def led_off(ip:str):
    try:
        session.get('http://' + ip + '/?led_2_on')
    except:
        pass
