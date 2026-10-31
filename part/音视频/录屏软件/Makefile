# Makefile for Screen Recorder with Cross-Compilation Support

# 检测目标平台
PLATFORM ?= linux
ifeq ($(OS),Windows_NT)
    PLATFORM = windows
endif

# 基础设置
SOURCES = main.cpp recording.cpp

# Linux 本地编译配置
ifeq ($(PLATFORM),linux)
    CXX = g++
    CXXFLAGS = -std=c++11 -Wall -Wextra -DLINUX_BUILD
    FFMPEG_LIBS = -lavcodec -lavdevice -lavfilter -lavformat -lavutil -lswscale
    X11_LIBS = -lX11 -lXext -lXfixes
    INCLUDES = -I/usr/include/x86_64-linux-gnu
    TARGET = screen_recorder
    OBJECTS = $(SOURCES:.cpp=.o)
    PLATFORM_LIBS = $(X11_LIBS)
endif

# Windows 交叉编译配置
ifeq ($(PLATFORM),windows)
    # MinGW-w64 交叉编译器
    CXX = x86_64-w64-mingw32-g++
    CXXFLAGS = -std=c++11 -Wall -Wextra -DWINDOWS_BUILD -static-libgcc -static-libstdc++
    
    # Windows FFmpeg 库路径 (需要预先下载Windows版本的FFmpeg)
    FFMPEG_WIN_PATH = ./ffmpeg-win64
    INCLUDES = -I$(FFMPEG_WIN_PATH)/include
    FFMPEG_LIBS = -L$(FFMPEG_WIN_PATH)/lib -lavcodec -lavdevice -lavfilter -lavformat -lavutil -lswscale
    
    # Windows 特有库
    WIN_LIBS = -lgdi32 -luser32 -lkernel32 -lole32 -loleaut32 -luuid -lstrmiids
    PLATFORM_LIBS = $(WIN_LIBS)
    
    TARGET = screen_recorder.exe
    OBJECTS = $(SOURCES:.cpp=.obj)
endif

# macOS 交叉编译配置 (可选)
ifeq ($(PLATFORM),macos)
    CXX = clang++
    CXXFLAGS = -std=c++11 -Wall -Wextra -DMACOS_BUILD
    FFMPEG_LIBS = -lavcodec -lavdevice -lavfilter -lavformat -lavutil -lswscale
    MACOS_LIBS = -framework AVFoundation -framework CoreMedia -framework CoreVideo
    INCLUDES = 
    TARGET = screen_recorder
    OBJECTS = $(SOURCES:.cpp=.o)
    PLATFORM_LIBS = $(MACOS_LIBS)
endif

# 构建规则
all: $(TARGET)

# 链接目标文件
$(TARGET): $(OBJECTS)
	$(CXX) $(OBJECTS) -o $(TARGET) $(FFMPEG_LIBS) $(PLATFORM_LIBS)

# Linux编译规则
%.o: %.cpp
	$(CXX) $(CXXFLAGS) $(INCLUDES) -c $< -o $@

# Windows编译规则
%.obj: %.cpp
	$(CXX) $(CXXFLAGS) $(INCLUDES) -c $< -o $@

# 清理生成的文件
clean:
	rm -f *.o *.obj $(TARGET) screen_recorder screen_recorder.exe

# 平台特定构建目标
linux:
	$(MAKE) PLATFORM=linux

windows:
	$(MAKE) PLATFORM=windows

macos:
	$(MAKE) PLATFORM=macos

# 安装交叉编译工具链
install-mingw:
	sudo apt update
	sudo apt install -y mingw-w64 mingw-w64-tools

# 下载Windows版FFmpeg
download-ffmpeg-windows:
	@echo "下载Windows版FFmpeg..."
	@mkdir -p ffmpeg-win64
	@if [ ! -f "ffmpeg-win64.zip" ]; then \
		wget -O ffmpeg-win64.zip "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl-shared.zip"; \
	fi
	@if [ ! -d "ffmpeg-win64/include" ]; then \
		unzip -q ffmpeg-win64.zip; \
		mv ffmpeg-master-latest-win64-gpl-shared/* ffmpeg-win64/; \
		rmdir ffmpeg-master-latest-win64-gpl-shared; \
	fi
	@echo "FFmpeg Windows版本已准备就绪"

# 安装依赖 (Ubuntu/Debian)
install-deps-ubuntu:
	sudo apt update
	sudo apt install -y ffmpeg libavcodec-dev libavdevice-dev libavfilter-dev \
	                   libavformat-dev libavutil-dev libswscale-dev \
	                   libx11-dev libxext-dev libxfixes-dev build-essential

# 安装依赖 (CentOS/RHEL/Fedora)
install-deps-fedora:
	sudo dnf install -y ffmpeg-devel libX11-devel libXext-devel libXfixes-devel \
	                   gcc-c++ make

# 安装Windows交叉编译环境
setup-windows-cross:
	@echo "设置Windows交叉编译环境..."
	$(MAKE) install-mingw
	$(MAKE) download-ffmpeg-windows
	@echo "Windows交叉编译环境设置完成"

# 创建输出目录
setup:
	mkdir -p media

# 运行程序 (仅Linux)
run: linux setup
	./$(TARGET)

# Windows构建并打包
build-windows: windows
	@echo "构建Windows版本完成: $(TARGET)"
	@echo "可执行文件: $(TARGET)"
	@if [ -d "ffmpeg-win64/bin" ]; then \
		echo "需要的DLL文件位于: ffmpeg-win64/bin/"; \
		echo "部署时需要将以下文件与可执行文件放在同一目录:"; \
		ls ffmpeg-win64/bin/*.dll 2>/dev/null || echo "未找到DLL文件"; \
	fi

# 显示帮助信息
help:
	@echo "Screen Recorder 构建系统"
	@echo ""
	@echo "可用目标:"
	@echo "  all              - 构建当前平台版本"
	@echo "  linux            - 构建Linux版本"
	@echo "  windows          - 构建Windows版本"
	@echo "  macos            - 构建macOS版本"
	@echo "  clean            - 清理生成的文件"
	@echo ""
	@echo "Windows交叉编译:"
	@echo "  setup-windows-cross  - 安装Windows交叉编译环境"
	@echo "  build-windows        - 构建Windows版本并显示部署信息"
	@echo ""
	@echo "依赖安装:"
	@echo "  install-deps-ubuntu  - 安装Ubuntu/Debian依赖"
	@echo "  install-deps-fedora  - 安装Fedora/CentOS依赖"
	@echo "  install-mingw        - 安装MinGW交叉编译器"
	@echo ""
	@echo "使用示例:"
	@echo "  make linux           - 构建Linux版本"
	@echo "  make setup-windows-cross && make windows - 设置并构建Windows版本"

.PHONY: all clean linux windows macos install-deps-ubuntu install-deps-fedora \
        install-mingw download-ffmpeg-windows setup-windows-cross run build-windows help
