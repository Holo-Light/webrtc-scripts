"""
  Declared error codes and error messages.
"""

NO_ERROR, \
ERROR_SYSTEM_ERROR, \
ERROR_SYSTEM_MISSING_GIT, \
ERROR_SYSTEM_MISSING_PERL,\
ERROR_SYSTEM_FAILED_USERDEF_CREATION,\
ERROR_SYSTEM_FAILED_DELETING_USERDEF,\
ERROR_TARGET_NOT_SUPPORTED,\
ERROR_PLATFORM_NOT_SUPPORTED,\
ERROR_PREPARE_CREATING_FOLDERS_FAILED,\
ERROR_PREPARE_CREATING_LINKS_FAILED,\
ERROR_PREPARE_COPYING_FILES_FAILED,\
ERROR_PREPARE_INSTALLING_CLANG_FAILED,\
ERROR_PREPARE_DOWNLOADING_TOOLS_FAILED,\
ERROR_PREPARE_SET_UP_FAILED,\
ERROR_PREPARE_OUTPUT_FOLDER_PREPARATION_FAILED,\
ERROR_PREPARE_UPDATING_DEPS_FAILED,\
ERROR_PREPARE_GN_GENERATION_FAILED,\
ERROR_NUGET_CREATION_MISSING_FILE,\
ERROR_ACQUIRE_NUGET_EXE_FAILED,\
ERROR_GET_NUGET_PACKAGE_VERSIONS_FAILED,\
ERROR_PACKAGE_VERSION_NOT_SUPPORTED,\
ERROR_CREATE_NUGET_FILE_FAILED,\
ERROR_CHANGE_NUSPEC_FAILED,\
ERROR_LOADING_NUGET_PACKAGES,\
ERROR_SELECTING_NUGET_PACKAGES,\
ERROR_BUILD_OUTPUT_FOLDER_NOT_EXIST,\
ERROR_BUILD_UPDATING_DEPS_FAILED,\
ERROR_BUILD_FAILED,\
ERROR_BUILD_MISSING_LIB_EXECUTABLE,\
ERROR_BUILD_MERGE_LIBS_FAILED,\
ERROR_BUILD_BUILDING_WRAPPER_FAILED,\
ERROR_BUILD_BACKUP_DELETION_FAILED,\
ERROR_BUILD_BACKUP_FAILED,\
ERROR_SUBPROCESS_EXECUTAION_FAILED,\
ERROR_CLEANUP_DELETING_OUTPUT_FAILED,\
ERROR_CLEANUP_DELETING_FLG_FILES_FAILED,\
ERROR_CLEANUP_DELETING_GENERATED_FILES_FAILED,\
ERROR_CLEANUP_REVERTING_PREPARE_CHANGES_FAILED = range(38)


ERROR_COPY_LIB_FILES_FAILED = "Failed to copy lib file!"

#TODO: give more details about perl if it is really required
#TODO: check python version and show error if it is 3.0 or later
error_codes = {
  ERROR_SYSTEM_ERROR : 'Unknown system erorr',
  ERROR_SYSTEM_MISSING_GIT : 'Git is missing!',
  ERROR_SYSTEM_MISSING_PERL : 'Perl is missing!',
  ERROR_SYSTEM_FAILED_USERDEF_CREATION : 'Failed userdef.py file cretion!',
  ERROR_SYSTEM_FAILED_DELETING_USERDEF : 'Failed deleting userdef.py file!',
  ERROR_TARGET_NOT_SUPPORTED : 'Target is not supported!',
  ERROR_PLATFORM_NOT_SUPPORTED : 'Platform is not supported!',
  ERROR_PREPARE_CREATING_FOLDERS_FAILED : 'Failed creating folders!',
  ERROR_PREPARE_CREATING_LINKS_FAILED : 'Failed creating links!',
  ERROR_PREPARE_COPYING_FILES_FAILED : 'Failed copying files!',
  ERROR_PREPARE_INSTALLING_CLANG_FAILED : 'Failed installing clang!',
  ERROR_PREPARE_DOWNLOADING_TOOLS_FAILED : 'Failed downloading tools!',
  ERROR_PREPARE_SET_UP_FAILED : 'Prepare set up failed!',
  ERROR_PREPARE_OUTPUT_FOLDER_PREPARATION_FAILED : 'Failed creating output folder or preparing args.gn!',
  ERROR_PREPARE_UPDATING_DEPS_FAILED : 'Failed updating target dependencies!',
  ERROR_PREPARE_GN_GENERATION_FAILED : 'Generating WebRtc projects has failed!',
  ERROR_NUGET_CREATION_MISSING_FILE : 'File missing',
  ERROR_ACQUIRE_NUGET_EXE_FAILED: 'Failed to acquire nuget.exe file!',
  ERROR_GET_NUGET_PACKAGE_VERSIONS_FAILED: 'Failed to retreve NuGet package versions!',
  ERROR_PACKAGE_VERSION_NOT_SUPPORTED: 'Nuget package version specified doesn\'t exist on nuget.org',
  ERROR_CREATE_NUGET_FILE_FAILED: 'Failed to create file necessary for packaging NuGet packet!',
  ERROR_CHANGE_NUSPEC_FAILED: 'Failed to change .nuspec file!',
  ERROR_LOADING_NUGET_PACKAGES: 'Failed to load NuGet packages!',
  ERROR_SELECTING_NUGET_PACKAGES: 'Failed to select NuGet package!',
  ERROR_BUILD_OUTPUT_FOLDER_NOT_EXIST : 'Output folder doesn\'t exist',
  ERROR_BUILD_UPDATING_DEPS_FAILED : 'Failed updating target dependencies!',
  ERROR_BUILD_FAILED : 'Build has failed',
  ERROR_BUILD_MISSING_LIB_EXECUTABLE : 'Missing file lib.exe file for specified CPU!',
  ERROR_BUILD_MERGE_LIBS_FAILED : 'Merging libraries has failed!',
  ERROR_BUILD_BUILDING_WRAPPER_FAILED : 'Building wrapper projects has failed!',
  ERROR_BUILD_BACKUP_DELETION_FAILED : 'Failed deleting old backup folder!',
  ERROR_BUILD_BACKUP_FAILED : 'Failed creating build backup!',
  ERROR_SUBPROCESS_EXECUTAION_FAILED : 'Subprocess execution has failed!',
  ERROR_CLEANUP_DELETING_OUTPUT_FAILED : 'Failed deleting output folders!',
  ERROR_CLEANUP_DELETING_FLG_FILES_FAILED : 'Failed deleting .flg files!',
  ERROR_CLEANUP_DELETING_GENERATED_FILES_FAILED : 'Failed deleting files generated with idl compiler!',
  ERROR_CLEANUP_REVERTING_PREPARE_CHANGES_FAILED : 'Failed reverting prepare changes!'
}