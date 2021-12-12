#################################################################################
# logic:
#black screen 
#↓ 
#determine whether IR input is LOW  → HIGH： back to black screen
# ↓
#LOW: Start inference,take photo, display photo, classifying → HAND : wait, continue classifying
#↓
#OTHER: display the result on the screen, ask the user correct or not →CORRECT : store the result, throw rubbish, back to the start
#↓
#WRONG: ask the user to input correct result, store the result, throw rubbish, and back to the start

#################################################################################
import tkinter
import RPi.GPIO as GPIO
import time
import cv2
from PIL import Image, ImageTk
import os
import capture
#import inference
import IR
import tensorflow as tf
import numpy as np
from tensorflow.python.saved_model import signature_constants, tag_constants
from tensorflow.python.framework import convert_to_constants
#################################################################################
#Functions

# Read from IR sensor untill there is people detected
def continueDetecting(): 
    isDetected =False
    while isDetected ==False:
        time.sleep(0.5)
        isDetected ==IR.isPeoplePresent()

# Call camera to take photos, it would return an image
def camera(): 
    # Use the function in capture.py to initialize camera and take photos
    img = capture.capture_input()
    return img

# Convert the img from np.array format to the format used by tkinter
def convertImage(img):
    img = cv2.cvtColor(img ,cv2.COLOR_BGR2RGB)
    img = Image.fromarray(img)
    img =  ImageTk.PhotoImage(image=img)
    return img

# Display the photos taken on the canvas
def displayImageOnCanvas(display, app,img):
    img = convertImage(img)
    # Display the top view
    display.create_image(0, 0, anchor=tkinter.NW, image=img)
    # Display the side view
    display.create_image(512, 0, anchor=tkinter.NW, image=img)
    # Update the canvas to display the photos
    app.update_idletasks()
    app.update()

# Start the inference and call the model to classify the photos
# The photos will be classified into 7 groups
def classfication(display):
    #prediction =inference()
    count=0
    testpara1=['empyty','empty','empyty','empty','hand','hand','hand','hand','hand','empty','empyty','empty','hand','cardboard']
    prediction=testpara1[count]
    # wait until the camera detected object
    while True():
        # if there is no object in the box
        if prediction == "empty":
            emptyAttentionLabel = tkinter.Label(app,
                                       text = "Hand present\nPlease put the rubbish there and remove your hand",
                                       fg="black",bg="white",justify="left",anchor="e",pady=50,font=("Arial",25))
            emptyAttentionLabel.pack()
            while prediction == 'empty':
                count+=1
                img = camera() #take new photo
                displayImageOnCanvas(display,app,img)
                prediction =testpara1[count]
                time.sleep(1)
            emptyAttentionLabel.destroy()
        # if the user is holding the object
        elif prediction =="hand":
            handAttentionLabel = tkinter.Label(app,
                                       text = "Hand present\nPlease put the rubbish there and remove your hand",
                                       fg="black",bg="white",justify="left",anchor="e",pady=50,font=("Arial",25))
            handAttentionLabel.pack()
            while prediction == 'hand':
                count+=1
                img = camera(count) #take new photo
                displayImageOnCanvas(display,app,img)
                prediction =testpara1[count]
                time.sleep(1)
            handAttentionLabel.destroy()
        else:
            # once the detection is not hand or empty, get out of the loop
            break
        return [prediction,img]

