#ifndef RECORDING_WIN_H
#define RECORDING_WIN_H

// Windows平台专用头文件
#ifdef WINDOWS_BUILD

#define WIN32_LEAN_AND_MEAN
#define NOMINMAX

extern "C" {
#include "libavcodec/avcodec.h"
#include "libavdevice/avdevice.h"
#include "libavformat/avformat.h"
#include "libavutil/opt.h"
#include "libavutil/imgutils.h"
#include "libavutil/mathematics.h"
#include "libswscale/swscale.h"
}

#include <iostream>
#include <cstdio>
#include <cstdlib>

#endif // WINDOWS_BUILD

#endif // RECORDING_WIN_H
