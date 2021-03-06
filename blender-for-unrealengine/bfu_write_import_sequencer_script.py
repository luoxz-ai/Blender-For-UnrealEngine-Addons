# ====================== BEGIN GPL LICENSE BLOCK ============================
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
# ======================= END GPL LICENSE BLOCK =============================


import bpy
import time
import configparser
from math import degrees

if "bpy" in locals():
    import importlib
    if "bfu_basics" in locals():
        importlib.reload(bfu_basics)
    if "bfu_utils" in locals():
        importlib.reload(bfu_utils)
    if "bfu_write_utils" in locals():
        importlib.reload(bfu_write_utils)

from . import bfu_basics
from .bfu_basics import *
from . import bfu_utils
from .bfu_utils import *
from . import bfu_write_utils
from .bfu_write_utils import *


def WriteImportSequencerScript():
    GetImportSequencerScriptCommand()
    scene = bpy.context.scene
    IsSpawnableCamera = True

    # Import
    ImportScript = ""
    ImportScript += "\t" + "import os.path" + "\n"
    ImportScript += "\t" + "import time" + "\n"

    ImportScript += "\t" + "import unreal" + "\n"

    ImportScript += "\t" "if int(unreal.SystemLibrary.get_engine_version()[:4][2:]) >= 26:" + "\n"
    ImportScript += "\t\t" + "import configparser as ConfigParser" + "\n"
    ImportScript += "\t" "else:" + "\n"
    ImportScript += "\t\t" + "import ConfigParser" + "\n"

    ImportScript += "\n"
    ImportScript += "\n"

    # Prepare var
    ImportScript += "\t" + "startFrame = " + str(scene.frame_start) + "\n"
    ImportScript += "\t" + "endFrame = " + str(scene.frame_end+1) + "\n"
    ImportScript += "\t" + "frameRateDenominator = " + str(scene.render.fps_base) + "\n"
    ImportScript += "\t" + "frameRateNumerator = " + str(scene.render.fps) + "\n"
    ImportScript += "\t" + "secureCrop = 0.0001 #add end crop for avoid section overlay" + "\n"
    ImportScript += "\n"
    ImportScript += "\n"

    # Prepare def
    ImportScript += "\t" + "def AddSequencerSectionTransformKeysByIniFile(SequencerSection, SectionFileName, FileLoc):" + "\n"

    ImportScript += "\t\t" + "Config = ConfigParser.ConfigParser()" + "\n"

    ImportScript += "\t\t" + "Config.read(FileLoc)" + "\n"
    ImportScript += "\t\t" + "for option in Config.options(SectionFileName):" + "\n"
    ImportScript += "\t\t\t" + "frame = float(option)/float(frameRateNumerator) #FrameRate" + "\n"
    ImportScript += "\t\t\t" + "list = Config.get(SectionFileName, option)" + "\n"

    ImportScript += "\t\t\t" + "for x in range(0, 9): #(x,y,z x,y,z x,y,z)" + "\n"
    ImportScript += "\t\t\t\t" + "value = float(list.split(',')[x])" + "\n"
    ImportScript += "\t\t\t\t" + "SequencerSection.get_channels()[x].add_key(unreal.FrameNumber(frame*float(frameRateNumerator)),value)" + "\n"

    ImportScript += "\n"
    ImportScript += "\n"

    ImportScript += "\t" + "def AddSequencerSectionFloatKeysByIniFile(SequencerSection, SectionFileName, FileLoc):" + "\n"

    ImportScript += "\t\t" + "Config = ConfigParser.ConfigParser()" + "\n"

    ImportScript += "\t\t" + "Config.read(FileLoc)" + "\n"
    ImportScript += "\t\t" + "for option in Config.options(SectionFileName):" + "\n"
    ImportScript += "\t\t\t" + "frame = float(option)/float(frameRateNumerator) #FrameRate" + "\n"
    ImportScript += "\t\t\t" + "value = float(Config.get(SectionFileName, option))" + "\n"

    ImportScript += "\t\t\t" + "SequencerSection.get_channels()[0].add_key(unreal.FrameNumber(frame*float(frameRateNumerator)),value)" + "\n"

    ImportScript += "\n"
    ImportScript += "\n"

    ImportScript += "\t" + "def AddSequencerSectionBoolKeysByIniFile(SequencerSection, SectionFileName, FileLoc):" + "\n"

    ImportScript += "\t\t" + "Config = ConfigParser.ConfigParser()" + "\n"

    ImportScript += "\t\t" + "Config.read(FileLoc)" + "\n"
    ImportScript += "\t\t" + "for option in Config.options(SectionFileName):" + "\n"
    ImportScript += "\t\t\t" + "frame = float(option)/float(frameRateNumerator) #FrameRate" + "\n"
    ImportScript += "\t\t\t" + "value = Config.getboolean(SectionFileName, option)" + "\n"

    ImportScript += "\t\t\t" + "SequencerSection.get_channels()[0].add_key(unreal.FrameNumber(frame*float(frameRateNumerator)),value)" + "\n"

    ImportScript += "\n"
    ImportScript += "\n"

    # Prepare process import
    ImportScript += "\t" + 'print("Warning this file already exists")' + "\n"
    ImportScript += "\t" + "factory = unreal.LevelSequenceFactoryNew()" + "\n"
    ImportScript += "\t" + "asset_tools = unreal.AssetToolsHelpers.get_asset_tools()" + "\n"
    ImportScript += "\t" + "seq = asset_tools.create_asset_with_dialog('MySequence', '/Game', None, factory)" + "\n"
    # ImportScript += "unreal.EditorAssetLibrary.save_loaded_asset(seq)" + "\n"

    ImportScript += "\t" + "if seq is None:" + "\n"
    ImportScript += "\t\t" + "return 'Error /!\\ level sequencer factory_create fail' " + "\n"
    ImportScript += "\n"

    ImportScript += "\t" + 'print("Sequencer reference created")' + "\n"
    ImportScript += "\t" + 'print(seq)' + "\n"
    ImportScript += "\t" + "ImportedCamera = [] #(CameraName, CameraGuid)" + "\n"
    ImportScript += "\t" + 'print("========================= Import started ! =========================")' + "\n"
    ImportScript += "\t" + "\n"

    ImportScript += "\t" + "#Set frame rate" + "\n"

    ImportScript += "\t" + "myFFrameRate = unreal.FrameRate()" + "\n"
    ImportScript += "\t" + "myFFrameRate.denominator = frameRateDenominator" + "\n"
    ImportScript += "\t" + "myFFrameRate.numerator = frameRateNumerator" + "\n"
    ImportScript += "\t" + "seq.set_display_rate(myFFrameRate)" + "\n"

    # Set playback range
    ImportScript += "\t" + "#Set playback range" + "\n"

    ImportScript += "\t" + "seq.set_playback_end_seconds((endFrame-secureCrop)/float(frameRateNumerator))" + "\n"
    ImportScript += "\t" + "seq.set_playback_start_seconds(startFrame/float(frameRateNumerator))" + "\n"  # set_playback_end_seconds
    ImportScript += "\t" + "camera_cut_track = seq.add_master_track(unreal.MovieSceneCameraCutTrack)" + "\n"
    ImportScript += "\t" + "camera_cut_track.set_editor_property('display_name', 'Imported Camera Cuts')" + "\n"
    ImportScript += "\t" + "camera_cut_track.set_color_tint(unreal.Color(b=200, g=0, r=0, a=0))" + "\n"

    # ImportScript += "\t" + "world = unreal.EditorLevelLibrary.get_editor_world()" + "\n"

    ImportScript += "\n"
    ImportScript += "\n"

    # Import camera
    for asset in scene.UnrealExportedAssetsList:
        if (asset.assetType == "Camera"):
            camera = asset.object
            ImportScript += "\t" + "#import " + camera.name + "\n"
            ImportScript += "\t" + 'print("Start import ' + camera.name + '")' + "\n"
            ImportScript += "\t" + "\n"

            ImportScript += "\t" + "#Import fbx transform" + "\n"
            AdditionalTracksLoc = (os.path.join(asset.exportPath, GetObjExportFileName(asset.object, "_AdditionalTrack.ini")))
            ImportScript += '\t' + 'AdditionalTracksLoc = os.path.join(r"'+AdditionalTracksLoc+'")' + '\n'
            fbxFilePath = (os.path.join(asset.exportPath, GetObjExportFileName(camera)))
            ImportScript += '\t' + 'fbxFilePath = os.path.join(r"'+fbxFilePath+'")' + '\n'

            # Create spawnable camera
            ImportScript += "\t" + "#Create spawnable camera and add camera in sequencer" + "\n"
            ImportScript += "\t" + "cine_camera_actor = unreal.EditorLevelLibrary().spawn_actor_from_class(unreal.CineCameraActor, unreal.Vector(0, 0, 0), unreal.Rotator(0, 0, 0)) #" + "\n"
            ImportScript += "\n"

            # Import additional tracks

            ImportScript += "\t" + "#Import additional tracks (camera_component)" + "\n"

            ImportScript += "\t" + "camera_component_binding = seq.add_possessable(cine_camera_actor.get_cine_camera_component()) #Get the last" + "\n"
            ImportScript += "\n"

            ImportScript += "\t" + "TrackFocalLength = camera_component_binding.add_track(unreal.MovieSceneFloatTrack)" + "\n"
            ImportScript += "\t" + "TrackFocalLength.set_property_name_and_path('CurrentFocalLength', 'CurrentFocalLength')" + "\n"
            ImportScript += "\t" + "TrackFocalLength.set_editor_property('display_name', 'Current Focal Length')" + "\n"
            ImportScript += "\t" + "sectionFocalLength = TrackFocalLength.add_section()" + "\n"
            ImportScript += "\t" + "sectionFocalLength.set_end_frame_bounded(False)" + "\n"
            ImportScript += "\t" + "sectionFocalLength.set_start_frame_bounded(False)" + "\n"
            ImportScript += "\t" + "AddSequencerSectionFloatKeysByIniFile(sectionFocalLength, 'FocalLength', AdditionalTracksLoc)" + "\n"
            ImportScript += "\n"

            ImportScript += "\t" + "TrackSensorWidth = camera_component_binding.add_track(unreal.MovieSceneFloatTrack)" + "\n"
            ImportScript += "\t" + "TrackSensorWidth.set_property_name_and_path('Filmback.SensorWidth', 'Filmback.SensorWidth')" + "\n"
            ImportScript += "\t" + "TrackSensorWidth.set_editor_property('display_name', 'Sensor Width (Filmback)')" + "\n"
            ImportScript += "\t" + "sectionSensorWidth = TrackSensorWidth.add_section()" + "\n"
            ImportScript += "\t" + "sectionSensorWidth.set_end_frame_bounded(False)" + "\n"
            ImportScript += "\t" + "sectionSensorWidth.set_start_frame_bounded(False)" + "\n"
            ImportScript += "\t" + "AddSequencerSectionFloatKeysByIniFile(sectionSensorWidth, 'SensorWidth', AdditionalTracksLoc)" + "\n"
            ImportScript += "\n"

            ImportScript += "\t" + "TrackSensorHeight = camera_component_binding.add_track(unreal.MovieSceneFloatTrack)" + "\n"
            ImportScript += "\t" + "TrackSensorHeight.set_property_name_and_path('Filmback.SensorHeight', 'Filmback.SensorHeight')" + "\n"
            ImportScript += "\t" + "TrackSensorHeight.set_editor_property('display_name', 'Sensor Height (Filmback)')" + "\n"
            ImportScript += "\t" + "sectionSensorHeight = TrackSensorHeight.add_section()" + "\n"
            ImportScript += "\t" + "sectionSensorHeight.set_end_frame_bounded(False)" + "\n"
            ImportScript += "\t" + "sectionSensorHeight.set_start_frame_bounded(False)" + "\n"
            ImportScript += "\t" + "AddSequencerSectionFloatKeysByIniFile(sectionSensorHeight, 'SensorHeight', AdditionalTracksLoc)" + "\n"
            ImportScript += "\n"

            ImportScript += "\t" + "TrackFocusDistance = camera_component_binding.add_track(unreal.MovieSceneFloatTrack)" + "\n"
            ImportScript += "\t" + "if int(unreal.SystemLibrary.get_engine_version()[:4][2:]) >= 24:" + "\n"
            ImportScript += "\t\t" + "TrackFocusDistance.set_property_name_and_path('CurrentFocusDistance', 'CurrentFocusDistance')" + "\n"
            ImportScript += "\t" + "else:" + "\n"
            ImportScript += "\t\t" + "TrackFocusDistance.set_property_name_and_path('ManualFocusDistance', 'ManualFocusDistance')" + "\n"
            ImportScript += "\t" + "TrackFocusDistance.set_editor_property('display_name', 'Current Focus Distance')" + "\n"
            ImportScript += "\t" + "sectionFocusDistance = TrackFocusDistance.add_section()" + "\n"
            ImportScript += "\t" + "sectionFocusDistance.set_end_frame_bounded(False)" + "\n"
            ImportScript += "\t" + "sectionFocusDistance.set_start_frame_bounded(False)" + "\n"
            ImportScript += "\t" + "AddSequencerSectionFloatKeysByIniFile(sectionFocusDistance, 'FocusDistance', AdditionalTracksLoc)" + "\n"
            ImportScript += "\n"

            ImportScript += "\t" + "TracknAperture = camera_component_binding.add_track(unreal.MovieSceneFloatTrack)" + "\n"
            ImportScript += "\t" + "TracknAperture.set_property_name_and_path('CurrentAperture', 'CurrentAperture')" + "\n"
            ImportScript += "\t" + "TracknAperture.set_editor_property('display_name', 'Current Aperture')" + "\n"
            ImportScript += "\t" + "sectionAperture = TracknAperture.add_section()" + "\n"
            ImportScript += "\t" + "sectionAperture.set_end_frame_bounded(False)" + "\n"
            ImportScript += "\t" + "sectionAperture.set_start_frame_bounded(False)" + "\n"
            ImportScript += "\t" + "AddSequencerSectionFloatKeysByIniFile(sectionAperture, 'Aperture', AdditionalTracksLoc)" + "\n"
            ImportScript += "\n"

            # add a binding for the camera

            ImportScript += "\t" + "camera_binding = seq.add_possessable(cine_camera_actor)" + "\n"

            # Transfer to spawnable camera

            if IsSpawnableCamera:
                ImportScript += "\t" + "camera_spawnable = seq.add_spawnable_from_class(unreal.CineCameraActor) #Add camera in sequencer" + "\n"
                ImportScript += "\t" + "camera_component_binding.set_parent(camera_spawnable)" + "\n"

            # Import fbx transform

            if IsSpawnableCamera:
                ImportScript += "\t" + "transform_track = camera_spawnable.add_track(unreal.MovieScene3DTransformTrack)" + "\n"
            else:
                ImportScript += "\t" + "transform_track = camera_binding.add_track(unreal.MovieScene3DTransformTrack)" + "\n"
            ImportScript += "\t" + "transform_section = transform_track.add_section()" + "\n"
            ImportScript += "\t" + "transform_section.set_end_frame_bounded(False)" + "\n"
            ImportScript += "\t" + "transform_section.set_start_frame_bounded(False)" + "\n"
            ImportScript += "\t" + "AddSequencerSectionTransformKeysByIniFile(transform_section, 'Transform', AdditionalTracksLoc)" + "\n"

            # Set property binding
            if IsSpawnableCamera:
                ImportScript += "\t" + "current_camera_binding = camera_spawnable" + "\n"
            else:
                ImportScript += "\t" + "current_camera_binding = camera_binding" + "\n"
            ImportScript += "\t" + "current_camera_binding.set_display_name('" + camera.name + "')" + "\n"

            ImportScript += "\t" + "tracksSpawned = current_camera_binding.find_tracks_by_exact_type(unreal.MovieSceneSpawnTrack)" + "\n"
            ImportScript += "\t" + "if len(tracksSpawned) > 0:" + "\n"
            # ImportScript += "\t\t" + "trackSpawned.set_property_name_and_path('Spawned', 'Spawned')" + "\n"
            # ImportScript += "\t\t" + "trackSpawned.set_editor_property('display_name', 'Spawned')" + "\n"
            ImportScript += "\t\t" + "sectionSpawned = tracksSpawned[0].get_sections()[0]" + "\n"
            # ImportScript += "\t\t" + "sectionSpawned.set_end_frame_bounded(False)" + "\n"
            # ImportScript += "\t\t" + "sectionSpawned.set_start_frame_bounded(False)" + "\n"
            ImportScript += "\t\t" + "AddSequencerSectionBoolKeysByIniFile(sectionSpawned, 'Spawned', AdditionalTracksLoc)" + "\n"
            ImportScript += "\n"

            # Set property actor
            if IsSpawnableCamera:
                ImportScript += "\t" + "current_cine_camera_actor = camera_spawnable.get_object_template()" + "\n"
            else:
                ImportScript += "\t" + "current_cine_camera_actor = cine_camera_actor" + "\n"

            ImportScript += "\t" + "current_cine_camera_actor.set_actor_label('" + camera.name + "')" + "\n"

            # Set property component
            ImportScript += "\t" + "camera_component = cine_camera_actor.camera_component" + "\n"
            resX = bpy.context.scene.render.resolution_x
            resY = bpy.context.scene.render.resolution_y
            ImportScript += "\t" + "camera_component.aspect_ratio = " + str(resX/resY) + "\n"
            ImportScript += "\t" + "camera_component.lens_settings.min_f_stop = 0" + "\n"
            ImportScript += "\t" + "camera_component.lens_settings.max_f_stop = 1000" + "\n"

            # Clean the created assets
            if IsSpawnableCamera:
                ImportScript += "\t" + "cine_camera_actor.destroy_actor()" + "\n"
                ImportScript += "\t" + "camera_binding.remove()" + "\n"

            if IsSpawnableCamera:
                ImportScript += "\t" + "ImportedCamera.append(('"+camera.name+"', camera_spawnable))" + "\n"
            else:
                ImportScript += "\t" + "ImportedCamera.append(('"+camera.name+"', camera_binding))" + "\n"

            ImportScript += "\n"
            ImportScript += "\n\n"

    def getMarkerSceneSections():
        scene = bpy.context.scene
        markersOrderly = []
        firstMarkersFrame = scene.frame_start
        lastMarkersFrame = scene.frame_end+1

        # If the scene don't use marker
        if len(bpy.context.scene.timeline_markers) < 1:
            return ([[scene.frame_start, scene.frame_end+1, bpy.context.scene.camera]])

        for marker in scene.timeline_markers:
            # Re set first frame
            if marker.frame < firstMarkersFrame:
                firstMarkersFrame = marker.frame

        for x in range(firstMarkersFrame, lastMarkersFrame):
            for marker in scene.timeline_markers:
                if marker.frame == x:
                    markersOrderly.append(marker)
        # ---
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
        # Camera cut sections
        ImportScript += "\t" + "#Import camera cut section" + "\n"

        ImportScript += "\t" + "camera_cut_section = camera_cut_track.add_section()" + "\n"
        if section[2] is not None:
            if section[2].ExportEnum == "export_recursive" or section[2].ExportEnum == "auto":
                ImportScript += "\t" + "for camera in ImportedCamera:" + "\n"
                ImportScript += "\t\t" + "if camera[0] == '"+section[2].name+"':" + "\n"
                ImportScript += "\t\t\t" + "camera_binding_id = unreal.MovieSceneObjectBindingID()" + "\n"
                # ImportScript += "\t\t\t" + "camera_binding_id.set_editor_property('guid', camera[1].get_id())" + "\n"
                ImportScript += "\t\t\t" + "camera_binding_id = seq.make_binding_id(camera[1], unreal.MovieSceneObjectBindingSpace.LOCAL)" + "\n"
                ImportScript += "\t\t\t" + "camera_cut_section.set_camera_binding_id(camera_binding_id)" + "\n"
            else:
                ImportScript += "\t" + "#Not camera found for this section" + "\n"
        else:
            ImportScript += "\t" + "#Not camera found for this section" + "\n"
        # ImportScript += "\t" + "sectionRange = unreal.MovieSceneFrameRange()" + "\n"
        # ImportScript += "\t" + "camera_cut_section.set_editor_property('section_range', sectionRange)" + "\n"

        ImportScript += "\t" + "camera_cut_section.set_end_frame_seconds(("+str(section[1])+"-secureCrop)/float(frameRateNumerator))" + "\n"
        ImportScript += "\t" + "camera_cut_section.set_start_frame_seconds("+str(section[0])+"/float(frameRateNumerator))" + "\n"
        ImportScript += "\t" + "\n"

    # Import result
    ImportScript += "\t" + "print('========================= Imports completed ! =========================')" + "\n"
    ImportScript += "\t" + "\n"
    ImportScript += "\t" + "for cam in ImportedCamera:" + "\n"
    ImportScript += "\t\t" + "print(cam[0])" + "\n"
    ImportScript += "\t" + "\n"
    ImportScript += "\t" + "print('=========================')" + "\n"

    ImportScript += "#Select and open seq in content browser" + "\n"

    ImportScript += "\t" + "if int(unreal.SystemLibrary.get_engine_version()[:4][2:]) >= 26:" + "\n"
    ImportScript += "\t\t" + "unreal.AssetEditorSubsystem.open_editor_for_assets(unreal.AssetEditorSubsystem(), [unreal.load_asset(seq.get_path_name())])" + "\n"
    ImportScript += "\t" + "else:" + "\n"
    ImportScript += "\t\t" + "unreal.AssetToolsHelpers.get_asset_tools().open_editor_for_assets([unreal.load_asset(seq.get_path_name())])" + "\n"
    ImportScript += "\t" + "unreal.EditorAssetLibrary.sync_browser_to_objects([seq.get_path_name()])" + "\n"
    ImportScript += "\t" + "return 'Sequencer created with success !' " + "\n"

    # -------------------------------------

    CheckScript = ""

    CheckScript += "import unreal" + "\n"

    CheckScript += "if hasattr(unreal, 'EditorAssetLibrary') == False:" + "\n"
    CheckScript += "\t" + "print('--------------------------------------------------')" + "\n"
    CheckScript += "\t" + "print('/!\\ Warning: Editor Scripting Utilities should be activated.')" + "\n"
    CheckScript += "\t" + "print('Plugin > Scripting > Editor Scripting Utilities.')" + "\n"
    CheckScript += "\t" + "return False" + "\n"

    CheckScript += "if hasattr(unreal.MovieSceneSequence, 'set_display_rate') == False:" + "\n"
    CheckScript += "\t" + "print('--------------------------------------------------')" + "\n"
    CheckScript += "\t" + "print('/!\\ Warning: Editor Scripting Utilities should be activated.')" + "\n"
    CheckScript += "\t" + "print('Plugin > Scripting > Sequencer Scripting.')" + "\n"
    CheckScript += "\t" + "return False" + "\n"

    CheckScript += "return True" + "\n"

    # -------------------------------------

    OutImportScript = ""
    OutImportScript += WriteImportPythonHeadComment(True)

    OutImportScript += "def CheckTasks():" + "\n"
    OutImportScript += bfu_utils.AddFrontEachLine(CheckScript, "\t")

    OutImportScript += "def CreateSequencer():" + "\n"
    OutImportScript += bfu_utils.AddFrontEachLine(ImportScript, "\t")

    OutImportScript += "if CheckTasks() == True:" + "\n"
    OutImportScript += "\t" + "print(CreateSequencer())" + "\n"

    return OutImportScript
