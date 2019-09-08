import pyautogui
screenWidth, screenHeight = pyautogui.size()
currentMouseX, currentMouseY = pyautogui.position()
print(screenWidth,screenHeight)
print(currentMouseX,currentMouseY)

#滑动右侧滑条从(1910,210)到(1910, 368)

# pyautogui.moveTo(1910, 210)
# pyautogui.dragTo(1910,368)

# 移动到某个起始位置
pyautogui.moveTo(544, 666)

# #  鼠标向右移动x像素
# pyautogui.moveRel(14, 0)

# 移动到某个结束位置
pyautogui.moveTo(1350, 666)

# pyautogui.moveTo(544, 1000)
# pyautogui.click()

# pyautogui.doubleClick()
# #  用缓动/渐变函数让鼠标2秒后移动到(500,500)位置
# #  use tweening/easing function to move mouse over 2 seconds.
# pyautogui.moveTo(1800, 500, duration=2, tween=pyautogui.easeInOutQuad)
# #  在每次输入之间暂停0.25秒
# pyautogui.typewrite('Hello world!', interval=0.25)  #输入文本
# pyautogui.press('esc')   #按下按键
# pyautogui.keyDown('shift')
# pyautogui.press(['left', 'left', 'left', 'left', 'left', 'left'])
# pyautogui.keyUp('shift')
# pyautogui.hotkey('ctrl', 'c')