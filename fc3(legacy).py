if starting:
    # --------功能设置部分--------
    is_roll_yaw_connect = False  # 偏航与滚转连动，启动时需设置鼠标操作限制部分中的连动程度
    is_aim_mode = True  # 瞄准模式，按下右键时禁用滚转，鼠标x轴映射至偏航，精确调整机头指向用
    # ------------------------
    # 映射vjoy设备
    v = vJoy[0]
    # vjoy最大轴行程
    axis_max = 8 + v.axisMax
    axis_min = -8 - v.axisMax

    # --------轴定义部分，勿动--------
    # xyz轴定义
    pitch_axis = 0
    roll_axis = 0
    yaw_axis = 0
    # 油门轴定义
    throttle_axis = axis_min
    # 视角轴定义
    view_x_axis = 0
    view_y_axis = 0
    view_back_x = 0
    # 辅助轴定义
    key_pitch_axis = 0
    key_roll_axis = 0
    key_yaw_axis = 0
    mouse_pitch_axis = 0
    # 键盘操作判断
    key_pitch = False
    key_roll = False
    key_yaw = False
    # ------------------------

    # --------鼠标操作限制，默认可操作至满行程的75%（偏航除外，偏航默认与滚转连动），可自行修改--------
    mouse_pitch_limit = 0.75
    mouse_roll_limit = 0.75
    mouse_yaw_limit = 0.5
    # ------------------------

    # --------键盘操作限制，默认键盘操作时满杆，可自行修改--------
    key_pitch_limit = 1
    key_roll_limit = 1
    key_yaw_limit = 1
    # ------------------------

    # --------头部转动限制，默认偏转至左右90度，可自行修改--------
    max_head_yaw = 0.5
    max_head_pitch = 0.5

    # --------各轴灵敏度，可自行修改--------
    mouse_pitch_sens = 30
    mouse_roll_sens = 30
    mouse_yaw_sens = 30
    throttle_sens = 0.03
    aim_mode_sens = 15

# --------按键设置部分--------

# xyz三轴满杆按键，可自行修改
key_roll_left = keyboard.getKeyDown(Key.A)  # 滚转
key_roll_right = keyboard.getKeyDown(Key.D)
key_pitch_up = keyboard.getKeyDown(Key.S)  # 俯仰
key_pitch_down = keyboard.getKeyDown(Key.W)
key_yaw_left = keyboard.getKeyDown(Key.Q)  # 偏航
key_yaw_right = keyboard.getKeyDown(Key.E)

# 类苦力帽式视角调整，快捷键可自行修改
key_view_left = keyboard.getKeyDown(
    Key.Q) & keyboard.getKeyDown(Key.LeftAlt)  # 向左看
key_view_right = keyboard.getKeyDown(
    Key.E) & keyboard.getKeyDown(Key.LeftAlt)  # 向右看
key_view_back = keyboard.getKeyDown(
    Key.S) & keyboard.getKeyDown(Key.LeftAlt)  # 向后看
key_view_up = keyboard.getKeyDown(
    Key.W) & keyboard.getKeyDown(Key.LeftAlt)  # 向上看

key_free_view = keyboard.getKeyDown(Key.LeftAlt)  # 自由视角
key_pitch_center = mouse.getButton(2)  # 俯仰回中
key_aim_mode = mouse.getButton(1)  # 瞄准模式，鼠标x轴变为偏航
key_throttle_up = keyboard.getKeyDown(Key.LeftShift)  # 油门轴增加
key_throttle_down = keyboard.getKeyDown(Key.LeftControl)  # 油门轴减少

# --------代码实现--------
# xyz三轴
if (not key_free_view):
    # 俯仰
    if key_pitch_center:
        pitch_axis = 0
    elif key_pitch_up:
        key_pitch_axis = axis_max*key_pitch_limit
        key_pitch = True
    elif key_pitch_down:
        key_pitch_axis = axis_min*key_pitch_limit
        key_pitch = True
    else:
        key_pitch = False
        mouse_pitch_axis -= (mouse.deltaY*mouse_pitch_sens)

    # 滚转&偏航
    if key_roll_left:
        key_roll_axis = axis_min*key_roll_limit
        key_roll = True
    elif key_roll_right:
        key_roll_axis = axis_max*key_roll_limit
        key_roll = True
    elif key_yaw_left:
        key_yaw_axis = axis_min*key_yaw_limit
        key_yaw = True
    elif key_yaw_right:
        key_yaw_axis = axis_max*key_yaw_limit
        key_yaw = True
    else:
        key_roll = False
        key_yaw = False
        if(key_aim_mode and is_aim_mode):
            yaw_axis += (mouse.deltaX*mouse_yaw_sens)
            roll_axis = 0
        else:
            roll_axis = (mouse.deltaX*mouse_roll_sens*mouse_roll_limit*10)
            if is_roll_yaw_connect:
                yaw_axis = (mouse.deltaX*mouse_yaw_sens*mouse_yaw_limit*10)
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

# 视角轴
if key_view_left and key_view_right:
    view_x_axis = 0
elif key_view_left and key_view_back:
    view_x_axis = axis_max
    view_back_x = 0
elif key_view_right and key_view_back:
    view_x_axis = -axis_max
    view_back_x = 1
elif key_view_back:
    if view_back_x == 0:
        view_x_axis = axis_max
    elif view_back_x == 1:
        view_x_axis = -axis_max
elif key_view_left:
    view_x_axis = axis_max*max_head_yaw
elif key_view_right:
    view_x_axis = -axis_max*max_head_yaw
elif key_view_up:
    view_y_axis = axis_max*max_head_pitch
else:
    view_x_axis = 0
    view_y_axis = 0

# 限制部分

if key_roll:
    roll_axis = key_roll_axis
    if roll_axis > axis_max*key_roll_limit:
        roll_axis = axis_max*key_roll_limit
    elif roll_axis < axis_min*key_roll_limit:
        roll_axis = axis_min*key_roll_limit
else:
    if roll_axis > axis_max*mouse_roll_limit:
        roll_axis = axis_max*mouse_roll_limit
    elif roll_axis < axis_min*mouse_roll_limit:
        roll_axis = axis_min*mouse_roll_limit

if key_yaw:
    yaw_axis = key_yaw_axis
    if yaw_axis > axis_max*key_yaw_limit:
        yaw_axis = axis_max*key_yaw_limit
    elif yaw_axis < axis_min*key_yaw_limit:
        yaw_axis = axis_min*key_yaw_limit
else:
    if yaw_axis > axis_max*mouse_yaw_limit:
        yaw_axis = axis_max*mouse_yaw_limit
    elif yaw_axis < axis_min*mouse_yaw_limit:
        yaw_axis = axis_min*mouse_yaw_limit

if key_pitch:
    pitch_axis = key_pitch_axis
    if pitch_axis > axis_max*key_pitch_limit:
        pitch_axis = axis_max*key_pitch_limit
    elif pitch_axis < axis_min*key_pitch_limit:
        pitch_axis = axis_min*key_pitch_limit
else:
    pitch_axis = mouse_pitch_axis
    if pitch_axis > axis_max*mouse_pitch_limit:
        pitch_axis = axis_max*mouse_pitch_limit
    elif pitch_axis < axis_min*mouse_pitch_limit:
        pitch_axis = axis_min*mouse_pitch_limit

# --------vjoy轴与按钮映射--------
v.x = pitch_axis
v.y = roll_axis
v.z = yaw_axis
v.rx = view_x_axis
v.ry = view_y_axis
v.slider = throttle_axis
