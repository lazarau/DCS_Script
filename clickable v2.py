import ctypes

if starting:
    screen_length = 1920
    screen_height = 1200

    v = vJoy[0]
    axis_max = 8+v.axisMax
    axis_min = -8-v.axisMax

    mouse_pitch_axis = 0
    mouse_roll_axis = 0
    mouse_yaw_axis = 0

    key_pitch_axis = 0
    key_roll_axis = 0
    key_yaw_axis = 0

    pitch_axis = 0
    roll_axis = 0
    yaw_axis = 0

    view_x_axis = 0
    view_y_axis = 0
    view_z_axis = 0

    pitch_mouse_indicator = screen_height/2
    roll_mouse_indicator = screen_length/2

    throttle_axis = axis_min

    key_pitch_limit = 1
    key_roll_limit = 1
    key_yaw_limit = 1

    mouse_pitch_limit = 1
    mouse_roll_limit = 0.75
    mouse_yaw_limit = 0.5

    mouse_pitch_sens = 30
    mouse_roll_sens = 300
    mouse_yaw_sens = 100

    throttle_sens = 0.03
    aim_mode_sens = 15

    view_x_sens = 10
    view_y_sens = 10
    view_z_sens = 1000

    is_mouse_control = False  # 当前是否处于鼠标控制
    is_mouse_control_prev = False  # True说明本次的操作是关闭鼠标控制，False则反之
    is_key_control_prev = False

    is_key_pitch_override = False
    is_key_roll_override = False
    is_key_yaw_override = False

    def axisLimitControl(value, multiplier):
        if value > axis_max*multiplier:
            return axis_max*multiplier
        elif value < axis_min*multiplier:
            return axis_min*multiplier
        else:
            return value

    def setMousePos(posX, posY):
        posX = int(posX)
        posY = int(posY)
        ctypes.windll.user32.SetCursorPos(posX, posY)

key_toggle_mouse_control = keyboard.getPressed(Key.CapsLock)

key_roll_left = keyboard.getKeyDown(Key.A)
key_roll_right = keyboard.getKeyDown(Key.D)
key_pitch_up = keyboard.getKeyDown(Key.S)
key_pitch_down = keyboard.getKeyDown(Key.W)
key_yaw_left = keyboard.getKeyDown(Key.Q)
key_yaw_right = keyboard.getKeyDown(Key.E)

key_pitch_center = mouse.getButton(2)

key_mouse_pitch_center = mouse.getButton(2)
key_free_view = keyboard.getKeyDown(Key.C)
key_view_center = keyboard.getKeyDown(
    Key.LeftAlt) & key_free_view

key_throttle_up = keyboard.getKeyDown(Key.LeftShift)
key_throttle_down = keyboard.getKeyDown(Key.LeftControl)

if key_toggle_mouse_control:
    is_mouse_control_prev = is_mouse_control
    is_mouse_control = not is_mouse_control

if not key_free_view:
    if key_pitch_up:
        key_pitch_axis = axis_max*key_pitch_limit
        is_key_pitch_override = True
        is_key_control_prev = True
        if (not is_mouse_control) and is_mouse_control_prev:
            is_mouse_control_prev = False
    elif key_pitch_down:
        key_pitch_axis = axis_min*key_pitch_limit
        is_key_pitch_override = True
        is_key_control_prev = True
        if (not is_mouse_control) and is_mouse_control_prev:
            is_mouse_control_prev = False
    else:
        if is_key_pitch_override:
            key_pitch_axis = 0
            is_key_pitch_override = False

    if key_roll_left:
        key_roll_axis = axis_min*key_roll_limit
        is_key_roll_override = True
    elif key_roll_right:
        key_roll_axis = axis_max*key_roll_limit
        is_key_roll_override = True
    else:
        key_roll_axis = 0
        is_key_roll_override = False

    if key_yaw_left:
        key_yaw_axis = axis_min*key_yaw_limit
        is_key_yaw_override = True
    elif key_yaw_right:
        key_yaw_axis = axis_max*key_yaw_limit
        is_key_yaw_override = True
    else:
        key_yaw_axis = 0
        is_key_yaw_override = False

    if is_mouse_control:
        mouse_pitch_axis -= mouse.deltaY*mouse_pitch_sens
        mouse_roll_axis = mouse.deltaX*mouse_roll_sens
        mouse_yaw_axis = mouse.deltaX*mouse_yaw_sens

        mouse_pitch_axis = axisLimitControl(
            mouse_pitch_axis, mouse_pitch_limit)
        mouse_roll_axis = axisLimitControl(mouse_roll_axis, mouse_roll_limit)
        mouse_yaw_axis = axisLimitControl(mouse_yaw_axis, mouse_yaw_limit)

        if key_mouse_pitch_center:
            mouse_pitch_axis = 0
        if is_key_pitch_override:
            mouse_pitch_axis = key_pitch_axis
        elif is_key_roll_override:
            mouse_roll_axis = key_roll_axis
        elif is_key_yaw_override:
            mouse_yaw_axis = key_yaw_axis
        else:
            if is_key_control_prev:
                mouse_pitch_axis = 0
                is_key_control_prev = False
        pitch_axis = mouse_pitch_axis
        roll_axis = mouse_roll_axis
        yaw_axis = mouse_yaw_axis

    else:
        if is_mouse_control_prev:
            key_pitch_axis = mouse_pitch_axis
        pitch_axis = key_pitch_axis
        roll_axis = key_roll_axis
        yaw_axis = key_yaw_axis

    if key_throttle_up:
        throttle_axis += axis_max*throttle_sens
    elif key_throttle_down:
        throttle_axis -= axis_max*throttle_sens

    throttle_axis = axisLimitControl(throttle_axis, 1)

    if is_mouse_control:
        pitch_mouse_indicator = round(
            screen_height/2-round(pitch_axis/mouse_pitch_limit/mouse_pitch_sens)/547*screen_height/2)
        # roll_mouse_indicator=round(screen_length/2-round(roll_axis/mouse_roll_sens))
        roll_mouse_indicator = round(
            screen_length/2+round(roll_axis/mouse_roll_limit/mouse_roll_sens)/62*screen_length/2)
        setMousePos(roll_mouse_indicator, pitch_mouse_indicator)
else:
    view_x_axis += mouse.deltaX*view_x_sens
    view_y_axis += mouse.deltaY*view_y_sens

    if mouse.wheelUp:
        view_z_axis += view_z_sens
    elif mouse.wheelDown:
        view_z_axis -= view_z_sens

    view_x_axis = axisLimitControl(view_x_axis, 1)
    view_y_axis = axisLimitControl(view_y_axis, 1)
    view_z_axis = axisLimitControl(view_z_axis, 1)
    if key_view_center:
        view_x_axis = 0
        view_y_axis = 0
        view_z_axis = 0

v.x = roll_axis
v.y = pitch_axis
v.z = yaw_axis
v.rx = view_x_axis
v.ry = view_y_axis
v.rz = view_z_axis
v.slider = throttle_axis
