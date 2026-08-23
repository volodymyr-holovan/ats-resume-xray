# Sources de recherche

Chaque règle de [`src/ats_xray/rules.py`](../src/ats_xray/rules.py) porte une
clé `source` renvoyant à une entrée de ce fichier, plutôt qu'une URL figée dans
le code : une citation se corrige ou s'enrichit ainsi à un seul endroit, sans
toucher au Python.

La plupart des entrées citent des ressources de conseil en carrière et de test
d'ATS plutôt qu'une étude évaluée par les pairs, parce que c'est là que réside
réellement ce savoir : les systèmes de suivi des candidatures sont fermés et
non documentés. Ce que l'on sait de leur comportement d'analyse provient de
prestataires et de conseillers qui testent de vrais CV sur de vrais ATS et
publient leurs constats — non de la documentation des éditeurs ni de la
recherche académique. Considérez cela comme un consensus sectoriel cohérent et
largement répété, pas comme des expériences contrôlées. Liens consultés en août
2026 et laissés en anglais : les articles le sont.

## ats-fonts

Les polices non standard ou non incorporées risquent d'être mal lues, remplacées ou entièrement écartées, produisant un texte illisible ou manquant.

- [How ATS Handles Fonts: Complete Guide to Resume Formatting](https://hireflow.net/blog/how-ats-handles-fonts)

## ats-headers-footers

Le contenu placé en en-tête ou pied de page est souvent entièrement ignoré par les analyseurs d'ATS, qui le considèrent comme de l'habillage hors du corps du document.

- [How ATS Reads Headers and Footers: Complete Guide to Resume Parsing](https://hireflow.net/blog/how-ats-reads-headers-and-footers)

## ats-text-boxes

Les zones de texte placent le contenu hors du flux normal de paragraphes ; beaucoup d'analyseurs ignorent totalement cette couche, si bien que le texte qui s'y trouve disparaît silencieusement.

- [Why ATS Rejects Resumes with Text Boxes: Complete Guide to ATS-Friendly Formatting](https://hireflow.net/blog/why-ats-rejects-resumes-with-text-boxes)

## ats-tables-columns

Les mises en page multicolonnes et les tableaux sont lus par de nombreux analyseurs ligne par ligne en travers des colonnes, brouillant l'association entre valeur et libellé (« salade de mots »).

- [Why ATS Tables and Columns Break Your Resume Parsing](https://www.jobscan.co/blog/resume-tables-columns-ats/)
- [Can ATS Read Tables & Columns? We Tested 8 Systems](https://cvcraft.roynex.com/blog/can-ats-read-tables-columns-formatting-2026)

## ats-graphics

Les CV exportés en image (courant avec les modèles d'outils de design comme Canva) présentent le contenu sous une forme que la plupart des analyseurs ne peuvent pas lire comme du texte.

- [Can ATS Read Tables, Columns and Canva Resumes?](https://www.mployee.me/blog/can-ats-read-tables-columns-canva-resumes)

## practical-necessity

Pas une citation externe : un CV sur lequel un recruteur ne trouve pas de coordonnées est injoignable, quoi qu'un analyseur ait extrait correctement par ailleurs. Cette règle existe pour des raisons pratiques, non de recherche.
