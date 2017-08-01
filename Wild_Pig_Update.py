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

    # Save to a layer file create feature class - update datefield and delete
    arcpy.SaveToLayerFile_management(out_Layer, saved_Layer)
    out_FGDB = 'N:\\Wild_Pig_Project\\All_Collars.gdb\\All_Collars'
    out_Heat = 'N:\\Wild_Pig_Project\\All_Collars.gdb\\Heatmap_Collars'
    out_FC = '\\' + 'All_Collars'
    Full_path = out_FGDB + out_FC
    arcpy.env.outputMFlag = "Disabled"
    arcpy.env.outputZFlag = "Disabled"
    arcpy.FeatureClassToFeatureClass_conversion(saved_Layer, out_FGDB, out_FC)
    arcpy.AddField_management(Full_path, 'Local_Date', 'DATE')
    arcpy.CalculateField_management(Full_path, 'Local_Date', '!Date___Time__Local_!', 'PYTHON')
    arcpy.DeleteField_management(Full_path, 'Date___Time__GMT_')
    arcpy.DeleteField_management(Full_path, 'Date___Time__Local_')

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
        Heat_Feature = out_Heat + '\\'
        Selection_q = '"Device_ID" ='+ refNumber
        print(refNumber)
        def Heatprocess(Selection_Feature, Output_Feature, ):
            arcpy.SelectLayerByAttribute_management('templayer', 'NEW_SELECTION',Selection_Feature)
            arcpy.FeatureClassToFeatureClass_conversion('templayer', feature, Output_Feature)

        arcpy.SelectLayerByAttribute_management('templayer', 'NEW_SELECTION', Selection_q)
        arcpy.FeatureClassToFeatureClass_conversion('templayer', feature, 'Device_ID' + refNumber)
        if refNumber == '44161':
            #arcpy.SelectLayerByAttribute_management('templayer', 'NEW_SELECTION', "Device_ID = 44161 AND Date >= date '2017-04-25 00:00:00'")
            #arcpy.FeatureClassToFeatureClass_conversion('templayer', Heat_Feature, 'Heatmap' + refNumber)
            Heatprocess("Device_ID = 44161 AND Date >= date '2017-04-25 00:00:00'",'Heatmap' + refNumber)
arcpy.Delete_management('templayer')
arcpy.Delete_management('in_memory/device')
del row
