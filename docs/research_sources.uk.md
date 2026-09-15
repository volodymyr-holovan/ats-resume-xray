# Джерела досліджень

Кожне правило у [`src/ats_xray/rules.py`](../src/ats_xray/rules.py) містить
ключ `source`, що вказує на запис у цьому файлі, замість URL, вшитого в код —
тож посилання можна виправити чи доповнити в одному місці, не чіпаючи Python.

Більшість записів нижче посилаються на матеріали кар'єрних консультантів і
тестувальників ATS, а не на рецензовані дослідження, бо саме там це знання й
живе: системи відстеження кандидатів мають закритий код і не задокументовані.
Усе, що відомо про їхню поведінку при розборі, походить від постачальників і
консультантів, які перевіряють справжні резюме на справжніх ATS і публікують
результати — а не з документації самих постачальників чи академічних робіт.
Сприймайте це як послідовний, багато разів повторений галузевий консенсус, а
не як контрольовані експерименти. Дата звернення у серпні 2026 року й
залишено англійською: самі статті англомовні.

## ats-fonts

Нестандартні або невбудовані шрифти можуть бути прочитані неправильно, підмінені чи відкинуті повністю — наслідком є спотворений або відсутній текст.

- [How ATS Handles Fonts: Complete Guide to Resume Formatting](https://hireflow.net/blog/how-ats-handles-fonts)

## ats-headers-footers

Вміст, розміщений у колонтитулах документа, ATS-парсери зазвичай пропускають повністю, вважаючи його службовим оформленням поза тілом документа.

- [How ATS Reads Headers and Footers: Complete Guide to Resume Parsing](https://hireflow.net/blog/how-ats-reads-headers-and-footers)

## ats-text-boxes

Текстові поля розміщують вміст поза звичайним потоком абзаців; багато парсерів ігнорують цей шар цілком, тож розміщений там текст мовчки зникає.

- [Why ATS Rejects Resumes with Text Boxes: Complete Guide to ATS-Friendly Formatting](https://hireflow.net/blog/why-ats-rejects-resumes-with-text-boxes)

## ats-tables-columns

Багатоколонкову верстку й таблиці багато парсерів читають рядок за рядком упоперек колонок, через що плутається, яке значення до якої назви належить («словесний салат»).

- [Why ATS Tables and Columns Break Your Resume Parsing](https://www.jobscan.co/blog/resume-tables-columns-ats/)
- [Can ATS Read Tables & Columns? We Tested 8 Systems](https://cvcraft.roynex.com/blog/can-ats-read-tables-columns-formatting-2026)

## ats-graphics

Резюме, збережені як зображення (типово для шаблонів дизайн-редакторів на кшталт Canva), подають вміст у формі, яку більшість парсерів взагалі не читає як текст.

- [Can ATS Read Tables, Columns and Canva Resumes?](https://www.mployee.me/blog/can-ats-read-tables-columns-canva-resumes)

## practical-necessity

Не зовнішнє джерело: той, хто не вказав контактів у резюме, лишається недосяжним для рекрутера незалежно від того, що парсер видобув правильно. Це правило існує з практичних, а не дослідницьких міркувань.

---

Записи нижче — правила іншого роду. Вони не про те, що може прочитати програма, а про те, чого рекрутери в певній країні очікують від резюме, і ніколи не впливають на оцінку зі 100. Їхні джерела — національні кар'єрні поради, наведені мовою країни, до якої належить конвенція. Дата звернення — вересень 2026 року.

## cv-volunteering

Німецькі поради одностайні: волонтерство (Ehrenamt) не замінює досвіду роботи й має стояти в окремому розділі після досвіду й освіти. Початківці можуть вказувати релевантне волонтерство як досвід, а Freiwilliges Soziales Jahr чи Bundesfreiwilligendienst може зараховуватися як практика. Українські поради виносять волонтерство в окремий розділ, якщо воно не було основною зайнятістю. Нідерландські, іспанські, французькі, британські й російські поради допускають волонтерство в досвіді, якщо воно релевантне або оплачуваного досвіду мало, — тому перевірка стосується лише німецьких і українських резюме.

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

Німецькі поради вважають перервою період понад два місяці без роботи чи навчання, вісім-десять тижнів — нешкідливими, а перерви від трьох-чотирьох місяців очікують пояснювати в резюме. Після закінчення навчання близько шести місяців пошуку роботи вважаються нормою.

- [Lücken im Lebenslauf: Sinnvoll füllen und erklären — karrierebibel.de](https://karrierebibel.de/luecken-im-lebenslauf/)
- [Lücke im Lebenslauf — StepStone](https://www.stepstone.de/magazin/artikel/luecke-im-lebenslauf)
- [Lücken im Lebenslauf füllen und erklären — workwise](https://www.workwise.io/karriereguide/bewerbung/luecken-im-lebenslauf)

## cv-date-logic

Системи відбору кандидатів рахують роки досвіду за датами кожного запису, а рекрутери фільтрують за цим числом. Дати, яких система не може обчислити, лишають поле досвіду порожнім або неправильно порахованим.

- [Resume Date Format: A Complete How-To Guide — Jobscan](https://www.jobscan.co/blog/resume-dates/)

## cv-first-person

Німецькі поради щодо табличного Lebenslauf подають записи короткими фразами, а не повними реченнями, з коротким профілем від першої особи як єдиним винятком. Американські кар'єрні центри так само радять уникати особових займенників.

- [Tabellarischer Lebenslauf: Aufbau, Inhalt, Vorlagen — karrierebibel.de](https://karrierebibel.de/tabellarischer-lebenslauf/)
- [Tabellarischer Lebenslauf: Tipps & Muster — e-fellows.net](https://www.e-fellows.net/bewerbung/lebenslauf/tabellarischer-lebenslauf)
- [Resume Tips — Duke University Career Center](https://careerhub.students.duke.edu/resources/resume-tips/)

## cv-personal-details

§ 1 Allgemeines Gleichbehandlungsgesetz захищає кандидатів від утисків, зокрема через релігію чи світогляд. Сімейний стан і діти до переліку ознак не входять; німецькі поради описують їх, як і віросповідання, як необов'язкові дані, які більшість уже не вказує, — а віросповідання важливе переважно для церковних роботодавців.

- [§ 1 Allgemeines Gleichbehandlungsgesetz — gesetze-im-internet.de](https://www.gesetze-im-internet.de/agg/__1.html)
- [Im Lebenslauf die Konfession angeben? — Indeed Deutschland](https://de.indeed.com/karriere-guide/bewerbung/lebenslauf-konfession)
- [Konfession im Lebenslauf: angeben oder weglassen? — cvlotse.de](https://cvlotse.de/ratgeber/konfession-im-lebenslauf)
- [Familienstand im Lebenslauf angeben oder nicht? — die-bewerbungsschreiber.de](https://www.die-bewerbungsschreiber.de/familienstand-lebenslauf)

## cv-reverse-chronological

Зворотний хронологічний порядок — остання посада першою — став стандартом німецького резюме, запозиченим з американського формату, де кар'єрні центри так само впорядковують кожен розділ.

- [Antichronologischer Lebenslauf — Indeed Deutschland](https://de.indeed.com/karriere-guide/bewerbung/antichronologischer-lebenslauf)
- [Lebenslauf chronologisch: Absteigend oder aufsteigend? — karrierebibel.de](https://karrierebibel.de/lebenslauf-chronologisch/)
- [Chronologischer oder antichronologischer Lebenslauf — cvlotse.de](https://cvlotse.de/ratgeber/lebenslauf-reihenfolge)
- [Resume Tips — Duke University Career Center](https://careerhub.students.duke.edu/resources/resume-tips/)
