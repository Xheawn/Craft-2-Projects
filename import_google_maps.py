import time
import googlemaps
import polyline
import math
from typing import List
import GPS
from Point import Point
import datetime

# 我们如果要调取实时方向就只能用swift获取ios的信息，我查了半天用windows基本不可能写swift，剩下的就靠你了加油

points: List[Point] = []

# 请用你的 API Key 替换下面的 YOUR_API_KEY
gmaps = googlemaps.Client(key='AIzaSyDuq-bA6uuLX6oXoUFuKVRZlShHYhdBsFQ')
icloud_data = GPS.login("3087837258@qq.com", "Okmijnuhb0987")

# 定义起点和终点地址（假设 UW 的 Maple Hall 和 UW 的 CSE Building 在 Seattle 校区）
origin = "Maple Hall, University of Washington, Seattle, WA"
destination = "CSE Building, University of Washington, Seattle, WA"

# 获取驾车路线的详细信息
directions_result = gmaps.directions(
    origin,
    destination,
    mode="walking",      # 可改为 "walking", "bicycling", "transit" 等模式
    departure_time="now" # 指定出发时间
)

# 提取 overview_polyline 中的编码字符串
encoded_poly = directions_result[0]['overview_polyline']['points']

# 解码为经纬度坐标列表
coords = polyline.decode(encoded_poly)

# 计算每2个坐标之间与x轴（纬线）所夹的角度
# 我们假设x轴正方向为0度，逆时针为正，我们想要输出0到360度的区间，所以我们对不同的象限（方向）分类讨论
for i in range(1, len(coords)):
    la_diff = coords[i][0] - coords[i - 1][0]
    long_diff = coords[i][1] - coords[i - 1][1]
    if (long_diff >= 0):
        if (la_diff >= 0): # 第一象限
            angle_degree = math.degrees(math.atan2(la_diff, long_diff))
        else: # 第四象限
            angle_degree = math.degrees(math.atan2(la_diff, long_diff)) + 360.0
    else: # 第二象限/第三象限
        angle_degree = math.degrees(math.atan2(la_diff, long_diff)) + 180.0
    
    points.append(Point(coords[i - 1][0], coords[i - 1][1], angle_degree))

# 导入最后一个点。因为最后一个点没有方向，我们把他设为none，也就是不传任何值。
points.append(Point(coords[len(coords) - 1][0], coords[len(coords) - 1][1]))

print(points)

# 提取并打印每一步的转向指示信息
print("\n转向指示：")
steps = directions_result[0]['legs'][0]['steps']
for i, step in enumerate(steps, start=1):
    instruction = step.get('html_instructions', '')
    maneuver = step.get('maneuver', '无')
    distance = step.get('distance', {}).get('text', '')
    duration = step.get('duration', {}).get('text', '')
    print(f"步骤 {i}: {instruction} (操作: {maneuver}, 距离: {distance}, 时间: {duration})")

# 打出目前所在的经纬度
with open("points_data.txt", "a", encoding="utf-8") as file:
    current_time = datetime.datetime.now()
    file.write(f"程序启动时间: {current_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
    while True:
        # 获取当前的位置数据
        curr_location = GPS.get_curr_location(icloud_data)
        # 将数据转换为字符串并写入文件，每次写入一行
        file.write(str(curr_location) + "\n")
        file.flush()  # 确保数据及时写入磁盘
        # 同时打印到控制台
        print(curr_location)
        # 每5秒钟写入一次
        time.sleep(5)



