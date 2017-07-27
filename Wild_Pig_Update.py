import arcpy
import Wild_Pig_Module

# Set environment settings
arcpy.env.workspace = "C:\\Users\\hawkinle\\Desktop\\STDTAS"
arcpy.env.overwriteOutput = True
try:
    # Set the local variables
    in_Table = "GPS_072417_201818.csv"
    x_coords = "Longitude"
    y_coords = "Latitude"
    z_coords = "Altitude"
    out_Layer = "Pig_Point"
    saved_Layer = "C:\\Users\\hawkinle\\Desktop\\STDTAS\\Pig_Point6.lyr"
    # Set the spatial reference
    spRef = 'N:\\Projection_FIles\\WGS_84.prj'

    # Make the XY event layer...
    arcpy.MakeXYEventLayer_management(in_Table, x_coords, y_coords, out_Layer, spRef)

    # Print the total rows
    #print(arcpy.GetCount_management(out_Layer))

    # Save to a layer file
    arcpy.SaveToLayerFile_management(out_Layer, saved_Layer)
    out_FGDB = 'N:\\Wild_Pig_Project\\Wild_Pig_output.gdb\\Glen_Innes\\'
    out_FC = '\\' + 'Glen_Innes'
    #arcpy.CopyFeatures_management(saved_Layer, out_FGDB + out_FC)
    #print('Copy Complete')
    arcpy.env.outputMFlag = "Disabled"
    arcpy.env.outputZFlag = "Disabled"
    arcpy.FeatureClassToFeatureClass_conversion(saved_Layer, out_FGDB, out_FC)

except Exception as err:
    print(err.args[0])

def unique_values(table, field):
    with arcpy.da.SearchCursor(table, [field]) as cursor:
        return sorted({row[0] for row in cursor})

Glen_Innes ='N:\\Wild_Pig_Project\\Wild_Pig_output.gdb\\Glen_Innes\\Glen_Innes'
Glen_Innes_Dissolve ='N:\\Wild_Pig_Project\\Wild_Pig_output.gdb\\Glen_Innes\\Glen_Innes_Dissolcve'
List_ofValues = unique_values(Glen_Innes, 'Device_ID')
print (List_ofValues)
arcpy.MakeFeatureLayer_management(Glen_Innes, 'tempLayer')
arcpy.Dissolve_management('tempLayer', 'in_memory/device', 'Device_ID')
print ('Dissolve Complete')

with arcpy.da.SearchCursor('in_memory/device' ,['Device_ID']) as dissolve_feature:
    for row in dissolve_feature:
        refNumber = str(row[0])
        print(refNumber)

