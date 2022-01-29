# -*- coding: utf-8 -*-
"""=== Face Analyzer Helpers =>
    Module : ui
    Author : Saifeddine ALOUI (ParisNeo)
    Licence : MIT
    Description :
        User interface helpers
<================"""
import time
import pygame
import cssutils
from FaceAnalyzer.helpers.geometry.euclidian import is_point_inside_rect
from FaceAnalyzer.helpers.ui.pygame.colors import get_color
# Widgets
from dataclasses import dataclass
from urllib.request import urlopen

import numpy as np
import io

# Initialize font
pygame.font.init()

# Define orientations
Horizontal  = 0
Vertical    = 1

@dataclass
class WidgetStyle:
    """Class for keeping track widget styling information.
        font: The font to use for the text.
        bg_color: The background color.
        border_color: The color of the border.
        text_color: The color of the text.
        border_size: The size of the border.
        font_name: The name of the font.
        font_size: The size of the font.
        x_margin: The margin on the x-axis.
        y_margin: The margin on the y-axis.
        width: The width of the widget.
        height: The height of the widget.
        align: The alignment of the text.
        img: The image to use for the widget.   
  
    """
    font : pygame.font.Font = pygame.font.Font('freesansbold.ttf', 14)
    bg_color: tuple = (100,100,100)
    border_color: tuple =(0,0,0)
    border_radius: float = 0
    text_color: tuple = (0,0,0)
    border_size: int = 0
    font_name: str = 'freesansbold'
    font_size: int = 24
    x_margin: int = 0
    y_margin: int = 0
    width: int = None
    height: int = None
    align:str = 'center'
    img:str = None


# =============================================== Widget ==========================================

