'''
Created on 11. July 2017
@author: resema

Tkinter widget exploration
'''

from numpy import *
from Tkinter import *
import regTrees

import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

def reDraw(tolS, tolN):
  reDraw.f.clf()
  reDraw.a = reDraw.f.add_subplot(111)
  reDraw.a.scatter(reDraw.rawDat[:,0].tolist(), reDraw.rawDat[:,1].tolist())
  reDraw.canvas.show()
  
def getInputs():
  try: tolN = int(tolNentry.get())
  except:
    tolN = 10
    print "enter Integer for tolN"
    # clear error and replace with default
    tolNentry.delete(0, END)
    tolNentry.insert(0, '10')
  try: tolS = float(tolSentry.get())
  except:
    tolS = 1.0
    print "enter Float for tolS"
    # clear error and replace with default
    tolSentry.delete(0, END)
    tolSentry.insert(0, '1.0')
  return tolN, tolS
  
def drawNewTree():
  tolN, tolS = getInputs()
  reDraw(tolS, tolN)
  
'''
GUI bootstrapping
'''
root = Tk()

# Label(root, text = "Plot Place Holder").grid(row=0, columnspan=3)
reDraw.f = Figure(figsize=(5,4), dpi=100)
reDraw.canvas = FigureCanvasTkAgg(reDraw.f, master=root)
reDraw.canvas.show()
reDraw.canvas.get_tk_widget().grid(row=0, columnspan=3)

Label(root, text="tolN").grid(row=1, column=0)
tolNentry = Entry(root)
tolNentry.grid(row=1, column=1)
tolNentry.insert(0,'10')

Label(root, text="tolS").grid(row=2, column=0)
tolSentry = Entry(root)
tolSentry.grid(row=2, column=1)
tolSentry.insert(0, '1.0')

Button(root, text="ReDraw", command=drawNewTree).grid(row=1, column=2, rowspan=3)

chkBtnVar = IntVar()
chkBtn = Checkbutton(root, text="Model Tree", variable=chkBtnVar)
chkBtn.grid(row=3, column=0, columnspan=2)

reDraw.rawDat = mat(regTrees.loadDataSet('sine.txt'))
reDraw.testDat = arange(min(reDraw.rawDat[:,0]), max(reDraw.rawDat[:,0]), 0.01)
# reDraw(1.0, 10)

root.mainloop()










