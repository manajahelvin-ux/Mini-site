#!/usr/bin/env python3
"""Construit les pages statiques locales à partir du contenu ci-dessous.

Aucune dépendance ni accès réseau. Le site généré fonctionne sans cette étape.
"""
from html import escape
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]


def entry(title, category, lead, heading, intro, points, follow_heading, follow, related=(), image=None, tags='', info=False):
    return dict(title=title, category=category, lead=lead, heading=heading, intro=intro,
                points=points, follow_heading=follow_heading, follow=follow,
                related=related, image=image, tags=tags, info=info)


PAGES = {
    'activite': entry('Assurer mon activité', 'Mon activité',
        'Repérez les risques qui peuvent concerner votre entreprise, ses responsabilités et ses biens.',
        'Les besoins de votre activité',
        'L’activité professionnelle peut être exposée à des dommages causés à des tiers, à un sinistre dans les locaux ou à une interruption d’exploitation.',
        ['Responsabilité civile professionnelle et responsabilité d’exploitation.', 'Locaux, matériel, marchandises et pertes d’exploitation selon le contrat.', 'Véhicules utilisés dans le cadre professionnel.'],
        'Comment avancer ?', 'Faites le point sur votre métier, vos locaux et votre organisation. Les garanties, franchises et exclusions dépendent du contrat choisi.',
        ('rc-pro', 'multirisque', 'locaux', 'vehicules'), 'assets/entreprise.jpg', 'entreprise activité exploitation'),
    'dirigeant': entry('Me protéger en tant que dirigeant', 'Ma protection',
        'Santé, prévoyance, retraite et responsabilités : les besoins du dirigeant méritent aussi d’être examinés.',
        'Des situations à anticiper',
        'La protection du dirigeant peut compléter celle de l’entreprise. Les besoins varient notamment selon le statut professionnel et la situation personnelle.',
        ['Dépenses de santé et complémentaire individuelle.', 'Arrêt de travail, invalidité ou décès.', 'Préparation de la retraite et responsabilité personnelle du dirigeant.'],
        'À retenir', 'Cette page présente des pistes générales. Elle ne réalise aucune analyse personnalisée et ne propose aucun contrat.',
        ('sante-individuelle', 'retraite', 'rc-pro'), 'assets/droit.jpg', 'professionnel indépendant dirigeant prévoyance'),
    'salaries': entry('Protéger mes salariés', 'Mes salariés',
        'Découvrez les grandes familles de protection collective pour les équipes.',
        'Santé et prévoyance collectives',
        'L’employeur peut avoir des obligations en matière de santé et de prévoyance ; elles dépendent notamment des textes applicables et de la situation des salariés.',
        ['Complémentaire santé collective.', 'Prévoyance en cas d’arrêt de travail, d’invalidité ou de décès.', 'Dispositifs de retraite ou d’épargne collectives selon l’entreprise.'],
        'Un point important', 'Les obligations et les garanties doivent être vérifiées pour chaque entreprise. Le présent site ne permet pas de souscrire une couverture.',
        ('sante-collective', 'prevoyance-collective'), 'assets/entreprise.jpg', 'employeur équipe collaborateurs'),
    'commercants': entry('Assurance des commerçants', 'Votre métier',
        'Prêt-à-porter, caviste, librairie, fromagerie, épicerie fine : chaque commerce a ses propres besoins.',
        'Protéger une activité commerciale',
        'Un commerce peut devoir faire face à un dommage dans ses locaux, à une perte de stock ou à une réclamation d’un client.',
        ['Locaux, mobilier, équipements et marchandises.', 'Responsabilité liée à l’accueil de clients et à l’activité.', 'Conséquences possibles d’une interruption après un sinistre garanti.'],
        'Quelles solutions explorer ?', 'Une assurance multirisque professionnelle peut rassembler plusieurs garanties. Leur étendue dépend du contrat et de l’activité.',
        ('multirisque', 'locaux', 'rc-pro'), 'assets/commercants.jpg', 'magasin boutique commerce caviste'),
    'droit-chiffre': entry('Professionnels du chiffre et du droit', 'Votre métier',
        'Avocats, notaires, huissiers, experts-comptables : identifiez les risques propres aux activités de conseil.',
        'Responsabilités et activité',
        'Une erreur, une omission ou un dommage causé à un client peut engager la responsabilité d’un professionnel. Certaines professions sont soumises à des obligations d’assurance.',
        ['Responsabilité civile professionnelle.', 'Locaux, matériel informatique et documents professionnels.', 'Protection juridique et continuité de l’activité selon les garanties.'],
        'Vérifiez vos obligations', 'Les obligations diffèrent selon la profession réglementée et les textes en vigueur. Consultez les règles applicables avant toute décision.',
        ('rc-pro', 'protection-juridique', 'locaux'), 'assets/droit.jpg', 'avocat notaire expert comptable juriste conseil'),
    'professions-sante': entry('Professionnels libéraux de la santé', 'Votre métier',
        'Médecins, pharmaciens, pédiatres et autres soignants : découvrez les sujets à examiner pour votre activité.',
        'Les besoins d’un professionnel de santé',
        'Une activité de soins peut nécessiter une couverture adaptée aux responsabilités professionnelles et à l’exercice en cabinet.',
        ['Responsabilité civile professionnelle selon les obligations de la profession.', 'Cabinet, équipements et matériel professionnel.', 'Protection du revenu et de la santé du professionnel.'],
        'À vérifier', 'L’assurance applicable et les obligations dépendent du métier, du statut et des actes pratiqués. Cette page est une présentation générale.',
        ('rc-pro', 'locaux', 'sante-individuelle'), 'assets/sante.jpg', 'médecin pharmacien infirmier santé cabinet'),
    'metiers': entry('Nos solutions par métier', 'Votre métier',
        'Artisans, commerçants, professionnels du conseil ou de la santé : explorez les besoins selon votre activité.',
        'Un métier, des risques spécifiques',
        'La nature des prestations, la présence de locaux, les outils et les relations avec les clients influencent les protections à envisager.',
        ['Commerce et accueil du public.', 'Conseil, chiffre et droit.', 'Santé, artisanat et activités indépendantes.'],
        'Commencez par votre activité', 'Parcourez les présentations locales puis utilisez le simulateur de besoins pour constituer un récapitulatif non contractuel.',
        ('commercants', 'droit-chiffre', 'professions-sante', 'auto-entrepreneur'), 'assets/artisans.jpg', 'artisan profession activité conseil métier'),
    'secteurs': entry('Assurance de l’entreprise', 'Votre secteur',
        'Vous dirigez une entreprise industrielle ou commerciale ? Examinez les besoins propres à votre secteur et à votre taille.',
        'De la PME à la grande entreprise',
        'Une entreprise peut avoir à protéger ses installations, ses biens, ses responsabilités, ses collaborateurs et la continuité de son activité.',
        ['Locaux, équipements, stocks et véhicules.', 'Responsabilité vis-à-vis des clients et des tiers.', 'Protection des collaborateurs et prévention des risques.'],
        'Explorer les profils', 'Start-ups, associations, acteurs du sport et réseaux organisés font face à des situations différentes.',
        ('activite', 'startups', 'associations', 'sport', 'franchises'), 'assets/entreprise.jpg', 'industrie entreprise commerciale secteur pme'),
    'multirisque': entry('Assurance multirisque professionnelle', 'Assurance de l’activité',
        'Une multirisque peut réunir des garanties destinées à protéger l’activité et les biens professionnels.',
        'Que peut couvrir une multirisque ?',
        'Selon les garanties du contrat, une multirisque professionnelle peut répondre à plusieurs événements susceptibles d’affecter l’entreprise.',
        ['Incendie, dégât des eaux, vol ou événements climatiques.', 'Locaux, matériel et stocks professionnels.', 'Responsabilité civile et pertes d’exploitation si ces garanties sont prévues.'],
        'Comparer les garanties', 'Les biens couverts, les limites, les franchises et les exclusions varient d’un contrat à l’autre. Cette page ne constitue pas une offre.',
        ('rc-pro', 'locaux', 'activite'), 'assets/entreprise.jpg', 'mri risques incendie eau vol boutique atelier'),
    'rc-pro': entry('Responsabilité civile professionnelle', 'Assurance de l’activité',
        'La responsabilité civile professionnelle concerne les dommages pouvant être causés à des tiers dans le cadre de l’activité.',
        'À quoi sert la RC Pro ?',
        'Une entreprise peut voir sa responsabilité engagée à la suite de dommages corporels, matériels ou immatériels causés à un client ou à un autre tiers.',
        ['Examinez les risques liés aux prestations et aux produits.', 'Vérifiez les obligations propres aux professions réglementées.', 'Étudiez les plafonds, exclusions et conditions du contrat.'],
        'Un tarif dépend de la situation', 'L’activité et la taille de l’entreprise font partie des éléments susceptibles d’influencer le prix. La simulation locale ne calcule aucun tarif.',
        ('multirisque', 'auto-entrepreneur', 'droit-chiffre'), 'assets/droit.jpg', 'responsabilité civile rc pro dommages tiers assurance'),
    'locaux': entry('Assurance des locaux et des biens', 'Assurance de l’activité',
        'Locaux, matériel et marchandises : identifiez les biens nécessaires à votre activité.',
        'Protéger les biens professionnels',
        'Un sinistre dans un local peut affecter les équipements, les stocks et le fonctionnement de l’entreprise.',
        ['Locaux occupés et aménagements.', 'Matériel, mobilier et marchandises.', 'Pertes d’exploitation lorsque la garantie est prévue.'],
        'À examiner dans le contrat', 'La valeur des biens, les événements couverts, les franchises et les exclusions doivent être étudiés pour votre situation.',
        ('biens', 'multirisque', 'prevention-climat'), 'assets/artisans.jpg', 'locaux bureau atelier commerce matériel stock'),
    'biens': entry('Assurance des biens professionnels', 'Assurance de l’activité',
        'Les biens de l’entreprise peuvent comprendre ses locaux, son matériel, son mobilier et ses stocks.',
        'Faire l’inventaire',
        'Identifier les biens indispensables permet de mieux comprendre les conséquences possibles d’un incendie, d’un dégât des eaux ou d’un vol.',
        ['Locaux et aménagements.', 'Équipements et matériel professionnel.', 'Marchandises et stock.'],
        'Prévention et garanties', 'Les mesures de prévention et les garanties dépendent des risques et du contrat. Les informations locales sont indicatives.',
        ('locaux', 'multirisque', 'prevention-climat'), 'assets/entreprise.jpg', 'biens matériel stock entreprise'),
    'sante-collective': entry('Complémentaire santé collective', 'Protection des salariés',
        'Une complémentaire santé collective participe à la couverture des frais de santé des salariés selon le contrat.',
        'Ce qu’il faut examiner',
        'La page source rappelle les obligations applicables aux employeurs privés en matière de complémentaire santé collective, sous réserve des règles et cas particuliers en vigueur.',
        ['Salariés concernés et cas éventuels de dispense.', 'Niveaux de remboursement et garanties.', 'Participation de l’employeur et obligations applicables.'],
        'Une présentation générale', 'Les règles et les garanties doivent être vérifiées pour votre entreprise. Aucun tarif ni adhésion n’est proposé ici.',
        ('salaries', 'prevoyance-collective', 'sante-individuelle'), 'assets/sante.jpg', 'mutuelle entreprise salariés employeur santé'),
    'prevoyance-collective': entry('Prévoyance collective', 'Protection des salariés',
        'La prévoyance collective peut contribuer à protéger les salariés et leurs proches face à certains aléas.',
        'Les événements concernés',
        'Selon les garanties souscrites, un contrat peut intervenir en cas d’arrêt de travail, d’invalidité ou de décès.',
        ['Maintien de revenus en cas d’arrêt de travail selon les dispositions applicables.', 'Garanties d’invalidité et de décès.', 'Obligations éventuelles liées au statut ou à la convention collective.'],
        'Avant de choisir', 'Examinez les obligations de l’entreprise et les conditions du contrat avec un professionnel compétent.',
        ('salaries', 'sante-collective'), 'assets/entreprise.jpg', 'arrêt travail invalidité décès employeur'),
    'sante-individuelle': entry('Complémentaire santé individuelle', 'Protection du dirigeant',
        'Une complémentaire santé individuelle peut compléter les remboursements du régime obligatoire selon les garanties choisies.',
        'Identifier ses besoins',
        'Les besoins de santé diffèrent selon les personnes et leur situation professionnelle.',
        ['Soins courants et consultations.', 'Hospitalisation et dépenses spécifiques.', 'Niveaux de remboursement et éventuelles exclusions.'],
        'Une information indicative', 'Cette démonstration ne recueille aucune donnée de santé et ne fournit ni conseil personnalisé ni devis.',
        ('dirigeant', 'sante-collective'), 'assets/sante.jpg', 'mutuelle santé indépendant dirigeant'),
    'retraite': entry('Préparer la retraite du dirigeant', 'Protection du dirigeant',
        'Anticiper sa retraite consiste notamment à examiner ses revenus futurs et les dispositifs disponibles.',
        'Les questions à se poser',
        'Les besoins varient selon le statut, la carrière et la situation de chaque dirigeant.',
        ['Faire le point sur les droits acquis.', 'Identifier les besoins de revenus à la retraite.', 'Comparer les solutions et leurs conditions avec un professionnel.'],
        'Limites de cette page', 'Aucun calcul de retraite, conseil financier personnalisé ou souscription n’est disponible dans la version locale.',
        ('dirigeant', 'sante-individuelle'), None, 'épargne retraite indépendant dirigeant'),
    'vehicules': entry('Assurance des véhicules professionnels', 'Assurance de l’activité',
        'Véhicule unique, flotte ou déplacement occasionnel : les besoins dépendent des usages professionnels.',
        'Les situations possibles',
        'Un véhicule doit être assuré au minimum en responsabilité civile. Des garanties complémentaires peuvent être envisagées selon les usages et le contrat.',
        ['Véhicule utilisé par un artisan ou un indépendant.', 'Plusieurs véhicules et flotte professionnelle.', 'Déplacement professionnel occasionnel avec un véhicule personnel.'],
        'Matériel transporté', 'Si vous transportez du matériel ou des marchandises, vérifiez les conditions de couverture du contenu du véhicule.',
        ('activite', 'multirisque'), 'assets/entreprise.jpg', 'auto voiture utilitaire flotte route véhicule'),
    'auto-entrepreneur': entry('Assurance de l’auto-entrepreneur', 'Votre métier',
        'Les micro-entrepreneurs peuvent avoir besoin de protéger leurs prestations, leurs biens et leurs responsabilités.',
        'Repérer ses risques',
        'Une activité indépendante peut causer des dommages à un tiers pendant une prestation ou à la suite d’une livraison.',
        ['Responsabilité civile professionnelle.', 'Matériel et locaux le cas échéant.', 'Véhicule professionnel et protection personnelle selon la situation.'],
        'Obligations et garanties', 'Certaines activités sont soumises à des obligations spécifiques. Vérifiez les textes applicables à votre profession et les conditions du contrat.',
        ('rc-pro', 'metiers', 'vehicules'), 'assets/artisans.jpg', 'micro entrepreneur auto entrepreneur indépendant'),
    'startups': entry('Assurance des start-ups', 'Votre secteur',
        'Marketing digital, robotique ou économie collaborative : les jeunes entreprises peuvent avoir des besoins variés.',
        'Développer son activité',
        'Avant de choisir une assurance, une start-up peut identifier ses prestations, ses clients, ses équipements et les risques liés à son organisation.',
        ['Responsabilités vis-à-vis des clients et partenaires.', 'Matériel et locaux professionnels.', 'Protection des équipes et continuité de l’activité.'],
        'Des besoins évolutifs', 'Les protections à examiner peuvent évoluer avec la taille, les contrats et l’activité de l’entreprise.',
        ('rc-pro', 'multirisque', 'salaries'), 'assets/entreprise.jpg', 'startup jeune entreprise numérique technologie'),
    'associations': entry('Assurance des associations', 'Votre secteur',
        'Associations, fédérations et organismes d’intérêt général peuvent être confrontés à des risques liés à leurs activités.',
        'Identifier les personnes et les activités',
        'Les besoins dépendent notamment des événements organisés, des locaux, des bénévoles et des personnes accueillies.',
        ['Responsabilité civile de l’association et de ses activités.', 'Locaux, matériel et événements selon les garanties.', 'Protection des personnes intervenant dans l’association.'],
        'Une couverture adaptée', 'Vérifiez les obligations de l’association et l’étendue des garanties envisagées pour chaque activité.',
        ('rc-pro', 'multirisque', 'sport'), None, 'association bénévoles fédération événement'),
    'sport': entry('Assurance des acteurs du sport', 'Votre secteur',
        'Sportifs, clubs, fédérations et organisateurs d’événements ont des besoins spécifiques.',
        'Les risques à examiner',
        'La pratique, les installations et l’organisation de manifestations peuvent exposer des personnes ou des biens à des dommages.',
        ['Responsabilités des structures et organisateurs.', 'Installations et équipements.', 'Protection des participants selon les conditions applicables.'],
        'Selon votre activité', 'La nature de la pratique et les obligations propres à la structure déterminent les points à vérifier.',
        ('associations', 'rc-pro', 'secteurs'), None, 'sport club sportif fédération événement'),
    'franchises': entry('Franchises et groupements', 'Votre secteur',
        'Franchises, réseaux organisés, concessions ou coopératives : chaque structure doit examiner ses propres risques.',
        'Des besoins en réseau',
        'Les membres d’un réseau peuvent partager une marque tout en conservant des activités et des responsabilités distinctes.',
        ['Locaux, équipements et stocks.', 'Responsabilités liées aux prestations et aux clients.', 'Organisation des garanties entre les différentes entités du réseau.'],
        'Faire le point', 'Les obligations et les protections dépendent de l’organisation du réseau et des contrats concernés.',
        ('commercants', 'secteurs', 'multirisque'), 'assets/commercants.jpg', 'franchise réseau groupement commerce concession coopérative'),
    'services': entry('Portail de services professionnels', 'Services',
        'La page source présente des services destinés à accompagner les professionnels au quotidien.',
        'Ce qui est disponible ici',
        'Cette reconstruction locale présente les thèmes et les liens du site d’origine, mais ne se connecte à aucun partenaire.',
        ['Consulter les informations sur les risques climatiques.', 'Découvrir les principes de la protection juridique.', 'Explorer les besoins de votre activité.'],
        'Pas de service partenaire réel', 'Aucun compte partenaire, rendez-vous ou prestation ne peut être demandé depuis cette démonstration.',
        ('prevention-climat', 'protection-juridique', 'activite'), None, 'portail partenaires service professionnel'),
    'protection-juridique': entry('Protection juridique professionnelle', 'Services',
        'La protection juridique peut accompagner un professionnel confronté à certains litiges, selon le contrat.',
        'À quoi penser en cas de litige ?',
        'Les situations couvertes et les modalités d’accompagnement dépendent des garanties prévues.',
        ['Nature des litiges couverts.', 'Information juridique et accompagnement éventuel.', 'Plafonds, exclusions et conditions de prise en charge.'],
        'Important', 'Cette page est descriptive ; elle ne fournit ni assistance juridique, ni garantie, ni conseil personnalisé.',
        ('rc-pro', 'services', 'droit-chiffre'), 'assets/droit.jpg', 'litige conflit juridique conseil'),
    'prevention-climat': entry('Fortes chaleurs et risques climatiques', 'Prévention',
        'Préparez votre activité aux effets possibles des fortes chaleurs et autres événements climatiques.',
        'Quelques points d’attention',
        'La prévention dépend des locaux, des équipements, de l’activité et des personnes concernées.',
        ['Surveiller les conditions de travail et l’état des équipements.', 'Adapter l’organisation en cas de fortes chaleurs.', 'Identifier les biens sensibles aux événements climatiques.'],
        'Vérifiez les consignes applicables', 'Consultez les recommandations et obligations actualisées adaptées à votre activité. Cette page n’est pas une expertise de prévention.',
        ('locaux', 'biens', 'services'), 'assets/entreprise.jpg', 'canicule chaleur climat prévention entreprise'),
    'assurance-credit': entry('Assurance-crédit', 'Votre secteur',
        'L’assurance-crédit peut aider une entreprise à gérer certains risques liés aux impayés de ses clients.',
        'Comprendre le principe',
        'La page source présente Allianz Trade et le sujet de l’assurance-crédit. Les solutions et garanties réelles ne sont pas reproduites.',
        ['Surveillance du risque client selon le service concerné.', 'Gestion des impayés et garanties éventuelles.', 'Conditions, limites et exclusions propres à chaque contrat.'],
        'Version locale', 'Aucune analyse financière, recherche d’entreprise ou souscription ne peut être réalisée ici.',
        ('secteurs', 'activite'), None, 'crédit impayé allianz trade clients'),
    'lexique': entry('Lexique de l’assurance professionnelle', 'Ressources',
        'Quelques termes utiles pour lire les pages de cette reconstruction locale.',
        'Définitions',
        'Ces définitions simplifiées ne remplacent pas les conditions d’un contrat.',
        ['Responsabilité civile : obligation de réparer certains dommages causés à autrui.', 'Franchise : part pouvant rester à la charge de l’assuré selon le contrat.', 'Garantie : engagement défini par un contrat, avec ses conditions et limites.', 'Sinistre : événement susceptible de déclencher une garantie, sous réserve des conditions du contrat.'],
        'Pour aller plus loin', 'Consultez les pages thématiques locales pour repérer les questions à poser avant de comparer des contrats.',
        ('rc-pro', 'multirisque', 'locaux'), None, 'vocabulaire franchise sinistre garantie définition'),
    'avis': entry('Avis clients reproduits', 'Informations',
        'La page source affichait une note et des extraits d’avis clients. Ces informations ne sont pas actualisées dans la démo.',
        'Données relevées sur la page source',
        'La page consultée affichait une note de 4,8/5 calculée sur 84 852 avis au cours des douze derniers mois, ainsi qu’un avis daté du 25 octobre 2026.',
        ['Ces données sont figées et peuvent devenir obsolètes.', 'Cette page ne se connecte pas à eKomi et ne permet pas de consulter tous les avis.', 'Aucun avis ne peut être soumis depuis la démonstration.'],
        'Contexte', 'Il s’agit d’un extrait du contenu public consulté, et non d’une mesure en temps réel ou d’une évaluation de cette reconstruction.',
        (), None, 'note satisfaction témoignage ekomi', True),
    'reclamation': entry('Réclamation', 'Informations',
        'Une réclamation réelle doit être adressée à l’assureur concerné par un canal officiel.',
        'Dans cette version locale',
        'Il n’existe aucun service de réception des réclamations ni de connexion à un contrat.',
        ['Ne saisissez pas de numéro de contrat ou de données sensibles ici.', 'Aucune demande n’est transmise à Allianz.', 'La page de contact reproduit des informations générales et des numéros publics.'],
        'Pour une démarche réelle', 'Utilisez les coordonnées officielles de votre assureur ou celles indiquées dans votre contrat.',
        (), None, 'réclamation plainte litige contact', True),
    'allianz': entry('Allianz en France', 'Informations',
        'Cette reconstruction couvre la page publique consacrée aux professionnels et aux entreprises.',
        'Périmètre de la démonstration',
        'La présentation institutionnelle complète n’a pas été reproduite. Cette application est indépendante et n’est pas affiliée à Allianz.',
        ['Les marques appartiennent à leurs propriétaires.', 'Le contenu est indicatif et ne constitue pas une offre.', 'Les services réels ne sont pas connectés.'],
        'Retour à la démo', 'Vous pouvez consulter le catalogue local ou revenir à la page d’accueil des professionnels.',
        (), None, 'allianz france institutionnel', True),
    'groupe': entry('Le groupe Allianz', 'Informations',
        'La présentation internationale du groupe ne fait pas partie de cette reconstruction locale.',
        'Périmètre', 'Cette page remplace le lien vers un site externe pour conserver une navigation locale.',
        ['Aucune information institutionnelle en temps réel.', 'Aucune connexion au site officiel.', 'Retour possible vers les contenus professionnels de la démo.'],
        'Version indépendante', 'Cette reconstruction est non officielle et n’est pas affiliée au groupe Allianz.', (), None, 'groupe international', True),
    'recrutement': entry('Recrutement', 'Informations',
        'Le portail de recrutement ne fait pas partie de cette démonstration locale.',
        'Aucune candidature', 'Aucune offre d’emploi réelle n’est chargée et aucune candidature ne peut être envoyée ici.',
        ['Ne saisissez pas de CV ni de données personnelles.', 'La liste des offres n’est pas disponible hors ligne.', 'Cette page ne se connecte à aucun service de recrutement.'],
        'Périmètre', 'Le lien est conservé sous forme d’information pour maintenir la navigation locale.', (), None, 'emploi carrière recrutement', True),
    'banque': entry('Allianz Banque', 'Informations',
        'Les services bancaires ne sont pas reproduits dans cette démonstration.',
        'Aucun accès bancaire', 'Cette page ne permet ni de consulter un compte, ni d’effectuer une opération ou une souscription.',
        ['Aucune authentification.', 'Aucune donnée bancaire demandée.', 'Aucun service bancaire réel disponible.'],
        'Périmètre', 'Revenez au catalogue des sujets professionnels disponibles localement.', (), None, 'banque compte bancaire', True),
    'particuliers': entry('Espace particuliers', 'Informations',
        'La version locale reproduit le contenu professionnel et ne comprend pas le site destiné aux particuliers.',
        'Périmètre', 'Cette page remplace un lien externe et permet de revenir à la version professionnelle.',
        ['Aucun contrat particulier.', 'Aucun compte ni service réel.', 'Toutes les pages de la démo restent consultables localement.'],
        'Retour à la démo', 'Explorez les assurances professionnelles depuis le catalogue local.', (), None, 'particulier personnel', True),
    'mentions-legales': entry('À propos de cette version locale', 'Informations légales',
        'Ce mini-site est une reconstruction indépendante, non officielle et non affiliée à Allianz.',
        'Démonstration uniquement', 'Les contenus sont inspirés de la page publique consultée. Ils peuvent être incomplets ou périmés et ne constituent ni un devis, ni une offre, ni un conseil.',
        ['Aucune souscription, authentification ou transmission à Allianz.', 'Les marques restent la propriété de leurs titulaires.', 'Les photographies sont des illustrations générées, et non les images de la page source.'],
        'Utilisation des données', 'Les interactions de démonstration sont traitées dans le navigateur. Le serveur local et l’historique du navigateur peuvent conserver les adresses consultées. Ne saisissez pas de données sensibles.',
        ('cookies', 'accessibilite'), None, 'légal non officiel confidentialité données', True),
    'cookies': entry('Cookies et confidentialité', 'Informations légales',
        'La reconstruction locale n’utilise pas de cookies de suivi, de publicité ou de mesure d’audience.',
        'Fonctionnement local', 'Le site ne transmet pas vos saisies à Allianz ou à un service tiers. Les simulations sont conservées uniquement dans la page tant qu’elle reste ouverte.',
        ['Pas de compte ni de mot de passe.', 'Pas de formulaire de contact ou de devis réel.', 'Un serveur local peut enregistrer les requêtes et le navigateur peut conserver l’historique.'],
        'Documents locaux', 'Le téléchargement d’un récapitulatif est déclenché dans votre navigateur ; vous choisissez ensuite où le conserver.',
        ('mentions-legales',), None, 'cookie suivi données confidentialité', True),
    'accessibilite': entry('Accessibilité de la démonstration', 'Informations légales',
        'Le mini-site propose une navigation au clavier, des libellés de formulaires et une structure de titres.',
        'Fonctionnalités', 'Les menus, les questions/réponses et les liens restent utilisables sans souris. Les principales informations sont accessibles sans JavaScript.',
        ['Lien d’accès direct au contenu.', 'Indicateur de focus visible et menus au clavier.', 'Mise en page adaptée aux petits écrans et au mouvement réduit.'],
        'Limites', 'Cette page ne constitue pas une déclaration de conformité réglementaire ou une certification d’accessibilité.',
        ('mentions-legales',), None, 'accessibilité clavier contraste', True),
}


