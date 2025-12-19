import pyqtgraph as pg
from pyqtgraph import QtCore
import numpy as np
import json

class LivePlot(): 
    def __init__(self, rd_data, colormap='viridis', window_title='Range-Doppler Map', width=800, height=800): 
        self.rd_data = rd_data # Stores the list of Range-Doppler matrices to display
        self.index = 0 # Current frame index for animation

        self.app = pg.mkQApp(window_title)
        self.win = pg.GraphicsLayoutWidget(show=True)
        self.win.setWindowTitle(window_title)
        self.win.resize(width, height)

        self.plot = self.win.addPlot()
        self.img = pg.ImageItem(self.rd_data[self.index]) # Initializes the image with the first RD frame
        self.plot.addItem(self.img) # Adds the image to the plot


        color_map = pg.colormap.get(colormap)
        self.bar = pg.ColorBarItem(colorMap=color_map, interactive=False) # Creates a non-interactive color bar
        self.bar.setImageItem(self.img, insert_in=self.plot)

        self.timer = QtCore.QTimer() # Creates a timer to update the image periodically
        self.timer.timeout.connect(self.update) # Connects the timer to the update function
        self.timer.start(100) # Starts the timer with a 10ms interval between updates

    def update(self): # Must check if the index is within the bounds of the list
        if self.index < len(self.rd_data):
            self.img.setImage(self.rd_data[self.index])
            print(f"Frame: {self.index}")
            self.index += 1
        else:
                  self.timer.stop() # Stops the timer when the last frame is reached
    def start(self):
            pg.exec()  # Starts the GUI event loop