#
"""
Python GUI to upload dataset on Blackfynn with folder structure conserved
This program uses elements from the Blackfynn Python API available here:
    https://github.com/Blackfynn/blackfynn-python
"""

### Import required modules
from tkinter import *
from tkinter.ttk import *
from PyQt5 import *
from tkinter import filedialog
from blackfynn import Blackfynn
import os
from os import listdir, walk
from os.path import isfile, join
import threading

### Create GUI frame
window = Tk()
window.title("DOPE-Blackfynn-GUI")
window.geometry("900x700")


### Configure the "Select dataset" environment
# Title
x20 = 10
y20 = 10
labeltitle1 = Label(window, text="1. Select destination dataset on Blackfynn", font=("Arial Bold", 10))
labeltitle1.place(x = x20, y = y20)

# Define GUI elements    
bf = Blackfynn()
dataset_combobox = Combobox(window)
dataset_list = ['Select dataset']
for ds in bf.datasets():
    dataset_list.append(ds.name) 
dataset_combobox['values']= dataset_list
dataset_combobox.current(0)
x30 = x20
y30 = y20 + 30
dataset_combobox.place(x = x30, y = y30)



### Configure the "Select folder" environment
# Title
x40 = x30
y40 = y30 + 50
labeltitle1 = Label(window, text="2. Select local folder on your computer that you want to upload", font=("Arial Bold", 10))
labeltitle1.place(x = x40, y = y40)

#Define GUI actions
selected_folder = ""
def selectfolder():
    global selected_folder
    selected_folder = filedialog.askdirectory(parent=window, title='Choose a file')
    printstring = "You selected folder %s" %selected_folder
    selectfolder_label.configure(text=printstring)
    
# Define GUI elements    
selectfolder_button = Button(window, text="Select folder", command=selectfolder)
x50 = x40
y50 = y40 + 30
selectfolder_button.place(x = x50, y = y50)

selectfolder_label = Label(window, text="")
x51 = x50 + 150
y51 = y50
selectfolder_label.place(x = x51, y = y51)


### Configure the "Upload folder" environment
# Title
x60 = x50
y60 = y50 + 50
labeltitle1 = Label(window, text="3. Upload your folder with structure conserved", font=("Arial Bold", 10))
labeltitle1.place(x = x60, y = y60)

#Define GUI actions
def uploadfolder():
    def calluploadfolder():
        uploadstatus_label.configure(text = "Uploading...")
        uploadwarning_label.configure(text = "")
        uploadfolder_text.delete('1.0', END)
        uploadfolder_text.insert(END, "Upload progress will be shown here \n")
        uploadfolder_text.insert(END, "" + "\n")
        uploadfolder_text.insert(END, "Started uploading to dataset %s \n" %(dataset_combobox.get()) )
        myds = bf.get_dataset(dataset_combobox.get())
        myfolder = myds.name
        mypath = selected_folder
        upload_structured_file(myds, mypath, myfolder, 0)
        uploadfolder_text.insert(END, "" + "\n")
        uploadfolder_text.insert(END, "Folder and associated files have been uploaded" + "\n")
        uploadstatus_label.configure(text = "Done!")
        uploadwarning_label.configure(text = "")
    
    if (dataset_combobox.get() == dataset_list[0]):
        uploadstatus_label.configure(text = "")
        uploadwarning_label.configure(text = "Please select a dataset")
        
    #elif ('selected_folder' not in vars() and 'selected_folder' not in globals()):
    #    uploadwarning_label.configure(text = "Please select a folder")
    elif (selected_folder==""):
        uploadstatus_label.configure(text = "")
        uploadwarning_label.configure(text = "Please select a folder")
        
    elif (uploadstatus_label["text"] == "Uploading..."):
        uploadwarning_label.configure(text = "Wait for current upload to finish")
        
    else:
        t = threading.Thread(target=calluploadfolder)
        t.start()
    
def upload_structured_file(myds, mypath, myfolder, foldercount):
    mypath = os.path.join(mypath)
    for f in listdir(mypath):
        if isfile(join(mypath, f)):  
            uploadfolder_text.insert(END, "Uploading " + f + " in " + myfolder + "\n")
            filepath = os.path.join(mypath, f)
            myds.upload(filepath)
            uploadfolder_text.insert(END, f + " uploaded" + "\n")
        else:
            uploadfolder_text.insert(END, "" + "\n")
            uploadfolder_text.insert(END, "Creating folder " + f + "\n")
            mybffolder = myds.create_collection(f)
            myfolderpath = os.path.join(mypath, f)
            foldercount += 1
            upload_structured_file(mybffolder, myfolderpath, f, foldercount)
        
# Define GUI elements    
uploadfolder_button = Button(window, text="Upload folder", command=uploadfolder)
x70 = x60
y70 = y60 + 30
uploadfolder_button.place(x = x70, y = y70)

uploadfolder_text = Text(window,  height=20, width=80)
uploadfolder_text.insert(END, "Upload progress will be shown here \n")
x71 = x70 + 180
y71 = y70
uploadfolder_text.place(x = x71, y = y71)

scrollb = Scrollbar(window, command= uploadfolder_text.yview)
uploadfolder_text.configure(yscrollcommand=scrollb.set)
scrollb.place(x = x71+650, y = y71)
#scrollb.grid(row=1,column=1,ipady=135)
scrollb.pack( side = RIGHT, fill = Y )

uploadstatus_label = Label(window, text="")
x80 = x70
y80 = y70 + 30
uploadstatus_label.place(x = x80, y = y80)

uploadwarning_label = Label(window, text="")
uploadwarning_label.config(foreground="red")
x90 = x80
y90 = y80 + 30
uploadwarning_label.place(x = x90, y = y90)


### End with this statement
window.mainloop()

