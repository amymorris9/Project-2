import arcpy
#from arcpy import env
import os
import csv


class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Project2"
        self.alias = "Project2"

        # List of tool classes associated with this toolbox
        self.tools = [CrimeCSVtoFeatureClass]


class CrimeCSVtoFeatureClass(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "STL Crime CSVs to Feature Class"
        self.description = "The user provides CSV file(s) that will be converted to a single point feature class"
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        param0 = arcpy.Parameter(
	       displayName = "CSV File(s)",
	       name = "csv_files",
	       datatype = "DEFile",
	       parameterType = "Required",
	       direction = "Input",
	       multiValue = True)

	   #To define a filter that only includes .csv and .txt extensions
        param0.filter.list = ['txt', 'csv']

        param1 = arcpy.Parameter(
	       displayName = "Output Feature Class",
	       name = "output_fc",
	       datatype = "GPFeatureLayer",
	       parameterType = "Required",
	       direction = "Output")

        params = [param0, param1]
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""

   	#Set Up The Work Space
    	#env.workspace = r"C:\Users\Tom and Amy\Documents\Amy SLU PhD\Coursework\GIS 5090 - Programming for Remote Sensing\Projects\Project 2"
       	arcpy.env.overwriteOutput=True
       	arcpy.AddMessage ("Modules Imported")

        	#Get CSV File(s) From User
       	csv_files = (parameters[0].valueAsText).split(";")
       	output_fc = parameters[1].value.value
    	arcpy.AddMessage(csv_files)
        for f in csv_files:
            arcpy.AddMessage(f)

    	#Define Variables
    	spRef = arcpy.SpatialReference("NAD 1983 StatePlane Missouri East FIPS 2401 (US Feet)")

    	output_gdb = os.path.split(output_fc)[0]
    	feature_class = os.path.split(output_fc)[1]
    	arcpy.AddWarning(output_gdb)
    	arcpy.AddWarning(feature_class)


    	#if arcpy.Exists(output_gdb) == False:
    	#    arcpy.AddWarning "Creating GDB..."
    	#    arcpy.CreateFileGDB_management(os.path.split(output_gdb)[0], os.path.split(output_gdb)[1])

    	#Perform Analysis
    	#csvList = csv_files.split(";")
    	for csv in csv_files:
    		arcpy.AddMessage(csv)
    		new_csv = csv
    		#new_csv = csv.replace("/","\\")
    		#new_csv = os.path.normpath(csv)
    		arcpy.AddMessage(new_csv)
    		monthly_crime = os.path.splitext(os.path.basename(new_csv))[0]
    		arcpy.AddMessage(monthly_crime)
    		arcpy.AddWarning("Copying Rows...")
    		temp_table = os.path.join(output_gdb, "temp_crime_table")
    		arcpy.CopyRows_management(new_csv, temp_table)

    		arcpy.AddWarning("Making Point Features...")
    		arcpy.MakeXYEventLayer_management(temp_table, "XCoord", "YCoord", "Temp_Points", spRef, "")
    		arcpy.FeatureClassToFeatureClass_conversion("Temp_Points", output_gdb, monthly_crime)

    		arcpy.AddWarning("Deleting Table...")
    		arcpy.Delete_management(temp_table)

    	arcpy.AddMessage("Done.")
        return
