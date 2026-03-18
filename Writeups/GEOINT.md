# GEOINT Challenges - Writeup

**Category:** GEOINT (Geospatial Intelligence)  
**Type:** Image-based Geolocation

---

## Challenge 1: Beautiful Date

### Challenge Description

```
I took this photo while exploring a developed precinct in a city during sports season. 
But I forgot to save the location as I was on date with my wife. 
Can you help me remember our moments?

Flag format: L3m0nCTF{The_Place_Name}
```

### Solution

**Step 1: Visual Analysis**

Examine the image carefully for identifiable landmarks or text:
- Modern glass building architecture
- **Key Finding:** "ILZA" signage visible on the building (Ilza Cafe)

**Step 2: Research Ilza Cafe Locations**

Search for "Ilza cafe" on Google:

```
Google Search: "ilza cafe"
```

**Findings:**
- Ilza is a Japanese cafe chain
- Multiple locations, need to narrow down
- One prominent result: **Ilza Japanese Cafe Docklands**

**Step 3: Cross-Reference with Challenge Clues**

The challenge mentions:
- "developed precinct" → Docklands is a developed precinct
- "sports season" → **Marvel Stadium** is located in Docklands

**Step 4: Verify Location**

From Google Maps/search results:
- Address: Shop 103/673 La Trobe St, Docklands VIC 3008, Australia
- Description: "Down-home Japanese dishes served in unpretentious surrounds outside **Marvel Stadium**"

**Flag:** `L3m0nCTF{Marvel_stadium}`

---

## Challenge 2: Historic Divine

### Challenge Description

```
A traveler documented a visit to a historic religious site during a journey.
The image was taken at the entrance of the site, but the exact location was never recorded. 
Identify where this photo was taken.

Flag format: L3m0nCTF{the_place_name}
```

### Solution

Search the given image with google Images, you will get the result as **Choub Poul Temple** since the flag format state lowercase the flag has to be in lowercase.

**Flag:** `L3m0nCTF{choub_poul_temple}`

---

## Challenge 3: Skateboard Stadium

### Challenge Description

```
I went out to skateboard, when I suddenly heard loud cheers echoing from a nearby stadium.
Curious, I took a photo from outside the complex but forgot to note the location.
Identify the stadium where this photo was taken.

Flag format: L3m0nCTF{Word1_Word2}
```

### Solution

**Step 1: Visual Analysis**

Scan the image for unique text or landmarks:

- Concrete skateboarding area with low wall covered in graffiti
- **Key Finding:** Black graffiti tag reading **"PSAROFAI"** on the right side


**Step 2: Information Gathering**

Search the unique graffiti text:

```
Google Search: "Psarofai"
```

**Result:** Psarofai is identified as a neighborhood (district) in **Patras, Greece**.

**Step 3: Locate the Stadium**

Search for stadiums in Patras:
- Google Maps: "Stadiums in Patras"
- Research Psarofai neighborhood

**Finding:** **Pampeloponnisiako Stadium** (also known as National Stadium of Patras) is located in this area.

**Step 4: Confirmation**

1. Open Google Maps satellite view of Pampeloponnisiako Stadium
2. Compare layout: Main stadium flanked by auxiliary basketball and tennis courts
3. The photo is taken from the perimeter of auxiliary courts looking toward the main stand


**Flag:** `L3m0nCTF{Pampeloponnisiako_Stadium}`

---