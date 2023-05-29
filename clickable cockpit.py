import ctypes


if starting:
    # 功能设置
    screen_length = 1920  # 屏幕分辨率，用于光标回中
    screen_height = 1080
    is_roll_yaw_connect = True  # 偏航与滚转连动，启动时需设置鼠标操作限制部分中的连动程度
    is_aim_mode = True  # 瞄准模式，按下右键时禁用滚转，鼠标x轴映射至偏航，精确调整机头指向用
    # 链接vJoy
    v = vJoy[0]
    # vJoy最大轴行程
    axis_max = 8+v.axisMax
    axis_min = -8-v.axisMax
    # 轴定义部分
    # 鼠标xy及滚轮轴定义
    mouse_x_axis = 0
    mouse_y_axis = 0
    mouse_z_axis = 0
    # 俯仰滚转偏航轴定义
    pitch_axis = 0
    roll_axis = 0
    yaw_axis = 0
    # 油门轴定义
    throttle_axis = axis_min
    # 视角xy及缩放轴定义
    view_x_axis = 0
    view_y_axis = 0
    view_z_axis = 0
    # 计算辅助轴定义
    mouse_pitch_axis = 0
    key_pitch_axis = 0
    key_roll_axis = 0
    key_yaw_axis = 0
    # 状态判断定义，无需修改
    is_key_pitch = False
    is_key_roll = False
    is_key_yaw = False
    # 鼠标控制飞行，由按键控制，无需修改
    is_mouse_control = False
    # 各轴灵敏度
    mouse_pitch_sens = 30
    mouse_roll_sens = 50
    mouse_yaw_sens = 20
    throttle_sens = 0.03
    aim_mode_sens = 15
    view_x_sens = 10
    view_y_sens = 10
    mouse_z_sens = 1000

    # 键盘操作限制，默认键盘操作滚转/俯仰/偏航时满杆，可自行修改
    key_pitch_limit = 1
    key_roll_limit = 1
    key_yaw_limit = 1

    # 鼠标操作限制，默认可操作至满行程的75%，可自行修改
    mouse_pitch_limit = 0.75
    mouse_roll_limit = 0.75
    mouse_yaw_limit = 0.4

    def axisLimitControl(value, multiplier):  # 限制函数，将超出轴行程的值限制在行程内
        if value > axis_max*multiplier:
            return axis_max*multiplier
        elif value < axis_min*multiplier:
            return axis_min*multiplier
        else:
            return value

    def setMousePos(posX, posY):
        ctypes.windll.user32.SetCursorPos(posX, posY)


# 按键设置，可自行更改
key_toggle_mouse_control = keyboard.getPressed(Key.Grave)  # 开关鼠标飞控，默认为~键

# 滚转/俯仰/偏航按键，按住对应按键再按下时也作为模拟苦力帽使用
key_roll_left = keyboard.getKeyDown(Key.A)  # 滚转，默认为A/D键
key_roll_right = keyboard.getKeyDown(Key.D)
key_pitch_up = keyboard.getKeyDown(Key.S)  # 俯仰，默认为W/S键
key_pitch_down = keyboard.getKeyDown(Key.W)
key_yaw_left = keyboard.getKeyDown(Key.Q)  # 偏航，默认为Q/E键
key_yaw_right = keyboard.getKeyDown(Key.E)
key_pitch_center = mouse.getButton(2)  # 俯仰回中，默认为鼠标中键

key_free_view = keyboard.getKeyDown(Key.C)  # 自由视角，默认为C键
key_view_center = keyboard.getKeyDown(
    Key.LeftAlt) & key_free_view  # 视角回中，默认为左alt+C键
key_aim_mode = mouse.getButton(1)  # 瞄准模式，鼠标x轴变为偏航
key_pov_hat_switch_1 = keyboard.getKeyDown(Key.LeftAlt)  # 按住时启动苦力帽#1
key_pov_hat_switch_2 = mouse.getButton(3)  # 苦力帽2
key_pov_hat_switch_3 = mouse.getButton(4)  # 苦力帽3

key_throttle_up = keyboard.getKeyDown(Key.LeftShift)  # 油门轴增加/减少，默认为左Shift/Ctrl
key_throttle_down = keyboard.getKeyDown(Key.LeftControl)

# 代码实现

# 鼠标控制飞行开关
if key_toggle_mouse_control:
    is_mouse_control = not is_mouse_control

# 轴控制
if not (key_free_view or key_pov_hat_switch_1 or key_pov_hat_switch_2 or key_pov_hat_switch_3):
    if key_pitch_center:
        mouse_pitch_axis = 0
    elif key_pitch_up:
        key_pitch_axis = axis_max*key_pitch_limit
        is_key_pitch = True
    elif key_pitch_down:
        key_pitch_axis = axis_min*key_pitch_limit
        is_key_pitch = True
    else:
        is_key_pitch = False
        if is_mouse_control:
            mouse_pitch_axis -= (mouse.deltaY*mouse_pitch_sens)
    key_pitch_axis = axisLimitControl(key_pitch_axis, key_pitch_limit)
    mouse_pitch_axis = axisLimitControl(mouse_pitch_axis, mouse_pitch_limit)

    if key_roll_left:
        key_roll_axis = axis_min*key_roll_limit
        is_key_roll = True
    elif key_roll_right:
        key_roll_axis = axis_max*key_roll_limit
        is_key_roll = True
    elif key_yaw_left:
        key_yaw_axis = axis_min*key_yaw_limit
        is_key_yaw = True
    elif key_yaw_right:
        key_yaw_axis = axis_max*key_yaw_limit
        is_key_yaw = True
    else:
        is_key_roll = False
        is_key_yaw = False
        if(key_aim_mode and is_aim_mode and is_mouse_control):
            yaw_axis += (mouse.deltaX*mouse_yaw_sens)
            roll_axis = 0
        else:
            if is_mouse_control:
                roll_axis = (mouse.deltaX*mouse_roll_sens*mouse_roll_limit*10)
                if is_roll_yaw_connect:
                    yaw_axis = (mouse.deltaX*mouse_yaw_sens*mouse_yaw_limit*10)
                else:
                    yaw_axis = 0
            else:
                roll_axis = 0
                yaw_axis = 0
