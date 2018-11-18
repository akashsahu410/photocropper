#!/usr/bin/env python2
# -*- coding: utf-8 -*-

'''
import rpErrorHandler
import Tkinter
#------------------------------------------------------------------------------#
#                                                                              #
#                                 PhotoCropper                                 #
#                                                                              #
#------------------------------------------------------------------------------#
class PhotoCropper(Tkinter.Frame):
    def __init__(self,Master=None,*pos,**kw):
        kw['borderwidth'] = '5'
        kw['height'] = '1'
        kw['width'] = '1'
# This code was deliberately ugly in order to prevent Rapyd-Tk from being
# too smart

'''
import argparse
import logging
import os
import re
import sys

import configparser as confpars
import tkinter, tkinter.messagebox

from PIL import Image, ImageTk
    
class PhotoCropper(tkinter.Frame):
    def __init__(self, Master=None, *pos, **kw):
        kw['borderwidth'] = '5'
        kw['height'] = '1'
        kw['width'] = '1'
        #
        #Your code here
        #

        tkinter.Frame.__init__(*(self,Master), **kw)
        self.bind('<Configure>',self.on_PhotoCropper_Config)
        self.textStatus = tkinter.StringVar()
        self.frameFiles = tkinter.Frame(self,highlightcolor='darkred'
            ,highlightthickness='3',width='1')
        self.frameFiles.pack(anchor='nw',fill='y',side='left')
        self.sbFiles = tkinter.Scrollbar(self.frameFiles)
        self.sbFiles.pack(anchor='nw',fill='y',side='right')
        self.lbFiles = tkinter.Listbox(self.frameFiles,takefocus=1
            ,yscrollcommand=self.sbFiles.set)
        self.lbFiles.pack(anchor='nw',fill='y',side='right')
        self.lbFiles.bind('<ButtonRelease-1>',self.on_lbFiles_mouseClick_1)
        self.lbFiles.bind('<KeyRelease-Down>',self.lbFiles_ArrowDown)
        self.lbFiles.bind('<KeyRelease-Up>',self.lbFiles_ArrowUp)
        self.frameMain = tkinter.Frame(self,borderwidth='1',width='1')
        self.frameMain.pack(expand='yes',fill='both',side='left')
        self.framePicture = tkinter.Frame(self.frameMain,borderwidth='1'
            ,relief='raised')
        self.framePicture.pack(anchor='nw',expand='yes',fill='both',side='top')
        self.canvas = tkinter.Canvas(self.framePicture,borderwidth='1'
            ,highlightcolor='darkred',highlightthickness='3',takefocus=1)
        self.canvas.pack(anchor='nw',expand='yes',fill='both',side='bottom')
        self.canvas.bind('<B1-Motion>',self.canvas_mouseb1move_callback)
        self.canvas.bind('<Button-1>',self.canvas_mouse1_callback)
        self.canvas.bind('<ButtonRelease-1>',self.canvas_mouseup1_callback)
        self.canvas.bind('<KeyRelease-Down>',self.canvas_ArrowDown)
        self.canvas.bind('<Shift-KeyRelease-Down>',self.canvas_ArrowDown_Shift)
        self.canvas.bind('<KeyRelease-KP_Add>',self.canvas_KP_Add)
        self.canvas.bind('<KeyRelease-KP_Down>',self.canvas_KP_ArrowDown)
        self.canvas.bind('<Control-KeyRelease-KP_Down>' \
            ,self.canvas_KP_ArrowDown_Control)
        self.canvas.bind('<KeyRelease-KP_Enter>',self.canvas_KP_Enter)
        self.canvas.bind('<KeyRelease-KP_Left>',self.canvas_KP_ArrowLeft)
        self.canvas.bind('<Control-KeyRelease-KP_Left>' \
            ,self.canvas_KP_ArrowLeft_Control)
        self.canvas.bind('<KeyRelease-KP_Next>',self.canvas_KP_PageDown)
        self.canvas.bind('<KeyRelease-KP_Prior>',self.canvas_KP_PageUp)
        self.canvas.bind('<KeyRelease-KP_Right>',self.canvas_KP_ArrowRight)
        self.canvas.bind('<Control-KeyRelease-KP_Right>' \
            ,self.canvas_KP_ArrowRight_Control)
        self.canvas.bind('<KeyRelease-KP_Subtract>',self.canvas_KP_Subtract)
        self.canvas.bind('<KeyRelease-KP_Up>',self.canvas_KP_ArrowUp)
        self.canvas.bind('<Control-KeyRelease-KP_Up>' \
            ,self.canvas_KP_ArrowUp_Control)
        self.canvas.bind('<KeyRelease-Left>',self.canvas_ArrowLeft)
        self.canvas.bind('<Shift-KeyRelease-Left>',self.canvas_ArrowLeft_Shift)
        self.canvas.bind('<KeyRelease-Next>',self.canvas_PageDown)
        self.canvas.bind('<KeyRelease-Prior>',self.canvas_PageUp)
        self.canvas.bind('<KeyRelease-Return>',self.canvas_Return)
        self.canvas.bind('<KeyRelease-Right>',self.canvas_ArrowRight)
        self.canvas.bind('<Shift-KeyRelease-Right>' \
            ,self.canvas_ArrowRight_Shift)
        self.canvas.bind('<KeyRelease-Up>',self.canvas_ArrowUp)
        self.canvas.bind('<Shift-KeyRelease-Up>',self.canvas_ArrowUp_Shift)
        self.canvas.bind('<KeyRelease-space>',self.canvas_SPACE)
        self.frameButtons = tkinter.Frame(self.frameMain,borderwidth='1'
            ,height='1')
        self.frameButtons.pack(anchor='nw',fill='x',side='top')
        self.btnSettings = tkinter.Button(self.frameButtons,text='Settings ...')
        self.btnSettings.pack(anchor='sw',expand='yes',fill='x',side='left')
        self.btnSettings.bind('<ButtonRelease-1>',self.on_btnSettings_ButRel_1)
        self.resetButton = tkinter.Button(self.frameButtons
            ,activebackground='#F00',command=self.reset,text='Reset')
        self.resetButton.pack(anchor='sw',expand='yes',fill='x',side='left')
        self.undoButton = tkinter.Button(self.frameButtons
            ,activebackground='#FF0',command=self.undo_last,text='Undo')
        self.undoButton.pack(anchor='sw',expand='yes',fill='x',side='left')
        self.zoomButton = tkinter.Checkbutton(self.frameButtons
            ,command=self.zoom_mode,text='Zoom')
        self.zoomButton.pack(anchor='sw',expand='yes',fill='x',side='left')
        self.unzoomButton = tkinter.Button(self.frameButtons
            ,activebackground='#00F',command=self.unzoom_image,text='<-|->')
        self.unzoomButton.pack(anchor='sw',expand='yes',fill='x',side='left')
        self.plusButton = tkinter.Button(self.frameButtons,command=self.plus_box
            ,text='+')
        self.plusButton.pack(anchor='sw',expand='yes',fill='x',side='left')
        self.goButton = tkinter.Button(self.frameButtons,activebackground='#0F0'
            ,command=self.start_cropping,text='Crops')
        self.goButton.pack(anchor='sw',expand='yes',fill='x',side='left')
        self.quitButton = tkinter.Button(self.frameButtons
            ,activebackground='#F00',command=self.quit,text='Quit')
        self.quitButton.pack(anchor='sw',expand='yes',fill='x',side='left')
        self.quitButton.bind('<ButtonRelease-1>',self.on_quitButton_ButRel_1)
        self.frmStatus = tkinter.Frame(self.frameMain)
        self.frmStatus.pack(anchor='nw',fill='y',side='top')
        self.lblStatus = tkinter.Label(self.frmStatus,relief='sunken'
            ,text='This is label',textvariable=self.textStatus)
        self.lblStatus.pack(anchor='sw',expand='yes',fill='y',side='top')
        #
        #Your code here
        #
        self.sbFiles.config(command=self.lbFiles.yview)
        self.quitButton_ttp = CreateToolTip(self.quitButton, "Exit")
        self.resetButton_ttp = CreateToolTip(self.resetButton, "Reset all rectangles")
        self.undoButton_ttp = CreateToolTip(self.undoButton, "Undo last rectangle")
        self.zoomButton_ttp = CreateToolTip(self.zoomButton, "On/Off Zoom mode")
        self.unzoomButton_ttp = CreateToolTip(self.unzoomButton, "Unzoom, view all image")
        self.plusButton_ttp = CreateToolTip(self.plusButton, "Plus box, extent rectangle")
        self.goButton_ttp = CreateToolTip(self.goButton, "Go, begin cropping")
        self.btnInputDirSettings_ttp = CreateToolTip(self.btnSettings, "Settings")
        self.croprect_start = None
        self.croprect_end = None
        self.crop_count = 0
        self.canvas_rects = []
        self.crop_rects = []
        self.current_rect = None
        self.zoommode = False
        self.w = 1
        self.h = 1
        self.x0 = 0
        self.y0 = 0
        self.n = 0
        self.config = None
        self.delimiters = ' |,|\t|#|\|' # String delimiters
        self._after_id = None
        self.filename = None
        self.lbIndex = None # Keeps item index in listbox
        self.cropIndex = 0
    #
    #Start of event handler methods
    #


    def canvas_ArrowDown(self, event=None):
        # MOVES crop rectangle ONE pixel DOWN
        self.move_rect(self.cropIndex, 0, 1)

    def canvas_ArrowDown_Shift(self, event=None):
        # MOVES crop rectangle AMOUNT OF pixels DOWN
        self.move_rect(self.cropIndex, 0, int(self.config['move-resize-step']))

    def canvas_ArrowLeft(self, event=None):
        # MOVES crop rectangle ONE pixel LEFT
        self.move_rect(self.cropIndex, -1, 0)

    def canvas_ArrowLeft_Shift(self, event=None):
        # MOVES crop rectangle AMOUNT OF pixels LEFT
        self.move_rect(self.cropIndex, -int(self.config['move-resize-step']), 0)

    def canvas_ArrowRight(self, event=None):
        # MOVES crop rectangle ONE pixel RIGHT
        self.move_rect(self.cropIndex, 1, 0)

    def canvas_ArrowRight_Shift(self, event=None):
        # MOVES crop rectangle AMOUNT OF pixels RIGHT
        self.move_rect(self.cropIndex, int(self.config['move-resize-step']), 0)

    def canvas_ArrowUp(self, event=None):
        # MOVES crop rectangle ONE pixel UP
        self.move_rect(self.cropIndex, 0, -1)

    def canvas_ArrowUp_Shift(self, event=None):
        # MOVES crop rectangle AMOUNT OF pixels UP
        self.move_rect(self.cropIndex, 0, -int(self.config['move-resize-step']))

    def canvas_KP_Add(self, event=None):
        # INCREASES size of crop rectangle for AMOUNT OF pixels on both X- and Y-axes
        log.debug("Canvas keypress numerical keypad PLUS")
        self.resize_rect(self.cropIndex, int(self.config['move-resize-step']), int(self.config['move-resize-step']))

    def canvas_KP_ArrowDown(self, event=None):
        # INCREASES size of crop rectangle by ONE pixel on Y axes
        self.resize_rect(self.cropIndex, 0, 1)

    def canvas_KP_ArrowDown_Control(self, event=None):
        # INCREASES size of crop rectangle by AMOUNT OF pixels on Y axes
        self.resize_rect(self.cropIndex, 0, int(self.config['move-resize-step']))

    def canvas_KP_ArrowLeft(self, event=None):
        # DECREASES size of crop rectangle by ONE pixel on X axes
        self.resize_rect(self.cropIndex, -1, 0)

    def canvas_KP_ArrowLeft_Control(self, event=None):
        # DECREASES size of crop rectangle by AMOUNT OF pixels on X axes
        self.resize_rect(self.cropIndex, -int(self.config['move-resize-step']), 0)

    def canvas_KP_ArrowRight(self, event=None):
        # INCREASES size of crop rectangle ONE pixel on X axes
        self.resize_rect(self.cropIndex, 1, 0)

    def canvas_KP_ArrowRight_Control(self, event=None):
        # INCREASES size of crop rectangle AMOUNT OF pixels on X axes
        self.resize_rect(self.cropIndex, int(self.config['move-resize-step']), 0)

    def canvas_KP_ArrowUp(self, event=None):
        # DECREASES size of crop rectangle ONE pixel on Y axes
        self.resize_rect(self.cropIndex, 0, -1)

    def canvas_KP_ArrowUp_Control(self, event=None):
        # DECREASES size of crop rectangle AMOUNT OF pixels on Y axes
        self.resize_rect(self.cropIndex, 0, -int(self.config['move-resize-step']))

    def canvas_KP_Enter(self, event=None):
        # CROPS selected areas
        log.debug("Canvas keypress numerical keypad ENTER")
        self.start_cropping()

    def canvas_KP_PageDown(self, event=None):
        # Moves file selection in listbox one down
        log.debug("Canvas keypress numerical keypad Page Down")
        self.pressPage(self.MOVE_DOWN)

    def canvas_KP_PageUp(self, event=None):
        # Moves file selection in listbox one up
        self.pressPage(self.MOVE_UP)

    def canvas_KP_Subtract(self, event=None):
        # Reduces rectangle by AMOUNT OF pixels on both X- and Y-axes
        log.debug("Canvas keypress numerical keypad MINUS")
        self.resize_rect(self.cropIndex, -int(self.config['move-resize-step']), -int(self.config['move-resize-step']))

    def canvas_PageDown(self, event=None):
        # Moves file selection in listbox one DOWN
        log.debug("Canvas keypress Page Down")
        self.pressPage(self.MOVE_DOWN)

    def canvas_PageUp(self, event=None):
        # Moves file selection in listbox one UP
        log.debug("Canvas keypress Page Up")
        self.pressPage(self.MOVE_UP)

    def canvas_Return(self, event=None):
        # CROPS selected areas
        log.debug("Canvas keypress ENTER")
        self.start_cropping()

    def canvas_SPACE(self, event=None):
        # CROPS selected areas
        log.debug("Canvas keypress SPACE")
        self.start_cropping()

    def canvas_mouse1_callback(self, event=None):
        self.croprect_start = (event.x, event.y)
        log.debug("Crop rectangle START: x={0} y={1}".format(event.x, event.y))

    def canvas_mouseb1move_callback(self, event=None):
        if self.current_rect:
            self.canvas.delete(self.current_rect)
        x1 = self.croprect_start[0]
        y1 = self.croprect_start[1]
        x2 = event.x
        y2 = event.y
        bbox = (x1, y1, x2, y2)
        cr = self.canvas.create_rectangle(bbox)
        self.current_rect = cr

    def canvas_mouseup1_callback(self, event=None):
        self.croprect_end = (event.x, event.y)
        log.debug("Crop rectangle END: x={0} y={1}".format(event.x, event.y))
        self.set_crop_area()
        self.canvas.delete(self.current_rect)
        self.current_rect = None

    def lbFiles_ArrowDown(self, event=None):
        # Moves file selection in listbox one DOWN
        log.debug("Files listbox arrow DOWN")
        self.pressPage(self.MOVE_DOWN)

    def lbFiles_ArrowUp(self, event=None):
        # Moves file selection in listbox one UP
        log.debug("Files listbox arrow UP")
        self.pressPage(self.MOVE_UP)

    def on_PhotoCropper_Config(self, event=None):
        if self._after_id:
            self.after_cancel(self._after_id)
        self._after_id = self.after(1200, self.draw_after_resize)

    def on_btnSettings_ButRel_1(self, event=None):
        tkinter.messagebox.showinfo("Information", "Not yet implemented.", parent=self)

    def on_lbFiles_mouseClick_1(self, event=None):
        self.lbIndex = self.lbFiles.curselection()[0]
        log.debug("File listbox selected")
        self.load_lbFiles_image(self.lbFiles.get(self.lbIndex))

    def on_quitButton_ButRel_1(self, event=None):
        conf['geometry'] = self.winfo_toplevel().geometry()
        conf.save()
        log.debug("Clicked 'Quit' button")
        self.quit()
    #
    #Start of non-Rapyd user code
    #
    
    # Constants for listbox with image file names
    MOVE_UP = -1
    MOVE_DOWN = 1
    MOVE_RIGHT = 1
    MOVE_LEFT = -1
    
    # Moves rectangle with "index" by "step" pixels
    def move_rect(self, index, xstep, ystep):
        if len(self.crop_rects) == index + 1:
            cr = self.crop_rects[index]
            self.canvas.delete(self.canvas_rects[index])
            self.canvas_rects.pop(index)
            self.crop_rects[index] = cr.move_rect(xstep, ystep)
            log.debug("Crop area moved: index={0} crop={1}".format(index, self.crop_rects[index]))
            self.redraw_rect()

    def resize_rect(self, index, xstep, ystep):
        if len(self.crop_rects) == index + 1:
            cr = self.crop_rects[index]
            self.canvas.delete(self.canvas_rects[index])
            self.canvas_rects.pop(index)
            self.crop_rects[index] = cr.resize_rect(xstep, ystep)
            log.debug("Crop area resized: index={0} crop={1}".format(index, self.crop_rects[index]))
            self.redraw_rect()
        
    def pressPage(self, direction=0):
        index = self.lbFiles.curselection()[0] + direction
        self.lbFiles.selection_clear(0, tkinter.END)
        self.lbSelect(index)
        # Move scrollbar in listbox so that it corresponds to selection
        self.lbFiles.yview_scroll(direction, 'units')

    # Programmatically select image in a listbox
    def lbSelect(self, index):
        if index < 0:
            index = 0
        elif index == self.lbFiles.size():
            index = self.lbFiles.size()-1  
        self.lbFiles.select_set(index)
        self.lbFiles.activate(index)
        log.debug("lbSelect: Got index {0}, listbox index {1}".format(index, self.lbIndex))
        if index != self.lbIndex:
            self.load_lbFiles_image(self.lbFiles.get(tkinter.ACTIVE))
            self.lbIndex = index
        
    def draw_after_resize(self):
        # Check if there is a selection in file list
        if self.filename:
            self.loadimage()
 
    def load_lbFiles_image(self, imagePath):
        self.filename = os.path.join(self.config['input-directory'], imagePath)
        if os.path.exists(self.filename):
            self.loadimage()
            self.winfo_toplevel().title('Photo Cropper - ' + imagePath)
            self.redraw_rect()
       
    def set_crop_area(self):
        r = Rect(self.croprect_start, self.croprect_end)
        r.set_thumboffset(int(self.config['thumb-offset']))
        
        # adjust dimensions
        r.clip_to(self.image_thumb_rect)

        # ignore rects smaller than this size
        if min(r.h, r.w) < 10:
            return

        ra = r
        ra = ra.scale_rect(self.scale)
        ra = ra.move_rect(self.x0, self.y0)
        ra = ra.valid_rect(self.w, self.h)
        if self.zoommode:
            self.canvas.delete(tkinter.ALL)
            self.x0 = ra.left
            self.y0 = ra.top
            za = (ra.left, ra.top, ra.right, ra.bottom)
            self.image_thumb = self.image.crop(za)
            self.image_thumb.thumbnail(thumbsize)
            self.image_thumb_rect = Rect(self.image_thumb.size)
            self.image_thumb_rect.set_thumboffset(int(self.config['thumb-offset']))
            self.displayimage()
            x_scale = float(ra.w) / self.image_thumb_rect.w
            y_scale = float(ra.h) / self.image_thumb_rect.h
            self.scale = (x_scale, y_scale)
            self.redraw_rect()
            self.zoommode = False
            self.zoomButton.deselect()
        else:
            self.drawrect(r)
            self.crop_rects.append(ra)
            self.n = self.n + 1

    def zoom_mode(self):
        if self.zoommode:
            self.zoommode = False
        else:
            self.zoommode = True
        log9.debug("Zoom mode: {0}".format(self.zoommode))

    def unzoom_image(self):
        self.canvas.delete(tkinter.ALL)
        self.zoommode = False
        self.zoomButton.deselect()
        self.x0 = 0
        self.y0 = 0
        self.image_thumb = self.image.copy()
        self.image_thumb.thumbnail(thumbsize)
        self.image_thumb_rect = Rect(self.image_thumb.size)
        self.image_thumb_rect.set_thumboffset(int(self.config['thumb-offset']))
        self.displayimage()
        x_scale = float(self.image_rect.w) / self.image_thumb_rect.w
        y_scale = float(self.image_rect.h) / self.image_thumb_rect.h
        self.scale = (x_scale, y_scale)
        self.redraw_rect()

    def plus_box(self):
        if self.n > 1:
            self.canvas.delete(tkinter.ALL)
            if self.crop_rects:
                ra = self.crop_rects[self.n - 1]
                self.crop_rects.pop()
                self.n = self.n - 1
                ra0 = self.crop_rects[self.n - 1]
                ra0 = ra0.plus_rect(ra)
                self.crop_rects[self.n - 1] = ra0
                self.displayimage()
                self.redraw_rect()
                self.zoommode = False
                self.zoomButton.deselect()

    def redraw_rect(self):
        self.displayimage()
        for croparea in self.crop_rects:
            self.drawrect(croparea.rescale_rect(self.scale, self.x0, self.y0))

    def undo_last(self):
        if self.canvas_rects:
            r = self.canvas_rects.pop()
            self.canvas.delete(r)

        if self.crop_rects:
            self.crop_rects.pop()

    def drawrect(self, rect):
        bbox = (rect.left, rect.top, rect.right, rect.bottom)
        cr = self.canvas.create_rectangle(
            bbox, activefill='', fill='yellow', stipple=self.config['stipple'])
        self.canvas_rects.append(cr)

    def reset(self):
        self.canvas.delete(tkinter.ALL)
        self.zoommode = False
        self.zoomButton.deselect()
        self.canvas_rects = []
        self.crop_rects = []
        self.displayimage()
        log.debug("Canvas reset")
        
    def displayimage(self):
        self.photoimage = ImageTk.PhotoImage(self.image_thumb)
        w, h = self.image_thumb.size
        self.canvas.delete("all") # Remove remnants of previous crop area
        
        self.canvas.create_image(
            int(self.config['thumb-offset']),
            int(self.config['thumb-offset']),
            anchor=tkinter.NW,
            image=self.photoimage)

    def loadimage(self):
        self.image = Image.open(self.filename)
        self.textStatus.set("{0} size {1}".format(os.path.basename(self.filename), self.image.size))
        log.debug("Loaded '{0}', size {1}".format(os.path.basename(self.filename), self.image.size))
        self.image_rect = Rect(self.image.size)
        self.image_rect.set_thumboffset(int(self.config['thumb-offset']))
        self.w = self.image_rect.w
        self.h = self.image_rect.h
        # TODO: needed? borderwidth = self.canvas.config()['borderwidth'][4]
        
        self.image_thumb = self.image.copy()
        self.image_thumb.thumbnail(
            [ self.canvas.winfo_width() - int(self.config['thumb-offset']),
              self.canvas.winfo_height() - int(self.config['thumb-offset']) ]
        )
        self.image_thumb_rect = Rect(self.image_thumb.size)
        self.image_thumb_rect.set_thumboffset(int(self.config['thumb-offset']))

        self.displayimage()
        x_scale = float(self.image_rect.w) / self.image_thumb_rect.w
        y_scale = float(self.image_rect.h) / self.image_thumb_rect.h
        self.scale = (x_scale, y_scale)

    def newfilename(self, filenum):
        f, e = os.path.splitext(self.filename)
        return '%s_crop_%s%s' % (f, filenum, e)

    def start_cropping(self):
        cropcount = 0
        status = "CROPPED {0} - region(s): ".format(self.lbFiles.get(tkinter.ACTIVE))
        for croparea in self.crop_rects:
            cropcount += 1
            filename = self.newfilename(cropcount)
            _, tail = os.path.split(filename) # Remove input directory
            self.crop(croparea, tail)
            status += "{0}:{1} ".format(cropcount, croparea)
        if cropcount != 0:
            self.textStatus.set(status.strip())

    def crop(self, croparea, filename):
        ca = (croparea.left, croparea.top, croparea.right, croparea.bottom)
        newimg = self.image.crop(ca)
        imagePath = os.path.join(self.config['output-directory'], filename)
        log.debug("Cropping area {0} of '{1}' to '{2}'".format(ca, os.path.basename(self.filename), imagePath))
        newimg.save(imagePath)
        
    def load_image_list(self):
        if self.config is not None:
            self.lbFiles.delete(0, tkinter.END)
            suffixtuple = tuple(re.split(self.delimiters, self.config['image-extensions']))
            for item in sorted(os.listdir(self.config['input-directory'])):
                if os.path.isfile(os.path.join(self.config['input-directory'], item)):
                    if item.lower().endswith(suffixtuple): # The arg can be a tuple of suffixes to look for
                        self.lbFiles.insert(tkinter.END, item)
            self.update_idletasks()
            # If there are items in listbox, select the 1st one
            if self.lbFiles.size() > 0:
                self.lbFiles.select_set(0)
                self.load_lbFiles_image(self.lbFiles.get(tkinter.ACTIVE))
                self.canvas.focus_set()


