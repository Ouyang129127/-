"""
这段代码的作用是命名点图层中的节点ID字段，按照ZH001、ZH002、ZH003的格式进行命名。
请将代码中的路径修改为你的节点图层的实际路径，然后运行代码即可完成。
"""

import arcpy
lyr = r"D:\DepositionModel\GIS管网导出数据\管道主河道正北方_New.shp"

arcpy.AddField_management(lyr, "NodeID", "TEXT", field_length=10)

with arcpy.da.UpdateCursor(lyr, ["NodeID"]) as cursor:
    i = 1
    for row in cursor:
        row[0] = "ZH{:03d}".format(i)
        cursor.updateRow(row)
        i += 1

print("完成！")