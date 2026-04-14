# 🔑 Vault-Crypt Pro

> **Gestionnaire de mots de passe sécurisé avec chiffrement AES-256**
> Un coffre-fort numérique en ligne de commande utilisant des standards de cryptographie de niveau militaire pour protéger vos identifiants.
> Python 3 · Cryptography · PBKDF2 · AES-GCM/Fernet.

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)
![Security](https://img.shields.io/badge/Security-AES--256--CBC-green)
![Category](https://img.shields.io/badge/Category-Defense%20%26%20Crypto-yellow)

---

## 📋 Présentation

**Vault-Crypt Pro** est une solution de stockage sécurisée qui repose sur le principe du "Zero-Knowledge" : votre mot de passe maître n'est jamais stocké, ni sur le disque, ni dans le code. Il sert uniquement à dériver une clé de chiffrement temporaire pour accéder à vos secrets.

### Fonctionnalités principales :

* **Chiffrement de bout en bout** : Utilisation de l'algorithme AES-256 (via Fernet) pour garantir la confidentialité et l'intégrité des données.
* **Dérivation de clé robuste** : Utilisation de **PBKDF2HMAC** avec SHA-256 et 100 000 itérations pour contrer les attaques par force brute.
* **Gestion du Sel (Salt)** : Un sel unique de 16 octets est généré à chaque sauvegarde pour empêcher les attaques par tables arc-en-ciel (rainbow tables).
* **Opérations CRUD sécurisées** : Ajout, consultation et suppression d'entrées avec réécriture immédiate du coffre-fort chiffré.

---

## ⚙️ Installation & Prérequis

### Prérequis

Le projet nécessite la bibliothèque `cryptography`, référence en Python pour les opérations sécurisées.

```bash
pip install cryptography
```

### Installation

```bash
git clone https://github.com/Maxime288/Vault-Crypt-Pro.git
cd Vault-Crypt-Pro
chmod +x vault_crypt.py
```

---

## 🚀 Utilisation

L'outil fonctionne entièrement via des arguments en ligne de commande. Le mot de passe maître vous sera demandé de manière interactive pour chaque opération.

**Ajouter un identifiant**
```bash
python3 vault_crypt.py --add "github:MonSuperMdp123!"
```

**Lister les secrets**
```bash
python3 vault_crypt.py --list
```

**Supprimer une entrée**
```bash
python3 vault_crypt.py --delete "github"
```

---

## 🔬 Architecture de Sécurité

1. **Saisie du Master Password** : Récupéré en mémoire vive uniquement.
2. **Génération de Clé** : Le mot de passe est combiné à un SEL aléatoire et passé dans l'algorithme PBKDF2.
3. **Chiffrement/Déchiffrement** : La clé résultante est utilisée pour lire ou écrire le fichier `vault.db`.
4. **Persistance** : Le fichier `vault.db` contient le SEL (en clair) et les DONNÉES (chiffrées). Sans le mot de passe maître, les données sont mathématiquement impossibles à déchiffrer.

---

## ⚠️ Avertissement

Ce projet est réalisé à des fins éducatives. Bien que les algorithmes utilisés soient reconnus et éprouvés, il est déconseillé de l'utiliser en production pour stocker des données sensibles critiques sans audit de sécurité préalable.