class CreateToolTip(object):
    """
    create a tooltip for a given widget
    """
    def __init__(self, widget, text='widget info'):
        self.waittime = 500     #miliseconds
        self.wraplength = 180   #pixels
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)
        self.widget.bind("<ButtonPress>", self.leave)
        self.id = None
        self.tw = None

    def enter(self, event=None):
        self.schedule()

    def leave(self, event=None):
        self.unschedule()
        self.hidetip()

    def schedule(self):
        self.unschedule()
        self.id = self.widget.after(self.waittime, self.showtip)

    def unschedule(self):
        id = self.id
        self.id = None
        if id:
            self.widget.after_cancel(id)

    def showtip(self, event=None):
        x = y = 0
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        # creates a toplevel window
        self.tw = tkinter.Toplevel(self.widget)
        # Leaves only the label and removes the app window
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry("+%d+%d" % (x, y))
        label = tkinter.Label(self.tw, text=self.text, justify='left',
            background="#fef9e7", relief='solid', borderwidth=1,
            wraplength = self.wraplength)
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tw
        self.tw= None
        if tw:
            tw.destroy()
            
class Rect(object):
    def __init__(self, *args):
        self.set_points(*args)
        self.thumboffset = 0

    def set_points(self, *args):
        if len(args) == 2:
            pt1 = args[0]
            pt2 = args[1]
        elif len(args) == 1:
            pt1 = (0, 0)
            pt2 = args[0]
        elif len(args) == 0:
            pt1 = (0, 0)
            pt2 = (0, 0)

        x1, y1 = pt1
        x2, y2 = pt2

        self.left = min(x1, x2)
        self.top = min(y1, y2)
        self.right = max(x1, x2)
        self.bottom = max(y1, y2)

        self._update_dims()

    def clip_to(self, containing_rect):
        cr = containing_rect
        self.top = max(self.top, cr.top + self.thumboffset)
        self.bottom = min(self.bottom, cr.bottom + self.thumboffset)
        self.left = max(self.left, cr.left + self.thumboffset)
        self.right = min(self.right, cr.right + self.thumboffset)
        self._update_dims()

    def _update_dims(self):
        """added to provide w and h dimensions."""
        self.w = self.right - self.left
        self.h = self.bottom - self.top

    def scale_rect(self, scale):
        x_scale = scale[0]
        y_scale = scale[1]

        r = Rect()
        r.top = int((self.top - self.thumboffset) * y_scale)
        r.bottom = int((self.bottom - self.thumboffset) * y_scale)
        r.right = int((self.right - self.thumboffset) * x_scale)
        r.left = int((self.left - self.thumboffset) * x_scale)
        r._update_dims()

        return r

    def move_rect(self, x0, y0):
        r = Rect()
        r.top = int(self.top + y0)
        r.bottom = int(self.bottom + y0)
        r.right = int(self.right + x0)
        r.left = int(self.left + x0)
        r._update_dims()
        return r

    # Resize rectangle by certain amount on X- and Y- axis
    def resize_rect(self, x0, y0):
        r = Rect()
        r.top = self.top
        r.left = self.left
        r.bottom = int(self.bottom + y0)
        r.right = int(self.right + x0)
        # Make sure rectangle does not disappear!
        if r.bottom - r.top < 10:
            r.bottom = self.bottom
        if r.right - r.left < 10:
            r.right = self.right
        r._update_dims()
        return r
        
    def rescale_rect(self, scale, x0, y0):
        x_scale = scale[0]
        y_scale = scale[1]

        r = Rect()
        r.top = int((self.top - y0) / y_scale + self.thumboffset)
        r.bottom = int((self.bottom - y0) / y_scale + self.thumboffset)
        r.right = int((self.right - x0) / x_scale + self.thumboffset)
        r.left = int((self.left - x0) / x_scale + self.thumboffset)
        r._update_dims()
        return r

    def plus_rect(self, r0):
        r = Rect()
        r.top = min(self.top, r0.top)
        r.bottom = max(self.bottom, r0.bottom)
        r.right = max(self.right, r0.right)
        r.left = min(self.left, r0.left)
        r._update_dims()
        return r

    def valid_rect(self, w, h):
        r = Rect()
        r.top = self.top
        if r.top < 0:
            r.top = 0
        if r.top > h - 1:
            r.top = h - 1
        r.bottom = self.bottom
        if r.bottom < 1:
            r.bottom = 1
        if r.bottom > h:
            r.bottom = h
        r.right = self.right
        if r.right < 1:
            r.right = 1
        if r.right > w:
            r.right = w
        r.left = self.left
        if r.left < 0:
            r.left = 0
        if r.left > w - 1:
            r.left = w - 1
        r._update_dims()
        return r

    def set_thumboffset(self, thumboffset=0):
        self.thumboffset = thumboffset

    def __repr__(self):
        return '(%d,%d)-(%d,%d)' % (self.left, self.top, self.right, self.bottom)

