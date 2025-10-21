# 📸 Photo Sorter  

=======
### Tri automatique de photos par reconnaissance faciale  

---

## 🧠 Description

**Photo Sorter** est un outil développé en **Python** qui permet de trier automatiquement des photos selon les personnes qui y apparaissent.  
Il repose sur la bibliothèque **InsightFace** pour la détection et la reconnaissance faciale.

Le programme compare les visages d’un dossier de photos avec ceux d’un dossier de références, puis classe automatiquement les images dans des sous-dossiers selon les correspondances détectées.  
Deux rapports sont générés à la fin du processus : un **rapport CSV** et un **rapport HTML visuel**.

---

## ⚙️ Fonctionnalités

- 🔍 Détection et reconnaissance faciale sur de grands ensembles de photos  
- 🗂️ Classement automatique dans des sous-dossiers par personne  
- 👥 Création d’un dossier combiné lorsqu’une photo contient plusieurs personnes reconnues  
- 🚫 Sauvegarde des images non reconnues dans un répertoire dédié  
- 📊 Génération de rapports **CSV** et **HTML** complets et illustrés  
- 💻 Fonctionne sur **Windows, macOS et Linux**  
- ⚡ Compatible **CPU** et **GPU (ONNX Runtime)**  

---

## 🗂️ Structure du projet
projet_tri_photo
│
├── A_references → dossiers contenant les visages de référence (un par personne)
│ ├── person1
│ │ ├── ref1.jpg
│ │ └── ref2.jpg
│ └── person2
│ └── ref1.jpg
│
├── B_photos → photos à analyser
│ ├── image001.jpg
│ ├── image002.jpg
│ └── …
│
├── C_resultats → dossiers générés automatiquement après analyse
│ ├── person1
│ ├── person2
│ └── person1_person2
│
├── logs → journaux et rapports générés
│ ├── no_match → photos sans visage reconnu
│ ├── tri_resultats.csv
│ └── rapport_resultats.html
│
└── photo_sorter.py → script principal

## 🧩 Configuration du script

Les principaux paramètres sont définis dans `photo_sorter.py` :

| Paramètre | Description | Valeur conseillée |
|------------|-------------|-------------------|
| `SIMILARITY_THRESHOLD` | Niveau de tolérance de la reconnaissance faciale | 0.30 (strict) → 0.45 (tolérant) |
| `MODEL_NAME` | Nom du modèle InsightFace utilisé | `"buffalo_l"` |
| `USE_GPU` | Active l’utilisation de la carte graphique | `True` / `False` |
| `DET_SIZE` | Taille d’analyse des visages | `640x640` (par défaut) |

---

## 🚀 Fonctionnement global

### Étape 1 — Analyse des références
Les images du dossier `A_references` sont analysées pour extraire les visages et générer leurs empreintes numériques (*embeddings*).

### Étape 2 — Analyse des photos
Chaque photo de `B_photos` est scannée, et les visages détectés sont comparés à ceux de la base de référence.

### Étape 3 — Tri automatique
- ✅ **1 personne reconnue** → la photo est copiée dans `C_resultats/nom_personne`  
- 👥 **plusieurs personnes reconnues** → la photo est copiée dans `C_resultats/nom1_nom2`  
- ❌ **aucun visage reconnu** → la photo est déplacée dans `logs/no_match`  

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

