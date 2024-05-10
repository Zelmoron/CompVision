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
jump = 0  #подсчет прыжков
slp = 0.1 # время перовой паузы
k = 200    #дистанция до препятствия
speed = 200  #скорость дин0
speed_counter = 400 # для изменения скорости
trex = pyautogui.screenshot("trex.png",
                            region=(n, m, k, 45)) 
image = cv2.imread("trex.png")
image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
labeled = label(image)
mx = labeled.max()          
pyautogui.press('Space')
print(f"Dino побежал: {slp}")
# print(labeled.max())      
time.sleep(1)       
while True:      
    """Delai scrin """ 
    trex = pyautogui.screenshot("trex.png", 
                                region=(n, m, k, 45))
    image = cv2.imread("trex.png")    
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    labeled = label(image)
 
    if labeled.max() > mx:  
        pyautogui.press('space')
        time.sleep(slp) 
        pyautogui.press( 'down')
        time.sleep(0.2) 
        jump += 10 
        print(f"{jump//10} Прыжок")
    # if jump > speed:
    #     print('Переключение передачи')
    #     k +=5 
    #     speed += 100
    #     print(k)
    #     if speed > speed_counter:
    #         slp -=0.01
    #         print(slp)
    #         print('Смена тайма')
    #         speed_counter+=100
        if jump == speed:
            slp -=0.01
            print('Смена тайма')
            if slp < 0: 
                slp = 0
            speed += 100
            if speed>speed_counter:
                k +=15
                speed_counter += 150
                print('Переключение  передачи')
                 
                print(slp,k ) 
            

    # tim e .sleep(0.3)                                                             
# # """# Box(left=643,      top=305, w idth=80,  height=84) 
## Box(left=89, top=355,   width=68, he ight=72)
# # """# print("Acces")       