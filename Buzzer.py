from gpiozero import Buzzer
from time import sleep
def buzz():
    t =0
    buzzer = Buzzer(23)
    while t<10:
        buzzer.on()
        sleep(1)
        buzzer.off()
        sleep(1)
        t=t+1
        print(t)
