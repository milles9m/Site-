# Transport routier spécialisé inc.

Le site complet se trouve dans `dist/` :

- `index.html` : version française.
- `en.html` : version anglaise.
- `style.css` : présentation responsive.
- `app.js` : demandes par courriel et carrousel automatique de 5 secondes.
- `images/` : logos, photos et images retouchées utilisées par le site.

Aucune installation ni compilation n'est nécessaire. Pour prévisualiser le site :

```sh
python3 -m http.server 8000 --directory dist
```

Ouvrir ensuite http://localhost:8000/. Le formulaire prépare un courriel dans l'application du visiteur; aucun serveur de messagerie ni clé API n'est requis.

Le fichier `.openai/hosting.json` décrit l'hébergement Sites existant. L'import dans GitHub ne modifie pas le site actuellement publié.

Le fichier README.md initial du dépôt GitHub est conservé. Les fichiers de secrets et de configuration locale sont exclus par `.gitignore`.
