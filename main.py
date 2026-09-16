from Xlib import display,X,XK,xobject,Xcursorfont
dpy=display.Display()
screen=dpy.screen()
root=screen.root
q_code=dpy.keysym_to_keycode(XK.string_to_keysym("q"))
r_code=dpy.keysym_to_keycode(XK.string_to_keysym("r"))
#註冊事件
screen.root.grab_key(q_code,X.Mod4Mask,1,X.GrabModeAsync, X.GrabModeAsync)
screen.root.grab_key(r_code,X.Mod4Mask,1,X.GrabModeAsync, X.GrabModeAsync)
screen.root.grab_button(X.Button1,X.Mod4Mask,True,X.ButtonPressMask| X.ButtonReleaseMask| X.PointerMotionMask,X.GrabModeAsync,X.GrabModeAsync,X.NONE,X.NONE,)
screen.root.grab_button(X.Button3,X.Mod4Mask,True,X.ButtonPressMask| X.ButtonReleaseMask| X.PointerMotionMask,X.GrabModeAsync,X.GrabModeAsync,X.NONE,X.NONE,)
font = dpy.open_font('cursor')           # 開啟 cursor 字型
cursor = font.create_glyph_cursor(
    font,                                # mask 用同一個 font
    Xcursorfont.gumby,                   # 游標形狀（source_char）https://xorg.freedesktop.org/archive/current/doc/libX11/libX11/libX11.html#x_font_cursors
    #Xcursorfont.left_ptr,
    Xcursorfont.gumby+1,                 # mask_char（通常是 +1）
    (0, 0, 0),                           # 前景色 RGB（黑色）
    (65535, 65535, 65535)                # 背景色 RGB（白色）
)

red = screen.default_colormap.alloc_named_color("red").pixel
green = screen.default_colormap.alloc_named_color("green").pixel
root.change_attributes(
    cursor=cursor,
    event_mask=X.SubstructureRedirectMask
)
status=None
focused_win=None
while True:
    event=dpy.next_event()
    if event.type==X.ButtonPress and event.child!=X.NONE:
        #event.child.change_attributes(border_pixel=green)
        status=event
        #滑鼠原本的xy
        mc_origin_x=event.root_x
        mc_origin_y=event.root_y
        
        if status.detail==X.Button1:
            #視窗原本的xy
            win_origin_x=event.child.get_geometry().x
            win_origin_y=event.child.get_geometry().y
        elif status.detail==X.Button3:
            #視窗原本的寬高
            win_origin_width=event.child.get_geometry().width
            win_origin_height=event.child.get_geometry().height
    elif event.type==X.MotionNotify and status!=None:
        #滑鼠移動後的xy
        moved_x=event.root_x
        moved_y=event.root_y
        
        #滑鼠了xy移動多少
        move_x=moved_x-mc_origin_x
        move_y=moved_y-mc_origin_y
        if status.detail==X.Button1:
            status.child.configure(
                x=win_origin_x+move_x,#視窗原本的位置+滑鼠移動了多少（也就是要移動多少）
                y=win_origin_y+move_y
            )
        elif status.detail==X.Button3:
            #最小視窗寬高常數（最小可設定為1）,根據PEP8規定常數名為全大寫,用底線分隔
            MIN_WIN_WIDTH=50
            MIN_WIN_HEIGHT=50

            status.child.configure(
                width=max(win_origin_width+move_x,MIN_WIN_WIDTH),#視窗原本的大小+滑鼠移動了多少,max()避免視窗大小小於最小視窗寬高常數
                height=max(win_origin_height+move_y,MIN_WIN_HEIGHT)
            )
    elif event.type==X.ButtonRelease and event.child!=X.NONE:
        #event.child.change_attributes(border_pixel=red)
        status=None
    elif event.type==X.KeyPress and event.child!= X.NONE:
        if event.detail==q_code:
            print(f"kill client:{event.child.get_wm_name()}")
            event.child.kill_client()
            #event.child是滑鼠底下的視窗
    elif event.type==X.MapRequest:
        window=event.window
        window.change_attributes(
            border_pixel=red,
            event_mask=X.EnterWindowMask|X.LeaveWindowMask
        )
        window.configure(border_width=3)
        window.map()
    elif event.type==X.EnterNotify:
        focus_win=event.window#要聚焦的視窗
        if focused_win!=None and focused_win.id != focus_win.id:#如果現在聚焦的視窗是其他視窗就把焦點給他並且邊框變色
            focused_win.change_attributes(border_pixel=red)
        focus_win.set_input_focus(
            X.RevertToParent,
            X.CurrentTime
        )
        focus_win.change_attributes(border_pixel=green)#把視窗邊框變色
        focused_win=focus_win
    #elif event.type==X.LeaveNotify:
    #    event.window.change_attributes(border_pixel=red)
    dpy.flush()
#記得關num lock
