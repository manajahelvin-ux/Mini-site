# Mini-site — assurance professionnelle

Reconstruction locale **non officielle et indépendante**, inspirée de la [page publique Allianz Professionnels et Entreprises](https://www.allianz.fr/assurances-professionnels-entreprises.html). Elle ne constitue pas une copie exacte : le HTML complet et les images originales n'ont pas pu être récupérés dans l'environnement de développement. Les bandeaux et les photos des cartes sont des illustrations générées ; quatre petits visuels proviennent des captures de référence fournies pour le projet. Les polices locales Quicksand et Open Sans remplacent la police propriétaire du site source.

Les marques appartiennent à leurs titulaires. Les textes, offres, avis et coordonnées reproduits correspondent à la page consultée le **27 octobre 2026** : ils ne sont pas actualisés et n'ont aucune valeur commerciale ou contractuelle. Pour une démarche réelle, utilisez les canaux officiels de votre assureur.

## Démarrer

Aucune installation ni connexion Internet n'est nécessaire pour afficher et parcourir le site. Dans ce dossier :

```bash
python3 -m http.server 8000 --bind 127.0.0.1
```

Ouvrir **http://localhost:8000**. Sous Windows, remplacer `python3` par `python` si nécessaire. Arrêter le serveur avec `Ctrl+C`. Le chemin `/assurances-professionnels-entreprises.html` redirige également vers l'accueil local. Dans un environnement de prévisualisation distant, utiliser `--bind 0.0.0.0` si celui-ci exige une interface accessible à l'extérieur.

## Ce qui fonctionne en local

- Page principale responsive : menus, barre d'accès rapides collante, carrousels, questions/réponses et conditions indicatives.
- [Catalogue de recherche](catalogue.html) et pages thématiques sur les métiers, secteurs, responsabilités, biens, santé et services. Les liens de la page principale ouvrent des pages locales, sans appeler les sites Allianz.
- [Simulation de besoins](devis.html) en quatre étapes, avec retour en arrière et téléchargement ou impression d'un récapitulatif. **Aucun tarif, devis officiel, contrat ou demande réelle n'est produit.** Les variantes `?product=ACT5`, `ACT2`, `PS1` et `ACT4` présélectionnent seulement un thème local.
- [Espace client de démonstration](espace-client.html) : exemples de contrats, de documents et de démarches. Aucun compte, identifiant, mot de passe ou attestation réelle.
- [Recherche d'agences](agences.html) : trois résultats **fictifs**, sans adresse ni coordonnées réelles. Aucun annuaire officiel n'est consulté.
- [Page de contact](contact.html) : informations reproduites, sans formulaire d'envoi. Les liens téléphoniques indiquent des numéros publics relevés sur la page source ; les appeler contacte un service réel et nécessite un téléphone. Leur disponibilité n'est pas vérifiée par cette démo.

Les rubriques qui dépassent le périmètre (banque, recrutement, particuliers, etc.) l'indiquent explicitement. Il n'y a aucun service d'authentification, partenaire, paiement, réclamation ou souscription relié à Allianz.

Les pages et les questions/réponses restent lisibles sans JavaScript ; les menus mobiles disposent d'un repli. La recherche interactive, le simulateur, les onglets de démonstration et les boutons des carrousels nécessitent JavaScript. Les listes demeurent consultables sans celui-ci.

## Confidentialité

Le mini-site ne contient ni suivi publicitaire ni cookie de mesure d'audience et ne transmet pas les saisies à Allianz. Le simulateur ne demande ni nom, ni SIRET, ni coordonnées, ni données sensibles : ses choix restent dans la page jusqu'à sa fermeture. Le téléchargement du récapitulatif est effectué par le navigateur. Selon votre configuration, l'historique du navigateur et les journaux du serveur local peuvent conserver les adresses consultées.

## Maintenir et vérifier

Les pages secondaires sont des fichiers HTML statiques. Leur contenu et leur génération se trouvent dans `scripts/generate_local_pages.py`, qui réutilise l'en-tête et le pied de page de `index.html`. Après modification de ces sources, régénérer les pages avec :

```bash
python3 scripts/generate_local_pages.py
```

Les modifications directes apportées aux pages générées seront écrasées à la prochaine génération. Pour vérifier les chemins, ancres, ressources CSS, champs et fichiers générés :

```bash
python3 -m unittest discover -s tests -v
```

Ces tests sont exécutables avec la bibliothèque standard de Python et ne nécessitent pas de serveur.

## Récupérer la page originale (facultatif)

Depuis un ordinateur ayant accès à `www.allianz.fr` et à **GNU wget**, la commande suivante tente de télécharger la page originale et ses ressources accessibles dans `original/`, sans modifier la reconstruction :

```bash
bash scripts/telecharger-original.sh
```

Le script refuse d'écraser un dossier existant. Protections du site, ressources tierces et services dynamiques peuvent empêcher une copie complète ou son fonctionnement hors connexion. Utilisez les contenus et marques conformément aux droits et conditions applicables.

## Ressources

- Structure et contenu : page publique Allianz indiquée ci-dessus, ainsi que ses pages publiques de contact, de présentation de l'espace client et du parcours de devis.
- Bandeaux et photos des cartes : illustrations générées pour ce projet, et non photographies originales d'Allianz.
- Trois photos rondes (« Expertise », « Solidité », « Innovation ») et logo eKomi : extraits des captures de référence fournies par l'utilisateur. Leurs droits appartiennent à leurs titulaires ; toute réutilisation doit respecter ces droits.
- Logo Allianz : [ressource SVG publique](https://github.com/tokyrakoto-ai/Allianz/blob/main/Allianz.svg). Les marques Allianz et eKomi appartiennent à leurs titulaires.
- Polices Quicksand et Open Sans : [Fontsource](https://github.com/fontsource/fontsource), licences SIL Open Font License disponibles dans `assets/fonts/QUICKSAND-LICENSE.txt` et `assets/fonts/OPEN-SANS-LICENSE.txt`.
