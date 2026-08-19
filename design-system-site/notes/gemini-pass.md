
===== SAMPLE 1/2  (gemini-3.6-flash, 109520+2483+2052 tok) =====
### 1. WHAT IS BEING BUILT
A design-system-first web application (landing page plus dedicated service sub-pages) and a multi-platform animated Ad Studio workspace for a regional roofing company ("Apex Roofing"). The workflow uses AI to generate vector logos, select brand typography and color palettes, assemble responsive UI components, and generate photorealistic ad assets.

---

### 2. STACK AND PREREQUISITES
* **Claude Design** (Anthropic web design & prototyping workspace)
* **Claude AI Chat** (Models: `Claude Sonnet 4.6` [Medium Effort], `Claude Opus 4.8` [High Effort])
* **Higgsfield** (AI image and vector generation tool)
  * `Recraft V4.1` (Vector mode for SVG logo creation)
  * `Seedream 4.5` (4K photorealistic image generation)

---

### 3. COMMANDS AND CONFIG, VERBATIM

#### Design System Setup
* **Company Name & Blurb:**
  `Apex Roofing. A midwestern roofing company serving southwest michigan and surrounding areas.`
* **Any Other Notes Input:**
  ```text
  Use google fonts: Instrument Sans + Plus Jakarta Sans. Both are geometric, confident sans-serifs that work well together because they share structural DNA but have just enough difference in character to give clear heading vs. body hierarchy. Sharp and professional — leans more tech/SaaS adjacent, which could actually differentiate a roofing company in a sea of rustic serif logos.

  Right now, the SVG logo that we've dropped in says Durable Roofing. I want it to say Apex Roofing in our fonts.

  Colors:
  Deep navy anchors authority, brick-red accent nods to roofing craft without being on-the-nose.
  Midnight Slate #182B3A
  Steel Blue #2E4A60
  Rust #B84C2B
  Warm Off-White #F2FE9
  White #FFFFFF

  I want you to create a brand guide and have all of the web components, motion graphic ideas, logo variations, color usage for backgrounds, where and when to use fonts. Don't want you to create an actual website or anything like that, I just want to see what components we can create assets with in the future.
  ```

#### Claude Chat Prompts
* **Font Pairing Request:**
  `Apex Roofing. A midwestern roofing company serving southwest michigan and surrounding areas. I want you to list out some Google fonts that would go well together for this company and this brand. Give me four variations of different heading and body fonts that would look good and unique for this brand. I don't want something that looks cliché, but I also don't want something too adventurous. Tell me the best four options for Google fonts.`
* **Color Palette Request:**
  `I'm going with option 4 for the fonts. Now I want you to present four color palettes for this company that would invoke trust and still keep it feeling like a local small town roofing company.`
* **Ad Script/Scene Generation Prompt:**
  `I want you to generate some image prompts that are going to be used to eventually generate videos. These are going to be for roofing ads, and I want some ads that are really going to show the transformation from a roof leak or a situation where the customer is upset about something or there's a pain point to a resolved issue at the very end, where it shows the good result. These are going to be for a roofing company ads, and they can have multiple scenes in them. Give me some prompts that are better than these ones here, because these are just pretty standard roofing ads.`

#### Website Generation Prompts & Questionnaire
* **Landing Page Prompt:**
  ```text
  I want you to create a basic landing page style website that has our free quote form at the top of the page on the right-hand side and a hero section with some information about our roofing company, like the fact that we're local and we're a trusted roofing company. I want you to add placeholders for all of the background images and all of the images for cards and things, and give me a prompt for each of those so that I can prompt some images, and give me also the aspect ratio that you need for those images, and then I will give those to you after for the image phase once we want to add in images.

  For now I'd just like to have that hero section with the free quote form built for high conversion and trust right up top, then below that I want to have a services section and then a location section and then a bottom hero section that actually shows the same free quote form, just with a bit of a different layout for people who scroll all the way to the bottom.

  We also want a nav and some headers in the landing page. I wanted to pull them through the landing page, like I want it to start at home, which would be the hero, and have anchor links in there. For services, we'll have a service page that each of those cards are linked to, so that if somebody clicks on the service page it brings them to a dedicated services page that shows info about that service. Services in the nav should be a drop-down pop-over that shows the different services underneath it with a toggle.
  ```
