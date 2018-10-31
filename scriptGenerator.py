"""
Allows user to select a .mb file and creates an Autodesk
script to render that file over a render farm.
"""


from Tkinter import *
import tkMessageBox
import subprocess
import Tkinter, Tkconstants, tkFileDialog


def createOutputMaya():
    """
    Creates the script for maya render and runs them in the terminal
    """
    global root
    global fileName
    projName = 'renderProject'
    fileSectionList = fileName.split("/")
    file1 = ""
    file2= ""
    file3 = fileName
    out = "/images"

    #Assigns filepaths to variables
    for i in range(5):
        if i == 0:
            file1 = fileSectionList[i]
        else:
            file1 = file1 + "/" + fileSectionList[i]

    for i in range(6):
        if i == 0:
            file2 = fileSectionList[i]
        else:
            file2 = file2 + "/" + fileSectionList[i]


    #Creates Script
    script = ("/opt/Autodesk/backburner/cmdjob -jobName render "
        + "-manager renderserver.falabs.rutgers.edu -port 7347 " 
        + "-group ProdLabSmall -priority 50 -taskList "
        + "/var/folders/zz/zyxvpxvq6csfxvn_n004xgm4017bx1/T/" + projName + ".txt "
        + "-taskName 1 /Applications/Autodesk/maya2017/Maya.app/Contents/bin/Render "
        + "-r file -s %tp2 -e %tp3 -proj " + file2 
        + " -rd " + file2 + out + "  " + file3)

    #Runs Script
    subprocess.call(script, shell=True)
    root.destroy()
    tkMessageBox.showinfo("Running", "Rendering Now")
    quit()


def createFile():
    """
    Creates a task file in /var/folders/zz/zyxvpxvq6csfxvn_n004xgm4017bx1/T/ 
    using the project name and the start and endframes inputed by the user
    """

    #Setup Variables
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
    file1 = open('/var/folders/zz/zyxvpxvq6csfxvn_n004xgm4017bx1/T/renderProject.txt', "w+")

    for x in line:
        file1.write(x + '\n')

    file1.close


def createRender(event):
    """
    Runs the createFile and createOutput function with one button click
    """
    createFile()
    createOutputMaya()


def frameSelect():
    global root
    global startFrame
    global endFrame

    #Clears window
    for widget in root.winfo_children():
        widget.destroy()

    #Creates labels
    label2 = Label(root, text="Enter Start Frame:")
    label3 = Label(root, text="Enter End Frame")

    #Create text fields to be placed in window
    startFrame = Entry(root)
    endFrame = Entry(root)

    #Create button to run createRender
    submit = Button(root, text="Submit")
    submit.bind("<Button-1>", createRender)

    #Creates a back button
    back = Button(root, text="Reselect")
    back.bind("<Button-1>", fileSelect)

    label2.grid(row=0, column=0)
    label3.grid(row=1, column=0)

    #place entry boxes in window
    startFrame.grid(row=0, column=1)
    endFrame.grid(row=1, column=1)

    #place button in window
    back.grid(row=2, column=0)
    submit.grid(row=2, column=1)



def fileSelect(event):
    """
    Creates files selection window and sets fileName to selected file
    """
    global fileName
    root.fileName = tkFileDialog.askopenfilename(initialdir = "/Volumes/render/backburner",
        title = "Select file",filetypes = (("mb files","*.mb"),("all files","*.*")))
    fileName = root.fileName

    #Quits program if no file is selected
    if fileName == '':
        quit()
    else:
        frameSelect()


def mayaRender():
    """
    Creates a window with labels and text filed, that take inputs based on the file 
    ment to be rendered, along with a button that runs the createRender method
    """

    #Create root window
    global root
    root = Tk("Render Farm")
    root.title("Render Farm")

    #Create labels to be placed in window
    label1 = Label(root, text="Select the file to render:")
    
    #Create global variables so they can be used outside this method
    global fileName
    global startFrame
    global endFrame

    #Create button to run createRender
    browse = Button(root, text="Browse")
    browse.bind("<Button-1>", fileSelect)

    #place labels in window
    label1.grid(row=0, column=0)

    #place button in window
    browse.grid(row=0, column=1)

    #open root window
    root = mainloop()


def main():
    mayaRender()
    

if __name__ == "__main__":
    main()
