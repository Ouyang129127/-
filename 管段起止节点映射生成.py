"""
脚本功能：为管段线图层添加起止节点ID字段，并根据节点点图层的坐标匹配填充这些字段。
"""
# -*- coding: utf-8 -*-
import arcpy
import math

# ====================== 【请修改这里为你的实际数据路径】 ======================
# 管段线图层
PIPE_FEATURE_CLASS = r"D:\DepositionModel\GIS管网导出数据\管段主河道正北方.shp"
# 节点点图层
NODE_FEATURE_CLASS = r"D:\DepositionModel\GIS管网导出数据\节点主河道正北方_New.shp"
# =============================================================================

# 1. 添加字段
try:
    arcpy.AddField_management(PIPE_FEATURE_CLASS, "START_NODE", "TEXT", field_length=20)
    arcpy.AddField_management(PIPE_FEATURE_CLASS, "END_NODE", "TEXT", field_length=20)
    print("✅ 成功添加 START_NODE / END_NODE 字段")
except Exception as e:
    if "already exists" in str(e):
        print("ℹ️ 字段已存在，继续执行")
    else:
        raise e

# 2. 创建节点坐标映射字典
node_dict = {}
with arcpy.da.SearchCursor(NODE_FEATURE_CLASS, ["SHAPE@XY", "NodeID"]) as cursor:
    for row in cursor:
        x, y = row[0]
        node_key = (round(x, 6), round(y, 6))
        node_dict[node_key] = row[1]
print("✅ 已加载 {0} 个节点坐标映射".format(len(node_dict)))

# 3. 遍历管段，匹配起止节点ID
update_fields = ["SHAPE@", "START_NODE", "END_NODE"]
with arcpy.da.UpdateCursor(PIPE_FEATURE_CLASS, update_fields) as cursor:
    for row in cursor:
        pipe_geom = row[0]
        start_point = pipe_geom.firstPoint
        end_point = pipe_geom.lastPoint
        
        start_node_id = None
        end_node_id = None
        
        if start_point:
            s_key = (round(start_point.X, 6), round(start_point.Y, 6))
            start_node_id = node_dict.get(s_key, "未匹配")
        if end_point:
            e_key = (round(end_point.X, 6), round(end_point.Y, 6))
            end_node_id = node_dict.get(e_key, "未匹配")
        
        row[1] = start_node_id
        row[2] = end_node_id
        cursor.updateRow(row)

print("🎉 全部完成！已为所有管段标注起止节点ID")