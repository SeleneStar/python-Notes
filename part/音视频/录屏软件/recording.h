#ifndef SCREENRECORDER_H
#define SCREENRECORDER_H

// 平台检测
#ifdef WINDOWS_BUILD
    #define PLATFORM_WINDOWS
    #include "recording_win.h"
#else
    // Linux/Unix平台
    #include <iostream>
    #include <cstdio>
    #include <cstdlib>
    #include <fstream>
    #include <cstring>

    #define __STDC_CONSTANT_MACROS

    #ifdef LINUX_BUILD
        #define PLATFORM_LINUX
    #elif defined(MACOS_BUILD)
        #define PLATFORM_MACOS
    #else
        // 自动检测平台
        #ifdef __linux__
            #define PLATFORM_LINUX
        #elif __APPLE__
            #define PLATFORM_MACOS
        #endif
    #endif

    //FFMPEG LIBRARIES
    extern "C"
    {
    #include "libavcodec/avcodec.h"
    #include "libavdevice/avdevice.h"
    #include "libavfilter/avfilter.h"
    #include "libavfilter/buffersink.h"
    #include "libavfilter/buffersrc.h"
    #include "libavformat/avformat.h"
    #include "libavformat/avio.h"
    #include "libavutil/opt.h"
    #include "libavutil/common.h"
    #include "libavutil/channel_layout.h"
    #include "libavutil/imgutils.h"
    #include "libavutil/mathematics.h"
    #include "libavutil/samplefmt.h"
    #include "libavutil/time.h"
    #include "libavutil/pixdesc.h"
    #include "libavutil/file.h"
    #include "libswscale/swscale.h"
    }
#endif



class ScreenRecorder
{
private:
	AVInputFormat *pAVInputFormat;
	AVOutputFormat *output_format;

	AVCodecContext *pAVCodecContext;

	AVFormatContext *pAVFormatContext;

	AVFrame *pAVFrame;
	AVFrame *outFrame;

	AVCodec *pAVCodec;
	AVCodec *outAVCodec;

	AVPacket *pAVPacket;

	AVDictionary *options;

	AVOutputFormat *outAVOutputFormat;
	AVFormatContext *outAVFormatContext;
	AVCodecContext *outAVCodecContext;

	AVStream *video_st;
	AVFrame *outAVFrame;

	const char *dev_name;
	const char *output_file;

	double video_pts;

	int out_size;
	int codec_id;
	int value;
	int VideoStreamIndx;

public:

	ScreenRecorder();
	~ScreenRecorder();

	/* function to initiate communication with display library */
	int openCamera();
	int init_outputfile();
	int CaptureVideoFrames();

};

#endif