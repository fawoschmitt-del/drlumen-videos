# Daily run – make and schedule one Dr. Lumen video

Read this whole file first, then do every step. Language of the videos: **English**. Length: **at least 65 s** (aim 75–100 s).

## 0. Setup
    bash setup.sh

## 1. Pick a topic
Open `topics.md`. Pick the most surprising question from the backlog that is NOT in "Done"
(you may also invent a better everyday question; it must not repeat a done one). Keep it family-friendly,
nothing medical-advice-like, nothing political.

## 2. Research (mandatory)
Use WebSearch/WebFetch. Find at least 3 reliable sources (universities, peer-reviewed papers, NASA/NOAA/USGS/NIH,
established science outlets). Every fact in the script must be backed by a source. Prefer one or two
"wow" facts (a number, an experiment, an animal). If something is disputed, say so or leave it out.

## 3. Write the episode: `episodes/<slug>.py`
Copy the structure of `episodes/tickle.py`:
- `TITLE`, `SLUG`, `CAPTION` (one punchy sentence + 5–6 hashtags, include #science #didyouknow #learnontiktok),
  `SOURCES` (list of URLs), `BEATS`.
- `BEATS` = list of `(visual_key, arms, text)`. arms: `down`, `point`, `shrug`, `up`.
  Pattern: 2 hook beats (talk to the viewer, create curiosity) → `('intro', 'point', "I'm Doctor Lumen, and today ...")`
  → title beat (the question) → 10–14 explanation beats, each one short sentence or two → a twist/"crazy part"
  → a short wrap-up → `('follow', 'up', "Follow for a new everyday mystery, every single day!")`.
- 230–300 words total. Write numbers as words the way they should be spoken ("a fifth of a second").
- Visuals: the keys `intro` and `follow` exist already. For the others, write 6–10 small illustration functions
  in the episode file and export them:

      import explainer as X
      def v_onion(lt, b):                 # lt = seconds since this beat started
          im, d = X.new_card()            # 940x680 card; draw with PIL ImageDraw
          X.label(d, (465, 90), 'ONION GAS', 84, X.INK, X.FA)
          ...
          return im
      VISUALS = {'onion': v_onion, ...}

  Helpers in explainer.py: new_card, label, arrow, brain, feather, meter, rat, waves, robot_arm, palm, stopwatch,
  colours INK/YEL/PINK/CYAN/GRN, fonts FA (Anton) / FI (Inter Black) / FB (Inter Bold). Use simple bold flat shapes,
  a big headline on each card, little animation via `lt`. Unknown keys fall back to a keyword card – avoid relying on that.

## 4. Preview and check
    python explainer.py <slug> preview      # -> out/<slug>/preview.png
Look at the preview with the Read tool. Fix anything clipped, overlapping, unreadable or ugly, then preview again.

## 5. Render
    python explainer.py <slug>              # -> out/<slug>/<slug>.mp4
Check with ffprobe: duration >= 65 s, 1080x1920, has audio. Look at 3 stills (ffmpeg -ss).

## 6. Publish the file
    python publish.py out/<slug>/<slug>.mp4 drlumen_<slug>.mp4
It prints the public URL (raw.githubusercontent.com/.../media/videos/...).

## 7. Schedule in Buffer (organization "My organization")
- organizationId `6b07ead9dd55bfceaae3d5bf`
- TikTok @editor_73902: channelId `6b07ebca8541f09ecbac83e4`
- YouTube "Hans peter": channelId `6b0812448541f09ecbadfd9e`
- Post time: the next **01:00 Europe/Berlin** (= 7 pm US East / 4 pm US West). Use get_account for currentTime
  and the right UTC offset (+01:00 in winter, +02:00 in summer). mode `customScheduled`, schedulingType `automatic`.
- TikTok: text = CAPTION, assets = [{video: {url}}], metadata.tiktok = {title: TITLE, isAiGenerated: true}
- YouTube: text = CAPTION (+ a line "Sources:" with the URLs), assets = [{video: {url}}],
  metadata.youtube = {type: "short", title: TITLE + " #shorts" (max 100 chars), categoryId: "27", isAiGenerated: true,
  madeForKids: false, privacy: "public"}
- Don't create a second post if one for this episode already exists (list_posts first). If a post is already
  scheduled at that 01:00 slot on a channel, use the following day's 01:00 instead (one video per day).

## 8. Save
Add the episode to the "Done" table in `topics.md` (remove it from the backlog), then
`git add -A && git commit -m "episode: <slug>" && git push origin main`.

## 9. Report
Send a short notification: topic, length, scheduled time, and anything that went wrong.
If any step fails and can't be fixed, still save what you have, and report the failure clearly. Never post a video
that is shorter than 60 s or that you haven't checked.