# Rubriques supplémentaires présentes dans le pied de page de la source.
PAGES.update({
    'responsabilite-environnementale': entry('Responsabilité environnementale', 'Assurance de l’activité',
        'Les activités professionnelles peuvent être exposées à des risques de dommages à l’environnement.',
        'Risques et prévention', 'Les obligations et les conséquences possibles dépendent de l’activité, des installations et de la réglementation applicable.',
        ['Identifier les risques de pollution ou de dommage.', 'Mettre en place les mesures de prévention adaptées.', 'Examiner les responsabilités et les garanties prévues par les contrats.'],
        'À vérifier', 'Cette page est une présentation générale : elle ne constitue ni une analyse réglementaire ni une garantie d’assurance.',
        ('activite', 'prevention-climat', 'rc-pro'), 'assets/entreprise.jpg', 'environnement pollution responsabilité entreprise'),
    'epargne-salariale': entry('Épargne salariale', 'Protection des salariés',
        'L’épargne salariale regroupe des dispositifs collectifs dont les conditions dépendent de l’entreprise et de la réglementation.',
        'Les sujets à examiner', 'Un dispositif d’épargne peut notamment être lié à la participation, à l’intéressement ou à un plan d’épargne entreprise.',
        ['Conditions de mise en place et salariés concernés.', 'Modalités de versement et de disponibilité.', 'Frais, risques et règles applicables au dispositif.'],
        'Pas de conseil financier', 'Cette démonstration ne propose aucun placement, calcul de rendement ou souscription. Consultez les documents et règles applicables avant toute décision.',
        ('salaries', 'retraite-collective'), None, 'épargne salariale pee participation intéressement salariés'),
    'retraite-collective': entry('Retraite collective', 'Protection des salariés',
        'Un dispositif de retraite collective peut contribuer à préparer la retraite des salariés selon ses règles propres.',
        'Points de repère', 'Les possibilités et obligations dépendent de l’entreprise, du dispositif et de la réglementation.',
        ['Salariés concernés et conditions d’adhésion.', 'Versements et modalités de sortie.', 'Frais, risques et règles fiscales applicables.'],
        'Information générale', 'Aucun conseil financier personnalisé, calcul ou contrat n’est proposé dans cette version locale.',
        ('salaries', 'epargne-salariale', 'retraite'), None, 'retraite collective épargne salariés'),
    'outre-mer': entry('Allianz Outre-mer', 'Informations',
        'Le site consacré à l’Outre-mer ne fait pas partie de cette reconstruction locale.',
        'Périmètre', 'Cette page remplace un lien externe pour conserver une navigation locale.',
        ['Aucun contrat ni service territorial réel.', 'Aucune information locale actualisée.', 'Retour possible vers la page professionnelle de démonstration.'],
        'Version indépendante', 'La reconstruction est non officielle et ne se connecte à aucun service Allianz.', (), None, 'outre mer', True),
    'investisseurs': entry('Allianz Global Investors', 'Informations',
        'Les services de gestion d’actifs ne sont pas reproduits dans cette démonstration.',
        'Aucun service financier', 'Il n’est pas possible de consulter des produits financiers, d’investir ou d’accéder à un compte depuis cette page.',
        ['Aucun placement ou conseil personnalisé.', 'Aucune donnée bancaire demandée.', 'Aucune connexion au service officiel.'],
        'Périmètre', 'Ce lien mène à une information locale et non à une plateforme d’investissement.', (), None, 'investisseurs gestion actifs placement', True),
    'immovalor': entry('Allianz Immovalor', 'Informations',
        'Les services immobiliers et financiers liés à cette rubrique ne sont pas reproduits ici.',
        'Périmètre', 'La démonstration ne permet ni de consulter des produits d’investissement ni d’effectuer une opération.',
        ['Aucune souscription.', 'Aucune donnée financière ou personnelle demandée.', 'Aucune connexion au service officiel.'],
        'Version locale', 'Revenez au catalogue professionnel pour consulter les pages disponibles.', (), None, 'immobilier investissement immovalor', True),
    'reseaux-sociaux': entry('Réseaux sociaux', 'Informations',
        'Les pages des réseaux sociaux externes ne sont pas intégrées dans cette démonstration.',
        'Périmètre', 'Les liens du pied de page mènent à cette information locale ; aucun réseau social n’est contacté.',
        ['Pas de compte ni de connexion.', 'Aucun contenu externe ou fil actualisé.', 'Aucun partage ou message envoyé.'],
        'Retour au site', 'Les contenus professionnels restent disponibles dans le catalogue de la démonstration.', (), None, 'facebook x linkedin youtube instagram social', True),
})

