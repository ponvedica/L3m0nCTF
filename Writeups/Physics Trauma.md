# OrbitalParameter - OSINT Challenge Writeup

**Challenge Name:** Physics Trauma   
**Category:** OSINT 

---

## Solution

### Step 1: Find the Reddit Account

The challenge starts with finding the Reddit user `OrbitalParameter`:

```
https://www.reddit.com/user/OrbitalParameter/submitted/?sort=hot
```


**OSINT Tools for Account Discovery:**

1. **Sherlock** - Username enumeration across 300+ social networks
   ```bash
   pip install sherlock-project
   sherlock OrbitalParameter
   ```

2. **WhatsMyName** - Web-based username checker
   ```
   https://whatsmyname.app/
   ```

3. **Manual Methods:**
   - **Google Dorking**: `"OrbitalParameter" site:github.com` or `"OrbitalParameter" site:reddit.com`
   - **GitHub User Search**: `https://github.com/search?q=OrbitalParameter&type=users`
   - **Reddit User Search**: Direct URL pattern `https://www.reddit.com/user/USERNAME`

---

### Step 2: Extract Orbital Inclination

From the Reddit posts, you'll find the **orbital inclination** parameter:

```
INC = 97.6721
```

> **This is a RED HERRING!** The INC value is misleading and not needed for the final solution. It's intentionally placed to distract you. Focus on finding the coordinates instead.

---

### Step 3: Find the Math Result

Another post on Reddit mentions a mathematical calculation with the result:

```
X = 12.541
```

This number is referenced as leading to a Pastebin link.

---

### Step 4: Access the Pastebin

Look carefully at the Reddit posts. One post appears to be complaining about professors:

```
Why do professors assume we remember entire prerequisite courses?
Just opened a problem set that expects us to "recall basic Fourier methods."

Like dude… I barely recall breakfast and what I threw in bin! jzWAEjDv skjasdiajhsiha
```

**Hidden Clue:** The Pastebin code is cleverly hidden in plain sight! Look at the phrase **"what I threw in bin! jzWAEjDv"** - the code `jzWAEjDv` appears right after mentioning "bin" (pastebin!).

The full Pastebin URL is:

```
https://pastebin.com/jzWAEjDv
```

Visit this link to find additional clues about the satellite parameters.

**Key Discovery:** Look at the comments in the Pastebin. You'll find:

```
(see analysis write-up: Med. notes 3)
```

This comment points you to a Medium article!

---

### Step 5: Find the Medium Article

The Pastebin comment leads you to a Medium article by `@strugglingorbit`:

```
https://medium.com/@strugglingorbit/trying-to-summarize-the-thermal-drift-lab-notes-probably-wrong-494d1bb6462f
```

In this article, you'll find a temperature calculation:

```
TEMP = (200 / 4) + 1.74 = 51.74
```

> **This is also a RED HERRING!** The TEMP value is misleading and NOT required for solving the challenge.

**The Real Clue:** In the Medium article, look for this line:

```
packet flag: u4pruydqqvj
```

There's also a comment stating:
```
maybe its hashed or just another student who is trying to impersonate me!!
```

---

### Step 6: Decode the Geohash

The string `u4pruydqqvj` is actually a **geohash**! This leads to two discoveries:

1. **Geohash Location** - Decode `u4pruydqqvj` using a geohash decoder:
   - Try: https://www.movable-type.co.uk/scripts/geohash.html
   - Or use Python: `pip install geohash2`

2. **GitHub Username** - The comment about "another student impersonating" hints at finding another account
   - Search for similar usernames on GitHub
   - Look for accounts related to "strugglingorbit" or orbital parameters

---

### Step 7: Decode Geohash to Point A

The geohash `u4pruydqqvj` from the Medium article decodes to **Point A**:

```
lat_A = 57.64911063015461
lon_A = 10.407439693808556
```

You can verify this using:
- Online geohash decoder: https://www.movable-type.co.uk/scripts/geohash.html
- Python:
  ```python
  import geohash2
  lat, lon = geohash2.decode('u4pruydqqvj')
  print(f"Point A: lat={lat}, lon={lon}")
  ```

---

### Step 8: Find the GitHub Account

The "impersonating student" hint and the geohash string itself leads you to a GitHub account:

```
https://github.com/u4pruydqqvj
```

**Key Discovery:** The GitHub username is the same as the geohash! `u4pruydqqvj`

---

### Step 9: Extract Point B from GitHub README

In the GitHub repository's **README.md**, you'll find a What3Words (W3W) code:

```
///relive.expresses.ripping
```

**To get Point B coordinates:**
1. Go to https://what3words.com/
2. Enter: `relive.expresses.ripping`
3. Click "Navigate" → Select "Google Maps"
4. This reveals **Point B** coordinates:

```
lat_B = 48.6695100
lon_B = 68.6144810
```

---

### Step 10: Find the Midpoint Hint

In the same GitHub repository, check the file **"i don't know what to do.md"**.

Under the **TODO** section, you'll find:

```
confirm whether midpoint == (lat1+lat2)/2 and (lon1+lon2)/2 and refer it with W3W?????
compare with the older notes from the Medium write-up
```

This is the hint! You need to calculate the **midpoint** of Point A and Point B.

---

### Step 11: Calculate Midpoint

To find the final location, calculate the midpoint between Point A and Point B:

**Latitude Midpoint:**
```
lat_midpoint = (lat_A + lat_B) / 2
lat_midpoint = (57.64911063015461 + 48.6695100) / 2
lat_midpoint = 106.31862063015461 / 2
lat_midpoint = 53.159310315077305
```

**Longitude Midpoint:**
```
lon_midpoint = (lon_A + lon_B) / 2
lon_midpoint = (10.407439693808556 + 68.6144810) / 2
lon_midpoint = 79.02192069380856 / 2
lon_midpoint = 39.51096034690428
```

**Final Coordinates:**
```
53.159310315077305, 39.51096034690428
```

---

### Step 12: Convert to What3Words for the Flag

1. Go to https://what3words.com/
2. Enter the exact coordinates: `53.159310315077305, 39.51096034690428`
3. What3Words will display:

```
///backtalk.seeded.restyled
```

4. Convert to flag format:

**FLAG:** `L3m0nCTF{backtalk_seeded_restyled}`

