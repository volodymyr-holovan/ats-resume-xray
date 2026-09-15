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

Pas une citation externe : qui ne met pas ses coordonnées sur son CV reste injoignable pour un recruteur, quoi qu'un analyseur ait extrait correctement par ailleurs. Cette règle existe pour des raisons pratiques, non de recherche.

---

Les entrées ci-dessous sont un autre type de règle. Elles ne portent pas sur ce qu'un logiciel peut lire, mais sur ce que les recruteurs d'un pays donné attendent d'un CV, et elles ne comptent jamais dans la note sur 100. Leurs sources sont des guides de carrière nationaux, cités dans la langue du pays concerné. Consultées en septembre 2026.

## cv-volunteering

Les conseils allemands s'accordent : le bénévolat (Ehrenamt) ne remplace pas l'expérience professionnelle et va dans sa propre rubrique, après l'expérience et la formation. Une personne débutante peut présenter un bénévolat pertinent comme expérience, et un Freiwilliges Soziales Jahr ou un Bundesfreiwilligendienst peut compter comme pratique. Les conseils ukrainiens placent le bénévolat dans une rubrique à part, sauf s'il était l'activité principale. Les guides néerlandais, espagnols, français, britanniques et russes acceptent le bénévolat dans l'expérience s'il est pertinent ou si l'expérience rémunérée est limitée — c'est pourquoi le contrôle ne s'applique qu'aux CV allemands et ukrainiens.

- [Ehrenamt im Lebenslauf: Beispiele, wie angeben? — karrierebibel.de](https://karrierebibel.de/ehrenamt-lebenslauf/)
- [Ehrenamt im Lebenslauf angeben: Wo es hingehört — cvlotse.de](https://cvlotse.de/ratgeber/ehrenamt-im-lebenslauf)
- [FSJ und BFD im Lebenslauf angeben — cvlotse.de](https://cvlotse.de/ratgeber/fsj-bfd-im-lebenslauf)
- [Як і навіщо описувати волонтерство у резюме — happymonday.ua](https://happymonday.ua/yak-opysuvaty-volonterstvo-v-rezyume)
- [Vrijwilligerswerk op je cv vermelden — cvmaker.nl](https://www.cvmaker.nl/blog/cv/vrijwilligerswerk-cv)
- [¿Deberías incluir experiencia como voluntario en tu currículum? — Forbes España](https://forbes.es/empresas/356465/deberias-incluir-experiencia-como-voluntario-en-tu-curriculum/)
- [Bénévolat sur le CV : conseils et exemples — OnlineCV](https://www.onlinecv.fr/comment-faire-un-cv/travail-volontaire/)
- [How to include volunteer experience on a CV — Indeed UK](https://uk.indeed.com/career-advice/cvs-cover-letters/volunteer-experience-cv)
- [Какой опыт волонтерства указывать в резюме — HR Time](https://hrtime.ru/material/kakoy-opyt-volonterstva-ukazyvat-v-reziume-89267/)

## cv-gaps

Les conseils allemands considèrent comme une période vide plus de deux mois sans emploi ni formation, jugent inoffensives huit à dix semaines, et attendent que les périodes à partir de trois ou quatre mois soient expliquées sur le CV. Après un diplôme, environ six mois de recherche d'emploi sont jugés normaux.

- [Lücken im Lebenslauf: Sinnvoll füllen und erklären — karrierebibel.de](https://karrierebibel.de/luecken-im-lebenslauf/)
- [Lücke im Lebenslauf — StepStone](https://www.stepstone.de/magazin/artikel/luecke-im-lebenslauf)
- [Lücken im Lebenslauf füllen und erklären — workwise](https://www.workwise.io/karriereguide/bewerbung/luecken-im-lebenslauf)

## cv-date-logic

Les logiciels de recrutement calculent les années d'expérience à partir des dates de chaque entrée, et le filtrage se fait sur ce chiffre. Les dates que le système ne peut pas calculer laissent le champ d'expérience vide ou mal compté.

- [Resume Date Format: A Complete How-To Guide — Jobscan](https://www.jobscan.co/blog/resume-dates/)

## cv-first-person

Les conseils allemands sur le Lebenslauf tabulaire présentent les entrées en fragments plutôt qu'en phrases complètes, avec un court profil à la première personne comme seule exception. Les services carrière américains conseillent eux aussi d'éviter les pronoms personnels.

- [Tabellarischer Lebenslauf: Aufbau, Inhalt, Vorlagen — karrierebibel.de](https://karrierebibel.de/tabellarischer-lebenslauf/)
- [Tabellarischer Lebenslauf: Tipps & Muster — e-fellows.net](https://www.e-fellows.net/bewerbung/lebenslauf/tabellarischer-lebenslauf)
- [Resume Tips — Duke University Career Center](https://careerhub.students.duke.edu/resources/resume-tips/)

## cv-personal-details

Le § 1 de l'Allgemeines Gleichbehandlungsgesetz protège les candidatures contre les désavantages fondés notamment sur la religion ou les convictions. La situation familiale et les enfants ne figurent pas parmi ces motifs ; les conseils allemands les décrivent, comme la religion, comme des informations facultatives que la plupart n'indiquent plus, la religion comptant surtout pour les employeurs confessionnels.

- [§ 1 Allgemeines Gleichbehandlungsgesetz — gesetze-im-internet.de](https://www.gesetze-im-internet.de/agg/__1.html)
- [Im Lebenslauf die Konfession angeben? — Indeed Deutschland](https://de.indeed.com/karriere-guide/bewerbung/lebenslauf-konfession)
- [Konfession im Lebenslauf: angeben oder weglassen? — cvlotse.de](https://cvlotse.de/ratgeber/konfession-im-lebenslauf)
- [Familienstand im Lebenslauf angeben oder nicht? — die-bewerbungsschreiber.de](https://www.die-bewerbungsschreiber.de/familienstand-lebenslauf)

## cv-reverse-chronological

L'ordre antichronologique — le poste le plus récent en premier — est devenu la norme des CV allemands, repris du format américain, où les services carrière organisent aussi chaque rubrique ainsi.

- [Antichronologischer Lebenslauf — Indeed Deutschland](https://de.indeed.com/karriere-guide/bewerbung/antichronologischer-lebenslauf)
- [Lebenslauf chronologisch: Absteigend oder aufsteigend? — karrierebibel.de](https://karrierebibel.de/lebenslauf-chronologisch/)
- [Chronologischer oder antichronologischer Lebenslauf — cvlotse.de](https://cvlotse.de/ratgeber/lebenslauf-reihenfolge)
- [Resume Tips — Duke University Career Center](https://careerhub.students.duke.edu/resources/resume-tips/)
