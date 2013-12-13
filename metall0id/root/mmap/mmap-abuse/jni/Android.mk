LOCAL_PATH := $(call my-dir)
 
include $(CLEAR_VARS)
 
LOCAL_MODULE    := mmap-abuse
LOCAL_SRC_FILES := mmap-abuse.c
 
include $(BUILD_EXECUTABLE)
