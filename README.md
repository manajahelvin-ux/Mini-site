# Mini-site — assurance professionnelle

Version locale **non officielle**, reconstruite à partir du contenu public de la [page Allianz Professionnels et Entreprises](https://www.allianz.fr/assurances-professionnels-entreprises.html). Le téléchargement direct du HTML et des ressources d'origine n'était pas possible depuis l'environnement de développement : il ne s'agit donc pas d'une copie exacte du site Allianz. Les photographies sont des illustrations générées pour cette version.

## Démarrer en local

Aucune installation de dépendances n'est nécessaire. Depuis ce dossier :

```bash
python3 -m http.server 8000 --bind 127.0.0.1
```

Sous Windows, remplacer `python3` par `python` si nécessaire. Ouvrir ensuite **http://localhost:8000** dans un navigateur. Le chemin `/assurances-professionnels-entreprises.html` redirige également vers l'accueil local. Arrêter le serveur avec `Ctrl+C`.

Le HTML, les styles, le JavaScript, les polices et les images utilisés pour l'affichage sont stockés localement. Les menus et les questions/réponses fonctionnent sans serveur applicatif. En revanche, les liens vers les devis, l'espace client, les coordonnées et les autres pages mènent au **site officiel Allianz** et nécessitent une connexion Internet. Aucun formulaire de devis, authentification, service Allianz ou suivi publicitaire n'est reproduit localement. Le texte, les avis et les offres affichés correspondent au contenu consulté et ne sont pas mis à jour automatiquement : vérifier les informations et conditions sur le site officiel.

## Récupérer la page originale (facultatif)

Depuis un ordinateur disposant d'un accès à `www.allianz.fr` et de **GNU wget**, cette commande tente de télécharger la page originale et ses ressources accessibles dans le dossier `original/` :

```bash
bash scripts/telecharger-original.sh
```

Elle ne modifie pas la version locale ci-dessus et refuse d'écraser un dossier `original/` existant. Le fichier obtenu peut ensuite être servi par le même serveur sous `/original/assurances-professionnels-entreprises.html`. Le serveur d'origine peut refuser les téléchargements automatisés. Certaines ressources tierces, protections, fonctions JavaScript et services en ligne peuvent ne pas fonctionner hors connexion ; le résultat n'est pas garanti comme copie complète du site. Utilisez les contenus et marques conformément aux droits et conditions applicables.

## Ressources

- Texte et liens : page publique Allianz mentionnée ci-dessus.
- Photographies : images illustratives générées pour ce projet, et non photographies du site d'origine.
- Logo Allianz : [ressource SVG publique](https://github.com/tokyrakoto-ai/Allianz/blob/main/Allianz.svg) ; les marques restent la propriété de leurs titulaires.
- Police Open Sans : [Fontsource](https://github.com/fontsource/fontsource), sous licence SIL Open Font License, reproduite dans `assets/fonts/OPEN-SANS-LICENSE.txt`.
