#!/usr/bin/python 

"""
Takes user input to create a task file for rendering and outputs 
Mac Terminal scrip to render a project with Autodesk 
"""


from Tkinter import *
import tkMessageBox


def createOutputMaya():
    """
    Creates the script in a message box using the parameters in the text field inputed by user
    """

    projName = str(projectName.get())
    file1 = str(fileName1.get())
    file2 = str(fileName2.get())
    file3 = str(fileName3.get())
    out = str(outputLocation.get())

    tkMessageBox.showinfo('Output', "/opt/Autodesk/backburner/cmdjob -jobName " 
	                    + projName + " -manager renderserver.falabs.rutgers.edu " 
                        + "-port 7347 -group Animlab -priority 50 -taskList" 
                        + "/var/folders/zz/zyxvpxvq6csfxvn_n004xgm4017bx1/T/" + projName 
                        +".txt -taskName 1 /Applications/Autodesk/maya2017/Maya.app/Contents/bin/Render" 
                        + " -r file -s %tp2 -e %tp3 " + "-proj /Volumes/render/backburner/" 
                        + file1 +  "/" + file2 + " -rd /Volumes/render/backburner/" 
                        + file1 +  "/" + file2 + "/" + out + " /Volumes/render/backburner/" 
                        + file1 +  "/" + file2 + "/" + file3 + ".mb\n")
    root.quit()


def createFile():
    """
    Creates a task file in /var/folders/zz/zyxvpxvq6csfxvn_n004xgm4017bx1/T/ 
    using the project name and the start and endframes inputed by the user
    """

    #Setup Variables
    fileName = projectName.get()
    start = int(startFrame.get())
    end = int(endFrame.get())
    line = []

    #Make sure it always starts on an odd frame
    if start%2 == 1:
        i = start
    else:
        i = start - 1

    #Creates the frame lines
    while i == end or i < end:
        line.append("frame" + str(i) + "-" + str(i+1) + "\t" + str(i) + "\t" + str(i+1))
        i = i + 2

    #Creates and writes the text file
    file1 = open('/var/folders/zz/zyxvpxvq6csfxvn_n004xgm4017bx1/T/' + fileName + '.txt', "w+")

    for x in line:
        file1.write(x + '\n')

    file1.close


def changeFunction(event):
    """
    Allows the user to change the what application the returned script will be for
    """

    tkMessageBox.showinfo('This Function is still in beta')


def createRender(event):
    """
    Runs the createFile and createOutput function with one button click
    """

    createFile()
    createOutputMaya()

def mayaRender():
    """
    Creates a window with labels and text filed, that take inputs based on the file 
    ment to be rendered, along with a button that runs the createRender method
    """

    #Create root window
    root = Tk()

    #Create labels to be placed in window
    label1 = Label(root, text="Give the project a name:")
    label2 = Label(root, text="Enter the name of your file inside backburner:")
    label3 = Label(root, text="Enter the project file name:")
    label4 = Label(root, text="Enter name of the .mb file")
    label5 = Label(root, text='Enter desired output location (default is "images")')
    label6 = Label(root, text="Enter start frame")
    label7 = Label(root, text="Enter end frame")
    
    #Create global variables so they can be used outside this method
    global projectName
    global fileName1
    global fileName2
    global fileName3
    global outputLocation
    global startFrame
    global endFrame

    #Create text fields to be placed in window
    projectName = Entry(root)
    fileName1 = Entry(root)
    fileName2 = Entry(root)
    fileName3 = Entry(root)
    outputLocation = Entry(root)
    startFrame = Entry(root)
    endFrame = Entry(root)

    #Create button to run createRender
    submit = Button(root, text="Submit")
    submit.bind("<Button-1>", createRender)

    #Menu to change function
    menu = Menu(root)
    root.config(menu=menu)
    submenu = Menu(menu)
    menu.add_cascade(label="Render Type(Beta)", menu=submenu)
    submenu.add_command(label = "Other")
    submenu.bind("<Button-1>", changeFunction)

    #place labels in window
    label1.grid(row=0, sticky=E)
    label2.grid(row=1, sticky=E)
    label3.grid(row=2, sticky=E)
    label4.grid(row=3, sticky=E)
    label5.grid(row=4, sticky=E)
    label6.grid(row=5, sticky=E)
    label7.grid(row=6, sticky=E)


    #place entry boxes in window
    projectName.grid(row=0, column=1)
    fileName1.grid(row=1, column=1)
    fileName2.grid(row=2, column=1)
    fileName3.grid(row=3, column=1)
    startFrame.grid(row=5, column=1)
    endFrame.grid(row=6, column=1)
    outputLocation.grid(row=4, column=1)

    #place button in window
    submit.grid(columnspan=2)

    #open root window
    root = mainloop()

def main():
    mayaRender()

if __name__ == "__main__":
    main()
