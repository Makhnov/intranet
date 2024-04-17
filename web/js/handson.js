(()=>{"use strict";var e,t={2618:(e,t,n)=>{var i=n(5311),l=n.n(i),r=n(1544);const o={contenteditable:"true","plaintext-only":"true",tabindex:"0"};function a(e,t){const n=e+"-handsontable-container";var i=e+"-handsontable-header",a=e+"-handsontable-col-header",s=e+"-table-header-choice";const d=e+"-handsontable-col-caption",c=l()("#"+e);var u=l()("#"+i),h=l()("#"+a),p=l()("#"+s);const f=l()("#"+d),g={};let A=null,C=null,b=!1;const m=l()("#"+e).parent(),_=function(){let e=0;return m.find(".htCore").each((function(){e+=l()(this).height()})),e+m.find("[data-field]").first().height()},v=[`#${n}`,".wtHider",".wtHolder"],w=function(t){const n=l()("#"+e);l().each(v,(function(){n.closest("[data-field]").find(this).height(t)}))};try{C=JSON.parse(c.val())}catch(e){}null!==C&&((0,r.R)(C,"table_caption")&&f.prop("value",C.table_caption),(0,r.R)(C,"table_header_choice")&&p.prop("value",C.table_header_choice)),(0,r.R)(t,"width")&&(0,r.R)(t,"height")||l()(window).on("resize",(()=>{var e;A.updateSettings({width:l()(".w-field--table_input").closest(".w-panel").width(),height:_()}),e="100%",l().each(v,(function(){l()(this).width(e)})),l()(".w-field--table_input").width(e)}));const S=function(){const e=[],t=[];A.getCellsMeta().forEach((t=>{let n,i;(0,r.R)(t,"className")&&(n=t.className),(0,r.R)(t,"hidden")&&(i=!0),(void 0!==n||i)&&e.push({row:t.row,col:t.col,className:n,hidden:i})})),A.getPlugin("mergeCells").isEnabled()&&A.getPlugin("mergeCells").mergedCellsCollection.mergedCells.forEach((e=>{t.push({row:e.row,col:e.col,rowspan:e.rowspan,colspan:e.colspan})})),c.val(JSON.stringify({data:A.getData(),cell:e,mergeCells:t,first_row_is_table_header:u.val(),first_col_is_header:h.val(),table_header_choice:p.val(),table_caption:f.val()}))},$=function(e,t){w(_()),S(),l()((()=>{l()(m).find("td, th").attr(o)}))};p.on("change",(()=>{S()})),f.on("change",(()=>{S()}));const M={afterChange:function(e,t){b&&"loadData"!==t&&"MergeCells"!==t&&S()},afterCreateCol:$,afterCreateRow:$,afterRemoveCol:$,afterRemoveRow:$,afterSetCellMeta:function(e,t,n,i){b&&"className"===n&&S()},afterMergeCells:function(e,t,n){b&&S()},afterUnmergeCells:function(e,t){b&&S()},afterInit:function(){b=!0}};null!==C&&((0,r.R)(C,"data")&&(M.data=C.data),(0,r.R)(C,"cell")&&(M.cell=C.cell)),Object.keys(M).forEach((e=>{g[e]=M[e]})),Object.keys(t).forEach((e=>{g[e]=t[e]})),(0,r.R)(g,"mergeCells")&&!0===g.mergeCells&&null!==C&&(0,r.R)(C,"mergeCells")&&(g.mergeCells=C.mergeCells),A=new Handsontable(document.getElementById(n),g),window.addEventListener("load",(()=>{A.render(),w(_()),m.find("td, th").attr(o),window.dispatchEvent(new Event("resize"))}))}window.initTable=a,window.telepath.register("wagtail.widgets.TableInput",class{constructor(e,t){this.options=e,this.strings=t}render(e,t,n,i){const r=document.createElement("div");r.innerHTML=`\n      <div class="w-field__wrapper" data-field-wrapper>\n        <label class="w-field__label" for="${n}-table-header-choice">${this.strings["Table headers"]}</label>\n          <select id="${n}-table-header-choice" name="table-header-choice">\n            <option value="">Choisissez une option</option>\n            <option value="row">\n                ${this.strings["Display the first row as a header"]}\n            </option>\n            <option value="column">\n                ${this.strings["Display the first column as a header"]}\n            </option>\n            <option value="both">\n                ${this.strings["Display the first row AND first column as headers"]}\n            </option>\n            <option value="neither">\n                ${this.strings["No headers"]}\n            </option>\n          </select>\n        <p class="help">${this.strings["Which cells should be displayed as headers?"]}</p>\n      </div>\n      <div class="w-field__wrapper" data-field-wrapper>\n        <label class="w-field__label" for="${n}-handsontable-col-caption">${this.strings["Table caption"]}</label>\n        <div class="w-field w-field--char_field w-field--text_input" data-field>\n          <div class="w-field__help" id="${n}-handsontable-col-caption-helptext" data-field-help>\n            <div class="help">${this.strings["A heading that identifies the overall topic of the table, and is useful for screen reader users."]}</div>\n          </div>\n          <div class="w-field__input" data-field-input>\n            <input type="text" id="${n}-handsontable-col-caption" name="handsontable-col-caption" aria-describedby="${n}-handsontable-col-caption-helptext" />\n          </div>\n        </div>\n      </div>\n      <div id="${n}-handsontable-container"></div>\n      <input type="hidden" name="${t}" id="${n}" placeholder="${this.strings.Table}">\n    `,l()((()=>{const e=document.getElementById(`${n}-handsontable-container`);l()(e).find("td, th").attr(o)})),e.replaceWith(r);const s=r.querySelector(`input[name="${t}"]`),d=this.options,c={getValue:()=>JSON.parse(s.value),getState:()=>JSON.parse(s.value),setState(e){s.value=JSON.stringify(e),a(n,d)},focus(){}};return c.setState(i),c}})},5311:e=>{e.exports=jQuery}},n={};function i(e){var l=n[e];if(void 0!==l)return l.exports;var r=n[e]={id:e,loaded:!1,exports:{}};return t[e].call(r.exports,r,r.exports,i),r.loaded=!0,r.exports}i.m=t,e=[],i.O=(t,n,l,r)=>{if(!n){var o=1/0;for(c=0;c<e.length;c++){for(var[n,l,r]=e[c],a=!0,s=0;s<n.length;s++)(!1&r||o>=r)&&Object.keys(i.O).every((e=>i.O[e](n[s])))?n.splice(s--,1):(a=!1,r<o&&(o=r));if(a){e.splice(c--,1);var d=l();void 0!==d&&(t=d)}}return t}r=r||0;for(var c=e.length;c>0&&e[c-1][2]>r;c--)e[c]=e[c-1];e[c]=[n,l,r]},i.n=e=>{var t=e&&e.__esModule?()=>e.default:()=>e;return i.d(t,{a:t}),t},i.d=(e,t)=>{for(var n in t)i.o(t,n)&&!i.o(e,n)&&Object.defineProperty(e,n,{enumerable:!0,get:t[n]})},i.g=function(){if("object"==typeof globalThis)return globalThis;try{return this||new Function("return this")()}catch(e){if("object"==typeof window)return window}}(),i.o=(e,t)=>Object.prototype.hasOwnProperty.call(e,t),i.r=e=>{"undefined"!=typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(e,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(e,"__esModule",{value:!0})},i.nmd=e=>(e.paths=[],e.children||(e.children=[]),e),i.j=986,(()=>{var e={986:0};i.O.j=t=>0===e[t];var t=(t,n)=>{var l,r,[o,a,s]=n,d=0;if(o.some((t=>0!==e[t]))){for(l in a)i.o(a,l)&&(i.m[l]=a[l]);if(s)var c=s(i)}for(t&&t(n);d<o.length;d++)r=o[d],i.o(e,r)&&e[r]&&e[r][0](),e[r]=0;return i.O(c)},n=globalThis.webpackChunkwagtail=globalThis.webpackChunkwagtail||[];n.forEach(t.bind(null,0)),n.push=t.bind(null,n.push.bind(n))})();var l=i.O(void 0,[751],(()=>i(2618)));l=i.O(l)})();
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
    console.log('traité');
    Handsontable.languages.registerLanguageDictionary(dictionary);
}