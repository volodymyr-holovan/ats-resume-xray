# Источники исследований

Каждое правило в [`src/ats_xray/rules.py`](../src/ats_xray/rules.py) содержит
ключ `source`, указывающий на запись в этом файле, вместо URL, вшитого в код —
поэтому ссылку можно исправить или дополнить в одном месте, не трогая Python.

Большинство записей ниже ссылаются на материалы карьерных консультантов и
тестировщиков ATS, а не на рецензируемые исследования, потому что именно там
это знание и живёт: системы отслеживания кандидатов имеют закрытый код и не
задокументированы. Всё, что известно об их поведении при разборе, исходит от
поставщиков и консультантов, которые проверяют настоящие резюме на настоящих
ATS и публикуют результаты — а не из документации самих поставщиков или
академических работ. Воспринимайте это как последовательный, многократно
повторённый отраслевой консенсус, а не как контролируемые эксперименты.
Дата обращения в августе 2026 года и оставлены на английском: сами статьи
англоязычные.

## ats-fonts

Нестандартные или невстроенные шрифты могут быть прочитаны неверно, подменены или отброшены полностью — следствием будет искажённый или отсутствующий текст.

- [How ATS Handles Fonts: Complete Guide to Resume Formatting](https://hireflow.net/blog/how-ats-handles-fonts)

## ats-headers-footers

Содержимое, размещённое в колонтитулах документа, ATS-парсеры обычно пропускают полностью, считая его служебным оформлением вне тела документа.

- [How ATS Reads Headers and Footers: Complete Guide to Resume Parsing](https://hireflow.net/blog/how-ats-reads-headers-and-footers)

## ats-text-boxes

Текстовые поля размещают содержимое вне обычного потока абзацев; многие парсеры игнорируют этот слой целиком, поэтому размещённый там текст молча исчезает.

- [Why ATS Rejects Resumes with Text Boxes: Complete Guide to ATS-Friendly Formatting](https://hireflow.net/blog/why-ats-rejects-resumes-with-text-boxes)

## ats-tables-columns

Многоколоночную вёрстку и таблицы многие парсеры читают строка за строкой поперёк колонок, из-за чего путается, какое значение к какому названию относится («словесный салат»).

- [Why ATS Tables and Columns Break Your Resume Parsing](https://www.jobscan.co/blog/resume-tables-columns-ats/)
- [Can ATS Read Tables & Columns? We Tested 8 Systems](https://cvcraft.roynex.com/blog/can-ats-read-tables-columns-formatting-2026)

## ats-graphics

Резюме, сохранённые как изображения (типично для шаблонов дизайн-редакторов вроде Canva), подают содержимое в форме, которую большинство парсеров вообще не читает как текст.

- [Can ATS Read Tables, Columns and Canva Resumes?](https://www.mployee.me/blog/can-ats-read-tables-columns-canva-resumes)

## practical-necessity

Не внешний источник: тот, кто не указал контактов в резюме, остаётся недоступным для рекрутера независимо от того, что парсер извлёк правильно. Это правило существует из практических, а не исследовательских соображений.

---

Записи ниже — правила другого рода. Они не о том, что может прочитать программа, а о том, чего рекрутеры в определённой стране ждут от резюме, и никогда не влияют на оценку из 100. Их источники — национальные карьерные советы, приведённые на языке страны, к которой относится конвенция. Дата обращения — сентябрь 2026 года.

## cv-volunteering

Немецкие советы единодушны: волонтерство (Ehrenamt) не заменяет опыта работы и должно стоять в отдельном разделе после опыта и образования. Начинающие могут указывать релевантное волонтерство как опыт, а Freiwilliges Soziales Jahr или Bundesfreiwilligendienst может засчитываться как практика. Украинские советы выносят волонтерство в отдельный раздел, если оно не было основной занятостью. Нидерландские, испанские, французские, британские и русские советы допускают волонтерство в опыте, если оно релевантно или оплачиваемого опыта мало, — поэтому проверка касается только немецких и украинских резюме.

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

Немецкие советы считают перерывом период свыше двух месяцев без работы или обучения, восемь-десять недель — безвредными, а перерывы от трёх-четырёх месяцев ожидают объяснять в резюме. После окончания обучения около шести месяцев поиска работы считаются нормой.

- [Lücken im Lebenslauf: Sinnvoll füllen und erklären — karrierebibel.de](https://karrierebibel.de/luecken-im-lebenslauf/)
- [Lücke im Lebenslauf — StepStone](https://www.stepstone.de/magazin/artikel/luecke-im-lebenslauf)
- [Lücken im Lebenslauf füllen und erklären — workwise](https://www.workwise.io/karriereguide/bewerbung/luecken-im-lebenslauf)

## cv-date-logic

Системы отбора кандидатов считают годы опыта по датам каждой записи, а рекрутеры фильтруют по этому числу. Даты, которые система не может вычислить, оставляют поле опыта пустым или неверно посчитанным.

- [Resume Date Format: A Complete How-To Guide — Jobscan](https://www.jobscan.co/blog/resume-dates/)

## cv-first-person

Немецкие советы по табличному Lebenslauf подают записи короткими фразами, а не полными предложениями, с коротким профилем от первого лица как единственным исключением. Американские карьерные центры так же советуют избегать личных местоимений.

- [Tabellarischer Lebenslauf: Aufbau, Inhalt, Vorlagen — karrierebibel.de](https://karrierebibel.de/tabellarischer-lebenslauf/)
- [Tabellarischer Lebenslauf: Tipps & Muster — e-fellows.net](https://www.e-fellows.net/bewerbung/lebenslauf/tabellarischer-lebenslauf)
- [Resume Tips — Duke University Career Center](https://careerhub.students.duke.edu/resources/resume-tips/)

## cv-personal-details

§ 1 Allgemeines Gleichbehandlungsgesetz защищает кандидатов от ущемления, в том числе из-за религии или мировоззрения. Семейное положение и дети в перечень признаков не входят; немецкие советы описывают их, как и вероисповедание, как необязательные данные, которые большинство уже не указывает, — а вероисповедание важно преимущественно для церковных работодателей.

- [§ 1 Allgemeines Gleichbehandlungsgesetz — gesetze-im-internet.de](https://www.gesetze-im-internet.de/agg/__1.html)
- [Im Lebenslauf die Konfession angeben? — Indeed Deutschland](https://de.indeed.com/karriere-guide/bewerbung/lebenslauf-konfession)
- [Konfession im Lebenslauf: angeben oder weglassen? — cvlotse.de](https://cvlotse.de/ratgeber/konfession-im-lebenslauf)
- [Familienstand im Lebenslauf angeben oder nicht? — die-bewerbungsschreiber.de](https://www.die-bewerbungsschreiber.de/familienstand-lebenslauf)

## cv-reverse-chronological

Обратный хронологический порядок — последняя должность первой — стал стандартом немецкого резюме, заимствованным из американского формата, где карьерные центры так же упорядочивают каждый раздел.

- [Antichronologischer Lebenslauf — Indeed Deutschland](https://de.indeed.com/karriere-guide/bewerbung/antichronologischer-lebenslauf)
- [Lebenslauf chronologisch: Absteigend oder aufsteigend? — karrierebibel.de](https://karrierebibel.de/lebenslauf-chronologisch/)
- [Chronologischer oder antichronologischer Lebenslauf — cvlotse.de](https://cvlotse.de/ratgeber/lebenslauf-reihenfolge)
- [Resume Tips — Duke University Career Center](https://careerhub.students.duke.edu/resources/resume-tips/)
