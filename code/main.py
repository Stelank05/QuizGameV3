# cant wait to make the V3.1 update - the i make it pretty update where i entirely rework the UI (Or refactor the entire codebase)

from tkinter import *
from tkinter import messagebox

from controls.sort_functions import *

from window.window_components import WindowComponents
from window.window_controls import WindowControls
from window.window_design import WindowDesign

from common_data import CommonData

CommonData.setup()
sort_questions(CommonData.usable_questions)
sort_questions(CommonData.discarded_questions)

window: Tk = Tk()
window.title("Aimee's Game V3 (I have a Problem)")

WindowControls.setup_window(window)
WindowDesign.create_login_page()
WindowComponents.window.mainloop()