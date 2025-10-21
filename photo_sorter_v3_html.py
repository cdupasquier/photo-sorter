import cv2
import shutil
import base64
import numpy as np
import pandas as pd
from pathlib import Path
from tqdm import tqdm
from insightface.app import FaceAnalysis

# ---------------- CONFIG ----------------
KNOWN_DIR = Path("A_references")
UNKNOWN_DIR = Path("B_photos")
RESULTS_DIR = Path("C_resultats")
LOGS_DIR = Path("logs")
NO_MATCH_DIR = LOGS_DIR / "no_match"
REPORT_CSV = LOGS_DIR / "tri_resultats.csv"
REPORT_HTML = LOGS_DIR / "rapport_resultats.html"

SIMILARITY_THRESHOLD = 0.35
MODEL_NAME = "buffalo_l"
USE_GPU = False
DET_SIZE = (640, 640)
# ----------------------------------------

def ensure_dirs():
    for d in [KNOWN_DIR, UNKNOWN_DIR, RESULTS_DIR, LOGS_DIR, NO_MATCH_DIR]:
        d.mkdir(exist_ok=True)

def cosine_similarity(v1, v2):
    return float(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)))

def load_embeddings(app):
    known_embeddings = []
    print("\n[INFO] Analyse des références...\n")

    for person_dir in KNOWN_DIR.iterdir():
        if not person_dir.is_dir():
            continue

        label = person_dir.name.lower().strip()

        for img_path in person_dir.glob("*.*"):
            if img_path.suffix.lower() not in [".jpg", ".jpeg", ".png", ".webp"]:
                continue

            img = cv2.imread(str(img_path))
            if img is None:
                print(f"[WARN] Impossible de lire {img_path.name}")
                continue

            faces = app.get(img)
            if not faces:
                print(f"[WARN] Aucun visage détecté dans {img_path.name}")
                continue

            for face in faces:
                known_embeddings.append((label, face.normed_embedding))

    print(f"[OK] {len(known_embeddings)} visages de référence chargés.\n")
    return known_embeddings

def encode_image_to_base64(path, max_width=200):
    try:
        img = cv2.imread(str(path))
        if img is None:
            return ""
        h, w = img.shape[:2]
        scale = max_width / w
        resized = cv2.resize(img, (int(w * scale), int(h * scale)))
        _, buffer = cv2.imencode(".jpg", resized)
        encoded = base64.b64encode(buffer).decode("utf-8")
        return f'<img src="data:image/jpeg;base64,{encoded}" width="{max_width}">'
    except Exception:
        return ""

def process_photos(app, known_embeddings):
    logs = []
    unknown_images = list(UNKNOWN_DIR.glob("*.*"))

    for img_path in tqdm(unknown_images, desc="Analyse des photos"):
        if img_path.suffix.lower() not in [".jpg", ".jpeg", ".png", ".webp"]:
            continue

        img = cv2.imread(str(img_path))
        if img is None:
            continue

        faces = app.get(img)
        if not faces:
            shutil.copy2(img_path, NO_MATCH_DIR / img_path.name)
            logs.append({
                "fichier": img_path.name,
                "image": encode_image_to_base64(img_path),
                "trouve": False,
                "personnes": "",
                "similarite_top1": "",
                "action": "aucun visage"
            })
            continue

        matched_labels = set()
        best_sim = 0.0
        best_label = ""

        for f in faces:
            for label, ref_emb in known_embeddings:
                sim = cosine_similarity(f.normed_embedding, ref_emb)
                if sim > best_sim:
                    best_sim = sim
                    best_label = label
                if sim > SIMILARITY_THRESHOLD:
                    matched_labels.add(label)

        if matched_labels:
            sorted_labels = sorted(matched_labels)
            folder_name = "_".join(sorted_labels)
            dest_dir = RESULTS_DIR / folder_name
            dest_dir.mkdir(parents=True, exist_ok=True)

            shutil.copy2(img_path, dest_dir / img_path.name)

            logs.append({
                "fichier": img_path.name,
                "image": encode_image_to_base64(img_path),
                "trouve": True,
                "personnes": ", ".join(sorted_labels),
                "similarite_top1": round(best_sim, 3),
                "action": f"copié vers {folder_name}"
            })
        else:
            shutil.copy2(img_path, NO_MATCH_DIR / img_path.name)
            logs.append({
                "fichier": img_path.name,
                "image": encode_image_to_base64(img_path),
                "trouve": False,
                "personnes": best_label,
                "similarite_top1": round(best_sim, 3),
                "action": "aucun match"
            })

    return pd.DataFrame(logs)

def generate_html_report(df: pd.DataFrame, output_path: Path):
    html = """
    <html><head><meta charset="utf-8">
    <title>Rapport de tri des photos</title>
    <style>
    body { font-family: Arial; background:#fafafa; color:#333; }
    table { border-collapse: collapse; width:95%; margin:auto; }
    th, td { border:1px solid #ccc; padding:8px; text-align:center; }
    th { background:#eee; }
    tr:nth-child(even){ background:#f9f9f9; }
    img { border-radius:8px; }
    .ok{ color:green; font-weight:bold; }
    .no{ color:red; font-weight:bold; }
    </style></head><body>
    <h1>Rapport de tri des photos</h1>
    <table><tr><th>Photo</th><th>Fichier</th><th>Reconnu</th><th>Personne(s)</th><th>Similarité</th><th>Action</th></tr>
    """
    for _, row in df.iterrows():
        found = '<span class="ok">Oui</span>' if row["trouve"] else '<span class="no">Non</span>'
        html += f"<tr><td>{row['image']}</td><td>{row['fichier']}</td><td>{found}</td><td>{row['personnes']}</td><td>{row['similarite_top1']}</td><td>{row['action']}</td></tr>"
    html += "</table></body></html>"
    output_path.write_text(html, encoding="utf-8")

def main():
    ensure_dirs()
    print("[INFO] Chargement du modèle InsightFace...")
    app = FaceAnalysis(name=MODEL_NAME)
    app.prepare(ctx_id=0 if USE_GPU else -1, det_size=DET_SIZE)

    known_embeddings = load_embeddings(app)
    if not known_embeddings:
        print("[ERREUR] Aucun visage de référence valide.")
        return

    df = process_photos(app, known_embeddings)
    df.to_csv(REPORT_CSV, index=False, encoding="utf-8")
    generate_html_report(df, REPORT_HTML)

    print("\n✅ Analyse terminée.")
    print(f"Rapport CSV : {REPORT_CSV.resolve()}")
    print(f"Rapport HTML : {REPORT_HTML.resolve()}")

if __name__ == "__main__":
    main()
