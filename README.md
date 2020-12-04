# bilibili_autorec  哔哩哔哩自动录播机

## README正在施工中...

## 功能

* 监测是否开播，开播后自动录制
* 自动合并可能出现的多片flv并转码，可根据需要选择是否遮挡画面
* 自动上传录播
* 实时监控输出

## 如何使用

1. 下载[ffmpeg](https://www.gyan.dev/ffmpeg/builds/)，下载ffmpeg-release-full版本，解压后重命名为ffmpeg，放在utils路径下
2. pip install streamlink
3. 根据提示修改两个demo配置文件
4. python main.py

## 用到的开源项目

* [bilibili_api](https://github.com/Passkou/bilibili_api)
* [rich](https://github.com/willmcgugan/rich)
* [FFmpeg](https://github.com/FFmpeg/FFmpeg)
* [Bilibili-Toolkit](https://github.com/Hsury/Bilibili-Toolkit)
* [streamlink](https://github.com/streamlink/streamlink)