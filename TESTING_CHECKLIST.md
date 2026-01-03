# UsageBar Phase 1 Testing Checklist

## Prerequisites

Before testing, ensure you have:
- [ ] A graphical desktop session (X11 or Wayland)
- [ ] UsageBar CLI built and installed
- [ ] GTK3 dependencies installed

## Installation (if needed)

### 1. Build the CLI
```bash
cd /mnt/data/projects/UsageBar
swift build -c release --product CodexBarCLI
sudo cp .build/release/CodexBarCLI /usr/local/bin/usagebar
```

### 2. Install dependencies (Ubuntu)
```bash
sudo apt install python3-gi gir1.2-appindicator3-0.1
```

## Launch Instructions

### Option A: Using the launcher script (Recommended)
```bash
cd /mnt/data/projects/UsageBar
./usagebar-tray-launcher.sh
```

### Option B: Direct Python execution
```bash
cd /mnt/data/projects/UsageBar
python3 usagebar-tray.py
```

### Option C: Background with logging
```bash
cd /mnt/data/projects/UsageBar
./usagebar-tray-launcher.sh > usagebar.log 2>&1 &
```

Then monitor logs:
```bash
tail -f usagebar.log
```

---

## Visual Upgrade Tests

### ✅ Test 1: Tray Icon

**What to check:**
- [ ] Custom purple gradient brain icon appears in system tray
- [ ] Icon is NOT the generic "utilities-system-monitor" icon
- [ ] Icon looks crisp (not blurry)

**Expected:** Modern SVG icon with gradient and usage gauge

**If fails:** Check `assets/icons/usagebar-icon.svg` exists and is valid SVG

---

### ✅ Test 2: Provider Icons

**What to check:**
- [ ] Click tray icon to open menu
- [ ] Each provider shows a custom colored icon (not emoji)
- [ ] Icons are approximately 20x20 pixels
- [ ] Claude: Orange circle
- [ ] Codex: Green hexagon
- [ ] Gemini: Blue/green star
- [ ] Cursor: Black cursor
- [ ] Z.ai: Purple lightning
- [ ] Antigravity: Purple rocket
- [ ] Factory: Orange factory

**Expected:** Professional SVG icons next to each provider name

**If fails:** Check console for "Warning: Custom icon not found"

---

### ✅ Test 3: Progress Bars

**What to check:**
- [ ] Progress bars are native GTK widgets (NOT ASCII text)
- [ ] Bars show smooth gradients (not blocks)
- [ ] Percentage text appears on the bar
- [ ] Bar width is approximately 180 pixels
- [ ] Bar height is thin (~12px)

**Expected:**
```
Session
[████████▓▓▓▓▓▓▓▓▓▓] 75%  ← Gradient fills from left
```

**If fails:** Check `assets/style.css` is being loaded

---

### ✅ Test 4: Status Colors

**What to check:**
- [ ] **Healthy (50%+)**: Green gradient bar, green badge background
- [ ] **Warning (20-50%)**: Yellow/orange gradient bar, yellow badge
- [ ] **Critical (<20%)**: Red gradient bar, red badge, pulsing animation

**Expected:** Automatic color coding based on percentage

**If fails:** Check CSS classes `.progress-healthy`, `.progress-warning`, `.progress-critical`

---

### ✅ Test 5: Status Badges

**What to check:**
- [ ] Provider names have percentage badges on the right
- [ ] Badges have colored backgrounds (not just text)
- [ ] Badge text is bold and centered
- [ ] Badge corners are rounded (8px radius)

**Expected:** `[Provider Name]        [75%]` ← badge with background color

**If fails:** Check `.status-badge` CSS class

---

### ✅ Test 6: Typography

**What to check:**
- [ ] Provider names are bold
- [ ] Fonts look modern (not monospace)
- [ ] Text is properly aligned (not overlapping)
- [ ] Email addresses are italic if shown

**Expected:** Clean, professional typography with proper spacing

**If fails:** Check `.provider-name` and `.provider-email` CSS

---

### ✅ Test 7: Layout & Spacing

