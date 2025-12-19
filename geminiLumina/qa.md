# Gemini & Lumina Q&A

Please answer the following questions to help us refine the Pac-Girl AI.

```markdown
### Q1: Pellet (Dot) Detection Strategy
**Context**: Detecting hundreds of small dots with template matching is very slow (low FPS).
**Option A**: Assume every "Walkable" tile that isn't empty has a dot. We track them in memory and remove them when Pac-Girl visits.
**Option B**: Use color thresholding (e.g., "Salmon" color pixels) to find them every frame.
**Question**: Which approach do you prefer? (Option A is faster, Option B is more robust to game resets), 
- Answer:maybe hybrid approach? ( Walkable tiles that are #D78A74 are dots, but the problem that the pixels around the dots are not in same color, maybe this: #593930, so we need to consider the gradient from #000000 to #D78A74)

### Q2: Bonus Coins (Fruits)
**Context**: Bonus items (Cherries, Strawberry) appear in the center.
**Question**: Do you have a screenshot or color code for these specific items? Or should we just treat any "Unknown Color" in the center as a bonus to eat?
- Answer: those bonus coins colors are: #FFAA8F, but they are randomly appears. also the size are bigger than normal walkable tiles. again the pixel around the bonus coins are not in same color, maybe this: #CB836E, so we need to consider the gradient from #000000 to #FFAA8F

### Q3: Map Extraction "Calibration Mode"
**Context**: To get a perfect map, we can ignore moving objects.
**Proposal**: Can we have a "Mapping Mode" where the bot watches the game for 5 seconds *without moving*? We can average the frames to erase the ghosts and Pac-Girl, leaving a clean map of walls and dots.
**Question**: Is this acceptable?
- Answer: yes ofcourse. 

### Q4: Data Logging Frequency
**Context**: Saving every single frame (30 FPS) will fill up your hard drive very fast.
**Question**: Should we save:
1. Every 10th frame? yes
2. Only frames where a "Decision" changed? yes
3. Only when something "interesting" happens (like a ghost detection)? yes
```
