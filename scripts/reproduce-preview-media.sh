#!/usr/bin/env bash
# Recreate preview media from the completed 30-second master. No scene rerender.
# Usage: bash reproduce-preview-media.sh path/to/master.mp4 [output-directory]
set -euo pipefail
src="${1:?Provide the exact completed master MP4}"
out="${2:-media}"
mkdir -p "$out"
ffmpeg -hide_banner -loglevel error -nostdin -y -i "$src" -map 0:v:0 -an -vf scale=640:360:flags=lanczos -c:v libx264 -preset slow -crf 24 -pix_fmt yuv420p -movflags +faststart -map_metadata -1 "$out/athens-30s-preview.mp4"
ffmpeg -hide_banner -loglevel error -nostdin -y -i "$src" -filter_complex 'fps=4,scale=360:202:flags=lanczos,split[s0][s1];[s0]palettegen=max_colors=80:stats_mode=diff[p];[s1][p]paletteuse=dither=bayer:bayer_scale=4' -loop 0 -map_metadata -1 "$out/athens-30s-preview.gif"
ffmpeg -hide_banner -loglevel error -nostdin -y -ss 12.5 -i "$src" -frames:v 1 -vf scale=960:540:flags=lanczos -q:v 2 -map_metadata -1 "$out/poster.jpg"
ffmpeg -hide_banner -loglevel error -nostdin -y -i "$src" -vf 'fps=1/2.5,scale=400:225:flags=lanczos,tile=4x3:padding=4:margin=4' -frames:v 1 -q:v 3 -map_metadata -1 "$out/contact-sheet.jpg"
