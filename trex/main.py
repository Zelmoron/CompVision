import matplotlib.pyplot as plt
import pyautogui
import webbrowser
import time
import cv2 
import keyboard
from skimage.measure import label
webbrowser.open('https://chromedino.com')
time.sleep(4)
""" Poisk locacii c dino"""
template = pyautogui.locateOnScreen('dino3.png')
n = template[0] #первая корда
m = template[1] #вторая корда
n = int(n) 
m = int(m)   
jump = 0  #по дсчет прыжков
slp = 0.15 #  время перовой паузы
k = 170    #ди станция до препятствия
speed = 150  #скорость дин0
tm = 0.03
speed_counter = 400 # для изменения скорости
trex = pyautogui.screenshot("trex.png",
                            region=(n, m, k, 45)) 
image = cv2.imread("trex.png")
image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
labeled = label(image) 
mx = labeled.max()            
pyautogui.press('Space') 
print(f"Dino побежал: {slp}")   
time.sleep(1)       
while True:      
    """Delai scrin """ 
    trex = pyautogui.screenshot("trex.png", 
                                region=(n, m, k, 45))
    image = cv2.imread("trex.png")    
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    labeled = label(image)
    if labeled.max() > mx:  
        pyautogui.press('up')
        time.sleep(slp) 
        pyautogui.keyDown('down')
        # time.sleep(0.03)
        pyautogui.keyUp('down')
        time.sleep(tm) 
        jump += 10 
        print(f"{jump//10} Прыжок")
        if jump == speed:
            slp -=0.01
            print('Смена тайма')
            print(slp,k) 
            if jump ==240:
                tm = 0.02
            if slp < 0.01: 
                slp = 0.01
            speed += 100
            if speed>speed_counter:
                k +=13
                tm = 0.001
                speed_counter += 150
                print('Переключение  передачи')
                print(slp,k,tm) 
             

    # tim e .sleep(0.3)                                                             
# # """# Box(left=643,      top=305, w idth=80,  height=84) 
## Box(left=89, top=355,   width=68, he ight=72)
# # """# print("Acces")    