# Class that handles configuration
class ScanConfig(object):

    def __init__(self, configFile=None, appName='PhotoCropper'):
        self.section = appName.upper()
        
        if configFile is None:
            # Create default configuration in OS-independent "home" directory
            configPath = os.path.join(os.path.expanduser('~'), '.config', appName.lower())
            if not os.path.exists(configPath):
                os.makedirs(configPath)
                log.debug("Created default configuration path: '{0}'".format(configPath))

            self.configFile = os.path.join(configPath, 'config.ini')
            log.debug("Loaded configuration from file: '{0}'".format(self.configFile))
            self.config = confpars.SafeConfigParser(self.get_default_config())
            
            if os.path.exists(self.configFile):
                self.config.read(self.configFile)
            else:
                self.config.add_section(self.section)
        elif os.path.exists(configFile):
            self.configFile = os.path.normpath(configFile)
            self.config = confpars.SafeConfigParser(self.get_default_config())
            self.config.read(self.configFile)
            log.debug("Loaded configuration from file: '{0}'".format(self.configFile))
        else:
            # Path given, but does not exist
            raise Exception("Configuration file '{0}' does not exist".format(configFile))
        self.debug()

    # Gets default configuration
    def get_default_config(self):
        defconf = {
            'geometry'         : '1024x768+10+10', # Position and size of main window
            'input-directory'  : os.path.expanduser('~'), # Directory with pictures to process
            'output-directory' : os.path.expanduser('~'), # Directory to write resulting pictures into
            'image-extensions' : 'tif tiff jpg jpeg gif png', # Extensions of files considered to be pictures
            'thumb-offset'     : '4', # Thumbnail offset from edge of canvas
            'stipple'          : 'gray12', # Stipple pattern ("net" that shows in crop area)
            'move-resize-step' : '10', # Amount of pixels to move crop area in all directions or resize
        }
        log.debug("Default configuration: {0}".format(defconf))
        return defconf

    def __getitem__(self, key):
        return self.config.get(self.section, key)

    def __setitem__(self, key, value):
        self.config.set(self.section, key, value)

    def save(self):
        with open(self.configFile, 'w') as cf:
            self.config.write(cf)
            log.debug("Configuration saved to file '{0}'".format(self.configFile))
            
    def debug(self):
        for section_name in self.config.sections():
            log.debug("Section: [{0}]".format(section_name))
            for name, value in self.config.items(section_name):
                log.debug("  {0} = {1}".format(name, value))
            log.debug("")

