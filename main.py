from Xlib import display,X,XK
dpy=display.Display()
screen=dpy.screen()
root=screen.root
#註冊事件
screen.root.grab_key(dpy.keysym_to_keycode(XK.string_to_keysym("q")),X.Mod4Mask,1,X.GrabModeAsync, X.GrabModeAsync)
#cursor=root.create_font_cursor(0)
#cursor=dpy.create_resource_object("cursor")
#root.define_cursor(cursor)
while True:
    event=dpy.next_event()
    if event.type==X.KeyPress:
        if event.detail==dpy.keysym_to_keycode(XK.string_to_keysym("q")):
            X.kill_client(dpy)
    dpy.flush()
