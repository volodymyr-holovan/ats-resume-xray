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
