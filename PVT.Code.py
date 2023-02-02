import random
import time
from psychopy import core, visual, event



#Create Window
win = visual.Window(size=(1000, 600), color=(0, 0, 0.26), units="height")
state = True


def end():
    core.quit()
    

event.globalKeys.clear()
event.globalKeys.add(key='q', modifiers=['ctrl'], func=end)



while state:    
    #Create text 
    
    msg1 = visual.TextBox2(win, 
        text="Psycomotor Vigilance Test", 
        font="Open Sans", letterHeight=0.1,
        pos=(-0.3, 0.2)) 

    msg2 = visual.TextBox2(win, 
        text="Press Space To Begin", 
        font="Open Sans", letterHeight=0.05,
        pos=(0, -0.3)) 
        
    msg3 = visual.TextBox2(win, 
        text="Instructions: You will either see a red circle on the left or a blue circle on the right. If the red circle appears you have to click E as fast as possible. If the blue circle appears you have to click I as fast as possible. Good Luck!", 
        font="Open Sans", letterHeight=0.03,
        pos=(0, -0.1))   

    #Draw text to hidden buffer
    msg1.draw()
    msg2.draw()
    msg3.draw()

    # Show the hidden buffer
    win.flip()

    if 'escape' in event.waitKeys():
        core.quit()
    #Wait until Space bar is pressed 
    
    win.flip(clearBuffer=True) #clear buffer (clear screen)


    #THE ACTUAL TEST
    #create circles 
    redCircle = visual.Circle(win, radius=0.05, pos=(-0.5,0), fillColor='red')
    blueCircle = visual.Circle(win, radius=0.05, pos=(0.5,0), fillColor='blue')

    #create last message
    lastDuration = visual.TextBox2(win, 
            text= "Last: ", 
            font="Open Sans", letterHeight=0.05,
            pos=(0, 0.3)) 

    counter = 0 #counter for while loop 
    runs = random.randint(4, 6) #determines number of runs
    results = [] #array for results 

    #testing phase 
    while counter < runs:
        lastDuration.draw() #draw last text to hidden buffer
        win.flip() #display hidden buffer 
        side = random.randint(1,2) #determines WHERE circle apears
        randomWait = random.uniform(0.8, 6) #determines WHEN circle apears
        core.wait(randomWait) 
        
        duration = 0
        
        if side == 1:
            begin = time.time() #time of start 
            lastDuration.draw()
            redCircle.draw()
            win.flip()
            
            event.waitKeys(maxWait=2, keyList='e') #it waits max. 2s till E is pressed 
            end = time.time() #time of end
            duration = (begin - end) * -1
            
        else:
            #same as above (if side ==1).......
            begin = time.time()
            lastDuration.draw()
            blueCircle.draw()
            win.flip()
            event.waitKeys(maxWait=2, keyList='i')
            end = time.time()
            duration = (begin - end) * -1

        
        #write value of duration in result array 
        if duration < -2: #if not pressed 
            results.append(-1) 
        else:
            results.append(duration)
        
        win.flip(clearBuffer=True) #deleate contents of screen
        
        #update last duration of test text
        lastDuration = visual.TextBox2(win, 
            text= "Last: " + str(round(duration,2)), 
            font="Open Sans", letterHeight=0.05,
            pos=(0, 0.3)) 

        lastDuration.draw()
        counter += 1


    #Last Page
    win.flip(clearBuffer=True) #clear buffer (clear screen)

    #'header'
    res = visual.TextBox2(win, 
            text= "Your results:", 
            font="Open Sans", letterHeight=0.1,
            pos=(0.4, 0.4)) 

    res.draw()

    #print results of test 
    y = 0.3

    for x in results:
        
        r = visual.TextBox2(win, 
            text= str(round(x,2)), 
            font="Open Sans", letterHeight=0.03,
            pos=(0, y)) 
        y -= 0.1
        r.draw()
        




    combined = 0
    for x in results:
        combined += x


    avg = round((combined/len(results)),2)
    a = visual.TextBox2(win, 
            text= "Average reaction time: " + str(avg), 
            font="Open Sans", letterHeight=0.05,
            pos=(0, (y-0.1)))
    b = visual.TextBox2(win, 
            text= "Press space to start again or press escape to quit: ", 
            font="Open Sans", letterHeight=0.03,
            pos=(0, (y-0.2)))        
    a.draw()
    b.draw()



    win.flip()
    #write results to file
    file = open('MyFile.txt', 'w')
    for x in results:
        file.write(str(x) + ",")
    file.close()
    
    if 'escape' in event.waitKeys():
        core.quit()
    
    #Wait until Space bar is pressed 
    event.waitKeys(keyList='space') 


win.close()
core.quit()






