# Diagnostic et correction de GitHub 403

## Constat vérifié pendant la préparation

- Le compte authentifié est `milles9m` et il dispose de droits d'administration sur `milles9m/Site-`.
- La lecture de ce dépôt public fonctionne. Cela ne démontre pas la capacité d'écriture de l'application.
- La création de `refs/heads/export/site-complet-2026-10-31` échoue avec HTTP 403, `Resource not accessible by integration`, par le connecteur et par l'API GitHub en ligne de commande.
- GitHub annonce `X-Accepted-GitHub-Permissions: contents=write` pour la création de branche.
- L'API `GET /user/installations` et le connecteur ne voient aucune installation de l'application pour cette connexion.

Le blocage se situe donc dans l'accès effectif de l'application à l'écriture du dépôt. Une sélection de dépôt ou une permission de compte administrateur n'accorde pas à elle seule ce droit au jeton d'application. La protection de `main` n'a pas pu être lue avec cette connexion et ne doit pas être supprimée; l'échec observé concerne déjà la création d'une autre branche.

## Résolution vérifiée

L’installation **178426539** de ChatGPT Codex Connector est maintenant visible pour le compte milles9m. Après installation, la création de la branche export/site-complet-2026-10-31 par le connecteur et le push Git de son code ont réussi. Le README et main n’ont pas été remplacés. L’erreur 403 initiale provenait de l’absence d’installation autorisée pour la connexion.

Le problème peut réapparaître dans un second compte si sa connexion n’est pas autorisée : appliquer les étapes ci-dessous pour chaque identité.

## Intervention du propriétaire

L’application a été identifiée par l’API GitHub : **ChatGPT Codex Connector**, propriétaire **openai**, avec les droits Contents et Pull requests en écriture. Son identifiant client public correspond à celui de la connexion active. Page officielle : https://github.com/apps/chatgpt-codex-connector. Si aucune installation n’apparaît, cliquer Install sur cette page, choisir milles9m puis autoriser Site-.

1. Dans le compte Codex/ChatGPT concerné, ouvrir la configuration de la connexion GitHub et relancer la configuration de l'accès aux dépôts. Selon l'interface, cette action se trouve dans les connecteurs/applications ou dans la configuration de l'environnement Codex.
2. Terminer le parcours GitHub **d'installation de l'application** sur le compte `milles9m`; une simple autorisation de connexion ne remplace pas cette installation.
3. Vérifier https://github.com/settings/installations. Ouvrir l'application réellement utilisée par la connexion, choisir Configure, sélectionner le dépôt `Site-` et enregistrer.
4. Accepter une éventuelle demande d'actualisation des permissions. L'application doit disposer de **Contents: Read and write** et de **Pull requests: Read and write**. Metadata: Read est normal. Aucune permission Workflows n'est nécessaire pour cet import, qui n'ajoute pas de workflow.
5. Si l'application ne propose pas l'écriture, elle ne peut pas être transformée manuellement en application d'écriture depuis la page de sélection des dépôts. Utiliser la connexion de développement Codex prévue pour modifier le code, ou faire corriger l'application par son administrateur. Ne pas multiplier les essais avec un jeton de lecture.
6. Reconnecter ou actualiser la connexion dans chaque environnement pour obtenir un nouveau jeton, puis relancer les vérifications.

Pour deux comptes GitHub distincts, inviter le second avec Write et lui faire accepter l'invitation; configurer aussi sa propre connexion Codex. Ne pas partager de jeton entre comptes. Ne coller aucun mot de passe, clé ou jeton dans une conversation.

## Vérification après correction

La lecture seule et les champs `permissions.push` ne suffisent pas. Vérifier successivement : création d'une branche de travail, envoi du commit, présence réelle des fichiers dans l'arbre GitHub, création et lecture de la PR. Ne pas fusionner l'import sans revue du propriétaire.

Une fois les droits corrigés, l'export préparé se pousse sur `export/site-complet-2026-10-31`, puis une PR est créée vers `main`. Le README initial est conservé. Aucun push forcé n'est nécessaire.

## Reprendre l'import préparé

Depuis le clone qui contient la branche locale export/site-complet-2026-10-31, après correction des permissions :

```sh
bash scripts/finish-import.sh
```

Ce script vérifie le dépôt, refuse un arbre de travail modifié, préserve main, pousse sans force, compare les fichiers locaux avec les SHA de l'arbre GitHub, puis crée ou retrouve la PR. Il ne fusionne pas la PR.
