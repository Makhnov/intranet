const CONTEXT_MENU_ITEMS_NAMESPACE = 'ContextMenu:items';

const CM_ALIAS = CONTEXT_MENU_ITEMS_NAMESPACE;

const dictionary = {
  languageCode: 'fr-FR',
  [`${CM_ALIAS}.insertRowAbove`]: 'Insérer une ligne au dessus',
  [`${CM_ALIAS}.insertRowBelow`]: 'Insérer une ligne en dessous',
  [`${CM_ALIAS}.insertColumnOnTheLeft`]: 'Insérer une colonne à gauche',
  [`${CM_ALIAS}.insertColumnOnTheRight`]: 'Insérer une colonne à droite',
  [`${CM_ALIAS}.removeRow`]: ['Supprimer une ligne', 'Supprimer les lignes'],
  [`${CM_ALIAS}.removeColumn`]: ['Supprimer une colonne', 'Supprimer les colonnes'],
  [`${CM_ALIAS}.undo`]: 'Annuler',
  [`${CM_ALIAS}.redo`]: 'Rétablir',
  [`${CM_ALIAS}.readOnly`]: 'Lecture seule',
  [`${CM_ALIAS}.clearColumn`]: 'Effacer la colonne',

  [`${CM_ALIAS}.align`]: 'Alignement',
  [`${CM_ALIAS}.align.left`]: 'Gauche',
  [`${CM_ALIAS}.align.center`]: 'Centre',
  [`${CM_ALIAS}.align.right`]: 'Droite',
  [`${CM_ALIAS}.align.justify`]: 'Justifié',
  [`${CM_ALIAS}.align.top`]: 'En haut',
  [`${CM_ALIAS}.align.middle`]: 'Au milieu',
  [`${CM_ALIAS}.align.bottom`]: 'En bas',

  [`${CM_ALIAS}.freezeColumn`]: 'Figer la colonne',
  [`${CM_ALIAS}.unfreezeColumn`]: 'Libérer la colonne',

  [`${CM_ALIAS}.borders`]: 'Bordures',
  [`${CM_ALIAS}.borders.top`]: 'Supérieure',
  [`${CM_ALIAS}.borders.right`]: 'Droite',
  [`${CM_ALIAS}.borders.bottom`]: 'Inférieure',
  [`${CM_ALIAS}.borders.left`]: 'Gauche',
  [`${CM_ALIAS}.borders.remove`]: 'Pas de bordure',

  [`${CM_ALIAS}.addComment`]: 'Ajouter commentaire',
  [`${CM_ALIAS}.editComment`]: 'Modifier commentaire',
  [`${CM_ALIAS}.removeComment`]: 'Supprimer commentaire',
  [`${CM_ALIAS}.readOnlyComment`]: 'Commentaire en lecture seule',

  [`${CM_ALIAS}.mergeCells`]: 'Fusionner les cellules',
  [`${CM_ALIAS}.unmergeCells`]: 'Séparer les cellules',

  [`${CM_ALIAS}.copy`]: 'Copier',
  [`${CM_ALIAS}.cut`]: 'Couper',

  [`${CM_ALIAS}.nestedHeaders.insertChildRow`]: 'Insérer une sous-ligne',
  [`${CM_ALIAS}.nestedHeaders.detachFromParent`]: 'Détacher de la ligne précédente',

  [`${CM_ALIAS}.hideColumn`]: ['Masquer colonne', 'Masquer les colonnes'],
  [`${CM_ALIAS}.showColumn`]: ['Afficher colonne', 'Afficher les colonnes'],

  [`${CM_ALIAS}.hideRow`]: ['Masquer ligne', 'Masquer les lignes'],
  [`${CM_ALIAS}.showRow`]: ['Afficher ligne', 'Afficher les lignes'],

  'Filters:conditions.none': 'Aucun',
  'Filters:conditions.isEmpty': 'Est vide',
  'Filters:conditions.isNotEmpty': 'N\'est pas vide',
  'Filters:conditions.isEqualTo': 'Egal à',
  'Filters:conditions.isNotEqualTo': 'Est différent de',
  'Filters:conditions.beginsWith': 'Commence par',
  'Filters:conditions.endsWith': 'Finit par',
  'Filters:conditions.contains': 'Contient',
  'Filters:conditions.doesNotContain': 'Ne contient pas',
  'Filters:conditions.greaterThan': 'Supérieur à',
  'Filters:conditions.greaterThanOrEqualTo': 'Supérieur ou égal à',
  'Filters:conditions.lessThan': 'Inférieur à',
  'Filters:conditions.lessThanOrEqualTo': 'Inférieur ou égal à',
  'Filters:conditions.isBetween': 'Est compris entre',
  'Filters:conditions.isNotBetween': 'N\'est pas compris entre',
  'Filters:conditions.after': 'Après le',
  'Filters:conditions.before': 'Avant le',
  'Filters:conditions.today': 'Aujourd\'hui',
  'Filters:conditions.tomorrow': 'Demain',
  'Filters:conditions.yesterday': 'Hier',

  'Filters:labels.filterByCondition': 'Filtrer par conditions',
  'Filters:labels.filterByValue': 'Filtrer par valeurs',

  'Filters:labels.conjunction': 'Et',
  'Filters:labels.disjunction': 'Ou',

  'Filters:values.blankCells': 'Cellules vides',

  'Filters:buttons.selectAll': 'Tout sélectionner',
  'Filters:buttons.clear': 'Effacer la sélection',
  'Filters:buttons.ok': 'OK',
  'Filters:buttons.cancel': 'Annuler',

  'Filters:buttons.placeholder.search': 'Chercher',
  'Filters:buttons.placeholder.value': 'Valeur',
  'Filters:buttons.placeholder.secondValue': 'Valeur de remplacement',
};

// On vérifie que Handsontable soit chargé et prêt
if (typeof Handsontable !== 'undefined') {
  Handsontable.languages.registerLanguageDictionary(dictionary);
}