* **Interactive Questionnaire Selections:**
  * **Services:** `Roof replacement`, `Roof repair`, `New construction`
  * **Phone Number:** `use a placeholder for now`
  * **Trust Stats:** `A+ rating on Better Business Bureau`, `500+ 4.7 star average on Reviews`, `Local and Family Owned`
  * **Service Areas:** `Kalamazoo`, `Portage`, `Battle Creek`, `Three Rivers`, `Paw Paw`, `Mattawan`, `Plainwell`
  * **Form Fields:** `Full name`, `Phone`, `Email`, `Address / ZIP`, `Service needed (dropdown)`, `Message / Details`, `How soon (Timeline)`
  * **Service Pages:** `Yes - build full service pages now`
  * **Tweaks Enabled:** `Hero layout variations`, `Quote form style`, `Accent intensity`, `Headline copy options`
* **Image Insertion Prompt:**
  `Insert these images based upon the number and how it corresponds to the prompt. I have image, which would be prompt one, I have image two, which would be prompt two, and so on.`

#### Ad Studio Prompt
* **Workspace Generation Prompt:**
  `I'd like to create ads for all of the Facebook, Meta, and Instagram ad formats that are video ads and static ads. Some of them will be animation, and some of them will be static. It's going to be uploading some images and videos that you need, but for right now I just want you to get the motion graphics all figured out for this company. I want you to add some tweaks here so that we can adjust the sizing, We can swap out images and videos and things like that. I just want to have a seamless dashboard that makes beautiful ads. Tell me the prompts that you need me to run and the sizing of those images and videos that you need for the backgrounds. Also start working on the actual animated intros and outros with just SVG designs.`

---

### 4. THE BUILD ORDER
1. Navigate to Claude Design -> **Design systems** -> **Create design system**.
2. Input company name and service blurb.
3. Open Claude Chat in a separate window; ask for Google Font pairings and color palette ideas suitable for local roofing services.
4. Open Higgsfield, select `Recraft V4.1` in **Vector mode**, and generate logo assets. Download the vector SVG.
5. Drag the SVG logo into the asset upload field in Claude Design and paste font, color, and SVG text override specifications into the notes box.
6. Generate the design system (~5 minutes using `Claude Opus 4.8`).
7. Publish the design system and open a **New design** linked to it.
8. Prompt Claude Design to generate a landing page and service sub-pages with image placeholders, prompt lists, and required aspect ratios.
9. Answer Claude Design's interactive setup questionnaire regarding business details and UI tweak toggles.
10. Copy generated placeholder prompts into Higgsfield (`Seedream 4.5`, 16:9 / 3:2 ratios) to generate realistic image assets.
11. Drag and drop generated images back into Claude Design to auto-populate page placeholders.
12. Return to the main Claude Design dashboard, choose the **Animation** template, and prompt it to generate a multi-format Ad Studio.
13. Generate 9:16 vertical scene images in Higgsfield using problem-solution scripts from Claude Chat for ad background sequences.

---

### 5. GOTCHAS
* **File Size Limits:** Generating images in 4K resolution can produce files too large for upload into design tools. Right-click and choose "Save Image As" (WebP format) or render in lower resolutions to prevent upload errors.
* **Vector Text Mismatches:** AI vector generators often insert filler company names into logos. Because SVG files preserve text metadata, you can instruct Claude Design to programmatically swap the filler text for your actual company name.

---

### 6. WHAT THE VIDEO DOES NOT SHOW
* Integrating actual GitHub repositories or Figma design files directly (mentioned verbally as setup options, but skipped).
* Converting static multi-scene ad frames into fully rendered MP4 video files via AI video generators.
* Production web hosting or domain deployment settings.

===== SAMPLE 2/2  (gemini-3.6-flash, 109520+2728+2169 tok) =====
### 1. WHAT IS BEING BUILT
A design-system-first web and marketing asset pipeline created via Claude Design and Higgsfield AI. The workflow builds a comprehensive design system for a fictional roofing company ("Apex Roofing"), including SVG logos, Google font pairings, and color palettes. It then generates a multi-page landing site with interactive design tweaks, AI photo placeholders, and a multi-platform animated Ad Studio for social media video ad templates.

---

