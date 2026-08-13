---
name: feature-reel
description: Record a RUNNING feature or gameplay demo and edit it into a vertical reel (Instagram Reels / TikTok / YouTube Shorts) — window capture, highlight cut, 9:16 conversion, burned captions, platform export. Use for "make a reel", "show this mechanic/feature/gameplay", shorts requests. Trailers/CTA videos are the marketing-video skill instead.
---

# Feature reel: running demo → vertical short

A reel SHOWS the thing working — real gameplay, real UI, real speed. No title cards,
no call-to-action padding: hook → demo → payoff. Target 15–45 s, 9:16, captioned
(most viewers watch muted).

## 0. Shot list (write 3 lines before recording)

1. **Hook (0–2 s)**: the single coolest moment, copied to the front as a teaser.
2. **Demo**: the mechanic in action, uncut enough to feel real.
3. **Payoff (last 2–3 s)**: the result on screen; end visually close to the hook so
   the loop feels seamless.

## 1. Record the running demo

- **Game/desktop window** (60 fps for gameplay). Find the window geometry, then capture
  exactly it:
  ```bash
  xdotool search --name "<window title>" getwindowgeometry --shell   # X, Y, WIDTH, HEIGHT
  ffmpeg -f x11grab -framerate 60 -video_size ${WIDTH}x${HEIGHT} -i :0.0+${X},${Y} \
         -f pulse -i default raw.mkv          # drop the pulse pair if no game audio
  ```
- **Web app**: `make up`, drive the flow with Selenium, record under a virtual display
  (commands: docs/03-technical/07-e2e-validation/02-screen-capture.md).
- Record 2–3 generous takes of real play — cut later, never stage jerky "perfect" runs.

## 2. Cut the highlights

Watch the take, note in/out timestamps, extract losslessly and assemble:

```bash
ffmpeg -ss 00:12 -to 00:19 -i raw.mkv -c copy clip1.mkv     # one per moment
printf "file 'clip_hook.mkv'\nfile 'clip1.mkv'\nfile 'clip2.mkv'\n" > list.txt
ffmpeg -f concat -safe 0 -i list.txt -c copy cut.mkv
```

`clip_hook` is a 1–2 s copy of the best moment placed first. Total ≤45 s.

## 3. Vertical 9:16 (1080×1920)

Pick per footage:

- **Blurred background** (default for landscape gameplay — full frame visible,
  blurred zoom fills top/bottom):
  ```bash
  ffmpeg -i cut.mkv -filter_complex \
    "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,gblur=sigma=30[bg];\
     [0:v]scale=1080:-2[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2" vertical.mkv
  ```
- **Center crop** when the action lives mid-screen: `-vf "crop=ih*9/16:ih,scale=1080:1920"`
- **Stacked** (gameplay + second panel like a map/UI): two inputs scaled 1080:-2,
  `vstack`, then pad/crop to 1920.

## 4. Captions (viewers are muted)

Caption the mechanic AS IT HAPPENS — short lines, high contrast, top third
(platform UI covers the bottom):

```bash
ffmpeg -i vertical.mkv -vf "drawtext=text='Tipo AGUA vence a FUEGO':fontsize=64:\
fontcolor=white:borderw=4:bordercolor=black:x=(w-text_w)/2:y=220:enable='between(t,3,7)'" captioned.mkv
```

Chain one `drawtext` per caption, or burn an `.srt`:
`-vf "subtitles=captions.srt:force_style='FontSize=22,Outline=2,Alignment=8'"`.
Hook text in the first 2 s ("watch what happens when…") decides the swipe.

## 5. Export

```bash
ffmpeg -i captioned.mkv -c:v libx264 -crf 21 -preset slow -r 60 -pix_fmt yuv420p \
       -movflags +faststart -c:a aac -b:a 128k reel.mp4
```

- Specs: 1080×1920, ≤60 s (Shorts) / ≤90 s (IG Reels), keep ≤50 MB (`du -h`); tighter
  size targets → two-pass math in the marketing-video skill.
- Name it `reel-<feature-slug>.mp4`, add an inventory row (type `reel`) in
  docs/03-technical/09-marketing/02-videos.md, and link it from the feature's
  `## Demo video` slot.
