# -*- coding:utf-8 -*-
# ---------------------------------------------------------------------------
# Author: YT.wsy
# Created on: 2021/11/27
# Reference:
"""
Description:Python2.7
Usage:
"""
# ---------------------------------------------------------------------------

import arcpy
import os



def point_to_shp(point_blank_shp,x,y,id):
    # arcpy.env.overwriteOutput = True  # 输出的shp文件可以覆盖同名文件
    # output_folder = os.getcwd()
    # # 创建空白 shp
    # name = ceng+"_Point"


    # point_blank_shp = arcpy.CreateFeatureclass_management(
    #     output_folder, name, "Point", spatial_reference=None)
    # # 创建、写入面

    fields = ["SHAPE@","shu_xin"]
    Rows = arcpy.da.InsertCursor(point_blank_shp, fields)

    arcpoint = arcpy.Point(x, y)

    Rows.insertRow([arcpoint,id])

    # write_sth = "Output path: " + os.path.join(output_folder, name)
    # print write_sth

def polyline_to_shp(coord_list, sr, y, x):
    """
    创建多边
    coord_list(List)：多个点组成的坐标
    sr: 投影系
    y(Int): y坐标列
    x(Int): x坐标列
    """
    parts = arcpy.Array()
    yuans = arcpy.Array()
    yuan = arcpy.Array()
    for part in coord_list:
        for pnt in part:
            if pnt:
                yuan.add(arcpy.Point(pnt[y], pnt[x]))
            else:
                # null point - we are at the start of a new ring
                yuans.add(yuan)
                yuan.removeAll()
        # we have our last ring, add it
        yuans.add(yuan)
        yuan.removeAll()
        # if we only have one ring: remove nesting
        if len(yuans) == 1:
            yuans = yuans.getObject(0)
        parts.add(yuans)
        yuans.removeAll()
    # 只有一个，单个图形
    if len(parts) == 1:
        parts = parts.getObject(0)
    return arcpy.Polyline(parts, sr)

def poly_to_shp(coord_list, sr, y, x):
    """
    创建多边形
    coord_list(List)：多个点组成的坐标
    sr: 投影系
    y(Int): y坐标列
    x(Int): x坐标列
    """
    parts = arcpy.Array()
    yuans = arcpy.Array()
    yuan = arcpy.Array()
    for part in coord_list:
        for pnt in part:
            if pnt:
                yuan.add(arcpy.Point(pnt[y], pnt[x]))
            else:
                # null point - we are at the start of a new ring
                yuans.add(yuan)
                yuan.removeAll()
        # we have our last ring, add it
        yuans.add(yuan)
        yuan.removeAll()
        # if we only have one ring: remove nesting
        if len(yuans) == 1:
            yuans = yuans.getObject(0)
        parts.add(yuans)
        yuans.removeAll()
    # 只有一个，单个图形
    if len(parts) == 1:
        parts = parts.getObject(0)
    return arcpy.Polygon(parts, sr)