for key, page in PAGES.items():
    for related in page['related']:
        if related not in PAGES:
            raise ValueError(f'{key}: page liée inconnue: {related}')


def e(value):
    return escape(str(value), quote=True)


def card(key, page):
    terms = ' '.join([page['title'], page['category'], page['lead'], page['tags']])
    return f'''<a class="catalog-card" data-search-item data-search="{e(terms)}" href="{{{{R}}}}pages/{e(key)}.html">
        <span class="catalog-category">{e(page['category'])}</span><h2>{e(page['title'])}</h2>
        <p>{e(page['lead'])}</p><span class="text-link">Découvrir <span aria-hidden="true">→</span></span></a>'''


def breadcrumb(title):
    return f'''<div class="wrap local-breadcrumb"><a href="{{{{R}}}}index.html">Accueil professionnels</a><span aria-hidden="true">›</span>{e(title)}</div>'''


def detail_page(key, page):
    image = (f'<div class="local-hero-image"><img src="{{{{R}}}}{e(page["image"])}" alt="" loading="eager"></div>' if page['image'] else '')
    related = ''.join(f'<a href="{{{{R}}}}pages/{e(k)}.html">{e(PAGES[k]["title"])} <span aria-hidden="true">→</span></a>' for k in page['related'])
    if page['info']:
        actions = '<a class="button" href="{{R}}catalogue.html">Explorer le catalogue local <span aria-hidden="true">→</span></a>'
        aside = '''<h2>Version de démonstration</h2><p>Cette reconstruction fonctionne sans connexion aux services Allianz.</p><a href="{{R}}index.html">Retour à l’accueil <span aria-hidden="true">→</span></a><a href="{{R}}contact.html">Informations de contact <span aria-hidden="true">→</span></a>'''
    else:
        actions = '<a class="button" href="{{R}}devis.html">Simuler mes besoins <span aria-hidden="true">→</span></a><a class="button button-outline" href="{{R}}catalogue.html">Toutes les solutions</a>'
        aside = f'''<h2>Pour aller plus loin</h2><p>La simulation locale ne donne ni tarif ni contrat.</p><a class="button" href="{{{{R}}}}devis.html">Faire une simulation</a>{related}<a href="{{{{R}}}}catalogue.html">Tout le catalogue <span aria-hidden="true">→</span></a>'''
    points = ''.join(f'<li>{e(item)}</li>' for item in page['points'])
    return f'''{breadcrumb(page['title'])}
    <section class="local-hero"><div class="wrap local-hero-grid {'no-image' if not image else ''}"><div>
      <p class="eyebrow blue-eyebrow"><span></span> {e(page['category'])}</p><h1>{e(page['title'])}</h1><p>{e(page['lead'])}</p>{actions}
    </div>{image}</div></section>
    <div class="wrap detail-content"><div class="detail-layout"><article class="detail-body">
      <section><h2>{e(page['heading'])}</h2><p>{e(page['intro'])}</p><ul>{points}</ul></section>
      <section><h2>{e(page['follow_heading'])}</h2><p>{e(page['follow'])}</p></section>
      <div class="local-note"><strong>Reconstruction locale non officielle.</strong> Les informations sont indicatives, sans valeur contractuelle et ne remplacent pas les conditions d’un contrat.</div>
    </article><aside class="detail-aside">{aside}</aside></div></div>'''


