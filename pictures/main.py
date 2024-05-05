import cv2

vid_capture = cv2.VideoCapture('pictures.avi')
if (vid_capture.isOpened() == False):
  print("Ошибка открытия видеофайла")

else:

  fps = vid_capture.get(5)
  print('Фреймов в секунду: ', fps,'FPS')
  frame_count = vid_capture.get(7)
  
  print('\n-----------------------------\nДля завершения нажмите "q" или Esc...')
file_count = 0
while(vid_capture.isOpened()):
  ret, frame = vid_capture.read()
  if ret == True: 
    gr = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # делаем в серый
    bl = cv2.medianBlur(gr, 5) # сделаю картинки менее четкими
    canny = cv2.Canny(bl, 150, 250) #делаю границы, подобрал значение для моей картинки
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
    closed = cv2.morphologyEx(canny, cv2.MORPH_CLOSE, kernel) #закрыть границы,чтобы проще находить
    contours = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0] # ищем контуры у фигур
    for cont in contours: 

        sm = cv2.arcLength(cont, True) 
        apd = cv2.approxPolyDP(cont, 0.0845*sm, True) # >85 сыпется  ||| - - |||  кол-во границ, подбором

        if len(apd) >5:#количество границ
            cv2.drawContours(frame, [apd], -1, (0,255,0), 4) # рисуем контур
            cv2.imshow('Look', closed) #выодим только мою картинку
            file_count += 1 #считаем
    
   
  
    key = cv2.waitKey(20)
    if (key == ord('q')) or key == 27:
      break
  else:
    break
print(f'Кол-во моей картинки = {file_count}')
vid_capture.release()
cv2.destroyAllWindows()