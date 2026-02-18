# Nebula Probe

> Nebula Probe est un petit scanner de ports TCP maison, écrit en Python dans un but **éducatif** — comprendre les sockets, le threading et la théorie derrière les outils comme Nmap.



## Objectif du projet

Ce projet est un exercice d'apprentissage autour de :

- **`socket`** — comment Python établit une connexion TCP et sonde un port
- **`concurrent.futures`** — paralléliser des tâches avec un ThreadPoolExecutor
- **`signal`** — intercepter les interruptions clavier proprement
- La théorie du scan de ports : différence entre port ouvert, fermé et filtré



## Fonctionnalités

- Validation du format hostname (regex) + résolution DNS avant le scan
- Scan des ports **1 à 8080** en TCP
- **200 threads en parallèle** pour un scan rapide
- Barre de progression en temps réel dans le terminal
- Interruption propre avec **Ctrl+C**
- Résumé des ports ouverts à la fin du scan



## Utilisation

```bash
python3 nebula.py
```

```
Set URL for Scanning (www.target.com): scanme.nmap.org

Scanning scanme.nmap.org (45.33.32.156)

[████████████████░░░░░░░░░░░░░░░░░░░░░░░░] 4040/8079 (50.0%)

FOUND : PORT 22 is OPEN
FOUND : PORT 80 is OPEN

Scan terminé !
```



## Prérequis

Aucune dépendance externe — uniquement la bibliothèque standard Python.

```bash
python3 --version  # 3.8+
```



## Ce que j'ai appris

| Concept | Ce que ça fait ici |
|---|---|
| `socket.connect_ex()` | Tente une connexion TCP, retourne 0 si le port est ouvert |
| `settimeout()` | Évite de bloquer indéfiniment sur un port filtré |
| `ThreadPoolExecutor` | Lance N scans en parallèle au lieu d'attendre port par port |
| `threading.Event` | Flag partagé entre threads pour un arrêt propre sur Ctrl+C |
| `signal.SIGINT` | Intercepte Ctrl+C avant que Python lève une exception |



## Avertissement

Ce scanner est un outil **d'apprentissage personnel**.  
Ne pas l'utiliser contre des systèmes sans autorisation explicite — c'est illégal.  
Pour des tests légaux, utiliser des cibles prévues à cet effet comme [scanme.nmap.org](http://scanme.nmap.org).

