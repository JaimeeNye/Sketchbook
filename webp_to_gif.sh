#!/bin/bash 

# REQUIRES
# 'anim_dump' and 'webpmux' from libwebp.
# See https://askubuntu.com/questions/1140873/how-can-i-convert-an-animated-webp-to-a-webm/1141049#1141049
# 
# 'convert' from ImageMagick
trap "exit 0" 2 3

mkdir gif_converted

gif_name=0

for filename in *.webp;
do
    gif_name=$(($gif_name+1))
    sticker_tmpdir=$(mktemp -d)
    anim_dump -folder $sticker_tmpdir $filename 1>/dev/null

    framerate=$(webpmux -info $filename | awk '{ print $7 }' | egrep -o '[[:digit:]]*' | sort -n | uniq)

    echo -ne "Converting $filename into $gif_name.gif "

    if [ $(echo "$framerate" | wc -l) != 1 ]
    then
        echo "Different frame durations in $filename."
        framerate=$(echo "$framerate" | head -1) # Get the lowest framerate
        echo "Now using framerate $framerate"
        
    fi 

    filesize=20000
    target_hw=512

    progression_message="."

    while [ $filesize -gt 95 ]
    do
        # While the size of the file is greater than 95kb, regenerate the GIF with smaller size.
        # Not optimal, but hey, it works!
        progression_message="${progression_message}."
        echo -ne "$progression_message"
        convert -delay $(($framerate/10)) -dispose Background -loop 0 $sticker_tmpdir/dump_*.png -resize ${target_hw}x$target_hw -coalesce -fuzz 8% +dither -layers OptimizePlus gif_converted/$gif_name.gif
        gifsicle --batch -O3 -i gif_converted/$gif_name.gif 2>/dev/null

        filesize=$((`stat -c%s gif_converted/$gif_name.gif`/1000))
        target_hw=$(($target_hw-20))
        
    done

    echo -e "\nFinal size: ${filesize}kb ($(identify -format '%wx%h' gif_converted/$gif_name.gif[0])) \n\n"
    rm -rf $sticker_tmpdir

done

echo "✨ Add done! ✨"
