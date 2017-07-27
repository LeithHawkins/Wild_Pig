import arcpy
import Wild_Pig_Module
import xlrd
import xlwt

# Set environment settings
arcpy.env.workspace = "C:\\Users\\hawkinle\\Desktop\\STDTAS"
arcpy.env.overwriteOutput = True
try:
    # Set the local variables
    in_Table = "GPS_072717_002024.CSV"
    x_coords = "Longitude"
    y_coords = "Latitude"
    z_coords = "Altitude"
    out_Layer = "Pig_Point"
    saved_Layer = "C:\\Users\\hawkinle\\Desktop\\STDTAS\\Pig_Point6.lyr"
    # Set the spatial reference
    spRef = 'N:\\Projection_FIles\\WGS_84.prj'

    # Make the XY event layer...
    arcpy.MakeXYEventLayer_management(in_Table, x_coords, y_coords, out_Layer, spRef)

    # Save to a layer file
    arcpy.SaveToLayerFile_management(out_Layer, saved_Layer)
    out_FGDB = 'N:\Wild_Pig_Project\All_Collars.gdb\All_Collars'
    out_FC = '\\' + 'All_Collars'
    arcpy.env.outputMFlag = "Disabled"
    arcpy.env.outputZFlag = "Disabled"
    arcpy.FeatureClassToFeatureClass_conversion(saved_Layer, out_FGDB, out_FC)

except Exception as err:
    print(err.args[0])

All_Collars = out_FGDB + out_FC
arcpy.MakeFeatureLayer_management(All_Collars, 'tempLayer')
arcpy.Dissolve_management('tempLayer', 'in_memory/device', 'Device_ID')
print ('Dissolve Complete')

with arcpy.da.SearchCursor('in_memory/device' ,['Device_ID']) as dissolve_feature:
    for row in dissolve_feature:
        refNumber = str(row[0])
        feature = out_FGDB + '\\'
        Selection_q = '"Device_ID" ='+ refNumber
        print (Selection_q)
        print(refNumber)
        arcpy.SelectLayerByAttribute_management('templayer', 'NEW_SELECTION', Selection_q)
        arcpy.FeatureClassToFeatureClass_conversion('templayer', feature, 'Device_ID' + refNumber)

arcpy.Delete_management('templayer')
arcpy.Delete_management('in_memory/device')
del row
