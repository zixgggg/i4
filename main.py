import subprocess
from Xlib.display import Display
from Xlib import X, XK
dpy = Display()
screen = dpy.screen()
root = screen.root
root.grab_key(dpy.keysym_to_keycode(XK.string_to_keysym("z")),X.Mod4Mask,1,X.GrabModeAsync,X.GrabModeAsync)
root.grab_key(dpy.keysym_to_keycode(XK.string_to_keysym("q")),X.Mod4Mask,X.ShiftMask,1,X.GrabModeAsync,X.GrabModeAsync)

def call_rofi():
    if ev.type==X.KeyPress:
        #print(f"press key:{ev.detail}")
        if ev.detail==dpy.keysym_to_keycode(XK.string_to_keysym("z")):
            subprocess.Popen(["rofi","-show","drun"])
def kill_window():
    if ev.type==X.KeyPress:
        if ev.detail==dpy.keysym_to_keycode(XK.string_to_keysym("q")):
            window.kill_client()
while True:
    ev=dpy.next_event()
    call_rofi()
    kill_window()
    dpy.flush()
