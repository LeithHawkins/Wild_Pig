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
    arcpy.MakeXYEventLayer_management(in_Table, x_coords, y_coords, out_Layer, spRef, z_coords)

    # Print the total rows
    print(arcpy.GetCount_management(out_Layer))

    # Save to a layer file
    arcpy.SaveToLayerFile_management(out_Layer, saved_Layer)
    out_FGDB = 'N:\\Wild_Pig_Project\\Wild_Pig_output.gdb\\Glen_Innes'
    out_FC = '\\' + 'Glen_Innes6'
    arcpy.FeatureClassToFeatureClass_conversion(saved_Layer, out_FGDB, out_FC)

except Exception as err:
    print(err.args[0])


    # with arcpy.da.SearchCursor('N:\\Wild_Pig_Project\\Wild_Pig_output.gdb\\Glen_Innes\\Glen_Innes6', 'Device_ID') as cursor:
    #     for row in cursor:
    #         dev_id = str(row[0])
    #     print (dev_id)

def unique_values(table, field):
    with arcpy.da.SearchCursor(table, [field]) as cursor:
        return sorted({row[0] for row in cursor})
        print (row[0])

List_ofValues = unique_values('N:\\Wild_Pig_Project\\Wild_Pig_output.gdb\\Glen_Innes\\Glen_Innes6', 'Device_ID')
print (List_ofValues)

for Device_ID in unique_values:
    dev_id = str(Device_ID)
    print (dev_id)


# with arcpy.da.SearchCursor(List_ofValues) as cursor:
#     for row in cursor:
#         dev_id = str(row[0])
#     print (dev_id)
