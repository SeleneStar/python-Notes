#include <iostream>
extern "C" {
#include "libavcodec/avcodec.h"
#include "libavdevice/avdevice.h"
#include "libavformat/avformat.h"
}

using namespace std;

int main() {
    cout << "Testing FFmpeg WSL setup..." << endl;
    
    // 初始化FFmpeg
    av_register_all();
    avdevice_register_all();
    cout << "✓ FFmpeg initialized" << endl;
    
    // 测试查找x11grab
    AVInputFormat *input_format = av_find_input_format("x11grab");
    if (input_format) {
        cout << "✓ x11grab input format found" << endl;
    } else {
        cout << "✗ x11grab input format not found" << endl;
        return 1;
    }
    
    // 测试打开显示器
    AVFormatContext *format_ctx = avformat_alloc_context();
    
    AVDictionary *options = NULL;
    av_dict_set(&options, "video_size", "640x480", 0);
    av_dict_set(&options, "framerate", "5", 0);
    
    int ret = avformat_open_input(&format_ctx, ":0.0", input_format, &options);
    if (ret < 0) {
        char errbuf[AV_ERROR_MAX_STRING_SIZE];
        av_strerror(ret, errbuf, AV_ERROR_MAX_STRING_SIZE);
        cout << "✗ Failed to open display: " << errbuf << endl;
        return 1;
    }
    
    cout << "✓ Successfully opened display :0.0" << endl;
    
    // 清理
    avformat_close_input(&format_ctx);
    av_dict_free(&options);
    
    cout << "✓ WSL X11 capture test successful!" << endl;
    return 0;
}
