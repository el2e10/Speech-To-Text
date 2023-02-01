#! /bin/bash
if test $# -eq 2; then
    parallel 'ffmpeg -y -ss 12 -to $(( $(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 {} |cut -d\. -f1) - 32))  -i {} -f wav -acodec pcm_s16le -ac 1 -ar 16000 {.}.wav' ::: $1/*.webm
    # parallel 'ffmpeg -ss 12 -i {} -f wav -acodec pcm_s16le -ac 1 -ar 16000 {.}.wav' ::: $1/*.webm
    if test $? -eq 0; then
        mkdir -p $2
        mv $1/*.wav $2 #&& rm $1/*.webm 
        echo "Audio files converted to wav format"
        exit 0
    else
        rm $1/*.wav
        echo "Audio processing failed"
        exit 1
    fi
else
    echo "Less num of inputs"
    exit 1
fi