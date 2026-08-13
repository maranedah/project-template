# Screen capture commands

Read this when: capturing UI evidence (review, docs, demo, bug report).

```bash
# Full-page screenshot of a URL (no test needed)
google-chrome --headless --disable-gpu --screenshot=shot.png --window-size=1440,900 "$E2E_BASE_URL"

# From inside a Selenium test/page object
driver.save_screenshot("frontend/e2e/screenshots/<name>.png")

# Record the screen (X11) — demos, bug reproductions
ffmpeg -f x11grab -framerate 30 -video_size 1920x1080 -i :0.0 -t 30 capture.mp4

# Record a compose-stack session headlessly (virtual display)
xvfb-run -s "-screen 0 1440x900x24" python -m pytest frontend/e2e/ -n 0

# Compare two screenshots (visual regression, needs imagemagick)
compare -metric AE before.png after.png diff.png
```

Video post-processing/size optimization: see the marketing-video skill
(`.claude/skills/marketing-video/SKILL.md`).
