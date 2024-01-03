# IMPORTS
import sys
import clr

clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager

clr.AddReference("RevitAPI")

import Autodesk
from Autodesk.Revit.DB import *

doc = DocumentManager.Instance.CurrentDBDocument

import os

# FUNCTIONS
def JrnSetupNSave():
	# init vars
	export_notes = ""
	
	# add variables to journal template
	JrnData = JrnFile_template.replace("XXX", filename)
	JrnData = JrnData.replace("YYY", expFolder)
	JrnData = JrnData.replace("1000", str(numberOfGroupsInFile))	

	# define jrn_filename
	jrn_filename = expFolder + "\jrn_ExpGroups_" + doc.Title + ".txt"

	# create journal txt file in expFolder	
	try:
		with open(jrn_filename, "w") as nf:
			nf.write(JrnData)
	except:
		export_notes = "Error while exporting journal file."
	return [JrnData,jrn_filename,export_notes]


# INPUTS
JrnFile_template = IN[0]
ExportToSameRVTFolder = IN[1]
ExportFolder = IN[2]


# CODE
#init vars
filename = ""
expFolder = ""
numberOfGroupsInFile = ""
gen_notes = ""
jrn_filename = ""
JrnData = ""
export_notes = ""
export_code = False

# get groups count in current document
fec_GroupTypes = FilteredElementCollector(doc).OfClass(GroupType).WhereElementIsElementType().ToElements()

# get data for output journal file
if len(fec_GroupTypes) > 0:
	numberOfGroupsInFile = len(fec_GroupTypes)
	filename = doc.PathName
	if ExportToSameRVTFolder:
		expFolder = filename[:filename.rfind('\\')+1]

		# add variables to journal template and create journal txt file in expFolder
		JrnSetupNSave()
		
		# store returned data to output variables		
		JrnData = Jrn[0]
		jrn_filename = Jrn[1]
		export_notes = Jrn[2]
	else:
		if "No file selected" in ExportFolder:
			gen_notes = "No export folder selected! No export journal file will be created."
		else:
			expFolder = ExportFolder + "\\"

			# add variables to journal template and create journal txt file in expFolder
			Jrn = JrnSetupNSave()
			
			# store returned data to output variables
			JrnData = Jrn[0]
			jrn_filename = Jrn[1]
			export_notes = Jrn[2]


else:
	gen_notes = "There isn't any group in current document! No export journal file will be created."


# check if file has been created
export_code = os.path.isfile(jrn_filename)

# OUTPUTS
OUT = {"doc_filename":filename, "exportFolder":expFolder,
		"numberOfGroupsInFile":numberOfGroupsInFile, "GeneralNotes":gen_notes,
		"JRN_filename":jrn_filename, "JrnData":JrnData,
		"export_notes":export_notes, "export_code":export_code}