class Widget():
    def __init__(
                    self,
                    parent=None,
                    rect:tuple=None, 
                    style:str="widget{background-color:#a9a9a9;}\n",
                    extra_styles={}
                ):
        """
            Creates a new Widget instance.

rect: 
within the window.
style:
extra_styles: A dictionary of additional CSS style properties
to be applied to the widget.
        Args:
            rect (tuple, optional): A tuple of four numbers, representing the position of the widget. Defaults to [0,0,100,50].
            style (str, optional):  A string containing the CSS style properties for the widget. Defaults to "widget{background-color:#a9a9a9;}\n".
            extra_styles (dict, optional): [description]. Defaults to {}.
        """


        self.parent = parent
        self.visible = True
        self.styles=self.merge_two_dicts({
            "widget":WidgetStyle()
        }, extra_styles)
        self.setStyleSheet(style)
        if rect is not None:
            self.setRect(rect)
        else:
            self.rect = None
            self.rect2 = None        

    def setParent(self, parent):
        self.parent = parent
        if self.parent is not None and self.rect is None:
            self.setRect(self.parent.rect)

    def setPosition(self, pos:list):
        """Sets the position of the rectangle.

        Args:
            pos (list): The position of the rectangle.

        """
        self.rect[0]=pos[0]
        self.rect[1]=pos[1]
        self.setRect(self.rect)

    def setSize(self, size):
        """This function sets the size of the widget.

        Args:
            size (list):  The size is given as a tuple of two numbers, the first representing the width and the second representing the height.
        """
        self.rect[2]=size[0]
        self.rect[3]=size[1]
        self.setRect(self.rect)

    def setRect(self, rect):
        """Creates a new Rectangle object.

        Args:
            rect (list): the rectangle's coordinates
        """
        self.rect = rect
        self.rect2 = (rect[0],rect[1],rect[0]+rect[2],rect[1]+rect[3])

    def merge_two_dicts(self, x, y):
        """
        Merges two dicts, x and y, into a new dict, z. x and y must have the same
        keys. z is created as a copy of x, and then z's keys and values are updated
        with those of y.

        Args:
            x ([type]): [description]
            y ([type]): [description]

        Returns:
            [type]: [description]
        """
        z = x.copy()   # start with keys and values of x
        z.update(y)    # modifies z with keys and values of y
        return z


    def draw_rect(self, screen, style: WidgetStyle, rect:tuple=None):
        if rect is None:
            rect = self.rect
        if style.bg_color is not None:
            pygame.draw.rect(screen,style.bg_color,rect, border_radius = style.border_radius)
        if style.border_size>0:
            pygame.draw.rect(screen,style.border_color,rect, style.border_size, border_radius = style.border_radius)

    def blit_text(self, text, style:WidgetStyle, screen, rect:tuple=None):
        """Blits button text using a css style

        Args:
            style (WidgetStyle): The style to be used
            screen ([type]): The screen on which to blit
        """
        if rect is None:
            rect = self.rect
        text_render = style.font.render(text,True, style.text_color)
        if style.align =='center':
            screen.blit(text_render,(rect[0]+rect[2]//2-text_render.get_width()//2,rect[1]+rect[3]//2-text_render.get_height()//2))   
        elif style.align =='left':
            screen.blit(text_render,(rect[0]+style.x_margin,rect[1]+rect[3]//2-text_render.get_height()//2))   
        elif style.align =='right':
            screen.blit(text_render,(rect[0]+rect[2]-text_render.get_width(),rect[1]+rect[3]//2-text_render.get_height()//2))   


    def setStyleSheet(self, style:str):
        """Sets the button stylesheet

        Args:
            style (str): A css stylesheet to specify the button caracteristics
        """
        self.style = cssutils.parseString(style)
        
        for rule in self.style:
            if rule.type == rule.STYLE_RULE:
                try:
                    style = self.styles[rule.selectorText]
                except:
                    continue
                # find property
                for property in rule.style:
                    if property.name == 'width':
                        v = property.value
                        if v is not None:
                            style.width = int(v)

                    if property.name == 'height':
                        v = property.value
                        if v is not None:
                            style.height = int(v)

                    if property.name == 'color':
                        v = get_color(property.value)
                        if v is not None:
                            style.text_color = v
                                                 
                    
                    if property.name == 'border-size':
                        style.border_size = int(property.value)
                    if property.name == 'border-radius':
                        style.border_radius = int(property.value)
                        
                        
                    if property.name == 'background-image':
                        bgi = property.value.strip()
                        if bgi.startswith("url"):
                            image_url = bgi[4:-1]
                            print(image_url)
                            image_str = urlopen(image_url).read()
                            # create a file object (stream)
                            image_file = io.BytesIO(image_str)
                            image = pygame.image.load(image_file)
                        if image is not None:
                            style.img = image
                    if property.name == 'background-color':
                        style.bg_color = get_color(property.value)

                    # Text stuff
                    if property.name=='x-margin':
                        style.x_margin = int(property.value)
                    if property.name=='y-margin':
                        style.y_margin = int(property.value)
                    if property.name=='align':
                        style.align = property.value
                    if property.name == 'font-size':
                        style.font_size=property.value
                        style.font = pygame.font.Font(style.font_name+'.ttf', style.font_size)
                    if property.name == 'font-name':
                        style.font_name=property.value
                        style.font = pygame.font.Font(style.font_name+'.ttf', style.font_size)

    def paint(self, screen):
        """Paints the button

        Args:
            screen ([type]): The screen on which to blit
        """
                          
        style = self.styles["widget"]
        if style.img is None:
            if style.bg_color is not None:
                self.draw_rect(screen, style)
        else:
            screen.blit(pygame.transform.scale(style.img, (self.rect[2], self.rect[3])), (self.rect[0],self.rect[1]))

    def handle_events(self, events):
        pass

class Layout(Widget):
    def __init__(self, parent=None, rect: tuple = None, style: str = "widget{background-color:#a9a9a9;}\n", extra_styles={}):
        super().__init__(parent, rect, style, extra_styles)
        self.parent = parent
        self.widgets=[]
    def addWidget(self, widget:Widget):
        self.widgets.append(widget)

class HorizontalLayout(Layout):
    def __init__(self, parent=None, rect: tuple = None, style: str = "widget{background-color:#a9a9a9;}\n", extra_styles={}):
        super().__init__(parent, rect, style, extra_styles)

    def addWidget(self, widget:Widget, percent=None):
        self.widgets.append([percent, widget])
        widget.parent = self

    def paint(self, screen):
        l = len(self.widgets)
        if self.rect is None:
            x = self.parent.rect[0]
            y = self.parent.rect[1]
            w = self.parent.rect[2]
            h = self.parent.rect[3]
        else:
            x = self.rect[0]
            y = self.rect[1]
            w = self.rect[2]
            h = self.rect[3]
        for percent, widget in self.widgets:
            if percent is None:
                percent=1/l            
            widget.setRect([x,y,int(w*percent),h])
            x += int(w*percent)
            widget.paint(screen)

    def handle_events(self, events):
        for percent, widget in self.widgets:
            widget.handle_events(events)


class VerticalLayout(Layout):
    def __init__(self, parent=None, rect: tuple = None, style: str = "widget{background-color:#a9a9a9;}\n", extra_styles={}):
        super().__init__(parent, rect, style, extra_styles)

    def addWidget(self, widget:Widget, percent=None):
        self.widgets.append([percent, widget])
        widget.parent = self

    def paint(self, screen):
        l = len(self.widgets)
        if self.rect is None:
            x = self.parent.rect[0]
            y = self.parent.rect[1]
            w = self.parent.rect[2]
            h = self.parent.rect[3]
        else:
            x = self.rect[0]
            y = self.rect[1]
            w = self.rect[2]
            h = self.rect[3]
        for percent, widget in self.widgets:
            if percent is None:
                percent=1/l            
            widget.setRect([x,y,w,int(h*percent)])
            y += int(h*percent)
            widget.paint(screen)

    def handle_events(self, events):
        for percent, widget in self.widgets:
            widget.handle_events(events)


# =============================================== Timer ==========================================
class Timer():
    def __init__(self, callback_fn, intrval_s:float=0.1) -> None:
        self.callback_fn = callback_fn
        self.intrval_s = intrval_s
        self.started = False
    def start(self):
        self.started = True
        self.last_time = time.time()
    def stop(self):
        self.started = False    
    def process(self):
        dt = time.time() - self.last_time
        if dt>=self.intrval_s:
            if self.callback_fn is not None:
                self.callback_fn()
            self.last_time = time.time()

# =============================================== Window Manager ==========================================

class WindowManager():
    def __init__(self, window_title:str="", resolution:tuple=(800,600), is_rezisable:bool=True):
        """Builds a window managaer object
        """
        if resolution is not None:
            if is_rezisable:
                self.screen = pygame.display.set_mode(resolution, pygame.RESIZABLE)
            else:
                self.screen = pygame.display.set_mode(resolution)
        else:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption(window_title)
        self.widgets = []
        self.events = None
        self.Running = True
        self.timers=[]
        self.menu = None
        self.update_rect()


    def build_menu_bar(self):
        self.menu = MenuBar(self)
        return self.menu

    def build_timer(self, callback_fn, intrval_ms:int=100):
        timer = Timer(callback_fn, intrval_ms)
        self.timers.append(timer)
        return timer

    def add_timer(self,  timer:Timer):
        self.timers.append(timer)
        return timer

    def update_rect(self):
        w, h = pygame.display.get_surface().get_size()
        if self.menu is not None:
            self.rect = [0,self.menu.height,w,h]
        else:
            self.rect = [0,0,w,h]

    def addWidget(self, widget:Widget):
        """Adds a new widget to the widgets list

        Args:
            widget (Widget): The widget to be added
        """
        self.widgets.append(widget)
        widget.parent = self
    
    def process(self, background_color:tuple = (0,0,0)):
        self.screen.fill(background_color)
        self.events = pygame.event.get()
        for event in self.events:
            if event.type == pygame.VIDEORESIZE:
                self.update_rect()

        for widget in self.widgets:
            if widget.visible:
                widget.paint(self.screen)
                widget.handle_events(self.events)

        if self.menu is not None:
            self.menu.paint(self.screen)
            self.menu.handle_events(self.events)
        # Update UI
        pygame.display.update()
        # Check timerds
        for timer in self.timers:
            timer.process()

    def loop(self):
        """[summary]
        """
        #  Main loop
        while self.Running:
            self.process()

            for event in self.events:
                if event.type == pygame.QUIT:
                    print("Done")
                    self.Running=False
            # Update UI
            pygame.display.update()

class Sprite(Widget):
    def __init__(
                    self,
                    image_path:str, 
                    parent=None,
                    rect:tuple=[0,0,800,600], 
                    clicked_event_handler=None
                ):
        Widget.__init__(self,parent,rect, style=
"""
    widget{
"""
+
    f"""
            background-image:url('file:///{image_path}')
    """
+
"""
        }
""",extra_styles={"label":WidgetStyle()})



# =============================================== ImageBox ==========================================

class ImageBox(Widget):
    def __init__(
                    self,
                    image:np.ndarray=None, 
                    parent=None,
                    rect:tuple=[0,0,800,600], 
                    style:str="btn.normal{color:white; background-color:#878787;}\nbtn.hover{color:white; background-color:#a9a9a9};\nbtn.pressed{color:red; background-color:#565656};",
                    clicked_event_handler=None,
                    color_key=None,
                    alpha=100
                ):
        Widget.__init__(self,parent,rect, style,extra_styles={"label":WidgetStyle()})
        self.color_key = color_key
        self.alpha = alpha
        if image is not None:
            self.setImage(image)
        else:
            self.surface = None

    def setImage(self, image:np.ndarray):
        self.surface = pygame.pixelcopy.make_surface(np.swapaxes(image,0,1).astype(np.uint8))
        if self.color_key is not None:
            self.surface.set_colorkey(self.color_key)
        if self.alpha<100:
            self.surface.set_alpha(self.alpha)
        self.surface = pygame.transform.scale(self.surface, (self.rect[2], self.rect[3]))

    def paint(self, screen):
        if self.surface is not None:
            screen.blit(pygame.transform.scale(self.surface, (self.rect[2], self.rect[3])),(self.rect[0],self.rect[1]))

# =============================================== Label ==========================================

class Label(Widget):
    def __init__(
                    self,
                    text, 
                    parent=None,
                    rect:tuple=[0,0,100,50], 
                    style:str="",
                    clicked_event_handler=None
                ):
        Widget.__init__(self, parent, rect, style,extra_styles={"label":WidgetStyle()})
        self.text = text
        self.hovered=False
        self.pressed=False
        self.clicked_event_handler = clicked_event_handler
        self.setStyleSheet(style)

    def setText(self,text:str)->None:
        """Changes the text to be displayed inside the label

        Args:
            text (str): The text to be displayed
        """
        self.text = text


    def paint(self, screen):
        """Paints the button

        Args:
            screen ([type]): The screen on which to blit
        """
        style = self.styles["label"]
        if style.img is None:
            self.draw_rect(screen, style)
        else:
            screen.blit(pygame.transform.scale(style.img, (self.rect[2], self.rect[3])), (self.rect[0],self.rect[1]))

        self.blit_text(self.text,style, screen)

# =============================================== Button ==========================================

class Button(Widget):
    def __init__(
                    self,
                    text,
                    parent=None,
                    rect:tuple=[0,0,100,50], 
                    style:str="",
                    extra_styles:dict={},
                    is_toggle=False,
                    clicked_event_handler=None,
                    lost_focus_event_handler=None
                ):
        Widget.__init__(
                        self,
                        parent,
                        rect,
                        style,
                        self.merge_two_dicts({
                            "btn.normal":WidgetStyle(border_radius=4,text_color=(255,255,255), bg_color=get_color("#878787")),
                            "btn.hover":WidgetStyle(border_radius=4,text_color=(255,255,255), bg_color=get_color("#a9a9a9")),
                            "btn.pressed":WidgetStyle(border_radius=4,text_color=(255,255,255), bg_color=get_color("#565656")),
                        }, extra_styles)
                        )

                                
            
        
        self.text = text
        self.is_toggle = is_toggle
        self.hovered=False
        self.pressed=False
        self.toggled=False
        self.clicked_event_handler = clicked_event_handler
        self.lost_focus_event_handler = lost_focus_event_handler


    def setText(self,text:str)->None:
        """Changes the text to be displayed inside the label

        Args:
            text (str): The text to be displayed
        """
        self.text = text

    def paint(self, screen):
        """Paints the button

        Args:
            screen ([type]): The screen on which to blit
        """
                          
        if self.pressed:
            style = self.styles["btn.pressed"]
        elif self.hovered:
            style = self.styles["btn.hover"]
        else:
            style = self.styles["btn.normal"]

        if style.img is None:
            self.draw_rect(screen, style)
        else:
            screen.blit(pygame.transform.scale(style.img, (self.rect[2], self.rect[3])), (self.rect[0],self.rect[1]))
        self.blit_text(self.text, style, screen)

    def handle_events(self, events):
        """Handles the events

        """
        for event in events:
            if event.type == pygame.MOUSEMOTION:
                self.hovered = is_point_inside_rect(event.pos,self.rect2)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.hovered = is_point_inside_rect(event.pos,self.rect2)
                if self.hovered == True:
                    if self.is_toggle:
                        if not self.toggled:
                            self.pressed=not self.pressed
                            self.toggled=True
                    else:
                        self.pressed=True
                    if self.clicked_event_handler is not None:
                        self.clicked_event_handler()
                else:
                    if self.lost_focus_event_handler is not None:
                        self.lost_focus_event_handler()
                

            elif event.type == pygame.MOUSEBUTTONUP:
                if not self.is_toggle:
                    self.pressed=False
                self.toggled=False




# =============================================== ProgressBar ==========================================

class ProgressBar(Widget):
    def __init__(
                self, 
                parent=None,
                rect: tuple = [0, 0, 100, 50], 
                style: str = "brogressbar.outer{background-color:#ffffff;}\nbrogressbar.inner{background-color:#ffffff;}", 
                value=0
            ):
        """Builds a progressbar widget

        Args:
            rect (tuple, optional): Rectangle where to put the progressbar. Defaults to [0, 0, 100, 50].
            style (str, optional): [description]. Defaults to "brogressbar.outer{background-color:#ffffff;}\nbrogressbar.inner{background-color:#ffffff;}".
            value (int, optional): [description]. Defaults to 0.
        """
        super().__init__(
                            parent,
                            rect=rect, 
                            style=style, 
                            extra_styles={
                                "brogressbar.outer":WidgetStyle(),
                                "brogressbar.inner":WidgetStyle(),
                            }
                        )
        self.value=value

    def setValue(self, value):
        self.value = value            

    def paint(self, screen):
        """Paints the button

        Args:
            screen ([type]): The screen on which to blit
        """
                          
        outer_style = self.styles["brogressbar.outer"]
        inner_style = self.styles["brogressbar.inner"]
        if outer_style.img is None:
            self.draw_rect(screen, outer_style)
        else:
            screen.blit(pygame.transform.scale(outer_style.img, (self.rect[2], self.rect[3])), (self.rect[0],self.rect[1]))
        
        if inner_style.img is None:
            self.draw_rect(screen, inner_style)
            if inner_style.bg_color is not None:
                pygame.draw.rect(screen,inner_style.bg_color,[self.rect[0], self.rect[1], self.rect[2]*self.value, self.rect[3]])
            if inner_style.border_size>0:
                pygame.draw.rect(screen,inner_style.border_color,[self.rect[0], self.rect[1], self.rect[2]*self.value, self.rect[3]], inner_style.border_size)

        else:
            screen.blit(pygame.transform.scale(inner_style.img, (self.rect[2], self.rect[3])), (self.rect[0],self.rect[1]))
        


class Slider(Widget):
    def __init__(
                self, 
                parent=None,
                rect: tuple = [0, 0, 100, 50], 
                style: str = "", 
                value=0,
                orientation=Horizontal,
                valueChanged_callback=None,
                mouse_down_callback=None
            ):
        """Builds a progressbar widget

        Args:
            rect (tuple, optional): Rectangle where to put the progressbar. Defaults to [0, 0, 100, 50].
            style (str, optional): [description]. Defaults to "slider.outer{background-color:#ffffff;}\nslider.selector{background-color:#ffffff;}".
            value (int, optional): [description]. Defaults to 0.
        """
        self.value = 0
        self.orientation = orientation
        if self.orientation == Horizontal:
            super().__init__(
                                parent,
                                rect=rect, 
                                style=style, 
                                extra_styles={
                                    "slider.outer":WidgetStyle(border_size=3,border_radius=3, text_color=get_color("white"),bg_color=get_color("#878787")),
                                    "slider.selector.normal":WidgetStyle(border_size=1,border_radius=15, text_color=get_color("white"),bg_color=get_color("#a7a7a7"), width=20),
                                    "slider.selector.hover":WidgetStyle(border_size=1,border_radius=15, text_color=get_color("white"),bg_color=get_color("#c6c6c6"), width=20),
                                    "slider.selector.pressed":WidgetStyle(border_size=1,border_radius=15, text_color=get_color("white"),bg_color=get_color("#565656"), width=20),
                                }
                            )
        else:
            super().__init__(
                                parent,
                                rect=rect, 
                                style=style, 
                                extra_styles={
                                    "slider.outer":WidgetStyle(border_size=3,border_radius=3, text_color=get_color("white"),bg_color=get_color("#878787")),
                                    "slider.selector.normal":WidgetStyle(border_size=1,border_radius=15, text_color=get_color("white"),bg_color=get_color("#a7a7a7"), height=20),
                                    "slider.selector.hover":WidgetStyle(border_size=1,border_radius=15, text_color=get_color("white"),bg_color=get_color("#c6c6c6"), height=20),
                                    "slider.selector.pressed":WidgetStyle(border_size=1,border_radius=15, text_color=get_color("white"),bg_color=get_color("#565656"), height=20),
                                }
                            )
        self.is_toggle = False
        self.setValue(value)
        self.hovered=False
        self.selector_hovered=False
        self.pressed=False
        self.valueChanged_callback = valueChanged_callback
        self.mouse_down_callback = mouse_down_callback

    def setValue(self, value):
        self.value = value            
        inner_style = self.styles["slider.selector.normal"]
        if self.orientation == Horizontal:
            self.slider_rect= [self.rect[0]+(self.rect[2]-inner_style.width)*self.value, self.rect[1], inner_style.width, self.rect[3]]
            self.slider_rect2 = (self.slider_rect[0],self.slider_rect[1],self.slider_rect[0]+self.slider_rect[2],self.slider_rect[1]+self.slider_rect[3])
        else:
            self.slider_rect= [self.rect[0], self.rect[1]+(self.rect[3]-inner_style.height)*self.value, self.rect[2], inner_style.height]
            self.slider_rect2 = (self.slider_rect[0],self.slider_rect[1],self.slider_rect[0]+self.slider_rect[2],self.slider_rect[1]+self.slider_rect[3])

    def setRect(self, rect):
        self.rect=rect
        self.rect2 = (rect[0],rect[1],rect[0]+rect[2],rect[1]+rect[3])
        inner_style = self.styles["slider.selector.normal"]
        if self.orientation == Horizontal:
            if inner_style.width is not None:            
                self.slider_rect= [self.rect[0]+(self.rect[2]-inner_style.width)*self.value, self.rect[1], inner_style.width, self.rect[3]]
                self.slider_rect2 = (self.slider_rect[0],self.slider_rect[1],self.slider_rect[0]+self.slider_rect[2],self.slider_rect[1]+self.slider_rect[3])
        else:
            if inner_style.height is not None:            
                self.slider_rect= [self.rect[0], self.rect[1]+(self.rect[3]-inner_style.height)*self.value, self.rect[2], inner_style.height]
                self.slider_rect2 = (self.slider_rect[0],self.slider_rect[1],self.slider_rect[0]+self.slider_rect[2],self.slider_rect[1]+self.slider_rect[3])

    def paint(self, screen):
        """Paints the button

        Args:
            screen ([type]): The screen on which to blit
        """
          
        outer_style = self.styles["slider.outer"]
        if self.selector_hovered:
            inner_style = self.styles["slider.selector.hover"]
        else:
            inner_style = self.styles["slider.selector.normal"]

        if self.orientation == Horizontal:
            if outer_style.img is None:
                self.draw_rect(screen, outer_style,[self.rect[0],self.rect[1]+5,self.rect[2],self.rect[3]-10])
            else:
                screen.blit(pygame.transform.scale(outer_style.img, (self.rect[2], self.rect[3])), (self.rect[0],self.rect[1]))
            
            if inner_style.img is None:
                if inner_style.bg_color is not None:
                    pygame.draw.rect(screen,inner_style.bg_color,self.slider_rect, border_radius = inner_style.border_radius)
                if inner_style.border_size>0:
                    pygame.draw.rect(screen,inner_style.border_color,self.slider_rect, inner_style.border_size, border_radius = inner_style.border_radius)
            else:
                screen.blit(pygame.transform.scale(inner_style.img, (self.rect[2], self.rect[3])), (self.rect[0],self.rect[1]))
        else:
            if outer_style.img is None:
                self.draw_rect(screen, outer_style,[self.rect[0]+5,self.rect[1],self.rect[2]-10,self.rect[3]])
            else:
                screen.blit(pygame.transform.scale(outer_style.img, (self.rect[2], self.rect[3])), (self.rect[0],self.rect[1]))
            
            if inner_style.img is None:
                if inner_style.bg_color is not None:
                    pygame.draw.rect(screen,inner_style.bg_color,self.slider_rect, border_radius = inner_style.border_radius)
                if inner_style.border_size>0:
                    pygame.draw.rect(screen,inner_style.border_color,self.slider_rect, inner_style.border_size, border_radius = inner_style.border_radius)
            else:
                screen.blit(pygame.transform.scale(inner_style.img, (self.rect[2], self.rect[3])), (self.rect[0],self.rect[1]))

    def handle_events(self, events):
        """Handles the events

        """
        for event in events:
            if event.type == pygame.MOUSEMOTION:
                self.selector_hovered = is_point_inside_rect(event.pos,self.slider_rect2)
                self.hovered = is_point_inside_rect(event.pos,self.rect2)
                if self.pressed:
                    self.value = min(max(0,(event.pos[0]-self.rect[0])/self.rect[2]),1)
                    if self.valueChanged_callback is not None:
                        self.valueChanged_callback(self.value)    

            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.selector_hovered = is_point_inside_rect(event.pos,self.slider_rect2)
                self.hovered = is_point_inside_rect(event.pos,self.rect2)
                if self.hovered == True and self.selector_hovered == False:
                    self.value = min(max(0,(event.pos[0]-self.rect[0])/self.rect[2]),1)
                    if self.valueChanged_callback is not None:
                        self.valueChanged_callback(self.value)    
                elif self.selector_hovered:
                    self.pressed = True



            elif event.type == pygame.MOUSEBUTTONUP:
                self.selector_hovered = is_point_inside_rect(event.pos,self.slider_rect2)
                self.hovered = is_point_inside_rect(event.pos,self.rect2)
                if self.selector_hovered:
                    if self.pressed:
                        self.value = min(max(0,(event.pos[0]-self.rect[0])/self.rect[2]),1)
                        if self.valueChanged_callback is not None:
                            self.valueChanged_callback(self.value)    
                self.pressed = False


# =============================================== List ==========================================
class List(Widget):
    def __init__(
                self,
                parent:WindowManager=None,
                list=[],
                style: str = "",
                selection_changed_callback=None
    ):
        Widget.__init__(self,parent,style=style, extra_styles={
            "list":WidgetStyle(),
            "list.item.normal":WidgetStyle(height=20,bg_color=get_color("#a7a7a7")),
            "list.item.hover":WidgetStyle(height=20,bg_color=get_color("#c6c6c6")),
            "list.item.pressed":WidgetStyle(height=20,bg_color=get_color("#565656"))
            })
        self.list = list
        self.parent = parent
        self.pressed = False
        self.hovered = False
        self.hovered_item_index = 0
        self.current_item = 0
        self.scroll_value = 0
        self.setStyleSheet(style)
        self.first_visible = 0
        self.selection_changed_callback = selection_changed_callback
        self.last_mouse_y_pos = 0
        self.scrolling = False

    def paint(self, screen):
        """Paints the button

        Args:
            screen ([type]): The screen on which to blit
        """
          
        outer_style = self.styles["list"]

        item_style_hovered = self.styles["list.item.hover"]
        item_style_normal = self.styles["list.item.normal"]
        item_style_selected = self.styles["list.item.normal"]

        if outer_style.img is None:
            self.draw_rect(screen, outer_style,[self.rect[0],self.rect[1]+5,self.rect[2],self.rect[3]-10])
        else:
            screen.blit(pygame.transform.scale(outer_style.img, (self.rect[2], self.rect[3])), (self.rect[0],self.rect[1]))
        
        y_pos = self.rect[1]
        x_pos = self.rect[0]
        for i in range(self.first_visible,len(self.list)):
            entry= self.list[i]
            item_rect=[x_pos, y_pos, self.rect[2], item_style_hovered.height]
            if i==self.hovered_item_index:
                self.draw_rect(screen, item_style_hovered,item_rect)
                self.blit_text(entry, item_style_hovered, screen, item_rect)
                y_pos += item_style_hovered.height
            elif i==self.current_item:
                self.draw_rect(screen, item_style_selected,item_rect)
                self.blit_text(entry, item_style_selected, screen, item_rect)
                y_pos += item_style_selected.height
            else:
                self.blit_text(entry, item_style_normal, screen, item_rect)
                y_pos += item_style_normal.height
            if y_pos>self.rect2[3]:
                break


    def handle_events(self, events):
        """Handles the events

        """
        for event in events:
            if event.type == pygame.MOUSEMOTION:
                self.hovered = is_point_inside_rect(event.pos,self.rect2)
                if self.hovered:
                    self.hovered_item_index = min((event.pos[1]-self.rect[1])//self.styles["list.item.normal"].height+self.first_visible,len(self.list)-1)
                else:
                    self.hovered_item_index = -1
                if self.pressed:
                    dy = event.pos[1]-self.last_mouse_y_pos
                    if abs(dy)>5:
                        self.last_mouse_y_pos = event.pos[1]
                        self.scrolling = True
                        if dy>5:
                            if self.first_visible>0:
                                self.first_visible-=1
                        else:
                            if self.first_visible<len(self.list)-1:
                                self.first_visible+=1

            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.hovered = is_point_inside_rect(event.pos,self.rect2)
                if self.hovered:
                    self.pressed= True
                    self.last_mouse_y_pos = event.pos[1]



            elif event.type == pygame.MOUSEBUTTONUP:
                self.pressed= False
                if self.hovered:
                    if not self.scrolling:
                        self.current_item = self.hovered_item_index
                    if not self.pressed:
                        self.value = min(max(0,(event.pos[0]-self.rect[0])/self.rect[2]),1)
                    if self.selection_changed_callback is not None:
                        self.selection_changed_callback(self.value)    
                    self.scrolling = False

# =============================================== Menus ==========================================
# ---------------------------------------------------- Menu Bar -----------------------------------------------------

class MenuBar(Widget):
    def __init__(
                self,
                parent:WindowManager,
                style: str = "menu_bar{background-color:#878787;}\n"
    ):
        Widget.__init__(self,parent,style=style, extra_styles={"menu_bar":WidgetStyle()})
        self.parent = parent
        self.menus=[]
        self.setStyleSheet(style)

    def addMenu(self, menu):
        self.menus.append(menu)

    @property
    def width(self):
        w, h = pygame.display.get_surface().get_size()
        return w

    @property
    def height(self):
        style = self.styles["menu_bar"]
        w, h = pygame.display.get_surface().get_size()
        if style.height is not None:
            h = style.height
        else:
            h = 20
        return h

    def paint(self, screen):
        """Paints the manue

        Args:
            screen ([type]): The screen on which to blit
        """
        style = self.styles["menu_bar"]
        w, h = pygame.display.get_surface().get_size()
        if style.height is not None:
            h = style.height
        else:
            h = 20
        self.setRect([0,0,w,h])

        self.draw_rect(screen, style)

        rect_x_start = 0
        rect_y_start=0
        for menu in self.menus:
            if menu.visible:
                rect_x_start, rect_y_start = menu.prepare(rect_x_start, rect_y_start)
                menu.paint(screen)

    def handle_events(self, events):
        for menu in self.menus:
            if menu.visible:
                menu.handle_events(events)
        return super().handle_events(events)                

# ---------------------------------------------------- Menu -----------------------------------------------------


class Menu(Button):
    def __init__(
                self,
                parent:MenuBar,
                caption="",
                style:str="",
    ):
        Button.__init__(self, caption,style=style,extra_styles={
            "btn.normal":WidgetStyle(border_radius=0,text_color=(255,255,255), bg_color=get_color("#878787")),
            "btn.hover":WidgetStyle(border_radius=0,text_color=(255,255,255), bg_color=get_color("#a9a9a9")),
            "btn.pressed":WidgetStyle(border_radius=0,text_color=(255,255,255), bg_color=get_color("#565656")),
        })
        self.parent = parent
        self.actions=[]
        parent.addMenu(self)
        self.clicked_event_handler      = self.fn_clicked_event_handler
        self.lost_focus_event_handler   = self.fn_lost_focus_event_handler

    def fn_clicked_event_handler(self):
        for action in self.actions:
            action.visible=not action.visible

    def fn_lost_focus_event_handler(self):
        for action in self.actions:
            action.visible=False

    def addAction(self, action):
        action.visible=False
        self.actions.append(action)

    def prepare(self, rect_xstart=0, rect_ystart=0):
        style = self.styles["widget"]
        if style.height is not None:
            h = style.height
        else:
            h = 20
        if style.width is not None:
            w = style.width
        else:
            w = 100

        self.setRect([rect_xstart,rect_ystart,w, h])

        return rect_xstart + w, rect_ystart

    def paint(self, screen):
        style = self.styles["widget"]
        Button.paint(self, screen)
        y=self.rect[1]+self.rect[3]
        for action in self.actions:
            _, y = action.prepare(self.rect[0], y)
            if action.visible:
                action.paint(screen)



    def handle_events(self, events):
        for action in self.actions:
            if action.visible:
                action.handle_events(events)
        return super().handle_events(events)     


# ---------------------------------------------------- Action -----------------------------------------------------


class Action(Button):
    def __init__(
                self,
                parent:Menu,
                caption="",
                style:str="",
    ):
        Button.__init__(self, caption,style=style,extra_styles={
            "btn.normal":WidgetStyle(border_radius=0,text_color=(255,255,255), bg_color=get_color("#878787")),
            "btn.hover":WidgetStyle(border_radius=0,text_color=(255,255,255), bg_color=get_color("#a9a9a9")),
            "btn.pressed":WidgetStyle(border_radius=0,text_color=(255,255,255), bg_color=get_color("#565656")),            
        })
        self.parent = parent
        self.actions=[]
        parent.addAction(self)

    def prepare(self, rect_xstart=0, rect_ystart=0):
        style = self.styles["widget"]
        if style.height is not None:
            h = style.height
        else:
            h = 20
        if style.width is not None:
            w = style.width
        else:
            w = 100

        self.setRect([rect_xstart,rect_ystart,w, h])        
        return rect_xstart, rect_ystart + h

    def paint(self, screen):
        style = self.styles["widget"]

        Button.paint(self, screen)

class MenuSeparator(Label):
    def __init__(
                self,
                parent:Menu,
                caption="",
                style:str="",
    ):
        Label.__init__(self, caption,style=style)
        self.parent = parent
        self.actions=[]
        parent.addAction(self)


    def prepare(self, rect_xstart=0, rect_ystart=0):
        style = self.styles["widget"]
        if style.height is not None:
            h = style.height
        else:
            h = 1
        if style.width is not None:
            w = style.width
        else:
            w = 100

        self.setRect([rect_xstart,rect_ystart,w, h])        
        return rect_xstart, rect_ystart + h


    def paint(self, screen):
        style = self.styles["widget"]
        self.draw_rect(screen, style)