def read_txt_to_Geotype(filename):
    f = open(filename)
    shp_size_line=f.readline()  #范围
    print "范围大小为"+shp_size_line

    count_ceng=f.readline()  #范围
    print "层数为"+count_ceng
    count_ceng=int(count_ceng)


    for i in range(count_ceng):
        name_ceng=f.readline().strip('\n')

        print "正在处理层号为："+name_ceng


        #Point 108

        type_and_count=f.readline()
        strpoint=type_and_count.split(" ")
        if strpoint[0]=="Point" and strpoint[1]!="0\n":

            count_point = int(strpoint[1])
            print count_point

            arcpy.env.overwriteOutput = True  # 输出的shp文件可以覆盖同名文件
            output_folder = os.getcwd()
            # 创建空白 shp
            name = name_ceng+ "_Point"
            point_blank_shp = arcpy.CreateFeatureclass_management(
                output_folder, name, "Point", spatial_reference=None)
            arcpy.AddField_management(os.path.join(output_folder, name) + ".shp", "shu_xin", "LONG", field_length=10)

            shu_xin_list=list()
            for point_i in range(count_point):
                id = int(f.readline())
                shu_xin_list.append(str(id))
                x_and_y=f.readline()
                x_and_y_list=x_and_y.split(", ")
                x=float(x_and_y_list[0])
                y = float(x_and_y_list[1])
                point_to_shp(point_blank_shp,x, y,id)

            write_sth = "Output path: " + os.path.join(output_folder, name)
            print write_sth

            # arcpy.AddField_management(os.path.join(output_folder, name)+".shp", "shu_xin", "TEXT", field_length=10)
            # with  arcpy.da.UpdateCursor(os.path.join(output_folder, name)+".shp", ['shu_xin']) as cursor:
            #     print type(cursor)
            #     shu_xin_ID=0
            #     for row in cursor:
            #         row[0] = shu_xin_list[shu_xin_ID]
            #         # print "更改完成"
            #         cursor.updateRow(row)
            #         shu_xin_ID+=1
            #
            # del cursor


        #Polyline 0

        type_and_count=f.readline()
        strline=type_and_count.split(" ")
        if strline[0]=="Polyline":
            if strline[1]!="0\n":

                count_line=int(strline[1])
                print count_line
                all_lines_with_ceng=list()
                shu_xin_list = list()

                for line_i in range(count_line):
                    id = int(f.readline())    #32033
                    shu_xin_list.append(str(id))
                    line_with_points= int(f.readline())   #6

                    line_i_all_points=list()
                    for one_line_with_points in range(line_with_points):
                        this_line_one_point_xy=f.readline()
                        this_line_one_point=this_line_one_point_xy.split(", ") #[20.0, 20.0]
                        this_line_one_point_float=list()
                        this_line_one_point_float.append(float(this_line_one_point[0]))
                        this_line_one_point[1]=this_line_one_point[1].strip('\n')
                        this_line_one_point_float.append(float(this_line_one_point[1]))
                        line_i_all_points.append(this_line_one_point_float)
                        # 目标= [
                        #      [30.0, 10.0], [20.0, 10.0]
                        #      ],
                    if f.readline()!="END_COOR\n":
                        print "读行出错"
                        return 0


                    all_lines_with_ceng.append(line_i_all_points)
                    # 目标= [
                    #     [[20.0, 20.0], [30.0, 20.0],
                    #      [30.0, 10.0], [20.0, 10.0]],
                    #
                    #     [[5.0, 3.0], [3.0, 3.0]],
                    # ]


                arcpy.env.overwriteOutput = True  # 输出的shp文件可以覆盖同名文件
                output_folder = os.getcwd()
                # 创建空白 shp
                name = name_ceng + "_Polyline"
                # ▶注释1◀
                polyline_blank_shp = arcpy.CreateFeatureclass_management(
                    output_folder, name, "Polyline", spatial_reference=None)

                arcpy.AddField_management(os.path.join(output_folder, name) + ".shp", "shu_xin", "LONG",
                                          field_length=10)

                shu_xin_list_i=0
                for i in all_lines_with_ceng:
                    all_lines_with_ceng_one=list()
                    all_lines_with_ceng_one.append(i)
                    p = polyline_to_shp(all_lines_with_ceng_one, sr=None, y=0, x=1)

                    fields = ["SHAPE@", "shu_xin"]

                    # 创建、写入面
                    Rows = arcpy.da.InsertCursor(polyline_blank_shp, fields)
                    # print all_lines_with_ceng
                    Rows.insertRow([p,shu_xin_list[shu_xin_list_i]])
                    shu_xin_list_i+=1

                write_sth = "Output path: " + os.path.join(output_folder, name)
                print write_sth

                # arcpy.AddField_management(os.path.join(output_folder, name)+".shp", "shu_xin", "TEXT", field_length=10)
                # with  arcpy.da.UpdateCursor(os.path.join(output_folder, name)+".shp", ('shu_xin')) as cursorline:
                #     print type(cursorline)
                #     shu_xin_ID=0
                #     for row in cursorline:
                #         row[0] = shu_xin_list[shu_xin_ID]
                #         # print "更改完成"
                #         cursorline.updateRow(row)
                #         shu_xin_ID+=1
                # del cursorline



        # Polygon 0

        type_and_count = f.readline()
        strpoly = type_and_count.split(" ")
        if strpoly[0] == "Polygon":
            if strpoly[1]!="0\n":
                # Polygon 204
                count_polygon=int(strpoly[1])
                print count_polygon

                shu_xin_list=list()
                all_Polygons_with_ceng = list()
                for Polygon_i in range(count_polygon):
                    id = int(f.readline())  # 32033
                    shu_xin_list.append(str(id))
                    Polygon_with_points = int(f.readline())  # 6
                    Polygon_i_all_points = list()
                    for one_Polygon_with_points in range(Polygon_with_points):
                        this_Polygon_one_point_xy = f.readline()
                        this_Polygon_one_point = this_Polygon_one_point_xy.split(", ")  # [20.0, 20.0]
                        this_Polygon_one_point[0]=float(this_Polygon_one_point[0])
                        this_Polygon_one_point[1]=this_Polygon_one_point[1].strip('\n')
                        this_Polygon_one_point[1]=float(this_Polygon_one_point[1])
                        Polygon_i_all_points.append(this_Polygon_one_point)
                        # 目标= [
                        #      [30.0, 10.0], [20.0, 10.0]
                        #      ],
                    if f.readline()!="END_COOR\n":
                        print "读行出错"
                        return 0

                    all_Polygons_with_ceng.append(Polygon_i_all_points)
                    # 目标= [
                    #     [[20.0, 20.0], [30.0, 20.0],
                    #      [30.0, 10.0], [20.0, 10.0]],
                    #
                    #     [[5.0, 3.0], [3.0, 3.0]],
                    # ]

                arcpy.env.overwriteOutput = True  # 输出的shp文件可以覆盖同名文件
                output_folder = os.getcwd()
                # 创建空白 shp
                name = name_ceng + "_Polygon"
                # ▶注释1◀
                Polygon_blank_shp = arcpy.CreateFeatureclass_management(
                    output_folder, name, "Polygon", spatial_reference=None)

                arcpy.AddField_management(os.path.join(output_folder, name) + ".shp", "shu_xin", "LONG",
                                          field_length=10)

                shu_xin_list_i=0
                for i in all_Polygons_with_ceng:
                    all_Polygons_with_ceng_one=list()
                    all_Polygons_with_ceng_one.append(i)
                    p = poly_to_shp(all_Polygons_with_ceng_one, sr=None, y=0, x=1)

                    fields = ["SHAPE@", "shu_xin"]

                    # 创建、写入面
                    Rows = arcpy.da.InsertCursor(Polygon_blank_shp, fields)
                    Rows.insertRow([p,shu_xin_list[shu_xin_list_i]])
                    shu_xin_list_i+=1


                write_sth = "Output path: " + os.path.join(output_folder, name)
                print write_sth

                # arcpy.AddField_management(os.path.join(output_folder, name)+".shp", "shu_xin", "TEXT", field_length=10)
                # with  arcpy.da.UpdateCursor(os.path.join(output_folder, name)+".shp", ('shu_xin')) as cursorpoly:
                #     print type(cursorpoly)
                #     shu_xin_ID=0
                #     for row in cursorpoly:
                #         row[0] = shu_xin_list[shu_xin_ID]
                #         # print "更改完成"
                #         cursorpoly.updateRow(row)
                #         shu_xin_ID+=1
                #     del cursorpoly



read_txt_to_Geotype("D:/GIS/Digital_Mapping/data.txt")
