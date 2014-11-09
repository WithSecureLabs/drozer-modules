LOCAL_PATH := $(call my-dir)
 
include $(CLEAR_VARS)
 
LOCAL_MODULE    := towelroot
LOCAL_SRC_FILES := towelroot.c
LOCAL_CFLAGS := -fno-stack-protector -mno-thumb -O0
 
include $(BUILD_EXECUTABLE)
