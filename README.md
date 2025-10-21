# 📸 Photo Sorter  

### Étape 4 — Génération des rapports
Deux fichiers sont créés :
- `tri_resultats.csv` → résumé technique du traitement  
- `rapport_resultats.html` → rapport visuel avec miniatures et scores de similarité  

---

## 📊 Rapports générés

### 🧾 Rapport CSV
Contient :
- Nom du fichier  
- Personnes reconnues  
- Score de similarité  
- Action effectuée  

### 🌐 Rapport HTML
Permet de visualiser :
- Les miniatures des images  
- Le statut de reconnaissance  
- Les scores de similarité  
- Les dossiers de destination  

---

## 💡 Conseils d’utilisation

- Utilisez **plusieurs photos de référence par personne** (angles, expressions, lumières).  
- Évitez les images floues ou sur/sous-exposées.  
- Gardez un **seuil de similarité entre 0.30 et 0.45**.  
- Si le programme est lent, **réduisez la taille d’entrée** (`DET_SIZE`) ou **activez le GPU**.  

---

## 🧱 Technologies utilisées

| Technologie | Rôle principal |
|--------------|----------------|
| **Python 3.10+** | Langage principal |
| **OpenCV** | Lecture et traitement d’images |
| **NumPy** | Calcul vectoriel |
| **Pandas** | Génération du rapport CSV |
| **TQDM** | Barre de progression |
| **InsightFace** | Détection & reconnaissance faciale |
| **ONNX Runtime** | Accélération sur CPU/GPU |

---

## ⚙️ Préparation de l’environnement

1. Installer **Python 3.10+**  
2. Créer un environnement virtuel :
   ```bash
   python -m venv venv
   source venv/bin/activate   # macOS/Linux
   venv\Scripts\activate      # Windows
   ```
3. Installer les dépendances 
   ```bash
    pip install -r requirements.txt
   ```
4. Placer les photos :
   ```bash
    A_references → visages de référence
    B_photos → photos à trier
   ```
5. Exécuter le script :
   ```bash
   python photo_sorter.py
   ```
## 📄 Résultats attendus

- 📁 **Photos triées** dans `C_resultats`  
- 🚫 **Images non reconnues** dans `logs/no_match`  
- 📊 **Rapports CSV et HTML** dans `logs`

## 🛠️ Dépannage

| Erreur | Solution |
|--------|-----------|
| `ModuleNotFoundError: tf_keras` | `pip install tf-keras` |
| `Microsoft Visual C++ 14.0 or greater is required` | Installer **Desktop development with C++** via **Visual Studio Build Tools** |
| `cannot import name 'distance' from 'deepface.commons'` | Ce projet n’utilise plus **DeepFace** — désinstallez-le |
| `CUDAExecutionProvider not available` | Installer `onnxruntime-gpu` et mettre `USE_GPU=True` |
| **Performances lentes** | Réduire `DET_SIZE` à `480×480` et/ou ajouter plus de références |

## 🧾 Licence

Projet libre sous **licence MIT**.  
Vous pouvez l’utiliser, le modifier et le distribuer librement, à des fins **personnelles ou professionnelles**.

## ✅ Fichier `requirements.txt`

## 📸 Développé avec passion

Pour simplifier le **tri photo** et l’**analyse d’images** grâce à l’**IA**.

