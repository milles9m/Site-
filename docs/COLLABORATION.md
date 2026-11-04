# Travailler à deux avec GitHub comme référence

## Première utilisation

L'import initial conserve le README existant et ajoute les fichiers du site dans une PR vers `main`. Cette PR doit être examinée puis fusionnée avant que les nouvelles tâches partent de `main`.

Pour chaque compte Codex :

1. Connecter sa propre identité GitHub et autoriser l'application sur `milles9m/Site-`.
2. Si les identités GitHub sont différentes, le propriétaire invite la seconde dans Settings → Collaborators avec le rôle Write; elle doit accepter l'invitation.
3. Cloner le même dépôt dans deux environnements distincts, sans copier les fichiers d'authentification.

```sh
git clone https://github.com/milles9m/Site-.git
cd Site-
git remote -v
```

Tant que l'import n'est pas fusionné, il est consultable sur sa branche une fois publiée :

```sh
git fetch origin
git switch --track origin/export/site-complet-2026-10-31
```

## Nouvelle tâche après fusion de l'import

Compte A :

```sh
bash scripts/start-work.sh compte-a ameliorer-texte
```

Compte B, dans son propre clone :

```sh
bash scripts/start-work.sh compte-b ajuster-photos
```

Le script vérifie le dépôt et l'absence de modifications locales, récupère `main`, puis crée une nouvelle branche à partir d'`origin/main`. Il refuse de repartir d'un `main` qui ne contient pas encore l'import du site.

## Vérifier et proposer une modification

```sh
python3 scripts/check-site.py
node --check dist/app.js
git diff
# Sélectionner les fichiers de la tâche, puis les enregistrer :
git add dist/index.html dist/en.html
git diff --cached
git commit -m "Décrire le changement"
bash scripts/publish-work.sh
```

Le script d'envoi refuse `main`, vérifie le site et impose que la branche contienne le dernier `origin/main`. Il pousse sans force et crée ou retrouve la PR. Si une autre PR a été fusionnée entre-temps :

```sh
git fetch origin
git merge origin/main
# Résoudre les conflits en préservant les deux contributions, puis revérifier.
bash scripts/publish-work.sh
```

Le dépôt n'a pas de CI ni de règle de protection configurée automatiquement par cet import. Le propriétaire peut ensuite ajouter une règle sur `main` exigeant une PR. Ne pas supposer cette protection active sans la vérifier.

## Mise en ligne

Une PR ouverte n'est ni une fusion dans `main` ni une publication du site. La procédure est : revue → fusion autorisée → récupération du commit `main` → déploiement du Site existant avec les outils autorisés → vérification du résultat.

Les fichiers `dist/` sont le code à servir. Aucun serveur applicatif, gestionnaire de paquets ou secret n'est nécessaire pour les prévisualiser :

```sh
python3 -m http.server 8000 --directory dist
```

Le formulaire ouvre le logiciel de courriel du visiteur. Il n'envoie pas de courriel depuis un serveur.