else:
    roll_axis = 0
    yaw_axis = 0

# 油门轴
if key_throttle_up:
    throttle_axis += (axis_max*throttle_sens)
if key_throttle_down:
    throttle_axis -= (axis_max*throttle_sens)
if throttle_axis > axis_max:
    throttle_axis = axis_max
elif throttle_axis < axis_min:
    throttle_axis = axis_min

if key_free_view:
    mouse_y_axis += (mouse.deltaY*view_y_sens)
    mouse_x_axis += (mouse.deltaX*view_x_sens)
if key_view_center:
    setMousePos(screen_length/2, screen_height/2)
    mouse_y_axis = 0
    mouse_x_axis = 0

view_x_axis = axisLimitControl(mouse_x_axis, 1)
view_y_axis = axisLimitControl(mouse_y_axis, 1)

view_x_axis = mouse_x_axis
view_y_axis = mouse_y_axis

if mouse.wheelUp and key_free_view:
    mouse_z_axis += mouse_z_sens
elif mouse.wheelDown and key_free_view:
    mouse_z_axis -= mouse_z_sens
elif key_view_center:
    mouse_z_axis = 0

if mouse.middleButton and keyboard.getKeyDown(Key.LeftAlt):
    setMousePos(screen_length/2, screen_height/2)


# # 视角轴
# if key_free_view:
#     mouse_y_axis += (mouse.deltaY*view_y_sens)
#     mouse_x_axis += (mouse.deltaX*view_x_sens)
# elif key_view_center:
#     ctypes.windll.user32.SetCursorPos(960, 540)
#     mouse_y_axis = 0
#     mouse_x_axis = 0
# view_x_axis = mouse_x_axis
# view_y_axis = mouse_y_axis

# # 滚轮缩放轴
# if mouse.wheelUp and key_free_view:
#     mouse_z_axis += mouse_z_sens
# elif mouse.wheelDown and key_free_view:
#     mouse_z_axis -= mouse_z_sens
# elif key_view_center:
#     mouse_z_axis = 0

# 限制部分
if is_key_roll:
    roll_axis = key_roll_axis
    roll_axis = axisLimitControl(roll_axis, key_roll_limit)
else:
    roll_axis = axisLimitControl(roll_axis, mouse_roll_limit)

if is_key_yaw:
    yaw_axis = key_yaw_axis
    yaw_axis = axisLimitControl(yaw_axis, key_yaw_limit)
else:
    yaw_axis = axisLimitControl(yaw_axis, mouse_yaw_limit)

if is_key_pitch:
    pitch_axis = key_pitch_axis
    pitch_axis = axisLimitControl(pitch_axis, key_pitch_limit)
else:
    pitch_axis = mouse_pitch_axis
    pitch_axis = axisLimitControl(pitch_axis, mouse_pitch_limit)

view_z_axis = mouse_z_axis
view_z_axis = axisLimitControl(view_z_axis, 1)

# vJoy轴映射
v.x = roll_axis
v.y = pitch_axis
v.z = yaw_axis
v.rx = view_x_axis
v.ry = view_y_axis
v.rz = view_z_axis
v.slider = throttle_axis

# 苦力帽#1
if key_pov_hat_switch_1:
    if key_roll_left:
        vJoy[0].setDigitalPov(0, VJoyPov.Left)
    elif key_roll_right:
        vJoy[0].setDigitalPov(0, VJoyPov.Right)
    elif key_pitch_down:
        vJoy[0].setDigitalPov(0, VJoyPov.Up)
    elif key_pitch_up:
        vJoy[0].setDigitalPov(0, VJoyPov.Down)
    else:
        vJoy[0].setDigitalPov(0, VJoyPov.Nil)

if key_pov_hat_switch_2:
    if key_roll_left:
        vJoy[0].setDigitalPov(1, VJoyPov.Left)
    elif key_roll_right:
        vJoy[0].setDigitalPov(1, VJoyPov.Right)
    elif key_pitch_down:
        vJoy[0].setDigitalPov(1, VJoyPov.Up)
    elif key_pitch_up:
        vJoy[0].setDigitalPov(1, VJoyPov.Down)
    else:
        vJoy[0].setDigitalPov(1, VJoyPov.Nil)

if key_pov_hat_switch_3:
    if key_roll_left:
        vJoy[0].setDigitalPov(2, VJoyPov.Left)
    elif key_roll_right:
        vJoy[0].setDigitalPov(2, VJoyPov.Right)
    elif key_pitch_down:
        vJoy[0].setDigitalPov(2, VJoyPov.Up)
    elif key_pitch_up:
        vJoy[0].setDigitalPov(2, VJoyPov.Down)
    else:
        vJoy[0].setDigitalPov(2, VJoyPov.Nil)