# Ask the user if the prediction is correct or not
def askIfCorrect(display,prediction,img):
    # destory the canvas of previous stage
    display.destroy()
    displayText = "I detected "+prediction+"\nIs this correct?"
    # print result and ask if it is correct
    ResultLabel = tkinter.Label(app, 
                                       text = displayText,justify="left",
                                       fg="black",bg="white",padx=100,pady=100,font=("Arial",25))
    ResultLabel.pack()
    # Make two buttons, right and wrong
    # clear all the widgets created
    def cleanFrame():
        ResultLabel.destroy()
        correctButton.destroy()
        wrongButton.destroy()
    # if the user says the result is correct
    def correct():
        cleanFrame()
        thankYou()
    # if the user says the result is wrong
    def wrong():
        cleanFrame()
        askForCorrection(img)
    # create the two buttons and put them onto the window
    correctButton=tkinter.Button(app,text="correct",command =correct,font=("Arial",25))
    correctButton.pack()
    wrongButton=tkinter.Button(app,text="wrong",command =wrong,font=("Arial",25))
    wrongButton.pack()

# Call the motor to move the rubbish into the container
def throwRubbish():
    print("This function will call the motor")
    #Make sure your hand is away, the machine will start to operat

# print thank you at the end 
def thankYou():
    displayText="thankyou!\nPlease put you hand away,\n I am going move the rubbish into the container"
    thankLabel = tkinter.Label(app, 
                                       text = displayText,justify="left",
                                       fg="black",bg="white",font=("Arial",25))
    thankLabel.pack()
    throwRubbish()
    # return to the start page
    def after():
        thankLabel.destroy()
        loopEvent()    
    thankLabel.after(5000,after)
    

# Save image after classification
def saveImage(path,img):
    isNamed=False
    count=1
    # go through the files in the folder to avoid same name
    while isNamed==False:
        file = path+str(count)+".jpg"
        if os.path.isfile(file)==False:
            isNamed = True
            cv2.imwrite(file,img)
        count+=1

# If the user saysthe classification is wrong, 
# this function will ask the correct group
def askForCorrection(img):
    Foldername = "EdgeDataset"
    # Clean the frame
    def destroyAll():
        askLabel.destroy()
        paperButton.destroy()
        cardboardButton.destroy()
        metalButton.destroy()
        plasticButton.destroy()
        glassButton.destroy()
        thankYou()
    # Save the image into the folder of the group corrected by the user
    def paper():
        path=Foldername +"/paper/"
        saveImage(path,img)
        destroyAll()
    def cardboard():
        path=Foldername +"/cardboard/"
        saveImage(path,img)
        destroyAll()
    def metal():
        path=Foldername +"/metal/"
        saveImage(path,img)
        destroyAll()
    def plastic():
        path=Foldername +"/plastic/"
        saveImage(path,img)
        destroyAll()
    def glass():
        path=Foldername +"/glass/"
        saveImage(path,img)
        destroyAll()
    # display the question and the buttons
    askLabel = tkinter.Label(app, 
                                       text ="Oh,sorry. Which is the correct category?",justify="left",
                                       fg="black",bg="white",padx=100,pady=100,font=("Arial",25))
    askLabel.pack()
    paperButton=tkinter.Button(app,text="Paper",command=paper,font=("Arial",25))
    paperButton.pack()
    cardboardButton=tkinter.Button(app,text="Cardboard",command =cardboard,font=("Arial",25))
    cardboardButton.pack()
    metalButton=tkinter.Button(app,text="Metal",command =metal,font=("Arial",25))
    metalButton.pack()
    plasticButton=tkinter.Button(app,text="Plastic",command =plastic,font=("Arial",25))
    plasticButton.pack()
    glassButton=tkinter.Button(app,text="Glass",command =glass,font=("Arial",25))
    glassButton.pack()

# This function loops the classification program
def loopEvent():
    display = tkinter.Canvas(app,bg='black',width=1024,height=384)
    display.pack(side="top")
    continueDetecting()
    [prediction,img]= classfication(display)
    askIfCorrect(display,prediction,img)

#################################################################################

try:
    app = tkinter.Tk()
    #app.attributes('-fullscreen', True)#set to full screen
    app.geometry("1024x600")
    app.configure(bg='white')
    app.title('Waste Classification Programme') # set the name of the window
    loopEvent()
    app.mainloop()
finally:
    IR.cleanup()
    capture.release()