### 2. STACK AND PREREQUISITES
* **Anthropic Claude Design** (Design System & Web App Generation UI)
* **Anthropic Claude Chat / Claude Code**
  * *Models used:* Claude Opus 4.8 / 4.8 High Effort, Claude Sonnet 4.6 Medium Effort (Claude Fable 5 noted as unavailable)
* **Higgsfield AI** (Higgsfield.ai) [Paid/Credits]
  * *Models used:* Recraft V4.1 (Vector mode for SVG), Seedream 4.5 (4K photo generation)
* **Integrations Mentioned in UI:** GitHub Repos, Figma (.fig), React codebase uploads

---

### 3. COMMANDS AND CONFIG, VERBATIM

#### Design System Setup
* **Company Blurb:**
  `Apex Roofing. A midwestern roofing company serving southwest michigan and surrounding areas.`

* **Font Query Prompt (Claude Chat - Sonnet 4.6 Medium):**
  `Apex Roofing. A midwestern roofing company serving southwest michigan and surrounding areas. I want you to list out some Google fonts that would go well together for this company and this brand. Give me four variations of different heading and body fonts that would look good and unique for this brand. I don't want something that looks cliché, but I also don't want something too adventurous. Tell me the best four options for Google fonts.`

* **Design System Notes Form Input:**
  ```text
  Use google fonts: Instrument Sans + Plus Jakarta Sans. Both are geometric, confident sans-serifs that work well together because they share structural DNA but have just enough difference in character to give clear heading vs. body hierarchy. Sharp and professional — leans more tech/SaaS adjacent, which could actually differentiate a roofing company in a sea of rustic serif logos.

  Right now, the SVG logo that we've dropped in says Durable Roofing. I want it to say Apex Roofing in our fonts.

  Colors:
  Deep navy anchors authority, brick-red accent nods to roofing craft without being on-the-nose.
  Midnight Slate #182B3A
  Steel Blue #2E4A60
  Rust #B84C2B
  Warm Off-White #FEFE9
  White #FFFFFF

  I want you to create a brand guide and have all of the web components, motion graphic ideas, logo variations, color usage for background, and where and when to use fonts. I don't want you to create an actual website or anything like that, I just want to see what components we can create assets with in the future.
  ```

#### Landing Page Generation Prompt
```text
I want you to create a basic landing page style website that has our free quote form at the top of the page on the right-hand side and a hero section with some information about our roofing company, like the fact that we're local and we're a trusted roofing company. I want you to add placeholders for all the background images and all the images for cards and things, and give me a prompt for each of those so that I can prompt some images, and give me also the aspect ratio that you need for those images and then I will give those to you after for the image phase once we want to add in images. For now I'd just like to have that hero section with the free quote form built for high conversion and trust right up top. Then below that I want to have a services section and then a location section and then a bottom hero section that actually shows the same free quote form just with a bit of a different layout for people who scroll all the way to the bottom. We also want a nav and some headers in the landing page...
```

#### Questionnaire Choices Selected in UI
* **Services:** Roof replacement, Roof repair, Storm damage response, Roof inspection, Commercial roofing, New construction.
* **Phone:** `use a placeholder for now`
* **Trust Stats:** `A+ rating on Better Business Bureau`, `500+ 4.7 star average on Reviews`, `Local and Family Owned`
* **Service Areas:** Kalamazoo, Portage, Battle Creek, Three Rivers, Paw Paw, Mattawan, Plainwell.
* **Form Fields:** Full name, Phone, Email, Address / ZIP, Service needed (dropdown), Message / Details, How soon (Timeline).
* **Service Pages:** Build full service pages now.
* **Tweaks:** Hero layout variations, Contour style form (card vs. inline), Accent intensity, Headline copy options.

#### Ad Studio Prompt
```text
I'd like to create ads for all of the Facebook, Meta, and Instagram ad formats that are video ads and static ads. Some of them will be animation, and some of them will be static. Its going to be uploading some images and videos that you need, but for right now I just want you to get the motion graphics all figured out for this company. I want you to add some tweaks here so that we can adjust the sizing. We can swap out images and videos and things like that. I just want to have a seamless dashboard that makes beautiful ads. Tell me the prompts that you need me to run and the sizing of those images and videos that you need for the backgrounds. Also start working on the actual animated intros and outros with just SVG designs.
```