def catalogue_page():
    cards = ''.join(card(k, v) for k, v in PAGES.items() if not v['info'])
    return f'''{breadcrumb('Rechercher une assurance')}
    <div class="wrap local-page"><header class="local-page-heading"><p class="eyebrow blue-eyebrow"><span></span> Toutes nos solutions</p><h1 class="page-title">Rechercher une assurance</h1><p>Découvrez les pages thématiques disponibles dans cette version locale. Les informations sont indicatives et ne sont pas des offres.</p></header>
      <form class="local-form search-form" role="search" action="{{{{R}}}}catalogue.html" method="get" data-catalog-search><div><label class="form-label" for="catalog-query">Votre recherche</label><input id="catalog-query" name="q" type="search" placeholder="Ex. : multirisque, santé, commerçant…" autocomplete="off"></div><button class="button" type="submit" disabled>Rechercher</button></form>
      <noscript><p class="nojs-note">La recherche interactive nécessite JavaScript. Toutes les pages restent accessibles ci-dessous.</p></noscript>
      <p class="results-count" data-result-count aria-live="polite">Toutes les solutions disponibles</p>
      <div class="catalog-grid" data-catalog-results>{cards}</div><p class="empty-result" data-no-results hidden>Aucun résultat. Essayez un autre terme, par exemple « santé », « activité » ou « commerce ».</p>
    </div>'''