pass #---end-of-form---
#------------------------------------------------------------------------------#
#                                                                              #
#                                 Preferences                                  #
#                                                                              #
#------------------------------------------------------------------------------#
class Preferences(tkinter.Frame):
    def __init__(self,Master=None,*pos,**kw):
        #
        #Your code here
        #

        tkinter.Frame.__init__(*(self,Master), **kw)
        self._Frame2 = tkinter.Frame(self)
        self._Frame2.pack(side='top')
        self._Frame1 = tkinter.Frame(self)
        self._Frame1.pack(side='top')
        #
        #Your code here
        #
    #
    #Start of event handler methods
    #

    #
    #Start of non-Rapyd user code
    #


pass #---end-of-form---

def window_close():
    conf['geometry'] = Root.geometry()
    conf.save() # Save configuration to keep window geometry
    Root.destroy()

try:
    #--------------------------------------------------------------------------#
    # User code should go after this comment so it is inside the "try".        #
    #     This allows rpErrorHandler to gain control on an error so it         #
    #     can properly display a Rapyd-aware error message.                    #
    #--------------------------------------------------------------------------#

    # Adjust sys.path so we can find other modules of this project
    if '.' not in sys.path:
        sys.path.append('.')
    #Put lines to import other modules of this project here
 
    if __name__ == '__main__':
        # Parse arguments
        parser = argparse.ArgumentParser(description='Picture cropper')
        parser.add_argument('-c', '--config', '--config-file', dest='configFile', default=None, help='Configuration file path')
        parser.add_argument('-d', '--debug', default=False, action="store_true", dest="debug", help='Show debugging information')
        parser.add_argument('-i', '--input-dir', '--input-directory', dest="inputDir", default=None, help='Input directory with pictures to be cropped')
        parser.add_argument('-o', '--output-dir', '--output-directory', dest="outputDir", default=None, help='Output directory for storing cropped pictures')
        args = parser.parse_args()
        
        logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)
        log = logging.getLogger('Photo Cropper')
        if args.debug:
            log.setLevel(logging.DEBUG)
        log.debug(args)
        
        '''

        Root = Tkinter.Tk()
        Tkinter.CallWrapper = rpErrorHandler.CallWrapper
        App = PhotoCropper(Root)
        App.pack(expand='yes',fill='both')

        '''
        Root = tkinter.Tk()
        App = PhotoCropper(Root)
        App.pack(expand='yes', fill='both')
        # Load configuration
        conf = ScanConfig(args.configFile, App.__class__.__name__)
        
        # Process input parameters
        if args.inputDir is not None:
            # Check if input dir exists
            if os.path.isdir(args.inputDir):
                conf['input-directory'] = args.inputDir
            else:
                log.error("Value for input directory '{0}' is not a directory".format(args.inputDir))
                exit(1)
        
        if args.outputDir is not None:
            # Check if output dir exists
            if os.path.isdir(args.outputDir):
                conf['output-directory'] = args.outputDir
            else:
                log.error("Value for output directory '{0}' is not a directory".format(args.outputDir))
                exit(1)

        # Set window
        Root.geometry(conf['geometry'])
        # Allow closing windows by clicking "X"
        Root.protocol("WM_DELETE_WINDOW", window_close)
        Root.title('Photo Cropper')
        App.config = conf
        App.load_image_list()
        Root.mainloop()
    #--------------------------------------------------------------------------#
    # User code should go above this comment.                                  #
    #--------------------------------------------------------------------------#
except:
    '''
    rpErrorHandler.RunError()
    '''
    raise