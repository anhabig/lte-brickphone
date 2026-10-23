import time

# --- MOCK GPIO SETUP (Keep this for PC testing, remove for Pi) ---
class MockGPIO:
    BCM, OUT, IN, PUD_DOWN, HIGH, LOW = "BCM", "OUT", "IN", "PUD_DOWN", 1, 0
    def setmode(self, m): pass
    def setwarnings(self, w): pass
    def setup(self, p, m, pull_up_down=None): pass
    def output(self, p, s): pass
    def input(self, p): return 0 

GPIO = MockGPIO()

# --- CONFIG ---
L1, L2, L3, L4, L5 = 25, 8, 7, 3, 4
C1, C2, C3, C4 = 12, 16, 20, 21
row_pins = [L1, L2, L3, L4, L5]
row_map = {25:"L1", 8:"L2", 7:"L3", 3:"L4", 4:"L5"}

# Global variable to store the phone number
dialed_number = ""

def process_key(key):
    global dialed_number
    
    if key == "CLR":
        dialed_number = dialed_number[:-1] # Remove last character
        print(f"\n[CLR] Current Number: {dialed_number}")
    
    elif key in "0123456789*#":
        if len(dialed_number) < 10:
            dialed_number += key
            print(f"\nAdded: {key} | Current Number: {dialed_number}")
        else:
            print("\n[!] Max 10 digits reached.")
            
    else:
        print(f"\nFunction Key Pressed: {key}")

def readLine(line_pin, characters):
    # For Terminal Testing:
    print(f"\nScanning {row_map[line_pin]}: {characters}")
    val = input("Col (1-4) or Enter: ")
    
    if val in ["1", "2", "3", "4"]:
        key = characters[int(val)-1]
        process_key(key)
        time.sleep(0.1)

# --- MAIN LOOP ---
try:
    print("--- Brick Phone Dialer System ---")
    while True:
        readLine(L1, ["1","2","3","RCL"])
        readLine(L2, ["4","5","6","STO"])
        readLine(L3, ["7","8","9","CLR"])
        readLine(L4, ["*","0","#","SND"])
        readLine(L5, ["PWR","VOL","FCN","END"])
        
        if len(dialed_number) == 10:
            print(f"\nREADY TO DIAL: {dialed_number}")
            # You could trigger a SND logic here
            
except KeyboardInterrupt:
    print("\nApplication stopped!")