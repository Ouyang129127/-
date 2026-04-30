"""
# 这个脚本的功能是从一个管线图层中提取所有的节点（起点和终点），并且自动去重，最后输出一个新的节点图层。
"""
# -*- coding: utf-8 -*-
import arcpy
import os

# 你的文件路径（已填写完毕）
PIPE_FEATURE_CLASS = r"D:\DepositionModel\GIS管网导出数据\管段主河道正北方.shp"
NODE_FEATURE_CLASS = r"D:\DepositionModel\GIS管网导出数据\节点主河道正北方_New.shp"

arcpy.env.overwriteOutput = True

# 提取所有管线的起点、终点并去重
node_set = set()

with arcpy.da.SearchCursor(PIPE_FEATURE_CLASS, ["SHAPE@"]) as cursor:
    for row in cursor:
        line = row[0]
        # 起点
        x1 = round(line.firstPoint.X, 6)
        y1 = round(line.firstPoint.Y, 6)
        node_set.add((x1, y1))
        # 终点
        x2 = round(line.lastPoint.X, 6)
        y2 = round(line.lastPoint.Y, 6)
        node_set.add((x2, y2))

# 排序，保证编号连续有序
node_list = sorted(node_set)

# 创建节点图层
sr = arcpy.Describe(PIPE_FEATURE_CLASS).spatialReference
arcpy.CreateFeatureclass_management(
    os.path.dirname(NODE_FEATURE_CLASS),
    os.path.basename(NODE_FEATURE_CLASS),
    "POINT",
    spatial_reference=sr
)

# 添加连续编号字段
arcpy.AddField_management(NODE_FEATURE_CLASS, "NodeID", "LONG")

# 写入节点，从1开始连续编号
with arcpy.da.InsertCursor(NODE_FEATURE_CLASS, ["SHAPE@XY", "NodeID"]) as cur:
    nid = 1
    for p in node_list:
        cur.insertRow([p, nid])
        nid += 1

print("=== 完成 ===")
print("节点总数：", len(node_list))
print("NodeID 从 1 连续编号")

