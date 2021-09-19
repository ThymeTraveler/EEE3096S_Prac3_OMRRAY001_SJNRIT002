# Import libraries
import RPi.GPIO as GPIO
import random
import ES2EEPROMUtils
import os
import time

# some global variables that need to change as we run the program
end_of_game = None  # set if the user wins or ends the game
number_displayed=0
number_correct=0
BuzzerPwm = None
LEDPwm=None


# DEFINE THE PINS USED HERE
LED_value = [11, 13, 15]
LED_accuracy = 32
btn_submit = 16
btn_increase = 18
buzzer = None
eeprom = ES2EEPROMUtils.ES2EEPROM()


# Print the game banner
def welcome():
    os.system('clear')
    print("  _   _                 _                  _____ _            __  __ _")
    print("| \ | |               | |                / ____| |          / _|/ _| |")
    print("|  \| |_   _ _ __ ___ | |__   ___ _ __  | (___ | |__  _   _| |_| |_| | ___ ")
    print("| . ` | | | | '_ ` _ \| '_ \ / _ \ '__|  \___ \| '_ \| | | |  _|  _| |/ _ \\")
    print("| |\  | |_| | | | | | | |_) |  __/ |     ____) | | | | |_| | | | | | |  __/")
    print("|_| \_|\__,_|_| |_| |_|_.__/ \___|_|    |_____/|_| |_|\__,_|_| |_| |_|\___|")
    print("")
    print("Guess the number and immortalise your name in the High Score Hall of Fame!")


# Print the game menu
def menu():
    global end_of_game
    option = input("Select an option:   H - View High Scores     P - Play Game       Q - Quit\n")
    option = option.upper()
    if option == "H":
        os.system('clear')
        print("HIGH SCORES!!")
        s_count, ss = fetch_scores()
        display_scores(s_count, ss)
    elif option == "P":
        os.system('clear')
        print("Starting a new round!")
        print("Use the buttons on the Pi to make and submit your guess!")
        print("Press and hold the guess button to cancel your game")
        value = generate_number()
        number_correct=value
        while not end_of_game:
            pass
    elif option == "Q":
        print("Come back soon!")
        exit()
    else:
        print("Invalid option. Please select a valid one!")


def display_scores(count, raw_data):
    # print the scores to the screen in the expected format
    print("There are {} scores. Here are the top 3!".format(count))
    # print out the scores in the required format
    pass

def joepapa():
    print("joe papa")
    pass

def joemama():
    print("joemama")
    pass

# Setup Pins
def setup():
    global LEDPwm, BuzzerPwm
    
    # Setup board mode
    GPIO.setmode(GPIO.BOARD)
   
    # Setup regular GPIO
    GPIO.setup(LED_value[0], GPIO.OUT)#LED
    GPIO.setup(LED_value[1], GPIO.OUT)#LED
    GPIO.setup(LED_value[2], GPIO.OUT)#LED
    GPIO.setup(32,GPIO.OUT)#PWM LED
    GPIO.setup(33,GPIO.OUT) #PWM BUZZER
    # Setup PWM channels
    if LEDPwm is None:
        LEDPwm = GPIO.PWM(32, 1000)
    if BuzzerPwm is None:
        BuzzerPwm = GPIO.PWM(33, 1000)

    LEDPwm.start(0)
    BuzzerPwm.start(0)
    
    # Setup debouncing and callbacks
    GPIO.setup(btn_increase, GPIO.IN, pull_up_down=GPIO.PUD_UP) #BUTTON
    GPIO.setup(btn_submit, GPIO.IN, pull_up_down=GPIO.PUD_UP) #BUTTON

    GPIO.add_event_detect(btn_increase, GPIO.FALLING, callback=btn_increase_pressed, bouncetime=200) #DEBOUNCE + callback
    
    GPIO.add_event_detect(btn_submit, GPIO.FALLING, callback=btn_guess_pressed, bouncetime=200) #DEBOUNCE + callback
    


    pass


# Load high scores
def fetch_scores():
    # get however many scores there are
    score_count = None
    # Get the scores
    
    # convert the codes back to ascii
    
    # return back the results
    return score_count, scores


# Save high scores
def save_scores():
    # fetch scores
    # include new score
    # sort
    # update total amount of scores
    # write new scores
    pass


# Generate guess number
def generate_number():
    return random.randint(0, pow(2, 3)-1)


