import RPi.GPIO as GPIO
import time

# --- GPIO PIN CONFIGURATION ---
# Rows (Outputs)
L1, L2, L3, L4, L5 = 25, 8, 7, 3, 4
# Columns (Inputs)
C1, C2, C3, C4 = 12, 16, 20, 21
# Buzzer Setup
BUZZER_PIN = 18 

# Frequency for each row (in Hz)
TONES = {L1: 440, L2: 494, L3: 523, L4: 587, L5: 659}

# Initialize GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# Setup Rows as Outputs
for pin in [L1, L2, L3, L4, L5]:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

# Setup Columns as Inputs with Pull-Down Resistors
for pin in [C1, C2, C3, C4]:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #remove pull downs if matrix has resistors

# Setup Buzzer
GPIO.setup(BUZZER_PIN, GPIO.OUT)
buzzer = GPIO.PWM(BUZZER_PIN, 440)

# Global variable to store the dialed digits
dialed_number = ""

def play_tone(line):
    buzzer.ChangeFrequency(TONES[line])
    buzzer.start(50) # 50% duty cycle
    time.sleep(0.1)  # Tone duration
    buzzer.stop()

def process_key(key, line):
    global dialed_number
    
    play_tone(line) # Trigger sound
    
    if key == "CLR":
        if len(dialed_number) > 0:
            dialed_number = dialed_number[:-1] # Remove last digit
            print(f"Cleared. Current: {dialed_number}")
    
    elif key in "0123456789*#":
        if len(dialed_number) < 10:
            dialed_number += key
            print(f"Dialed: {dialed_number}")
        else:
            print("Limit reached (10 digits).")
    
    elif key == "SND":
        if len(dialed_number) > 0:
            print(f"CALLING: {dialed_number}...")
        else:
            print("No number entered to call.")
            
    else:
        print(f"Function Pressed: {key}")

def readLine(line, characters):
    GPIO.output(line, GPIO.HIGH)
    
    for i, col in enumerate([C1, C2, C3, C4]):
        if GPIO.input(col) == GPIO.HIGH:
            key = characters[i]
            process_key(key, line)
            
            # Wait for button release (debounce)
            while GPIO.input(col) == GPIO.HIGH:
                time.sleep(0.05) #delay between numbers
            
    GPIO.output(line, GPIO.LOW)

# --- MAIN RUN LOOP ---
print("Brick Phone Matrix Online. Start dialing...")

try:
    while True:
        # Scan each row one by one
        readLine(L1, ["1","2","3","RCL"])
        readLine(L2, ["4","5","6","STO"])
        readLine(L3, ["7","8","9","CLR"])
        readLine(L4, ["*","0","#","SND"])
        readLine(L5, ["PWR","VOL","FCN","END"])
        
        time.sleep(0.02) # Small delay to save CPU power

except KeyboardInterrupt:
    buzzer.stop()
    GPIO.cleanup()
    print("\nSystem Shutdown.")