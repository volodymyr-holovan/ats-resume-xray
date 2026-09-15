# Fuentes de investigación

Cada regla de [`src/ats_xray/rules.py`](../src/ats_xray/rules.py) lleva una
clave `source` que apunta a una entrada de este archivo, en lugar de una URL
incrustada en el código: así una cita se corrige o amplía en un solo sitio sin
tocar Python.

La mayoría de las entradas citan recursos de orientación profesional y de
pruebas de ATS en lugar de un estudio revisado por pares, porque ahí es donde
vive realmente este conocimiento: los sistemas de seguimiento de candidatos son
de código cerrado y no están documentados. Lo que se sabe de su comportamiento
al analizar procede de proveedores y asesores que prueban currículums reales
contra ATS reales y publican lo que encuentran, no de la documentación de los
propios proveedores ni de investigación académica. Tómalo como un consenso del
sector, coherente y repetido, no como experimentos controlados. Enlaces
consultados en agosto de 2026 y mantenidos en inglés: los artículos lo son.

## ats-fonts

Las fuentes no estándar o no incrustadas pueden ser mal leídas, sustituidas o descartadas por completo, produciendo texto ilegible o ausente.

- [How ATS Handles Fonts: Complete Guide to Resume Formatting](https://hireflow.net/blog/how-ats-handles-fonts)

## ats-headers-footers

El contenido colocado en el encabezado o el pie de un documento suele ser omitido por completo por los analizadores de ATS, que lo tratan como decoración fuera del cuerpo del documento.

- [How ATS Reads Headers and Footers: Complete Guide to Resume Parsing](https://hireflow.net/blog/how-ats-reads-headers-and-footers)

## ats-text-boxes

Los cuadros de texto sitúan el contenido fuera del flujo normal de párrafos; muchos analizadores ignoran esa capa por completo, así que el texto ahí colocado se pierde en silencio.

- [Why ATS Rejects Resumes with Text Boxes: Complete Guide to ATS-Friendly Formatting](https://hireflow.net/blog/why-ats-rejects-resumes-with-text-boxes)

## ats-tables-columns

Muchos analizadores leen las maquetaciones a varias columnas y las tablas fila a fila cruzando las columnas, mezclando qué valor corresponde a qué etiqueta ("ensalada de palabras").

- [Why ATS Tables and Columns Break Your Resume Parsing](https://www.jobscan.co/blog/resume-tables-columns-ats/)
- [Can ATS Read Tables & Columns? We Tested 8 Systems](https://cvcraft.roynex.com/blog/can-ats-read-tables-columns-formatting-2026)

## ats-graphics

Los currículums exportados como imágenes (habitual en plantillas de herramientas de diseño como Canva) presentan el contenido en una forma que la mayoría de analizadores no puede leer como texto.

- [Can ATS Read Tables, Columns and Canva Resumes?](https://www.mployee.me/blog/can-ats-read-tables-columns-canva-resumes)

## practical-necessity

No es una cita externa: quien no pone datos de contacto en el currículum queda ilocalizable para quien recluta, por bien que un analizador haya extraído lo demás. Esta regla existe por motivos prácticos, no de investigación.

---

Las entradas siguientes son otro tipo de regla. No tratan de lo que el software puede leer, sino de lo que quien selecciona en un país concreto espera que diga un CV, y nunca cuentan para la puntuación sobre 100. Sus fuentes son guías profesionales de cada país, citadas en su idioma. Consultadas en septiembre de 2026.

## cv-volunteering

La orientación alemana coincide en que el voluntariado (Ehrenamt) no sustituye a la experiencia laboral y va en su propia sección, después de la experiencia y la formación. Quien empieza puede incluir voluntariado relevante como experiencia, y un Freiwilliges Soziales Jahr o un Bundesfreiwilligendienst puede contar como práctica. La orientación ucraniana sitúa el voluntariado en su propia sección, salvo que fuera la ocupación principal. Las guías neerlandesas, españolas, francesas, británicas y rusas aceptan el voluntariado en la experiencia si es relevante o hay poca experiencia remunerada, por eso la comprobación solo se aplica a CV alemanes y ucranianos.

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

La orientación alemana considera hueco un periodo de más de dos meses sin empleo ni formación, ve inofensivas de ocho a diez semanas y espera que los huecos a partir de tres o cuatro meses se expliquen en el CV. Tras terminar los estudios, unos seis meses de búsqueda de empleo se consideran normales.

- [Lücken im Lebenslauf: Sinnvoll füllen und erklären — karrierebibel.de](https://karrierebibel.de/luecken-im-lebenslauf/)
- [Lücke im Lebenslauf — StepStone](https://www.stepstone.de/magazin/artikel/luecke-im-lebenslauf)
- [Lücken im Lebenslauf füllen und erklären — workwise](https://www.workwise.io/karriereguide/bewerbung/luecken-im-lebenslauf)

## cv-date-logic

Los sistemas de seguimiento de candidaturas calculan los años de experiencia a partir de las fechas de cada entrada, y se filtra por esa cifra. Las fechas que el sistema no puede calcular dejan el campo de experiencia vacío o mal contado.

- [Resume Date Format: A Complete How-To Guide — Jobscan](https://www.jobscan.co/blog/resume-dates/)

## cv-first-person

La orientación alemana sobre el Lebenslauf tabular presenta las entradas como fragmentos y no como frases completas, con un breve perfil en primera persona como única excepción. Los servicios de carrera de EE. UU. también aconsejan evitar los pronombres personales.

- [Tabellarischer Lebenslauf: Aufbau, Inhalt, Vorlagen — karrierebibel.de](https://karrierebibel.de/tabellarischer-lebenslauf/)
- [Tabellarischer Lebenslauf: Tipps & Muster — e-fellows.net](https://www.e-fellows.net/bewerbung/lebenslauf/tabellarischer-lebenslauf)
- [Resume Tips — Duke University Career Center](https://careerhub.students.duke.edu/resources/resume-tips/)

## cv-personal-details

El § 1 de la Allgemeines Gleichbehandlungsgesetz protege a las candidaturas frente a desventajas por motivos que incluyen la religión o las convicciones. El estado civil y los hijos no figuran entre esos motivos; la orientación alemana los describe, igual que la religión, como datos opcionales que la mayoría ya no incluye, siendo la religión relevante sobre todo para empleadores eclesiásticos.

- [§ 1 Allgemeines Gleichbehandlungsgesetz — gesetze-im-internet.de](https://www.gesetze-im-internet.de/agg/__1.html)
- [Im Lebenslauf die Konfession angeben? — Indeed Deutschland](https://de.indeed.com/karriere-guide/bewerbung/lebenslauf-konfession)
- [Konfession im Lebenslauf: angeben oder weglassen? — cvlotse.de](https://cvlotse.de/ratgeber/konfession-im-lebenslauf)
- [Familienstand im Lebenslauf angeben oder nicht? — die-bewerbungsschreiber.de](https://www.die-bewerbungsschreiber.de/familienstand-lebenslauf)

## cv-reverse-chronological

El orden cronológico inverso —el puesto más reciente primero— se ha convertido en el estándar de los CV alemanes, tomado del formato estadounidense, donde los servicios de carrera también ordenan así cada sección.

- [Antichronologischer Lebenslauf — Indeed Deutschland](https://de.indeed.com/karriere-guide/bewerbung/antichronologischer-lebenslauf)
- [Lebenslauf chronologisch: Absteigend oder aufsteigend? — karrierebibel.de](https://karrierebibel.de/lebenslauf-chronologisch/)
- [Chronologischer oder antichronologischer Lebenslauf — cvlotse.de](https://cvlotse.de/ratgeber/lebenslauf-reihenfolge)
- [Resume Tips — Duke University Career Center](https://careerhub.students.duke.edu/resources/resume-tips/)
