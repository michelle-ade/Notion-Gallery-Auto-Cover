## 🎵 Notion Gallery Auto-Cover

This script automatically adds album cover art to a Notion database of songs by querying the MusicBrainz API.  
It was created to streamline the process of documenting music collections, 
and particularly to make my Piano Repertoire more visually appealing 😌

![Notion Gallery](gallery_example.png)

### 🔧 Features
- Fetches cover art for songs using their **song title + album name**.
- Skips entries that are already marked as done with a `Cover` checkbox.
- Uses **MusicBrainz API** to find releases and retrieve their cover art.
- Uses **Notion API** to update page covers directly.
- Designed for personal music databases 

## 🧩 Requirements

- A Notion database with the following properties:

| Property Name  | Type     | Description                           |
|----------------|----------|---------------------------------------|
| `song title`   | Text     | The name of the song                  |
| `album name`   | Text     | The album the song belongs to         |
| `cover`        | Checkbox | Marks whether the cover is already set|

⚠️ Property names must match **exactly** (including spaces and lowercase letters).



## 🔧 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/notion-cover-fetcher.git
cd notion-cover-fetcher
```

### 2. Install Dependencies

pip install -r requirements.txt

### 3. Set Up Your Environment

Create a .env file in the root directory with the following contents:

NOTION_TOKEN=YOUR_TOKEN
DATABASE_ID=YOUR_ID

You can find your integration token from https://www.notion.so/my-integrations

### 4. Run the Script

```bash
python notion_auto_cover.py
```


## 🐞 Known Issues

  ### Inaccurate album matching
  MusicBrainz results may return the wrong album art, especially for:
  - Songs with common or ambiguous titles
  - Albums with multiple volumes
  - Tracks released in tribute albums or karaoke versions
  
  ✅ A workaround is to ensure correct, specific album names (e.g. “The Shimmering Voyage Vol. 3”) are entered in your Notion database.

  ### Non-English Songs & Albums
  MusicBrainz search results tend to favour English releases, in my experience. 
  Song or album names in other languages may lead to incorrect cover art from unrelated artists,
  or blank placeholder images.

  ### No fallback or manual review step (yet)
  The script doesn’t currently verify accuracy or offer a choice of results, and just uses the first one returned.
  

## 🚧 Future Improvements

  ### Better Result Filtering
  Match on artist name, album date, or exact album MBID to reduce incorrect results.

  ### Multi-language Support
  Include fuzzy searching or alternate title handling for songs/albums in other languages.

  ### Manual Review Mode
  Option to preview the fetched covers before applying.

  ### Image Padding
  Automatically pad images to improve their appearance in gallery view. Padded covers will need to be re-uploaded and hosted somewhere else.

  ### Rate Limiting & Retry Logic
  Prevent hitting API limits during large updates and retry failed queries gracefully.
  
  
## 🧠 Challenges & Learnings
- MusicBrainz often returns unofficial covers or mismatches, especially for translated or fan covered tracks.
 So to improve accuracy and to only retrieve official release covers, I added a separate `Album Name` field to both my database and the script.
- Through this project I also learned how to integrate multiple APIs.


