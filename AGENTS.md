# Collaboration Codex — Transport routier spécialisé inc.

## Référence commune

- Dépôt unique du code : `https://github.com/milles9m/Site-.git`.
- `origin` désigne ce dépôt GitHub. `main` contient la version intégrée après revue.
- Conserver les fichiers existants et les modifications des autres contributeurs. Ne pas réinitialiser le projet ni remplacer son historique.
- L'import initial est proposé sur `export/site-complet-2026-10-31`. Tant que sa pull request n'est pas fusionnée, les fichiers du site ne sont pas sur `main`.

## Deux comptes et deux environnements

Chaque compte utilise son propre clone et sa propre authentification GitHub. Ne jamais partager les jetons, cookies, clés privées ou fichiers d'authentification. Chaque identité GitHub doit avoir le rôle Write sur le dépôt et sa connexion d'application doit autoriser ce dépôt avec Contents et Pull requests en lecture/écriture.

Avant toute modification, lire ce fichier, `docs/COLLABORATION.md` et l'état Git local. Exécuter `git fetch origin`. Ne pas changer de branche si le travail local n'est pas sauvegardé.

Après fusion de l'import initial, utiliser une branche distincte par compte et par tâche :

```sh
bash scripts/start-work.sh compte-a sujet
# Autre environnement : compte-b, avec un autre sujet.
```

- Ne pas travailler directement sur `main` ni sur la branche de l'autre Codex.
- Synchroniser sa branche avec `origin/main` avant l'envoi. Préserver les deux contributions lors d'un conflit.
- Ne jamais utiliser `git push --force`, `reset --hard`, `clean -fd` ni supprimer des fichiers sans instruction explicite de l'utilisateur.
- Envoyer sa branche, puis créer une pull request vers `main`. Ne pas fusionner sa propre PR sans autorisation de l'utilisateur.
- Ne pas prétendre qu'un commit, une PR ou un déploiement existe sans vérifier le résultat distant.

## Structure et exigences du site

Site statique sans compilation : `dist/index.html` (FR), `dist/en.html` (EN), `dist/style.css`, `dist/app.js` et `dist/images/`.

Maintenir les deux langues cohérentes. Le carrousel principal affiche les photos toutes les 5 secondes, sans boutons de navigation/pause ni agrandissement. Les images des six secteurs restent distinctes des photos de transport. Conserver le logo approuvé, les coordonnées et les images originales; les copies retouchées du carrousel sont des fichiers séparés.

Avant tout commit, exécuter :

```sh
python3 scripts/check-site.py
node --check dist/app.js
```

Examiner `git diff` et `git diff --cached`. Ne jamais suivre `.env`, secrets, clés API, clés privées ou identifiants locaux. `.gitignore` ne retire pas un secret déjà suivi : arrêter la publication et demander sa révocation si un secret est trouvé. Ne pas afficher sa valeur.

## Hébergement

GitHub est la référence du code; Sites reste l'hébergeur du site public. Il n'y a pas de déploiement automatique GitHub configuré par cet import.

Préserver `.openai/hosting.json` et son `project_id`. Pour publier, partir du commit approuvé sur `origin/main`, utiliser les outils Sites autorisés et préserver l'audience existante. Ne pas déployer directement une branche de travail. Un second compte qui doit déployer doit aussi disposer des droits d'édition sur le Site existant; l'accès GitHub seul ne les accorde pas. Ne pas créer un deuxième Site pour contourner un refus d'accès.

En cas de 403, consulter `docs/GITHUB_ACCESS.md`. Ne pas contourner les restrictions, supprimer la protection de branche ou demander qu'un secret soit collé dans le chat.
