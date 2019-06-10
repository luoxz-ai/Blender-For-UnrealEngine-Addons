#====================== BEGIN GPL LICENSE BLOCK ============================
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.	 See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.	 If not, see <http://www.gnu.org/licenses/>.
#  All rights reserved.
#
#======================= END GPL LICENSE BLOCK =============================


import bpy
import time
import configparser
from math import degrees


import importlib
from . import bfu_Basics
importlib.reload(bfu_Basics)
from .bfu_Basics import *

from . import bfu_Utils
importlib.reload(bfu_Utils)
from .bfu_Utils import *


def WriteImportSequencerScript():
	ImportScript = "#This script was generated with the addons Blender for UnrealEngine : https://github.com/xavier150/Blender-For-UnrealEngine-Addons" + "\n"
	ImportScript += "#This script will import in unreal all camera in target sequencer" + "\n"
	ImportScript += "#Use this command : " + GetImportSequencerScriptCommand() + "\n"
	return ImportScript
	
def WriteImportSequencerScript_20tab():
	#Generate a config file for import camera in Ue4 sequencer
	scene = bpy.context.scene
	
	#Comment
	ImportScript = "#This script was generated with the addons Blender for UnrealEngine : https://github.com/xavier150/Blender-For-UnrealEngine-Addons" + "\n"
	ImportScript += "#This script will import in unreal all camera in target sequencer" + "\n"
	ImportScript += "#The script must be used in Unreal Engine Editor with UnrealEnginePython : https://github.com/20tab/UnrealEnginePython" + "\n"
	ImportScript += "#Use this command : " + GetImportSequencerScriptCommand() + "\n"
	ImportScript += "\n"
	ImportScript += "\n"
	
	#Import
	ImportScript += "import os.path" + "\n"
	ImportScript += "import unreal" + "\n"
	ImportScript += "\n"
	ImportScript += "\n"
	
	
	#Prepare var	
	ImportScript += "seqLocation = r'"+os.path.join(r"/Game/",scene.unreal_levelsequence_import_location)+"'" + "\n"
	ImportScript += "seqName = r'"+scene.unreal_levelsequence_name+"'" + "\n"
	ImportScript += "seqTempName = r'"+scene.unreal_levelsequence_name+"'+str(time.time())" + "\n"
	ImportScript += "mustBeReplace = False" + "\n"
	ImportScript += "startFrame = " + str(scene.frame_start) + "\n"
	ImportScript += "endFrame = " + str(scene.frame_end+1) + "\n"
	ImportScript += "frameRateDenominator = " + str(scene.render.fps_base) + "\n"
	ImportScript += "frameRateNumerator = " + str(scene.render.fps) + "\n"
	ImportScript += "secureCrop = 0.0001 #add end crop for avoid section overlay" + "\n"
	ImportScript += "\n"
	ImportScript += "\n"

	
	#Prepare def	
	ImportScript += "def AddSequencerSectionFloatKeysByIniFile(SequencerSection, SectionFileName, FileLoc):" + "\n"
	ImportScript += "\t" + "Config = configparser.ConfigParser()" + "\n"
	ImportScript += "\t" + "Config.read(FileLoc)" + "\n"
	ImportScript += "\t" + "for option in Config.options(SectionFileName):" + "\n"
	ImportScript += "\t\t" + "frame = float(option)/frameRateNumerator #FrameRate" + "\n"
	ImportScript += "\t\t" + "value = float(Config.get(SectionFileName, option))" + "\n"
	ImportScript += "\t\t" + "SequencerSection.sequencer_section_add_key(frame,value)" + "\n"
	ImportScript += "\n"
	ImportScript += "\n"
	
	ImportScript += "def AddSequencerSectionBoolKeysByIniFile(SequencerSection, SectionFileName, FileLoc):" + "\n"
	ImportScript += "\t" + "Config = configparser.ConfigParser()" + "\n"
	ImportScript += "\t" + "Config.read(FileLoc)" + "\n"
	ImportScript += "\t" + "for option in Config.options(SectionFileName):" + "\n"
	ImportScript += "\t\t" + "frame = float(option)/frameRateNumerator #FrameRate" + "\n"
	ImportScript += "\t\t" + "value = Config.getboolean(SectionFileName, option)" + "\n"
	ImportScript += "\t\t" + "SequencerSection.sequencer_section_add_key(frame,value)" + "\n"
	ImportScript += "\n"
	ImportScript += "\n"
	
			
	#Prepare process import

	ImportScript += "if ue.find_asset(seqLocation+'/'+seqName):" + "\n"
	ImportScript += "\t" + 'print("Warning this file already exists")' + "\n"
	ImportScript += "\t" + "factory = LevelSequenceFactoryNew()" + "\n"
	ImportScript += "\t" + "seq = factory.factory_create_new(seqLocation+'/'+seqTempName.replace('.',''))" + "\n"
	ImportScript += "\t" +	"mustBeReplace = True" + "\n"
	ImportScript += "else:" + "\n"
	ImportScript += "\t" + "factory = LevelSequenceFactoryNew()" + "\n"
	ImportScript += "\t" + "seq = factory.factory_create_new(seqLocation+'/'+seqName.replace('.',''))" + "\n"
	ImportScript += "\n"

	ImportScript += 'if seq:' + "\n"
	ImportScript += "\t" + 'print("Sequencer reference created")' + "\n"
	ImportScript += "\t" + 'print(seq)' + "\n"
	ImportScript += "\t" + "ImportedCamera = [] #(CameraName, CameraGuid)" + "\n"
	ImportScript += "\t" + 'print("========================= Import started ! =========================")' + "\n"
	ImportScript += "\t" + "\n"
	
	ImportScript += "\t" + "#Set frame rate" + "\n"
	#Set frame rate for 4.20 and bigger
	ImportScript += "\t" + "if ue.ENGINE_MINOR_VERSION >= 20:" + "\n"
	ImportScript += "\t\t" + "myFFrameRate = FrameRate()" + "\n"
	ImportScript += "\t\t" + "myFFrameRate.Denominator = frameRateDenominator" + "\n"
	ImportScript += "\t\t" + "myFFrameRate.Numerator = frameRateNumerator" + "\n"
	ImportScript += "\t\t" + "seq.MovieScene.DisplayRate = myFFrameRate" + "\n"		
	#Set frame rate for 4.19	
	ImportScript += "\t" + "else:" + "\n"
	ImportScript += "\t\t" + "seq.MovieScene.FixedFrameInterval = frameRateDenominator/frameRateNumerator" + "\n"
	ImportScript += "\t" + "\n"
		
	#Set playback range
	ImportScript += "\t" + "#Set playback range" + "\n"
	ImportScript += "\t" + "seq.sequencer_set_playback_range(startFrame/frameRateNumerator, (endFrame-secureCrop)/frameRateNumerator)" + "\n"
	ImportScript += "\t" + "camera_cut_track = seq.sequencer_add_camera_cut_track()" + "\n"
	ImportScript += "\t" + "world = ue.get_editor_world()" + "\n"
	
	ImportScript += "else:" + "\n"
	ImportScript += "\t" + 'print("Fail to create Sequencer")' + "\n"
	ImportScript += "\n"
	ImportScript += "\n"

	#Import camera
	for asset in scene.UnrealExportedAssetsList:	
		if (asset.assetType == "Camera"):
			camera = asset.object
			ImportScript += "#import " + camera.name + "\n"
			ImportScript += "if seq:" + "\n"
			ImportScript += "\t" + 'print("Start import ' + camera.name + '")' + "\n"
			ImportScript += "\t" + "\n"
			
			#Create spawnable camera
			ImportScript += "\t" + "#Create spawnable camera" + "\n"
			ImportScript += "\t" + "cine_camera_actor = world.actor_spawn(CineCameraActor) #Create camera" + "\n"
			ImportScript += "\t" + "cine_camera_actor.set_actor_label('" + camera.name + "')" + "\n"
			ImportScript += "\t" + "cine_camera_actor.CameraComponent.LensSettings.MinFStop = 0" + "\n"
			ImportScript += "\t" + "cine_camera_actor.CameraComponent.LensSettings.MaxFStop = 1000" + "\n"
			ImportScript += "\t" + "camera_spawnable_guid = seq.sequencer_make_new_spawnable(cine_camera_actor) #Add camera in sequencer" + "\n"
			ImportScript += "\t" + "cine_camera_actor.actor_destroy()" + "\n"
			ImportScript += "\t" + "ImportedCamera.append(('"+camera.name+"', camera_spawnable_guid))"
			
			ImportScript += "\n"
			
			#Import fbx transform
			ImportScript += "\t" + "#Import fbx transform" + "\n"
			AdditionalTracksLoc = (os.path.join(asset.exportPath, GetObjExportFileName(asset.object,"_AdditionalTrack.ini")))
			ImportScript += "\t" + "AdditionalTracksLoc = os.path.join(r'"+AdditionalTracksLoc+"')" + "\n"
			fbxFilePath = (os.path.join(asset.exportPath, GetObjExportFileName(camera)))
			ImportScript += "\t" + "fbxFilePath = os.path.join(r'"+fbxFilePath+"')" + "\n"
			ImportScript += "\t" + "for obj in seq.MovieScene.ObjectBindings:" + "\n"
			ImportScript += "\t\t" + "if obj.ObjectGuid == ue.string_to_guid(camera_spawnable_guid):" + "\n"
			ImportScript += "\t\t\t" + "transform_track = obj.tracks[0]" + "\n"
			ImportScript += "\t\t\t" + "transform_camera_section = transform_track.Sections[0]" + "\n"
			ImportScript += "\t\t\t" + "transform_camera_section.sequencer_import_fbx_transform(fbxFilePath, '" + camera.name + "')" + "\n"
			ImportScript += "\n"
			ImportScript += "\t\t\t" + "#Import additional tracks" + "\n"
			ImportScript += "\t\t\t" + "spawned_track = obj.tracks[1]" + "\n"
			ImportScript += "\t\t\t" + "spawned_camera_section = spawned_track.Sections[0]" + "\n"
			ImportScript += "\t\t\t" + "AddSequencerSectionBoolKeysByIniFile(spawned_camera_section, 'Spawned', AdditionalTracksLoc)" + "\n"
			ImportScript += "\n"
			
			#Import additional tracks
			ImportScript += "\t" + "#Import additional tracks" + "\n"
			ImportScript += "\t" + "Component = seq.MovieScene.ObjectBindings[-1] #Get the last" + "\n"
			ImportScript += "\t" + "sectionFocalLength = Component.Tracks[0].Sections[0]" + "\n"
			ImportScript += "\t" + "AddSequencerSectionFloatKeysByIniFile(sectionFocalLength, 'FocalLength', AdditionalTracksLoc)" + "\n"
			ImportScript += "\n"
			ImportScript += "\t" + "sectionFocusDistance = Component.Tracks[1].Sections[0]" + "\n"
			ImportScript += "\t" + "AddSequencerSectionFloatKeysByIniFile(sectionFocusDistance, 'FocusDistance', AdditionalTracksLoc)" + "\n"
			ImportScript += "\n"
			ImportScript += "\t" + "sectionAperture = Component.Tracks[2].Sections[0]" + "\n"
			ImportScript += "\t" + "AddSequencerSectionFloatKeysByIniFile(sectionAperture, 'Aperture', AdditionalTracksLoc)" + "\n"
			ImportScript += "\n"
			ImportScript += "\n\n"

	def getMarkerSceneSections():
		scene = bpy.context.scene
		markersOrderly = [] 
		firstMarkersFrame = scene.frame_start
		lastMarkersFrame = scene.frame_end+1
		
		#If the scene don't use marker
		if len(bpy.context.scene.timeline_markers) < 1:
			return ([[scene.frame_start, scene.frame_end+1, bpy.context.scene.camera]])
		
		for marker in scene.timeline_markers:
			#Re set first frame
			if marker.frame < firstMarkersFrame:
				firstMarkersFrame = marker.frame

		for x in range(firstMarkersFrame, lastMarkersFrame):
			for marker in scene.timeline_markers:
				if marker.frame == x:
					markersOrderly.append(marker)
		#---
		sectionCuts = []		
		for x in range(len(markersOrderly)):
			if scene.frame_end+1 > markersOrderly[x].frame:
				startTime = markersOrderly[x].frame
				if x+1 != len(markersOrderly):
					EndTime = markersOrderly[x+1].frame
				else:
					EndTime = scene.frame_end+1
				sectionCuts.append([startTime, EndTime, markersOrderly[x].camera])
			
		return sectionCuts
		
	for section in getMarkerSceneSections():	
				#Camera cut sections
			ImportScript += "#Import camera cut section" + "\n"
			ImportScript += "if seq:" + "\n"
			ImportScript += "\t" + "camera_cut_section = camera_cut_track.sequencer_track_add_section()" + "\n"
			if section[2] is not None:
				if section[2].ExportEnum == "export_recursive" or section[2].ExportEnum == "auto":
					ImportScript += "\t" + "for camera in ImportedCamera:" + "\n"
					ImportScript += "\t\t" + "if camera[0] == '"+section[2].name+"':" + "\n"
					ImportScript += "\t\t\t" + "camera_cut_section.CameraBindingID = MovieSceneObjectBindingID( Guid=ue.string_to_guid( camera[1] ), Space=EMovieSceneObjectBindingSpace.Local )" + "\n"
				else:
					ImportScript += "\t" + "#Not camera found for this section" + "\n"
			else:
				ImportScript += "\t" + "#Not camera found for this section" + "\n"
			ImportScript += "\t" + "camera_cut_section.sequencer_set_section_range("+str(section[0])+"/frameRateNumerator, ("+str(section[1])+"-secureCrop)/frameRateNumerator)" + "\n"
	
	#Replace
	ImportScript += "if mustBeReplace == True:" + "\n"
	ImportScript += "\t" + "OldSeq = seqLocation+'/'+seqName.replace('.','')+'.'+seqName.replace('.','')" + "\n"
	ImportScript += "\t" + "NewSeq = seqLocation+'/'+seqTempName.replace('.','')+'.'+seqTempName.replace('.','')" + "\n"
	ImportScript += "\t" + "print(OldSeq)" + "\n"
	ImportScript += "\t" + "print(NewSeq)" + "\n"
	ImportScript += "\t" + "print(\"LevelSequence'\"+OldSeq+\"'\")" + "\n"
	ImportScript += "\t" + "ue.delete_asset(OldSeq)" + "\n"
	#ImportScript += "\t" + "ue.rename_asset(NewSeq, seqName.replace('.',''))" + "\n"

	#import result
	ImportScript += "if seq:" + "\n"
	ImportScript += "\t" + "print('========================= Imports completed ! =========================')" + "\n"
	ImportScript += "\t" + "\n"
	ImportScript += "\t" + "for cam in ImportedCamera:" + "\n"
	ImportScript += "\t\t" + "print(cam[0])" + "\n"
	ImportScript += "\t" + "\n"
	ImportScript += "\t" + "print('=========================')" + "\n"
	ImportScript += "\t" + "seq.sequencer_changed(True)" + "\n"
	
	return ImportScript