def quote_page():
    return f'''{breadcrumb('Simulation de besoins')}
    <div class="wrap local-page"><header class="local-page-heading"><p class="eyebrow blue-eyebrow"><span></span> Démonstration locale</p><h1 class="page-title">Simulation de besoins professionnels</h1><p>En quelques étapes, créez un récapitulatif indicatif. Aucun tarif officiel, contrat ou demande de devis ne sera produit.</p></header>
      <div class="local-note"><strong>Simulation sans transmission.</strong> Aucun nom, SIRET, mot de passe, coordonnée ou donnée sensible n’est demandé. Vos choix restent dans cette page jusqu’à sa fermeture.</div>
      <noscript><p class="nojs-note">La simulation interactive nécessite JavaScript. Consultez le <a href="{{{{R}}}}catalogue.html">catalogue local</a> sans JavaScript.</p></noscript>
      <ol class="step-list" aria-label="Étapes de la simulation"><li aria-current="step"><span class="step-number">1</span><span>Votre entreprise</span></li><li><span class="step-number">2</span><span>Votre besoin</span></li><li><span class="step-number">3</span><span>Votre résultat</span></li><li><span class="step-number">4</span><span>Récapitulatif</span></li></ol>
      <div class="wizard-layout"><form class="local-form wizard-card" data-quote-form novalidate>
        <section class="step-panel" data-quote-step="1" aria-labelledby="quote-title-1"><h2 id="quote-title-1" tabindex="-1">Votre entreprise</h2><p>Choisissez uniquement des caractéristiques générales, sans identifier votre entreprise.</p>
          <div class="form-row"><fieldset><label class="form-label" for="quote-activity">Votre activité</label><select id="quote-activity" name="activity" aria-describedby="quote-error-1" required><option value="">Sélectionnez une activité</option><option>Commerce</option><option>Artisanat et construction</option><option>Conseil, chiffre ou droit</option><option>Santé</option><option>Industrie ou entreprise</option><option>Association ou sport</option><option>Autre activité</option></select></fieldset>
          <fieldset><label class="form-label" for="quote-size">Taille de la structure</label><select id="quote-size" name="size" aria-describedby="quote-error-1" required><option value="">Sélectionnez une taille</option><option>Indépendant sans salarié</option><option>1 à 9 salariés</option><option>10 à 49 salariés</option><option>50 salariés ou plus</option></select></fieldset></div>
          <p class="form-error" id="quote-error-1" data-step-error="1" role="alert" hidden></p><div class="form-actions"><button class="button" type="button" data-next disabled>Continuer <span aria-hidden="true">→</span></button></div>
        </section>
        <section class="step-panel" data-quote-step="2" aria-labelledby="quote-title-2" hidden><h2 id="quote-title-2" tabindex="-1">Votre besoin</h2><p>Sélectionnez un ou plusieurs sujets à examiner.</p>
          <fieldset aria-describedby="quote-error-2"><legend>Que souhaitez-vous protéger ? (au moins un choix)</legend><div class="choice-grid"><label class="choice"><input type="checkbox" name="need" value="Responsabilité civile professionnelle"> Responsabilité civile professionnelle</label><label class="choice"><input type="checkbox" name="need" value="Locaux, matériel et multirisque"> Locaux, matériel et multirisque</label><label class="choice"><input type="checkbox" name="need" value="Véhicules professionnels"> Véhicules professionnels</label><label class="choice"><input type="checkbox" name="need" value="Santé des salariés"> Santé des salariés</label><label class="choice"><input type="checkbox" name="need" value="Protection du dirigeant"> Protection du dirigeant</label><label class="choice"><input type="checkbox" name="need" value="Autre besoin"> Autre besoin</label></div></fieldset>
          <p class="form-error" id="quote-error-2" data-step-error="2" role="alert" hidden></p><div class="form-actions"><button class="button button-quiet" type="button" data-prev disabled>Retour</button><button class="button" type="button" data-next disabled>Voir mon résultat <span aria-hidden="true">→</span></button></div>
        </section>
        <section class="step-panel" data-quote-step="3" aria-labelledby="quote-title-3" hidden><h2 id="quote-title-3" tabindex="-1">Votre résultat indicatif</h2><div class="local-note"><strong>Aucun tarif n’est calculé.</strong> Les choix suivants constituent un simple résumé de besoins, sans valeur de devis ni de conseil personnalisé.</div><dl class="summary-list" data-quote-summary></dl><div class="form-actions"><button class="button button-quiet" type="button" data-prev disabled>Retour</button><button class="button" type="button" data-next disabled>Continuer <span aria-hidden="true">→</span></button></div></section>
        <section class="step-panel" data-quote-step="4" aria-labelledby="quote-title-4" hidden><h2 id="quote-title-4" tabindex="-1">Votre récapitulatif</h2><p>Vous pouvez télécharger ou imprimer ce résumé. Aucune demande n’a été envoyée.</p><dl class="summary-list" data-quote-summary></dl><p class="form-help">Document de démonstration : il ne constitue ni une attestation, ni un devis, ni un contrat.</p><div class="form-actions"><button class="button button-quiet" type="button" data-prev disabled>Retour</button><button class="button" type="button" data-download-summary disabled>Télécharger le résumé</button><button class="button button-quiet" type="button" data-print-summary disabled>Imprimer</button></div></section>
      </form><aside class="side-facts"><strong>Votre simulation en toute clarté</strong><ul><li>Aucun compte ni mot de passe.</li><li>Aucune coordonnée ou donnée sensible.</li><li>Aucun envoi et aucun prix.</li><li>Des informations indicatives uniquement.</li></ul></aside></div>
    </div>'''