**What to check:**
- [ ] Menu items have breathing room (margins)
- [ ] Session/Weekly/Model sections are separated
- [ ] Icons, names, and badges are evenly spaced
- [ ] Progress bars have proper padding
- [ ] No text is cut off or overlapping

**Expected:** Professional 8px grid alignment

**If fails:** Check margin/padding in CSS

---

### ✅ Test 8: Menu Structure

**What to check:**
- [ ] Clicking a provider shows expandable submenu
- [ ] Session usage appears first with progress bar
- [ ] Weekly usage appears below (if available)
- [ ] Model-specific usage appears (if available)
- [ ] Dashboard link at bottom of submenu
- [ ] "Refresh Now" and "Settings" at menu bottom

**Expected:** Hierarchical menu structure

**If fails:** Check `build_full_menu()` logic

---

### ✅ Test 9: Hover Effects

**What to check:**
- [ ] Menu items highlight on hover
- [ ] Progress bars don't flicker
- [ ] Icons don't shift position
- [ ] No GTK warnings in console

**Expected:** Smooth hover transitions

**If fails:** Check GTK CSS hover states

---

### ✅ Test 10: Tray Label Updates

**What to check:**
- [ ] Tray shows percentage when any provider is < 50%
- [ ] Tray shows "✅" when all providers are healthy
- [ ] Tray shows emoji + percentage when warning/critical
- [ ] Label updates after refresh

**Expected:** Dynamic tray icon label

**If fails:** Check label update logic in `build_full_menu()`

---

## Dark Mode Test (Optional)

**Steps:**
1. Switch system to dark theme
2. Relaunch UsageBar
3. Check that colors remain readable
4. Verify badges have proper contrast

**Expected:** Automatic dark theme adaptation

---

## Performance Test

**Check:**
- [ ] Memory usage stays < 50MB (run `ps aux | grep usagebar`)
- [ ] Menu opens instantly (no lag)
- [ ] Refresh completes in < 5 seconds
- [ ] No CPU spikes when idle

---

## Console Output

**Expected startup messages:**
```
[UsageBar] Initializing system tray application...
[UsageBar] Custom CSS loaded from /path/to/assets/style.css
[UsageBar] Initialization complete.
```

**Warnings to ignore:**
- None (should be clean)

**Errors that indicate problems:**
- `Warning: Custom icon not found` → Icons missing
- `Failed to load CSS` → CSS file missing or invalid
- `GTK import failed` → Missing dependencies

---

## Screenshots

Please take screenshots of:
1. Tray icon in system panel
2. Full menu (all providers visible)
3. One provider submenu expanded
4. Critical status (if any provider < 20%)

---

## Troubleshooting

### "No module named 'gi'"
```bash
sudo apt install python3-gi gir1.2-appindicator3-0.1
```

### "Custom icon not found"
```bash
ls -la assets/icons/
# Should show 10 SVG files
```

### "Failed to load CSS"
```bash
cat assets/style.css | head -20
# Should show CSS content
```

### Menu doesn't appear
- Check system tray is enabled in your desktop environment
- Try running directly: `python3 usagebar-tray.py`
- Check console for error messages

### Icons don't render
- Verify SVG files are valid: `file assets/icons/*.svg`
- Check GdkPixbuf support: `python3 -c "from gi.repository import GdkPixbuf"`

---

## Success Criteria

✅ **All 10 tests pass**
✅ **No GTK warnings in console**
✅ **Visual quality rivals PromptBar**
✅ **No functionality regressions**
✅ **Memory usage < 50MB**

---

## After Testing

**If everything works:**
```bash
git add usagebar-tray.py assets/ test-ui.py PHASE1_UPGRADE_SUMMARY.md
git commit -m "feat: Phase 1 visual foundation - custom SVG icons and modern GTK UI"
```

**If issues found:**
1. Note which tests failed
2. Check console output
3. Review relevant CSS/Python code
4. Rollback if needed: `git checkout ae54401`

---

**Testing Date:** _________________

**Tester:** _________________

**Result:** □ Pass  □ Fail  □ Partial

**Notes:**
___________________________________________________________
___________________________________________________________
___________________________________________________________
