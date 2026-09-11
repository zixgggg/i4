from Xlib import display,X,XK,xobject,Xcursorfont
dpy=display.Display()
screen=dpy.screen()
root=screen.root
#註冊事件
screen.root.grab_key(dpy.keysym_to_keycode(XK.string_to_keysym("q")),X.Mod4Mask,1,X.GrabModeAsync, X.GrabModeAsync)
screen.root.grab_key(dpy.keysym_to_keycode(XK.string_to_keysym("r")),X.Mod4Mask,1,X.GrabModeAsync, X.GrabModeAsync)
screen.root.grab_button(X.Button1,X.Mod4Mask,True,X.ButtonPressMask| X.ButtonReleaseMask| X.PointerMotionMask,X.GrabModeAsync,X.GrabModeAsync,X.NONE,X.NONE,)
#screen.root.grab_button(X.Button3,X.Mod4Mask,True,X.ButtonPressMask| X.ButtonReleaseMask| X.PointerMotionMask,X.GrabModeAsync,X.GrabModeAsync,X.NONE,X.NONE,)
font = dpy.open_font('cursor')           # 開啟 cursor 字型
cursor = font.create_glyph_cursor(
    font,                                # mask 用同一個 font
    Xcursorfont.gumby,                   # 游標形狀（source_char）https://xorg.freedesktop.org/archive/current/doc/libX11/libX11/libX11.html#x_font_cursors
    #Xcursorfont.left_ptr,
    Xcursorfont.gumby+1,                 # mask_char（通常是 +1）
    (0, 0, 0),                           # 前景色 RGB（黑色）
    (65535, 65535, 65535)                # 背景色 RGB（白色）
)

root.change_attributes(cursor=cursor)
q_code=dpy.keysym_to_keycode(XK.string_to_keysym("q"))
r_code=dpy.keysym_to_keycode(XK.string_to_keysym("r"))

status=None
while True:
    event=dpy.next_event()
    """
    root.set_input_focus(X.RevertToParent,X.CurrentTime)
    if event.child!=X.NONE:
        print(dpy.get_input_focus())
    """
    if event.type==X.ButtonPress and event.child!=X.NONE:
        status=event
        win_origin_x=event.child.get_geometry().x#視窗原本的x
        win_origin_y=event.child.get_geometry().y#視窗原本的y
        mc_origin_x=event.root_x#滑鼠原本的x
        mc_origin_y=event.root_y#滑鼠原本的y
    elif event.type==X.MotionNotify and status!=None:
        moved_x=event.root_x#滑鼠移動後的x
        moved_y=event.root_y#滑鼠移動後的y
        move_x=moved_x-mc_origin_x#x移動多少
        move_y=moved_y-mc_origin_y#y移動多少
        status.child.configure(x=win_origin_x+move_x,y=win_origin_y+move_y)#視窗原本的位置+要移動多少
        dpy.flush()
    elif event.type==X.ButtonRelease:
        status=None
    elif event.type==X.KeyPress and event.child!= X.NONE:
        if event.detail==q_code:
            print(f"kill client:{event.child.get_wm_name()}")
            event.child.kill_client()
            #event.child是滑鼠底下的視窗
        elif event.detail==r_code:
            print(f"moving window:{event.child.get_wm_name()}")
            
            event.child.configure(x=100,y=100,width=200,height=300,border_width=100)
            #configure(x,y,width,height)
        dpy.flush()
#記得關num lock
