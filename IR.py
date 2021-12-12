import RPi.GPIO as GPIO

# the data pin of IR sensor is connected to pin 16
inputPin = 16

# Use Board pin numbering scheme
GPIO.setmode(GPIO.BOARD)

# Set this pin as input pin
GPIO.setup(inputPin,GPIO.IN)

# Ask  IR sensor if the people present
def isPeoplePresent(): 
     # GPIO.LOW when people present,HIGH when not present
    value =GPIO.input(inputPin)
    if (value == GPIO.HIGH):
        return False
    else: 
        return True

def cleanup():
    GPIO.cleanup()