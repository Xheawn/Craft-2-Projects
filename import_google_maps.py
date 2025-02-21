import googlemaps
import polyline

# 请用你的 API Key 替换下面的 YOUR_API_KEY
gmaps = googlemaps.Client(key='AIzaSyDuq-bA6uuLX6oXoUFuKVRZlShHYhdBsFQ')

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
print("路线坐标：")
print(coords)

# 提取并打印每一步的转向指示信息
print("\n转向指示：")
steps = directions_result[0]['legs'][0]['steps']
for i, step in enumerate(steps, start=1):
    instruction = step.get('html_instructions', '')
    maneuver = step.get('maneuver', '无')
    distance = step.get('distance', {}).get('text', '')
    duration = step.get('duration', {}).get('text', '')
    print(f"步骤 {i}: {instruction} (操作: {maneuver}, 距离: {distance}, 时间: {duration})")


