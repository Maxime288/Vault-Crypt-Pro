#!/usr/bin/env python3
"""
🔑 Vault-Crypt Pro
Gestionnaire de mots de passe sécurisé avec chiffrement AES-256.
"""

import os
import json
import base64
import argparse
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet

# ──────────────────────────────────────────────────────────────
# Couleurs ANSI & Style
# ──────────────────────────────────────────────────────────────
class C:
    RESET   = "\033[0m"
    BOLD    = "\033[1m"
    RED     = "\033[38;5;196m"
    GREEN   = "\033[38;5;82m"
    YELLOW  = "\033[38;5;226m"
    BLUE    = "\033[38;5;45m"
    CYAN    = "\033[38;5;51m"
    GRAY    = "\033[38;5;244m"

BANNER = fr"""
{C.YELLOW}  __      __         _ _      {C.CYAN}  _____                      _  {C.RESET}
{C.YELLOW}  \ \    / /        | | |     {C.CYAN} / ____|                    | | {C.RESET}
{C.YELLOW}   \ \  / /_ _ _   _| | |_    {C.CYAN}| |     _ __ _   _ _ __  | |_ {C.RESET}
{C.YELLOW}    \ \/ / _` | | | | | __|   {C.CYAN}| |    | '__| | | | '_ \ | __|{C.RESET}
{C.YELLOW}     \  / (_| | |_| | | |_    {C.CYAN}| |____| |  | |_| | |_) || |_ {C.RESET}
{C.YELLOW}      \/ \__,_|\__,_|_|\__|   {C.CYAN} \_____|_|   \__, | .__/  \__|{C.RESET}
{C.GRAY}          Secure Password Manager v1.1      |___/|_|{C.RESET}
"""

def derive_key(master_password, salt):
    """Génère une clé robuste via PBKDF2."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    return base64.urlsafe_b64encode(kdf.derive(master_password.encode()))

def save_vault(data, password):
    """Chiffre et sauvegarde le vault sur le disque."""
    salt = os.urandom(16)
    key = derive_key(password, salt)
    f = Fernet(key)
    encrypted_data = f.encrypt(json.dumps(data).encode())
    with open("vault.db", "wb") as v_file:
        v_file.write(salt + encrypted_data)

def load_vault(password):
    """Charge et déchiffre le vault."""
    if not os.path.exists("vault.db"):
        return {}
    with open("vault.db", "rb") as v_file:
        content = v_file.read()
        salt = content[:16]
        encrypted_data = content[16:]
    try:
        key = derive_key(password, salt)
        f = Fernet(key)
        return json.loads(f.decrypt(encrypted_data).decode())
    except:
        return None

def main():
    print(BANNER)
    parser = argparse.ArgumentParser(description="Vault-Crypt Pro: Gestionnaire sécurisé")
    parser.add_argument("--add", help="Ajouter (format site:password)")
    parser.add_argument("--delete", help="Supprimer un site (nom du site)")
    parser.add_argument("--list", action="store_true", help="Lister les entrées")
    args = parser.parse_args()

    # Demander le mot de passe maître de manière sécurisée
    master_pwd = input(f"{C.BOLD}[?] Entrez votre Master Password : {C.RESET}")
    vault = load_vault(master_pwd)

    if vault is None:
        print(f"{C.RED}[!] Accès refusé : Mot de passe incorrect.{C.RESET}")
        return

    # LOGIQUE DE SUPPRESSION
    if args.delete:
        if args.delete in vault:
            del vault[args.delete]
            save_vault(vault, master_pwd)
            print(f"{C.GREEN}[+] L'entrée '{args.delete}' a été supprimée.{C.RESET}")
        else:
            print(f"{C.YELLOW}[!] Le site '{args.delete}' n'existe pas dans le vault.{C.RESET}")

    # LOGIQUE D'AJOUT
    elif args.add:
        try:
            site, pwd = args.add.split(":")
            vault[site] = pwd
            save_vault(vault, master_pwd)
            print(f"{C.GREEN}[+] Identifiant pour {site} enregistré !{C.RESET}")
        except ValueError:
            print(f"{C.RED}[!] Format invalide. Utilisez --add site:password{C.RESET}")
    
    # LOGIQUE DE LISTE
    elif args.list:
        if not vault:
            print(f"{C.GRAY}Le vault est vide.{C.RESET}")
        else:
            print(f"\n{C.CYAN}--- VOS SECRETS CHIFFRÉS ---{C.RESET}")
            for site, pwd in vault.items():
                print(f" {C.BOLD}{site:<15}{C.RESET} : {pwd}")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
