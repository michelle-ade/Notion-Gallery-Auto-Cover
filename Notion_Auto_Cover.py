from notion_client import Client
import musicbrainzngs
import os
from dotenv import load_dotenv

# --- Config ---
load_dotenv()
NOTION_TOKEN = os.getenv("NOTION_TOKEN")
DATABASE_ID = os.getenv("DATABASE_ID")

notion = Client(auth=NOTION_TOKEN)

# --- Init clients ---
notion = Client(auth=NOTION_TOKEN)
musicbrainzngs.set_useragent("Notion_Auto_Cover", "1.0", "email")


def get_album_cover_url(song_title, album_name=None):
    try:
        query = {
            "recording": song_title,
            "limit": 10,
        }
        if album_name:
            query["release"] = album_name

        results = musicbrainzngs.search_recordings(**query)

        for recording in results.get("recording-list", []):
            for release in recording.get("release-list", []):
                release_title = release.get("title", "").lower()
                if (
                    release.get("status", "").lower() == "official"
                    and release.get("release-group", {}).get("primary-type") == "Album"
                    and (not album_name or album_name.lower() in release_title)
                ):
                    return f"https://coverartarchive.org/release/{release['id']}/front"
    except Exception as e:
        print(f"⚠️ Error fetching cover for '{song_title}': {e}")
    return None


def fetch_database_entries():
    pages = []
    start_cursor = None
    while True:
        response = notion.databases.query(
            **{
                "database_id": DATABASE_ID,
                "start_cursor": start_cursor,
            }
        )
        pages.extend(response["results"])
        if not response.get("has_more"):
            break
        start_cursor = response["next_cursor"]
    return pages


def update_cover_art_for_page(page):
    props = page["properties"]

    # Skip if cover already marked as done
    if props.get("Cover", {}).get("checkbox", False):
        return

    # Get title
    title_obj = props.get("Song Title", {}).get("title", [])
    if not title_obj:
        return
    song_title = title_obj[0]["plain_text"]

    # Get album name (if provided)
    album_obj = props.get("Album Name", {}).get("rich_text", [])
    album_name = album_obj[0]["plain_text"] if album_obj else None

    # Try getting cover URL
    cover_url = get_album_cover_url(song_title, album_name)
    if not cover_url:
        print(f"❌ No cover found for: {song_title}")
        return

    # Update cover image
    notion.pages.update(
        page["id"],
        cover={
            "type": "external",
            "external": {
                "url": cover_url
            }
        }
    )

    
    print(f"✅ Updated cover for: {song_title}")


def main():
    print("📦 Fetching songs from Notion...")
    pages = fetch_database_entries()
    for page in pages:
        update_cover_art_for_page(page)
    print("🎉 Done!")


if __name__ == "__main__":
    main()

