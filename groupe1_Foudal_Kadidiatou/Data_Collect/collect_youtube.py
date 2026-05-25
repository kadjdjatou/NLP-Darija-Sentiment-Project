from googleapiclient.discovery import build
import json
import time

# =====================================
# 🔑 CONFIGURATION
# =====================================

API_KEY = "AIzaSyCgqbd9atfjvp0Xs1OjeGok6ka6RA1nUL4"  # <-- ta clé API
OUTPUT_FILE = "comments_2025_2026_new.json"
MAX_TOTAL_COMMENTS = 60000
TARGET_PER_CHANNEL = 20000  # objectif par chaîne

CHANNELS = [
    "Bladna 24",
    "Rimal TV",
    "SAFAA",
    "Swinga",
    "PILOTA",
    "BOTATO"
]

DATE_START = "2025-01-01T00:00:00Z"
DATE_END = "2026-02-28T23:59:59Z"

# =====================================
# 🚀 INITIALISATION
# =====================================

youtube = build("youtube", "v3", developerKey=API_KEY)

# =====================================
# 🔎 Récupérer ID chaîne
# =====================================

def get_channel_id(channel_name):
    request = youtube.search().list(
        q=channel_name,
        part="snippet",
        type="channel",
        maxResults=1
    )
    response = request.execute()
    if response["items"]:
        return response["items"][0]["id"]["channelId"]
    return None

# =====================================
# 📹 Récupérer vidéos d’une chaîne
# =====================================

def get_videos(channel_id):
    videos = []
    next_page_token = None
    while True:
        request = youtube.search().list(
            channelId=channel_id,  # ✅ il faut l’ID ici
            part="id",
            type="video",
            order="date",
            publishedAfter=DATE_START,
            publishedBefore=DATE_END,
            maxResults=50,
            pageToken=next_page_token
        )
        response = request.execute()
        for item in response["items"]:
            videos.append(item["id"]["videoId"])
        next_page_token = response.get("nextPageToken")
        if not next_page_token:
            break
    return videos

# =====================================
# 💬 Récupérer commentaires d’une vidéo
# =====================================

def get_comments(video_id, seen_ids, max_needed):
    comments = []
    next_page_token = None
    while len(comments) < max_needed:
        try:
            request = youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                maxResults=100,
                pageToken=next_page_token,
                textFormat="plainText"
            )
            response = request.execute()
            for item in response["items"]:
                snippet = item["snippet"]["topLevelComment"]["snippet"]
                comment_id = item["id"]
                if comment_id in seen_ids:
                    continue
                comments.append({
                    "comment_id": comment_id,
                    "text": snippet["textDisplay"],
                    "likes": snippet["likeCount"],
                    "date": snippet["publishedAt"]
                })
                seen_ids.add(comment_id)
                if len(comments) >= max_needed:
                    break
            next_page_token = response.get("nextPageToken")
            if not next_page_token:
                break
            time.sleep(0.3)
        except Exception as e:
            print("⚠️ Erreur commentaires :", e)
            break
    return comments

# =====================================
# 🎯 SCRAPING PRINCIPAL
# =====================================

def scrape():
    all_comments = []
    seen_ids = set()
    remaining_total = MAX_TOTAL_COMMENTS

    for channel in CHANNELS:
        if remaining_total <= 0:
            break
        print("\n" + "="*60)
        print(f"🔍 Chaîne : {channel}")
        print("="*60)

        channel_id = get_channel_id(channel)
        if not channel_id:
            print("❌ Chaîne non trouvée")
            continue

        videos = get_videos(channel_id)  # ✅ passer l’ID ici
        print(f"📹 {len(videos)} vidéos trouvées")

        channel_comments = []
        max_for_channel = min(TARGET_PER_CHANNEL, remaining_total)

        for video in videos:
            if len(channel_comments) >= max_for_channel:
                break
            remaining_for_channel = max_for_channel - len(channel_comments)
            comments = get_comments(video, seen_ids, remaining_for_channel)
            channel_comments.extend(comments)
            print(f"📝 {len(channel_comments)} commentaires collectés pour {channel}")
            print(f"📊 Total global : {len(all_comments) + len(channel_comments)} / {MAX_TOTAL_COMMENTS}")

        all_comments.extend(channel_comments)
        remaining_total = MAX_TOTAL_COMMENTS - len(all_comments)
        print(f"✅ Fin chaîne {channel} : {len(channel_comments)} commentaires")
        print(f"🔹 Reste à collecter : {remaining_total} commentaires\n")

    if len(all_comments) > MAX_TOTAL_COMMENTS:
        all_comments = all_comments[:MAX_TOTAL_COMMENTS]

    # Supprimer doublons
    unique = {c["comment_id"]: c for c in all_comments}
    final_comments = list(unique.values())

    # Sauvegarder JSON
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(final_comments, f, ensure_ascii=False, indent=2)

    print("\n" + "="*60)
    print("✅ SCRAPING TERMINÉ")
    print(f"📊 Total final : {len(final_comments)} commentaires")
    print(f"💾 Fichier sauvegardé : {OUTPUT_FILE}")
    print("="*60)

# =====================================
# ▶️ EXECUTION
# =====================================

if __name__ == "__main__":
    scrape()