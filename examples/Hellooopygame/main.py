from OOPyGame import FormLayout, Label, TextBox, WindowManager, Button, List, MenuBar, Menu, Action, MenuSeparator, HorizontalLayout, VerticalLayout, ImageBox, Slider
import pygame
# ===== Build pygame window and populate with widgets ===================
pygame.init()
class MainWindow(WindowManager):
    def __init__(self):
        # Initialize the window manager
        WindowManager.__init__(self, "Face box", (800,600))
        self.mn_bar = self.build_menu_bar()
        self.file = Menu(self.mn_bar,"File")
        new = Action(self.file,"New")
        sep = MenuSeparator(self.file)
        quit = Action(self.file,"Quit")
        quit.clicked_event_handler = self.fn_quit
        self.edit = Menu(self.mn_bar,"Edit")

        self.layout_1 = HorizontalLayout()
        self.layout_2 = VerticalLayout()
        self.layout_3 = FormLayout(fixed_title_size=200)
        

        # Build an image Box
        self.main_video = ImageBox()

        # Build a slider
        self.time_slider = Slider()
        self.time_slider.value=0.5
        self.time_slider.valueChanged_callback = self.slider_updated
        self.time_slider.mouse_down_callback = self.slider_mouse_down

        # Build a list of items
        self.test_ui1 = List(list=[f"item {i}" for i in range(100)])
        self.test_ui3 = Button("This is a button",rect=[0,0,100,20])
        self.test_ui4 = Label("This is a label")
        self.test_ui5 = TextBox("This is a textbox")

        self.layout_3.addWidget(self.test_ui3,"Title")
        self.layout_3.addWidget(self.test_ui4,"Title 2")
        self.layout_3.addWidget(self.test_ui5,"Title 3")
        

        self.layout_1.addWidget(self.test_ui1,0.2)
        self.layout_1.addWidget(self.layout_2,0.8)

        self.layout_2.addWidget(self.main_video,0.7)
        self.layout_2.addWidget(self.time_slider,0.05)

        self.layout_2.addWidget(self.layout_3,0.25)

        self.addWidget(self.layout_1)

        # Build a timer that repeats every 1/24 secondes
        self.timer = self.build_timer(self.do_stuf,1/24)
        self.timer.start()

    def slider_mouse_down(self):
        # when the slider is pressed with mouse this callback is triggered
        pass

    def slider_updated(self, val):
        # When slider value changed this callback is triggered
        pass

    def do_stuf(self):
        # Here do something that will be executed every timer tick
        pass

    def fn_quit(self):
        self.Running=False

# =======================================================================

#
#clip.preview()
if __name__=="__main__":
    mw = MainWindow()
    mw.loop()