def client_page():
    return f'''{breadcrumb('Espace client de démonstration')}
    <div class="wrap local-page"><header class="local-page-heading"><p class="eyebrow blue-eyebrow"><span></span> Mes services clients</p><h1 class="page-title">Espace client de démonstration</h1><p>Explorez la présentation des contrats, documents et démarches. Cet espace n’est pas relié à Allianz et ne contient aucune donnée client.</p></header>
      <div class="local-note"><strong>Aucune connexion réelle.</strong> Ne saisissez pas d’identifiant, de mot de passe ou de numéro de contrat. Aucune attestation ne peut être délivrée.</div>
      <div data-demo-tabs><div class="demo-tabs" role="tablist" aria-label="Rubriques de l’espace de démonstration"><button type="button" id="tab-contracts" role="tab" aria-selected="true" aria-controls="panel-contracts" disabled>Mes contrats</button><button type="button" id="tab-documents" role="tab" aria-selected="false" aria-controls="panel-documents" disabled>Mes documents</button><button type="button" id="tab-requests" role="tab" aria-selected="false" aria-controls="panel-requests" disabled>Mes démarches</button></div>
        <section class="demo-panel" id="panel-contracts" role="tabpanel" aria-labelledby="tab-contracts"><h2>Mes contrats</h2><div class="demo-card-grid"><article class="demo-card"><span class="tag-demo">Exemple fictif</span><h3>Contrat professionnel</h3><p>Aucun contrat réel n’est disponible. Cette carte illustre l’emplacement d’un contrat.</p><a class="text-link" href="{{{{R}}}}pages/multirisque.html">Comprendre la multirisque →</a></article><article class="demo-card"><h3>Explorer les solutions</h3><p>Consultez les thèmes présentés dans le catalogue local.</p><a class="text-link" href="{{{{R}}}}catalogue.html">Voir le catalogue →</a></article></div></section>
        <section class="demo-panel" id="panel-documents" role="tabpanel" aria-labelledby="tab-documents"><h2>Mes documents</h2><div class="demo-card-grid"><article class="demo-card"><span class="tag-demo">Document de démonstration</span><h3>Exemple de document</h3><p>Un simple fichier explicatif, sans valeur d’attestation ou de contrat.</p><a class="text-link" href="{{{{R}}}}assets/exemple-document-demo.txt" download>Télécharger l’exemple →</a></article><article class="demo-card"><h3>Attestation RC Pro</h3><p>La démo ne peut pas produire d’attestation réelle. Contactez votre assureur pour un document officiel.</p></article></div></section>
        <section class="demo-panel" id="panel-requests" role="tabpanel" aria-labelledby="tab-requests"><h2>Mes démarches</h2><div class="demo-card-grid"><article class="demo-card"><span class="tag-demo">Simulation</span><h3>Exemple de démarche</h3><p>Essayez l’interaction : rien n’est transmis ni enregistré après fermeture de la page.</p><button class="button button-outline" type="button" data-demo-request disabled>Simuler une demande</button><p class="demo-status" data-demo-request-status role="status"></p></article><article class="demo-card"><h3>Besoin d’aide ?</h3><p>Retrouvez les informations de contact reproduites dans cette version.</p><a class="text-link" href="{{{{R}}}}contact.html">Voir les contacts →</a></article></div></section>
      </div><noscript><p class="nojs-note">Les onglets interactifs nécessitent JavaScript ; toutes les rubriques sont affichées ci-dessus.</p></noscript>
    </div>'''