#### Image Generation Prompts (Higgsfield)
* **Logo SVG:** `Durable Roofing` / `Vertex Roofing` (Recraft V4.1, Vector Mode).
* **Hero Background (16:9):** `Wide cinematic photo of a roofing crew installing dark charcoal architectural asphalt shingles on a two-story SW Michigan home; warm late afternoon light, slightly desaturated; clean roof ridge line, shallow depth of field; framing leaves darker open space on the left third for text.`
* **Roof Repair Detail (3:2):** `Close-up of a roofer's gloved hands replacing damaged flashing around a chimney; warm late afternoon light; crisp texture, editorial documentary photography, shallow depth of field.`
* **Storm Response (4:3):** `Storm-response scene: a roofer on a ladder securing tarps over damaged shingles in a dark Michigan thunderstorm; overcast diffused light, serious and reassuring mood.`
* **Ad Scene 1 (9:16):** `Interior wide shot — a stressed homeowner in a dim kitchen, standing over a plastic bucket catching drips from the ceiling. Rain hammers the window. Water-stained drywall above. Face tired, jaw tight. Practical lamp light, cool blue cast from the storm outside. Photorealistic, desaturated.`
* **Ad Scene 2 (9:16):** `Exterior. A two-man crew in rain gear stabilizing a tarp over the damaged section, mid-storm. Flashlights cutting through dark overcast. Urgency without panic. Documentary handheld feel.`
* **Ad Scene 3 (9:16):** `Bright morning after. The same homeowner standing in the driveway looking up at crisp new architectural shingles. Arms crossed but relaxed. Slight smile. Warm golden-hour light. Clean symmetrical front facade.`

---

### 4. THE BUILD ORDER
1. Navigate to **Design Systems** tab in Claude Design and select **Create design system**.
2. Input company name and brief narrative blurb.
3. Generate vector SVG logo in Higgsfield AI (Recraft V4.1 model with Vector mode ON). Download SVG and drag into **Add fonts, logos and assets**.
4. Open parallel Claude Chat window to query Google font pairings and color hex codes.
5. Paste selected font pairing (`Instrument Sans` + `Plus Jakarta Sans`) and color hex codes into **Any other notes**. Add instructions to update the SVG logo text to "Apex Roofing".
6. Click **Continue to generation** to compile design system tokens, components, and motion graphic ideas.
7. Publish the finished design system.
8. Create a new design project linked to the published design system.
9. Enter website landing page prompt. Complete Claude's interactive multi-choice questionnaire.
10. Preview generated site; test "Tweaks" panel (hero layouts, form styles, brand intensity).
11. Copy generated image placeholder prompts and aspect ratios.
12. Generate 4K photos in Higgsfield AI using Seedream 4.5. Upload named image files (`image1.webp`, `image2.webp`, etc.) to Claude Design.
13. Submit prompt instructing Claude to replace placeholder slots with uploaded images.
14. Return to Claude Design home, select Apex Roofing design system + **Animation** template to generate an **Ad Studio**.
15. Generate 3-scene storyboards (Pain -> Action -> Resolution) in Claude Chat.
16. Generate 9:16 vertical images in Higgsfield AI for each ad scene slot.

---

### 5. GOTCHAS
* **File Size Upload Limits:** High-resolution 4K images exported from Higgsfield can exceed Claude Design’s file upload limit (>25MB). Save as compressed `.webp` or disable 4K output.
* **SVG Logo Text Mismatch:** Generated vector SVGs often contain placeholder brand text. Explicitly instruct Claude Design in prompt notes to update the text elements inside the uploaded SVG file.
* **Placeholder Alignment:** Placeholder prompts carry index numbers and aspect ratios; uploaded assets must be explicitly mapped to corresponding prompt IDs.

---

### 6. WHAT THE VIDEO DOES NOT SHOW
* Hosting or live website deployment steps (mentioned verbally at 18:00 but skipped).
* Conversion of static ad scene images into animated video clips within Higgsfield.
* Initial account creation, API setup, or credit purchasing for Higgsfield AI and Anthropic services.

===== HOW TO READ THESE =====
Keep: tool names, command strings, error messages, and any claim that appears in BOTH samples.
Flag: anything that appears in only one sample. That is where the model is guessing.
Never trust: timestamps, counts, durations, version numbers it did not clearly read on screen.
