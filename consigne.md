***

# <b><span style="color:rgba(16,185,129,1)">Analyse complète des ventes d’un distributeur de café</span></b>

***

### <span style="color:rgba(59,130,246,1)">I. Contexte métier</span>

Vous êtes **Data Engineer** pour une enseigne spécialisée dans la vente de boissons chaudes à New York. L'entreprise exploite plusieurs magasins répartis sur différents quartiers et souhaite tirer parti de ses données de transaction pour mieux piloter ses décisions commerciales. Cet ensemble de données capture les transactions de vente quotidiennes en mars 2024. Il comprend les horodatages des transactions, les types de paiement (carte/espèces), les noms des produits à base de café et les revenus par transaction. Votre mission est de concevoir une solution de bout en bout permettant de collecter, transformer, stocker et visualiser les données de vente afin de fournir des indicateurs clés aux équipes marketing et direction.

***

### <span style="color:rgba(59,130,246,1)">II. Objectifs</span>

- Collecter les données depuis un fichier CSV brut
- Stocker les données dans une base PostgreSQL
- Nettoyer et structurer les données pour l’analyse
- Réaliser une exploration des ventes
- Créer un tableau de bord interactif pour les équipes métier

***

### <span style="color:rgba(59,130,246,1)">III. Données</span>

Les données sont issues d’un fichier CSV contenant l’historique des transactions réalisées dans les différents points de vente.

Les colonnes incluent des informations sur les produits, les magasins, les quantités vendues, les prix unitaires, ainsi que la date et l'heure de la transaction.

***

### <span style="color:rgba(59,130,246,1)">IV. Étapes du projet</span>

#### <span style="color:rgba(244,63,94,1)">1. Collecte et stockage</span>

**Tâches** :

- Charger les données dans un DataFrame avec Python - 
- Créer une base PostgreSQL et un schéma relationnel adapté - 
- Insérer les données nettoyées dans la base - 

**Livrables** :

- Script de chargement Python
- Schéma SQL de la table ou des tables

***

#### <span style="color:rgba(244,63,94,1)">2. Transformation et nettoyage</span>

**Tâches** :

- Vérifier et traiter les valeurs manquantes ou incohérentes
- Standardiser les formats de date et d’heure
- Créer des colonnes dérivées utiles (ex. : revenu, heure, jour)
- Organiser les données pour faciliter l’analyse (agrégations, jointures si besoin)

**Livrables** :

- Script de transformation
- Tables ou vues enrichies dans PostgreSQL

***

#### <span style="color:rgba(244,63,94,1)">3. Analyse exploratoire</span>

**Tâches** :

- Identifier les tendances de vente (produits, lieux, horaires)
- Produire des graphiques simples pour appuyer les constats
- Mettre en évidence des KPIs métiers pertinents

**Livrables** :

- Rapport d’analyse ou notebook avec visualisations

***

#### <span style="color:rgba(244,63,94,1)">4. Visualisation des données</span>

**Tâches** :

- Connecter un outil de visualisation (Power BI, Tableau, Metabase…) à la base PostgreSQL
- Créer un tableau de bord interactif avec filtres
- Inclure au minimum les visualisations suivantes :

  - Ventes par point de vente
  - Produits les plus vendus
  - Évolution temporelle des ventes
  - Répartition par type ou catégorie de produit


**Livrables** :

- Tableau de bord interactif
- Captures d’écran ou export

***

### <span style="color:rgba(59,130,246,1)">V. Contraintes techniques</span>

- Python pour le traitement de données
- PostgreSQL pour le stockage
- Outil de visualisation au choix (Power BI, Tableau, Metabase…)

***

### <span style="color:rgba(59,130,246,1)">VI. Critères d’évaluation</span>

- Pipeline clair, modulaire et reproductible
- Base de données bien structurée
- Code Python lisible et documenté
- Visualisations utiles, claires et interactives
- Démarche rigoureuse et orientée métier

***