def contact_page():
    return f'''{breadcrumb('Nous contacter')}
    <div class="wrap local-page"><header class="local-page-heading"><p class="eyebrow blue-eyebrow"><span></span> Assistance et sinistres</p><h1 class="page-title">Nous contacter</h1><p>Retrouvez les principales démarches décrites sur la page source et les possibilités de cette démonstration.</p></header>
      <div class="local-note"><strong>Aucun message ne peut être envoyé depuis cette page.</strong> Les numéros publics ci-dessous sont reproduits à titre d’information ; un appel contacte un service réel et nécessite un téléphone. Leur disponibilité n’est pas vérifiée par cette démo.</div>
      <h2 class="local-section-title">Comment pouvons-nous vous aider ?</h2><div class="contact-grid">
        <article class="demo-card"><h3>Déclarer un sinistre</h3><p>La page source indique le numéro suivant pour déclarer un sinistre ou obtenir des informations sur les garanties :</p><a href="tel:0978978000">09 78 97 80 00</a></article>
        <article class="demo-card"><h3>Assistance</h3><p>La page source indique ce numéro pour une assistance ou un accompagnement psychologique :</p><a href="tel:0140255295">01 40 25 52 95</a></article>
        <article class="demo-card"><h3>Votre contrat ou votre agence</h3><p>L’espace local ne contient aucun contrat. Le moteur d’agences ne présente que des exemples fictifs.</p><a href="{{{{R}}}}agences.html">Explorer les agences de démonstration →</a></article>
        <article class="demo-card"><h3>Devis et réclamation</h3><p>Essayez le simulateur de besoins ou consultez les limites des démarches reproduites.</p><a href="{{{{R}}}}devis.html">Faire une simulation →</a><br><a href="{{{{R}}}}pages/reclamation.html">À propos des réclamations →</a></article>
      </div>
    </div>'''