# Increase button pressed
def btn_increase_pressed(channel):
    # Increase the value shown on the LEDs
    # You can choose to have a global variable store the user's current guess, 
    # or just pull the value off the LEDs when a user makes a guess
    global number_displayed

    number_displayed+=1
    if number_displayed==8:
        number_displayed=0

    if number_displayed==0:
        GPIO.output(LED_value[0],GPIO.LOW)
        GPIO.output(LED_value[1],GPIO.LOW)
        GPIO.output(LED_value[2],GPIO.LOW)
    elif number_displayed==1:
        GPIO.output(LED_value[0],GPIO.HIGH)
        GPIO.output(LED_value[1],GPIO.LOW)
        GPIO.output(LED_value[2],GPIO.LOW)
    elif number_displayed==2:
        GPIO.output(LED_value[0],GPIO.LOW)
        GPIO.output(LED_value[1],GPIO.HIGH)
        GPIO.output(LED_value[2],GPIO.LOW)
    elif number_displayed==3:
        GPIO.output(LED_value[0],GPIO.HIGH)
        GPIO.output(LED_value[1],GPIO.HIGH)
        GPIO.output(LED_value[2],GPIO.LOW)
    elif number_displayed==4:
        GPIO.output(LED_value[0],GPIO.LOW)
        GPIO.output(LED_value[1],GPIO.LOW)
        GPIO.output(LED_value[2],GPIO.HIGH)
    elif number_displayed==5:
        GPIO.output(LED_value[0],GPIO.HIGH)
        GPIO.output(LED_value[1],GPIO.LOW)
        GPIO.output(LED_value[2],GPIO.HIGH)
    elif number_displayed==6:
        GPIO.output(LED_value[0],GPIO.LOW)
        GPIO.output(LED_value[1],GPIO.HIGH)
        GPIO.output(LED_value[2],GPIO.HIGH)
    elif number_displayed==7:
        GPIO.output(LED_value[0],GPIO.HIGH)
        GPIO.output(LED_value[1],GPIO.HIGH)
        GPIO.output(LED_value[2],GPIO.HIGH)
        
    print("increase button")    
        
    pass


# Guess button
def btn_guess_pressed(channel):
    # If they've pressed and held the button, clear up the GPIO and take them back to the menu screen
    # Compare the actual value with the user value displayed on the LEDs
    global number_displayed, LEDPwm, BuzzerPwm
    
    correctness=0
    diff=abs(number_displayed-number_correct)
    if number_displayed<number_correct :
        correctness=100*number_displayed/number_correct
    else:
        correctness=100*diff/8
    # Change the PWM LED
    accuracy_leds(correctness)
    # if it's close enough, adjust the buzzer
    trigger_buzzer(diff)
    # if it's an exact guess:
    # - Disable LEDs and Buzzer
    LEDPwm.stop()
    BuzzerPwm.stop()
    # - tell the user and prompt them for a name
    name=input("Howsit bru u won - tell me your name")
    # - fetch all the scores
    # - add the new score
    # - sort the scores
    # - Store the scores back to the EEPROM, being sure to update the score count
    print("guess button")
    pass


# LED Brightness
def accuracy_leds(correctness):
    # Set the brightness of the LED based on how close the guess is to the answer
    # - The % brightness should be directly proportional to the % "closeness"
    # - For example if the answer is 6 and a user guesses 4, the brightness should be at 4/6*100 = 66%
    # - If they guessed 7, the brightness would be at ((8-7)/(8-6)*100 = 50%
    global LEDPwm
    LEDPwm.ChangeDutyCycle(correctness)
    print("LED ACCURACY")
    pass

# Sound Buzzer
def trigger_buzzer(diff):
    # The buzzer operates differently from the LED
    # While we want the brightness of the LED to change(duty cycle), we want the frequency of the buzzer to change
    # The buzzer duty cycle should be left at 50%
    # If the user is off by an absolute value of 3, the buzzer should sound once every second
    # If the user is off by an absolute value of 2, the buzzer should sound twice every second
    # If the user is off by an absolute value of 1, the buzzer should sound 4 times a second
    BuzzerPwm.ChangeDutyCycle(50)
    BuzzerPwm.ChangeFrequency(2**abs(3-diff))
    if diff<=3:
        BuzzerPwm.start()
        time.sleep(1000)
        BuzzerPwm.stop()
    print("triggered")
    pass




if __name__ == "__main__":
    try:
        # Call setup function
        setup()
      
        welcome()
        while True:
            menu()
            pass
    except Exception as e:
        print(e)
    finally:
        GPIO.cleanup()
