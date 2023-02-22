import random
import time
from psychopy import core, visual, event
from psychopy import gui

file = open('MyFile.txt', 'w')

#Create Window
win = visual.Window(size=(1000, 600), color=(0, 0, 0.26), units="height")
state = True

#print results of test
y = 0.3 #y index for positioning on screen

def end():
    core.quit()

event.globalKeys.clear()
event.globalKeys.add(key='q', modifiers=['ctrl'], func=end)

#Create Welcome Text
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
    
#Initialize last round message
lastDuration = visual.TextBox2(win,
    text= "Last: ",
    font="Open Sans", letterHeight=0.05,
    pos=(0.28, 0.3))
    
#Header for result screen
txtres = visual.TextBox2(win,
    text= "Your results:",
    font="Open Sans", letterHeight=0.1,
    pos=(0.05, 0.4))
    
txtdecision = visual.TextBox2(win,
    text= "Press space to start again or press escape to quit.",
    font="Open Sans", letterHeight=0.03,
    pos=(0.05, (y-0.7)))

while state:
    #Draw text to hidden buffer
    msg1.draw()
    msg2.draw()
    msg3.draw()

    # Show the hidden buffer
    win.flip()

    if 'escape' in event.waitKeys():
        core.quit()
    #Wait until Space bar is pressed
    
    myDlg = gui.Dlg(title="JWP's experiment")
    myDlg.addText('Subject info')
    myDlg.addField('Name:')
    myDlg.addField('Age:')
    myDlg.addField('Gender:', choices=["Male", "Female", "Divers"])
    data = myDlg.show()  # show dialog and wait for OK or Cancel
    
    if myDlg.OK:  # or if ok_data is not None
        #THE ACTUAL TEST
    
        #create circles
        redCircle = visual.Circle(win, radius=0.05, pos=(-0.5,0), fillColor='red')
        blueCircle = visual.Circle(win, radius=0.05, pos=(0.5,0), fillColor='blue')

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
           
            begin = time.time() #time of start 
            lastDuration.draw()
            
            if side == 1:
                redCircle.draw()
                win.flip()
                event.waitKeys(maxWait=2, keyList='e') #it waits max. 2s till E is pressed
            else:
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

            #update last duration of test in textbox defined at top 
            lastDuration = visual.TextBox2(win,
                text= "Last: " + str(round(duration,2)),
                font="Open Sans", letterHeight=0.05,
                pos=(0.28, 0.3))

            lastDuration.draw()
            counter += 1
    else:
        print('user cancelled')

    win.flip(clearBuffer=True) #clear buffer (clear screen)

    #Last Page
    win.flip(clearBuffer=True) #clear buffer (clear screen)
    
    txtres.draw()

    for x in results:
        r = visual.TextBox2(win,
            text= str(round(x,2)),
            font="Open Sans", letterHeight=0.03,
            pos=(0.33, y))
        y -= 0.1
        r.draw()
    y = 0.3

    combined = 0
    for x in results:
        combined += x

    avg = round((combined/len(results)),2)
    txtavg = visual.TextBox2(win,
            text= "Average reaction time: " + str(avg),
            font="Open Sans", letterHeight=0.05,
            pos=(0.05, (y-0.6)))
  
    txtavg.draw()
    txtdecision.draw()

    win.flip()
    
    print(data)
    
    #write results to file    
    file.write("Name: " +  str(data[0]) + "\n")
    file.write("Age: " +  str(data[1]) + "\n")
    file.write("Gender: " +  str(data[2]) + "\n")
    file.write("Average Reaction time: " +  str(avg) + "\n")
    
    i = 0
    for x in results:
        file.write(str(i) + "----" + str(x) + ",\n")
        i += 1
    
    file.write("------------------\n")
    
    if 'escape' in event.waitKeys():
        core.quit()

    #Wait until Space bar is pressed
    event.waitKeys(keyList='space')

win.close()
core.quit()
file.close()





