from Xlib import display,X,XK
#import ewmhlib
dpy=display.Display()
screen=dpy.screen()
root=screen.root
#註冊事件
screen.root.grab_key(dpy.keysym_to_keycode(XK.string_to_keysym("q")),X.Mod4Mask,1,X.GrabModeAsync, X.GrabModeAsync)
screen.root.grab_key(dpy.keysym_to_keycode(XK.string_to_keysym("r")),X.Mod4Mask,1,X.GrabModeAsync, X.GrabModeAsync)
#cursor=root.create_font_cursor(0)
#cursor=dpy.create_font_cursor(Xcursorfont.left_ptr)
#cursor=dpy.create_font_cursor()
#cursor=dpy.create_resource_object("cursor")
#root.define_cursor(cursor)
font = dpy.open_font('cursor')           # 開啟 cursor 字型
cursor = font.create_glyph_cursor(
    font,                                # mask 用同一個 font
    68,                                  # 游標形狀（source_char）https://xorg.freedesktop.org/archive/current/doc/libX11/libX11/libX11.html#x_font_cursors
    68 + 1,                              # mask_char（通常是 +1）
    (0, 0, 0),                           # 前景色 RGB（黑色）
    (65535, 65535, 65535)                # 背景色 RGB（白色）
)
root.change_attributes(cursor=cursor)
while True:
    event=dpy.next_event()
    if event.type==X.KeyPress:
        if event.detail==dpy.keysym_to_keycode(XK.string_to_keysym("q")):
            event.child.kill_client()
            #event.child是滑鼠底下的視窗
        if event.detail==dpy.keysym_to_keycode(XK.string_to_keysym("r")):
            event.child.configure(x=100,y=100)
            #configure(x,y,w,h)
    dpy.flush()
