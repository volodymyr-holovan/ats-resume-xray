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
