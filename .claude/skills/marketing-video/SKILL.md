---
name: marketing-video
description: Produce trailers, app demos, videogame captures, and presentation videos — capture, programmatic composition (Remotion), narration, and size optimization. Use for any "record a demo", "make a trailer", or "feature video" request.
---

# Marketing video production

Content (scripts, inventory, per-feature checklist) lives in
docs/03-technical/09-marketing/02-videos.md — this skill is the HOW.

**Vertical reels showing functionality** (gameplay, mechanics, feature demos as
running footage) are their own format → use the `feature-reel` skill. This skill
covers trailers, narrated demos, and presentation videos.

## 1. Capture

- **App demo (scripted, repeatable)**: drive the flow with Selenium against `make up`,
  record the screen. X11: `ffmpeg -f x11grab -framerate 30 -video_size 1920x1080 -i :0.0 out.mp4`;
  headless: run under `xvfb-run` and record the virtual display. A Playwright script
  with `recordVideo` is an alternative when the flow needs smooth cursor motion.
- **Videogame demo**: capture the game window with ffmpeg `x11grab` (add
  `-f pulse -i default` for audio) or OBS when you need scene switching; 60 fps
  (`-framerate 60`) for gameplay.

## 2. Compose (trailers, intros, captions)

- **Remotion** (React-based programmatic video) for branded intros/outros, captions,
  and data-driven sequences. An official Remotion skill for Claude Code exists —
  prefer installing/invoking it for composition work; fall back to
  `npx create-video@latest` + remotion.dev/docs. Feed captured .mp4 clips in via
  `<OffthreadVideo>`; render with `npx remotion render`.
- Quick assemblies (concat + title cards + fades) don't need Remotion — use ffmpeg
  `concat` demuxer + `drawtext`/`xfade` filters.

## 3. Narration

- TTS: `edge-tts --voice es-CL-LorenzoNeural --text "$SCRIPT" --write-media narration.mp3`
  (pick the voice per audience language); mux with
  `ffmpeg -i video.mp4 -i narration.mp3 -c:v copy -map 0:v -map 1:a out.mp4`.

## 4. Size optimization (trailers must stay small)

- Default preset: `ffmpeg -i in.mp4 -c:v libx264 -crf 23 -preset slow -movflags +faststart -c:a aac -b:a 96k out.mp4`
- Hard size target (e.g. ≤20 MB for 60 s): two-pass with computed bitrate
  `bitrate_kbps ≈ (target_MB*8192 / seconds) - 96`:
  `ffmpeg -i in.mp4 -c:v libx264 -b:v {rate}k -pass 1 -an -f null /dev/null &&
   ffmpeg -i in.mp4 -c:v libx264 -b:v {rate}k -pass 2 -c:a aac -b:a 96k out.mp4`
- AV1 (`-c:v libsvtav1 -crf 32`) ≈ 30% smaller when playback targets are modern.
- 1080p max for demos; trim dead time before compressing; verify with `du -h`.
- Record resulting size/quality trade-offs in docs/04-findings/benchmarks/disk.md.