def agency_page():
    return f'''{breadcrumb('Trouver une agence')}
    <div class="wrap local-page"><header class="local-page-heading"><p class="eyebrow blue-eyebrow"><span></span> Trouver une agence</p><h1 class="page-title">Recherche d’agence de démonstration</h1><p>Le moteur local permet d’essayer une recherche parmi trois exemples fictifs. Il ne consulte pas l’annuaire des agences réelles.</p></header>
      <div class="local-note"><strong>Adresses et coordonnées réelles indisponibles.</strong> Les résultats ci-dessous sont inventés pour la démonstration, sans adresse, numéro de téléphone ou service associé.</div>
      <form class="local-form search-form" data-agency-search><div><label class="form-label" for="agency-query">Ville de l’exemple</label><input id="agency-query" type="search" placeholder="Essayez Paris, Lyon ou Marseille" autocomplete="off"><small class="form-help">Ne saisissez pas d’adresse personnelle.</small></div><button type="submit" class="button" disabled>Rechercher</button></form>
      <noscript><p class="nojs-note">Le filtrage nécessite JavaScript. Les exemples restent affichés ci-dessous.</p></noscript><p class="results-count" data-agency-count aria-live="polite">3 exemples fictifs</p>
      <div class="agency-list"><article class="demo-card" data-agency-item data-search="Paris"><span class="tag-demo">Exemple fictif</span><h3>Agence exemple · Paris</h3><p>Aucune adresse ni coordonnée réelle.</p></article><article class="demo-card" data-agency-item data-search="Lyon"><span class="tag-demo">Exemple fictif</span><h3>Agence exemple · Lyon</h3><p>Aucune adresse ni coordonnée réelle.</p></article><article class="demo-card" data-agency-item data-search="Marseille"><span class="tag-demo">Exemple fictif</span><h3>Agence exemple · Marseille</h3><p>Aucune adresse ni coordonnée réelle.</p></article></div><p class="empty-result" data-agency-empty hidden>Aucun exemple fictif pour cette recherche. Essayez Paris, Lyon ou Marseille.</p>
    </div>'''


def rewrite_shell(html, nested):
    # Preserve fragment-only links (skip link, icons, back-to-top) on the current page.
    html = html.replace('href="#questions"', 'href="{{R}}index.html#questions"')
    if nested:
        def rewrite(match):
            attr, value = match.groups()
            if value.startswith(('#', 'tel:', 'mailto:', 'https:', 'http:', '{{R}}')):
                return match.group(0)
            if value == './':
                value = '../'
            else:
                value = '../' + value
            return f'{attr}="{value}"'
        html = re.sub(r'\b(href|src)="([^"]+)"', rewrite, html)
    return html


def render_page(path, title, main):
    nested = len(Path(path).parts) > 1
    index = (ROOT / 'index.html').read_text(encoding='utf-8')
    head, rest = index.split('<main id="contenu">', 1)
    _, tail = rest.split('</main>', 1)
    head = re.sub(r'<title>.*?</title>', f'<title>{e(title)} | Démo locale assurance professionnelle</title>', head, count=1)
    head = head.replace(' aria-current="page"', '')
    head = rewrite_shell(head, nested)
    tail = rewrite_shell(tail, nested)
    prefix = '../' if nested else ''
    arrow = '<svg class="icon inline-arrow" aria-hidden="true"><use href="#i-arrow-right"></use></svg>'
    main = main.replace('→', arrow)
    result = (head + '<main id="contenu">\n' + main + '\n  </main>' + tail).replace('{{R}}', prefix)
    (ROOT / path).write_text(result, encoding='utf-8')


def main():
    (ROOT / 'pages').mkdir(exist_ok=True)
    for key, page in PAGES.items():
        render_page(f'pages/{key}.html', page['title'], detail_page(key, page))
    for path, title, body in [
        ('catalogue.html', 'Rechercher une assurance', catalogue_page()),
        ('devis.html', 'Simulation de besoins', quote_page()),
        ('espace-client.html', 'Espace client de démonstration', client_page()),
        ('contact.html', 'Nous contacter', contact_page()),
        ('agences.html', 'Recherche d’agence de démonstration', agency_page()),
    ]:
        render_page(path, title, body)
    print(f'{len(PAGES) + 5} pages statiques générées.')


if __name__ == '__main__':
    main()
