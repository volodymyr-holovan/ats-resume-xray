"""Interface translations.

Keyed by string id, then language. ``t()`` falls back to English for any
id a language has not been given yet, so adding a key does not have to mean
translating it into everything at once, and a missing translation degrades
to readable English rather than a KeyError in front of a user.

This covers the interface and the rule descriptions -- the text a reader
sees. Rule *ids*, source keys and the research citations stay in English:
they are identifiers and references, not prose, and translating them would
break the link to the sources they point at.
"""

UI_LANGUAGES: dict[str, str] = {
    "en": "English",
    "de": "Deutsch",
    "uk": "Українська",
    "ru": "Русский",
    "es": "Español",
    "nl": "Nederlands",
    "fr": "Français",
}

DEFAULT_LANGUAGE = "en"

TRANSLATIONS: dict[str, dict[str, str]] = {
    "language_label": {
        "en": "Language",
        "de": "Sprache",
        "uk": "Мова",
        "ru": "Язык",
        "es": "Idioma",
        "nl": "Taal",
        "fr": "Langue",
    },
    "intro": {
        "en": (
            "Upload a resume (PDF or DOCX) to see what a resume-parsing pipeline actually "
            "extracts from it — not a black-box score, an actual diff. Findings are "
            "documented, common failure patterns ([sources]({sources_url})), not a "
            "guarantee of how any specific employer's system will behave."
        ),
        "de": (
            "Laden Sie einen Lebenslauf (PDF oder DOCX) hoch und sehen Sie, was eine "
            "Parsing-Pipeline tatsächlich daraus liest — kein Blackbox-Score, sondern ein "
            "echter Vergleich. Die Befunde sind dokumentierte, häufige Fehlermuster "
            "([Quellen]({sources_url})), keine Garantie für das Verhalten eines bestimmten "
            "Arbeitgebersystems."
        ),
        "uk": (
            "Завантажте резюме (PDF або DOCX), щоб побачити, що з нього насправді видобуває "
            "програма розбору — не таємничий бал, а реальне порівняння. Знахідки — це "
            "задокументовані типові збої ([джерела]({sources_url})), а не гарантія поведінки "
            "системи конкретного роботодавця."
        ),
        "ru": (
            "Загрузите резюме (PDF или DOCX), чтобы увидеть, что из него на самом деле "
            "извлекает программа разбора — не загадочный балл, а реальное сравнение. "
            "Находки — это задокументированные типичные сбои ([источники]({sources_url})), "
            "а не гарантия поведения системы конкретного работодателя."
        ),
        "es": (
            "Sube un currículum (PDF o DOCX) para ver qué extrae realmente un sistema de "
            "análisis — no una puntuación opaca, sino una comparación real. Los hallazgos "
            "son fallos documentados y frecuentes ([fuentes]({sources_url})), no una "
            "garantía del comportamiento del sistema de un empleador concreto."
        ),
        "nl": (
            "Upload een cv (PDF of DOCX) om te zien wat een parser er werkelijk uit haalt — "
            "geen ondoorzichtige score, maar een echte vergelijking. Bevindingen zijn "
            "gedocumenteerde, veelvoorkomende fouten ([bronnen]({sources_url})), geen "
            "garantie voor hoe het systeem van een specifieke werkgever zich gedraagt."
        ),
        "fr": (
            "Téléversez un CV (PDF ou DOCX) pour voir ce qu'un moteur d'analyse en extrait "
            "réellement — pas un score opaque, mais une vraie comparaison. Les constats sont "
            "des défauts documentés et courants ([sources]({sources_url})), pas une garantie "
            "du comportement du système d'un employeur donné."
        ),
    },
    "privacy": {
        "en": (
            "🔒 Your file is written to a temporary location only for the few seconds needed "
            "to process it, then deleted immediately. Nothing is stored, logged, or sent "
            "anywhere else."
        ),
        "de": (
            "🔒 Ihre Datei wird nur für die wenigen Sekunden der Verarbeitung temporär "
            "gespeichert und danach sofort gelöscht. Nichts wird aufbewahrt, protokolliert "
            "oder weitergegeben."
        ),
        "uk": (
            "🔒 Ваш файл записується у тимчасове місце лише на ті кілька секунд, що потрібні "
            "для обробки, і одразу видаляється. Нічого не зберігається, не журналюється і "
            "нікуди не надсилається."
        ),
        "ru": (
            "🔒 Ваш файл записывается во временное место только на те несколько секунд, что "
            "нужны для обработки, и сразу удаляется. Ничего не сохраняется, не журналируется "
            "и никуда не отправляется."
        ),
        "es": (
            "🔒 Tu archivo se guarda temporalmente solo los segundos necesarios para "
            "procesarlo y luego se elimina de inmediato. No se almacena, registra ni envía "
            "a ningún sitio."
        ),
        "nl": (
            "🔒 Je bestand wordt alleen tijdelijk opgeslagen voor de paar seconden die de "
            "verwerking kost en daarna meteen verwijderd. Er wordt niets bewaard, gelogd of "
            "verstuurd."
        ),
        "fr": (
            "🔒 Votre fichier n'est stocké temporairement que le temps du traitement, puis "
            "supprimé immédiatement. Rien n'est conservé, journalisé ni transmis."
        ),
    },
    "upload_label": {
        "en": "Upload your resume",
        "de": "Lebenslauf hochladen",
        "uk": "Завантажте резюме",
        "ru": "Загрузите резюме",
        "es": "Sube tu currículum",
        "nl": "Upload je cv",
        "fr": "Téléversez votre CV",
    },
    "analyzing": {
        "en": "Analyzing…",
        "de": "Wird analysiert…",
        "uk": "Аналізую…",
        "ru": "Анализирую…",
        "es": "Analizando…",
        "nl": "Bezig met analyseren…",
        "fr": "Analyse en cours…",
    },
    "score_heading": {
        "en": "Parse readiness",
        "de": "Lesbarkeit für Parser",
        "uk": "Придатність до розбору",
        "ru": "Пригодность к разбору",
        "es": "Legibilidad para el análisis",
        "nl": "Leesbaarheid voor parsers",
        "fr": "Lisibilité pour l'analyse",
    },
    "score_caption": {
        "en": (
            "How much of this resume survives an automated read. This is **not** a "
            "keyword-match score against a job posting: that needs the posting and the "
            "employer's weighting, neither of which this tool has. Every number below is "
            "derived from evidence in your file, shown in full."
        ),
        "de": (
            "Wie viel von diesem Lebenslauf eine maschinelle Lesung übersteht. Das ist "
            "**kein** Keyword-Abgleich mit einer Stellenanzeige: dafür bräuchte es die "
            "Anzeige und die Gewichtung des Arbeitgebers. Jede Zahl unten stammt aus "
            "Belegen in Ihrer Datei und wird vollständig gezeigt."
        ),
        "uk": (
            "Скільки з цього резюме переживає машинне читання. Це **не** оцінка збігу "
            "ключових слів із вакансією: для неї потрібні сам опис вакансії та ваги "
            "роботодавця, а їх інструмент не має. Кожне число нижче виведене з доказів "
            "у вашому файлі й показане повністю."
        ),
        "ru": (
            "Сколько из этого резюме переживает машинное чтение. Это **не** оценка "
            "совпадения ключевых слов с вакансией: для неё нужны сам текст вакансии и веса "
            "работодателя, которых у инструмента нет. Каждое число ниже выведено из "
            "доказательств в вашем файле и показано полностью."
        ),
        "es": (
            "Cuánto de este currículum sobrevive a una lectura automática. Esto **no** es "
            "una puntuación de coincidencia de palabras clave con una oferta: eso requiere "
            "la oferta y la ponderación del empleador, que esta herramienta no tiene. Cada "
            "número procede de evidencias de tu archivo y se muestra por completo."
        ),
        "nl": (
            "Hoeveel van dit cv een geautomatiseerde lezing overleeft. Dit is **geen** "
            "score voor overeenkomst met een vacaturetekst: daarvoor zijn de vacature en de "
            "weging van de werkgever nodig, die deze tool niet heeft. Elk getal hieronder "
            "komt uit bewijs in je bestand en wordt volledig getoond."
        ),
        "fr": (
            "Quelle part de ce CV survit à une lecture automatisée. Ce n'est **pas** un "
            "score de correspondance avec une offre : cela exigerait l'offre et la "
            "pondération de l'employeur, dont cet outil ne dispose pas. Chaque chiffre "
            "ci-dessous provient de preuves dans votre fichier et est affiché en entier."
        ),
    },
    "findings_heading": {
        "en": "Findings",
        "de": "Befunde",
        "uk": "Знахідки",
        "ru": "Находки",
        "es": "Hallazgos",
        "nl": "Bevindingen",
        "fr": "Constats",
    },
    "no_findings": {
        "en": "No documented parsing risks triggered.",
        "de": "Keine dokumentierten Parsing-Risiken ausgelöst.",
        "uk": "Жодного задокументованого ризику розбору не виявлено.",
        "ru": "Ни одного задокументированного риска разбора не выявлено.",
        "es": "No se ha activado ningún riesgo de análisis documentado.",
        "nl": "Geen gedocumenteerde parsing-risico's aangetroffen.",
        "fr": "Aucun risque d'analyse documenté déclenché.",
    },
    "evidence": {
        "en": "Evidence",
        "de": "Beleg",
        "uk": "Доказ",
        "ru": "Доказательство",
        "es": "Evidencia",
        "nl": "Bewijs",
        "fr": "Preuve",
    },
    "source": {
        "en": "Source",
        "de": "Quelle",
        "uk": "Джерело",
        "ru": "Источник",
        "es": "Fuente",
        "nl": "Bron",
        "fr": "Source",
    },
    "pages_heading": {
        "en": "Where the problems are",
        "de": "Wo die Probleme liegen",
        "uk": "Де саме проблеми",
        "ru": "Где именно проблемы",
        "es": "Dónde están los problemas",
        "nl": "Waar de problemen zitten",
        "fr": "Où sont les problèmes",
    },
    "legend": {
        "en": "Boxes mark the exact area each finding refers to.",
        "de": "Die Rahmen markieren den genauen Bereich jedes Befunds.",
        "uk": "Рамки позначають точну ділянку, якої стосується кожна знахідка.",
        "ru": "Рамки отмечают точный участок, к которому относится каждая находка.",
        "es": "Los recuadros marcan el área exacta a la que se refiere cada hallazgo.",
        "nl": "De kaders markeren precies het gebied waar elke bevinding op slaat.",
        "fr": "Les cadres marquent la zone exacte visée par chaque constat.",
    },
    "docx_layout_note": {
        "en": (
            "This DOCX was laid out with LibreOffice to produce pages; your own word "
            "processor may break lines slightly differently."
        ),
        "de": (
            "Dieses DOCX wurde mit LibreOffice gesetzt, um Seiten zu erzeugen; Ihr eigenes "
            "Textprogramm bricht Zeilen möglicherweise etwas anders um."
        ),
        "uk": (
            "Цей DOCX було зверстано через LibreOffice, щоб отримати сторінки; ваш власний "
            "текстовий редактор може переносити рядки трохи інакше."
        ),
        "ru": (
            "Этот DOCX был свёрстан через LibreOffice, чтобы получить страницы; ваш "
            "текстовый редактор может переносить строки немного иначе."
        ),
        "es": (
            "Este DOCX se maquetó con LibreOffice para generar páginas; tu procesador de "
            "textos puede cortar las líneas de forma algo distinta."
        ),
        "nl": (
            "Dit DOCX is met LibreOffice opgemaakt om pagina's te maken; je eigen "
            "tekstverwerker breekt regels mogelijk iets anders af."
        ),
        "fr": (
            "Ce DOCX a été mis en page avec LibreOffice pour produire des pages ; votre "
            "traitement de texte peut couper les lignes un peu différemment."
        ),
    },
    "docx_no_libreoffice": {
        "en": (
            "Page previews for DOCX need LibreOffice, which isn't available here. A DOCX "
            "stores content but no page positions, so it has to be laid out before anything "
            "can be drawn on it. The findings above still apply."
        ),
        "de": (
            "Seitenvorschauen für DOCX brauchen LibreOffice, das hier nicht verfügbar ist. "
            "Ein DOCX speichert Inhalt, aber keine Seitenpositionen, muss also erst gesetzt "
            "werden. Die Befunde oben gelten weiterhin."
        ),
        "uk": (
            "Перегляд сторінок для DOCX потребує LibreOffice, якого тут немає. DOCX зберігає "
            "вміст, але не позиції на сторінці, тож його спершу треба зверстати. Знахідки "
            "вище лишаються чинними."
        ),
        "ru": (
            "Просмотр страниц для DOCX требует LibreOffice, которого здесь нет. DOCX хранит "
            "содержимое, но не позиции на странице, поэтому его сначала нужно сверстать. "
            "Находки выше остаются в силе."
        ),
        "es": (
            "La vista previa de páginas para DOCX necesita LibreOffice, que no está "
            "disponible aquí. Un DOCX guarda contenido pero no posiciones de página, así que "
            "hay que maquetarlo primero. Los hallazgos anteriores siguen siendo válidos."
        ),
        "nl": (
            "Paginavoorbeelden voor DOCX vereisen LibreOffice, dat hier niet beschikbaar is. "
            "Een DOCX bevat inhoud maar geen paginaposities, dus het moet eerst worden "
            "opgemaakt. De bevindingen hierboven blijven gelden."
        ),
        "fr": (
            "L'aperçu des pages pour DOCX nécessite LibreOffice, indisponible ici. Un DOCX "
            "contient du contenu mais aucune position de page : il faut d'abord le mettre en "
            "page. Les constats ci-dessus restent valables."
        ),
    },
    "page": {
        "en": "Page",
        "de": "Seite",
        "uk": "Сторінка",
        "ru": "Страница",
        "es": "Página",
        "nl": "Pagina",
        "fr": "Page",
    },
    "nothing_flagged": {
        "en": "nothing flagged",
        "de": "nichts markiert",
        "uk": "нічого не позначено",
        "ru": "ничего не отмечено",
        "es": "nada señalado",
        "nl": "niets gemarkeerd",
        "fr": "rien de signalé",
    },
    "naive_expander": {
        "en": "Naive extraction — what a basic, layout-blind parser sees",
        "de": "Naive Extraktion — was ein einfacher, layoutblinder Parser sieht",
        "uk": "Наївний розбір — що бачить простий парсер, сліпий до верстки",
        "ru": "Наивный разбор — что видит простой парсер, слепой к вёрстке",
        "es": "Extracción ingenua — lo que ve un analizador ciego al diseño",
        "nl": "Naïeve extractie — wat een simpele, opmaak-blinde parser ziet",
        "fr": "Extraction naïve — ce que voit un analyseur aveugle à la mise en page",
    },
    "aware_expander": {
        "en": "Layout-aware extraction — columns and tables handled",
        "de": "Layoutbewusste Extraktion — Spalten und Tabellen berücksichtigt",
        "uk": "Розбір із урахуванням верстки — колонки й таблиці оброблено",
        "ru": "Разбор с учётом вёрстки — колонки и таблицы обработаны",
        "es": "Extracción consciente del diseño — columnas y tablas tratadas",
        "nl": "Opmaak-bewuste extractie — kolommen en tabellen verwerkt",
        "fr": "Extraction consciente de la mise en page — colonnes et tableaux traités",
    },
    "error_unreadable": {
        "en": (
            "Couldn't read this file — it may be corrupted, password-protected, or not a "
            "valid PDF/DOCX. Try re-exporting it and uploading again."
        ),
        "de": (
            "Diese Datei konnte nicht gelesen werden — sie ist möglicherweise beschädigt, "
            "passwortgeschützt oder kein gültiges PDF/DOCX. Exportieren Sie sie neu und "
            "laden Sie sie erneut hoch."
        ),
        "uk": (
            "Не вдалося прочитати цей файл — можливо, він пошкоджений, захищений паролем або "
            "не є коректним PDF/DOCX. Спробуйте експортувати його заново й завантажити ще раз."
        ),
        "ru": (
            "Не удалось прочитать этот файл — возможно, он повреждён, защищён паролем или не "
            "является корректным PDF/DOCX. Попробуйте экспортировать его заново и загрузить "
            "ещё раз."
        ),
        "es": (
            "No se ha podido leer este archivo — puede estar dañado, protegido con contraseña "
            "o no ser un PDF/DOCX válido. Prueba a exportarlo de nuevo y subirlo otra vez."
        ),
        "nl": (
            "Dit bestand kon niet worden gelezen — het is mogelijk beschadigd, met een "
            "wachtwoord beveiligd of geen geldig PDF/DOCX. Exporteer het opnieuw en probeer "
            "het nog eens."
        ),
        "fr": (
            "Impossible de lire ce fichier — il est peut-être corrompu, protégé par mot de "
            "passe, ou n'est pas un PDF/DOCX valide. Réexportez-le et réessayez."
        ),
    },
    "component_contact": {
        "en": "Contact reachability",
        "de": "Erreichbarkeit",
        "uk": "Доступність контактів",
        "ru": "Доступность контактов",
        "es": "Localizabilidad de contacto",
        "nl": "Bereikbaarheid",
        "fr": "Joignabilité",
    },
    "component_sections": {
        "en": "Section survival",
        "de": "Erhalt der Abschnitte",
        "uk": "Виживання розділів",
        "ru": "Выживание разделов",
        "es": "Supervivencia de secciones",
        "nl": "Behoud van secties",
        "fr": "Survie des sections",
    },
    "component_structure": {
        "en": "Structural integrity",
        "de": "Strukturelle Integrität",
        "uk": "Структурна цілісність",
        "ru": "Структурная целостность",
        "es": "Integridad estructural",
        "nl": "Structurele integriteit",
        "fr": "Intégrité structurelle",
    },
    "rating_clean": {
        "en": "Parses cleanly",
        "de": "Wird sauber gelesen",
        "uk": "Читається чисто",
        "ru": "Читается чисто",
        "es": "Se analiza sin problemas",
        "nl": "Wordt schoon gelezen",
        "fr": "Analyse sans souci",
    },
    "rating_mostly": {
        "en": "Mostly parses, some risk",
        "de": "Weitgehend lesbar, mit Risiko",
        "uk": "Здебільшого читається, є ризик",
        "ru": "В основном читается, есть риск",
        "es": "Se analiza en su mayor parte, con riesgo",
        "nl": "Grotendeels leesbaar, enig risico",
        "fr": "Analyse en grande partie, avec risque",
    },
    "rating_significant": {
        "en": "Significant parsing risk",
        "de": "Erhebliches Parsing-Risiko",
        "uk": "Значний ризик при розборі",
        "ru": "Значительный риск при разборе",
        "es": "Riesgo de análisis considerable",
        "nl": "Aanzienlijk parsing-risico",
        "fr": "Risque d'analyse important",
    },
    "rating_poor": {
        "en": "Likely to parse badly",
        "de": "Wird vermutlich schlecht gelesen",
        "uk": "Найімовірніше, прочитається погано",
        "ru": "Скорее всего, прочитается плохо",
        "es": "Es probable que se analice mal",
        "nl": "Wordt waarschijnlijk slecht gelezen",
        "fr": "Sera probablement mal analysé",
    },
    "detail_contact_both": {
        "en": "Email and phone both recovered from a plain, layout-blind read",
        "de": "E-Mail und Telefon wurden auch bei einfachem, layoutblindem Lesen gefunden",
        "uk": "І пошту, і телефон вдалося дістати простим читанням, сліпим до верстки",
        "ru": "И почту, и телефон удалось получить простым чтением, слепым к вёрстке",
        "es": "Se recuperan correo y teléfono en una lectura simple, ciega al diseño",
        "nl": "E-mail en telefoon beide gevonden bij een eenvoudige, opmaak-blinde lezing",
        "fr": "E-mail et téléphone retrouvés par une lecture simple, aveugle à la mise en page",
    },
    "detail_contact_one": {
        "en": "Found {found}, but no {missing}",
        "de": "{found} gefunden, aber kein {missing}",
        "uk": "Знайдено {found}, але немає {missing}",
        "ru": "Найдено {found}, но нет {missing}",
        "es": "Se encontró {found}, pero no {missing}",
        "nl": "{found} gevonden, maar geen {missing}",
        "fr": "{found} trouvé, mais pas de {missing}",
    },
    "detail_contact_none": {
        "en": "Neither email nor phone could be recovered",
        "de": "Weder E-Mail noch Telefon konnten gefunden werden",
        "uk": "Не вдалося дістати ні пошту, ні телефон",
        "ru": "Не удалось получить ни почту, ни телефон",
        "es": "No se ha podido recuperar ni correo ni teléfono",
        "nl": "Noch e-mail noch telefoon kon worden gevonden",
        "fr": "Ni e-mail ni téléphone n'ont pu être retrouvés",
    },
    "detail_sections_absent": {
        "en": "No standard section headings found at all, so there is nothing to compare",
        "de": "Keine Standard-Abschnittsüberschriften gefunden, es gibt nichts zu vergleichen",
        "uk": "Стандартних заголовків розділів не знайдено взагалі, тож порівнювати нема що",
        "ru": "Стандартных заголовков разделов не найдено вовсе, поэтому сравнивать нечего",
        "es": "No se han encontrado encabezados de sección estándar, no hay nada que comparar",
        "nl": "Geen standaard sectiekoppen gevonden, dus er valt niets te vergelijken",
        "fr": "Aucun intitulé de section standard trouvé, il n'y a rien à comparer",
    },
    "detail_sections_all": {
        "en": "{survived} of {total} sections survive a layout-blind read",
        "de": "{survived} von {total} Abschnitten überstehen ein layoutblindes Lesen",
        "uk": "{survived} з {total} розділів переживають читання, сліпе до верстки",
        "ru": "{survived} из {total} разделов переживают чтение, слепое к вёрстке",
        "es": "{survived} de {total} secciones sobreviven a una lectura ciega al diseño",
        "nl": "{survived} van {total} secties overleven een opmaak-blinde lezing",
        "fr": "{survived} sections sur {total} survivent à une lecture aveugle à la mise en page",
    },
    "detail_sections_lost": {
        "en": "{survived} of {total} sections survive a layout-blind read (lost: {lost})",
        "de": "{survived} von {total} Abschnitten überstehen ein layoutblindes Lesen (verloren: {lost})",
        "uk": "{survived} з {total} розділів переживають читання, сліпе до верстки (втрачено: {lost})",
        "ru": "{survived} из {total} разделов переживают чтение, слепое к вёрстке (потеряно: {lost})",
        "es": "{survived} de {total} secciones sobreviven a una lectura ciega al diseño (perdidas: {lost})",
        "nl": "{survived} van {total} secties overleven een opmaak-blinde lezing (verloren: {lost})",
        "fr": "{survived} sections sur {total} survivent à une lecture aveugle (perdues : {lost})",
    },
    "detail_structure_clean": {
        "en": "No structural parsing risks detected",
        "de": "Keine strukturellen Parsing-Risiken erkannt",
        "uk": "Структурних ризиків розбору не виявлено",
        "ru": "Структурных рисков разбора не выявлено",
        "es": "No se han detectado riesgos estructurales de análisis",
        "nl": "Geen structurele parsing-risico's gevonden",
        "fr": "Aucun risque structurel d'analyse détecté",
    },
    "detail_structure_deductions": {
        "en": "Deductions: {deductions}",
        "de": "Abzüge: {deductions}",
        "uk": "Віднято: {deductions}",
        "ru": "Вычтено: {deductions}",
        "es": "Descuentos: {deductions}",
        "nl": "Aftrek: {deductions}",
        "fr": "Déductions : {deductions}",
    },
    "cap_reason_one": {
        "en": "Capped at {cap}: 1 high-severity finding puts content at risk of being lost (before the cap: {uncapped})",
        "de": "Auf {cap} begrenzt: 1 schwerwiegender Befund gefährdet Inhalte (vor der Begrenzung: {uncapped})",
        "uk": "Обмежено до {cap}: 1 критична знахідка ставить вміст під загрозу втрати (до обмеження: {uncapped})",
        "ru": "Ограничено до {cap}: 1 критическая находка ставит содержимое под угрозу потери (до ограничения: {uncapped})",
        "es": "Limitado a {cap}: 1 hallazgo grave pone el contenido en riesgo de perderse (antes del límite: {uncapped})",
        "nl": "Begrensd op {cap}: 1 ernstige bevinding zet inhoud op het spel (voor de begrenzing: {uncapped})",
        "fr": "Plafonné à {cap} : 1 constat grave met le contenu en risque de perte (avant plafond : {uncapped})",
    },
    "cap_reason_many": {
        "en": "Capped at {cap}: {count} high-severity findings put content at risk of being lost (before the cap: {uncapped})",
        "de": "Auf {cap} begrenzt: {count} schwerwiegende Befunde gefährden Inhalte (vor der Begrenzung: {uncapped})",
        "uk": "Обмежено до {cap}: {count} критичні знахідки ставлять вміст під загрозу втрати (до обмеження: {uncapped})",
        "ru": "Ограничено до {cap}: {count} критические находки ставят содержимое под угрозу потери (до ограничения: {uncapped})",
        "es": "Limitado a {cap}: {count} hallazgos graves ponen el contenido en riesgo de perderse (antes del límite: {uncapped})",
        "nl": "Begrensd op {cap}: {count} ernstige bevindingen zetten inhoud op het spel (voor de begrenzing: {uncapped})",
        "fr": "Plafonné à {cap} : {count} constats graves mettent le contenu en risque de perte (avant plafond : {uncapped})",
    },
    "not_scored": {
        "en": "not scored",
        "de": "nicht bewertet",
        "uk": "не оцінюється",
        "ru": "не оценивается",
        "es": "sin puntuar",
        "nl": "niet gescoord",
        "fr": "non noté",
    },
    "weight": {
        "en": "weight",
        "de": "Gewicht",
        "uk": "вага",
        "ru": "вес",
        "es": "peso",
        "nl": "gewicht",
        "fr": "poids",
    },
    "evidence_verbatim": {
        "en": "{text}",
        "de": "{text}",
        "uk": "{text}",
        "ru": "{text}",
        "es": "{text}",
        "nl": "{text}",
        "fr": "{text}",
    },
    "evidence_fonts": {
        "en": "Non-embedded fonts: {fonts}",
        "de": "Nicht eingebettete Schriften: {fonts}",
        "uk": "Невбудовані шрифти: {fonts}",
        "ru": "Невстроенные шрифты: {fonts}",
        "es": "Fuentes no incrustadas: {fonts}",
        "nl": "Niet-ingesloten lettertypen: {fonts}",
        "fr": "Polices non incorporées : {fonts}",
    },
    "evidence_repeated_line": {
        "en": "[{zone}] \"{text}\" on pages {pages}",
        "de": "[{zone}] \"{text}\" auf Seiten {pages}",
        "uk": "[{zone}] \"{text}\" на сторінках {pages}",
        "ru": "[{zone}] \"{text}\" на страницах {pages}",
        "es": "[{zone}] \"{text}\" en las páginas {pages}",
        "nl": "[{zone}] \"{text}\" op pagina's {pages}",
        "fr": "[{zone}] \"{text}\" aux pages {pages}",
    },
    "evidence_textless_image": {
        "en": "page {page}, {percent}% of page area",
        "de": "Seite {page}, {percent}% der Seitenfläche",
        "uk": "сторінка {page}, {percent}% площі сторінки",
        "ru": "страница {page}, {percent}% площади страницы",
        "es": "página {page}, {percent}% del área de la página",
        "nl": "pagina {page}, {percent}% van het paginaoppervlak",
        "fr": "page {page}, {percent}% de la surface de la page",
    },
    "evidence_table_cells": {
        "en": "One or more table cells contain resume content",
        "de": "Eine oder mehrere Tabellenzellen enthalten Inhalte des Lebenslaufs",
        "uk": "Одна або кілька комірок таблиці містять вміст резюме",
        "ru": "Одна или несколько ячеек таблицы содержат содержимое резюме",
        "es": "Una o más celdas de tabla contienen contenido del currículum",
        "nl": "Een of meer tabelcellen bevatten cv-inhoud",
        "fr": "Une ou plusieurs cellules de tableau contiennent du contenu du CV",
    },
    "evidence_no_contact": {
        "en": "No email or phone found anywhere in the extracted text",
        "de": "Weder E-Mail noch Telefon im extrahierten Text gefunden",
        "uk": "У видобутому тексті не знайдено ні пошти, ні телефону",
        "ru": "В извлечённом тексте не найдено ни почты, ни телефона",
        "es": "No se ha encontrado correo ni teléfono en el texto extraído",
        "nl": "Geen e-mail of telefoon gevonden in de geëxtraheerde tekst",
        "fr": "Ni e-mail ni téléphone trouvés dans le texte extrait",
    },
    "evidence_sections_lost_one": {
        "en": "{sections} section found layout-aware but missing under naive parsing",
        "de": "Abschnitt {sections} wird layoutbewusst erkannt, fehlt aber beim naiven Parsen",
        "uk": "Розділ {sections} розпізнано з урахуванням верстки, але при наївному розборі його немає",
        "ru": "Раздел {sections} распознан с учётом вёрстки, но при наивном разборе его нет",
        "es": "La sección {sections} se detecta con el diseño en cuenta, pero falta en el análisis ingenuo",
        "nl": "Sectie {sections} wordt opmaak-bewust herkend, maar ontbreekt bij naïeve parsing",
        "fr": "La section {sections} est détectée avec la mise en page, mais absente à l'analyse naïve",
    },
    "evidence_sections_lost_many": {
        "en": "{sections} sections found layout-aware but missing under naive parsing",
        "de": "Abschnitte {sections} werden layoutbewusst erkannt, fehlen aber beim naiven Parsen",
        "uk": "Розділи {sections} розпізнано з урахуванням верстки, але при наївному розборі їх немає",
        "ru": "Разделы {sections} распознаны с учётом вёрстки, но при наивном разборе их нет",
        "es": "Las secciones {sections} se detectan con el diseño en cuenta, pero faltan en el análisis ingenuo",
        "nl": "Secties {sections} worden opmaak-bewust herkend, maar ontbreken bij naïeve parsing",
        "fr": "Les sections {sections} sont détectées avec la mise en page, mais absentes à l'analyse naïve",
    },
    "update_available": {
        "en": "Version {latest} is available — you have {current}. [Download the update]({url})",
        "de": "Version {latest} ist verfügbar — Sie haben {current}. [Update herunterladen]({url})",
        "uk": "Доступна версія {latest} — у вас {current}. [Завантажити оновлення]({url})",
        "ru": "Доступна версия {latest} — у вас {current}. [Скачать обновление]({url})",
        "es": "La versión {latest} está disponible — tienes {current}. [Descargar la actualización]({url})",
        "nl": "Versie {latest} is beschikbaar — je hebt {current}. [Update downloaden]({url})",
        "fr": "La version {latest} est disponible — vous avez {current}. [Télécharger la mise à jour]({url})",
    },
    "open_source": {
        "en": "Open source",
        "de": "Open Source",
        "uk": "Відкритий код",
        "ru": "Открытый код",
        "es": "Código abierto",
        "nl": "Open source",
        "fr": "Code ouvert",
    },
}


def t(key: str, language: str, **kwargs) -> str:
    """Return the translated string, falling back to English when a language
    has no entry for it. Unknown keys surface as ``[key]`` rather than
    raising, so a typo shows up in the interface instead of taking the page
    down mid-render.
    """
    entry = TRANSLATIONS.get(key)
    if entry is None:
        return f"[{key}]"

    text = entry.get(language) or entry.get(DEFAULT_LANGUAGE, f"[{key}]")
    return text.format(**kwargs) if kwargs else text


RULE_DESCRIPTIONS: dict[str, dict[str, str]] = {
    "pdf_non_embedded_font": {
        "en": (
            "A font used in the PDF is not embedded and is not one of the 14 standard PDF "
            "base fonts. Non-embedded, non-standard fonts risk character-mapping issues "
            "that cause garbled or missing text during parsing."
        ),
        "de": (
            "Eine im PDF verwendete Schrift ist nicht eingebettet und gehört nicht zu den 14 "
            "PDF-Standardschriften. Solche Schriften riskieren Zeichenzuordnungsfehler, die "
            "beim Parsen zu verstümmeltem oder fehlendem Text führen."
        ),
        "uk": (
            "Шрифт, використаний у PDF, не вбудований і не належить до 14 стандартних "
            "шрифтів PDF. Такі шрифти ризикують дати збій відповідності символів, через що "
            "текст при розборі спотворюється або зникає."
        ),
        "ru": (
            "Шрифт, использованный в PDF, не встроен и не входит в число 14 стандартных "
            "шрифтов PDF. Такие шрифты рискуют дать сбой соответствия символов, из-за чего "
            "текст при разборе искажается или пропадает."
        ),
        "es": (
            "Una fuente usada en el PDF no está incrustada ni es una de las 14 fuentes base "
            "estándar. Las fuentes no incrustadas arriesgan errores de correspondencia de "
            "caracteres que producen texto ilegible o ausente al analizar."
        ),
        "nl": (
            "Een in de PDF gebruikt lettertype is niet ingesloten en behoort niet tot de 14 "
            "standaard PDF-lettertypen. Zulke lettertypen riskeren fouten in de "
            "tekentoewijzing, waardoor tekst bij het parsen verminkt raakt of verdwijnt."
        ),
        "fr": (
            "Une police utilisée dans le PDF n'est pas incorporée et ne fait pas partie des "
            "14 polices de base standard. Ces polices risquent des erreurs de correspondance "
            "de caractères, produisant un texte illisible ou manquant à l'analyse."
        ),
    },
    "pdf_repeated_header_footer_content": {
        "en": (
            "Text repeats in the same header/footer zone across multiple PDF pages. Parsers "
            "commonly treat repeated header/footer content as boilerplate and strip it — a "
            "problem if essential info (phone, email) lives there."
        ),
        "de": (
            "Text wiederholt sich auf mehreren PDF-Seiten in derselben Kopf-/Fußzeile. Parser "
            "behandeln wiederholte Kopf-/Fußzeilen meist als Beiwerk und entfernen sie — ein "
            "Problem, wenn dort wichtige Angaben (Telefon, E-Mail) stehen."
        ),
        "uk": (
            "Текст повторюється в тій самій зоні колонтитула на кількох сторінках PDF. "
            "Парсери зазвичай вважають повторюваний колонтитул службовим і відкидають його — "
            "це проблема, якщо там важлива інформація (телефон, пошта)."
        ),
        "ru": (
            "Текст повторяется в той же зоне колонтитула на нескольких страницах PDF. "
            "Парсеры обычно считают повторяющийся колонтитул служебным и отбрасывают его — "
            "это проблема, если там важная информация (телефон, почта)."
        ),
        "es": (
            "Hay texto que se repite en la misma zona de encabezado/pie en varias páginas. "
            "Los analizadores suelen tratar ese contenido como plantilla y descartarlo — un "
            "problema si ahí están datos esenciales (teléfono, correo)."
        ),
        "nl": (
            "Tekst herhaalt zich in dezelfde kop-/voettekstzone op meerdere PDF-pagina's. "
            "Parsers beschouwen herhaalde kop-/voetteksten meestal als opvulling en "
            "verwijderen ze — een probleem als daar essentiële gegevens staan."
        ),
        "fr": (
            "Du texte se répète dans la même zone d'en-tête/pied sur plusieurs pages. Les "
            "analyseurs traitent souvent ce contenu comme accessoire et le suppriment — "
            "problématique si des informations essentielles s'y trouvent."
        ),
    },
    "pdf_textless_image": {
        "en": (
            "A large image on the page has no extracted text overlapping it — a sign that a "
            "name banner, skills chart, or whole section may have been exported as a picture "
            "instead of real text, which most parsers cannot read at all."
        ),
        "de": (
            "Ein großes Bild auf der Seite überschneidet sich mit keinem extrahierten Text — "
            "ein Hinweis, dass ein Namensbanner, ein Diagramm oder ein ganzer Abschnitt als "
            "Bild statt als Text exportiert wurde, was die meisten Parser gar nicht lesen."
        ),
        "uk": (
            "Велике зображення на сторінці не перетинається з жодним видобутим текстом — "
            "ознака, що банер з іменем, діаграма навичок чи цілий розділ збережені картинкою "
            "замість тексту, а більшість парсерів такого не читає взагалі."
        ),
        "ru": (
            "Большое изображение на странице не пересекается ни с одним извлечённым текстом — "
            "признак, что баннер с именем, диаграмма навыков или целый раздел сохранены "
            "картинкой вместо текста, а большинство парсеров такое не читает вообще."
        ),
        "es": (
            "Una imagen grande de la página no se solapa con ningún texto extraído — señal de "
            "que un rótulo con el nombre, un gráfico o una sección entera se exportó como "
            "imagen en vez de texto, algo que la mayoría de analizadores no puede leer."
        ),
        "nl": (
            "Een grote afbeelding op de pagina overlapt met geen enkele geëxtraheerde tekst — "
            "een teken dat een naambanner, vaardighedendiagram of hele sectie als plaatje is "
            "geëxporteerd in plaats van tekst, wat de meeste parsers niet kunnen lezen."
        ),
        "fr": (
            "Une grande image de la page ne recouvre aucun texte extrait — signe qu'un "
            "bandeau de nom, un graphique ou une section entière a été exporté en image "
            "plutôt qu'en texte, ce que la plupart des analyseurs ne lisent pas du tout."
        ),
    },
    "docx_table_content": {
        "en": (
            "Resume content lives inside a DOCX table. Many parsers flatten table rows in a "
            "way that scrambles which value belongs to which label, or skip table content "
            "entirely."
        ),
        "de": (
            "Inhalte des Lebenslaufs stehen in einer DOCX-Tabelle. Viele Parser lesen "
            "Tabellenzeilen so aus, dass die Zuordnung von Wert und Bezeichnung verloren "
            "geht, oder überspringen Tabelleninhalte ganz."
        ),
        "uk": (
            "Вміст резюме розміщено в таблиці DOCX. Багато парсерів розгортають рядки "
            "таблиці так, що плутається, яке значення до якої назви належить, або пропускають "
            "вміст таблиць повністю."
        ),
        "ru": (
            "Содержимое резюме размещено в таблице DOCX. Многие парсеры разворачивают строки "
            "таблицы так, что путается, какое значение к какому названию относится, либо "
            "пропускают содержимое таблиц полностью."
        ),
        "es": (
            "Hay contenido del currículum dentro de una tabla DOCX. Muchos analizadores "
            "aplanan las filas de forma que se mezcla qué valor corresponde a qué etiqueta, "
            "o se saltan el contenido de las tablas por completo."
        ),
        "nl": (
            "Cv-inhoud staat in een DOCX-tabel. Veel parsers plooien tabelrijen zo plat dat "
            "onduidelijk wordt welke waarde bij welk label hoort, of slaan tabelinhoud "
            "helemaal over."
        ),
        "fr": (
            "Du contenu du CV se trouve dans un tableau DOCX. Beaucoup d'analyseurs aplatis"
            "sent les lignes de sorte que l'association valeur/libellé se perd, ou ignorent "
            "entièrement le contenu des tableaux."
        ),
    },
    "docx_header_footer_content": {
        "en": (
            "Resume content (often contact info) lives in a DOCX header or footer — a part of "
            "the file that lives outside the main document body and that many parsers skip "
            "entirely."
        ),
        "de": (
            "Inhalte (oft Kontaktdaten) stehen in einer DOCX-Kopf- oder Fußzeile — einem "
            "Bereich außerhalb des Hauptdokuments, den viele Parser vollständig überspringen."
        ),
        "uk": (
            "Вміст резюме (часто контакти) розміщено в колонтитулі DOCX — частині файлу поза "
            "основним тілом документа, яку багато парсерів пропускають повністю."
        ),
        "ru": (
            "Содержимое резюме (часто контакты) размещено в колонтитуле DOCX — части файла вне "
            "основного тела документа, которую многие парсеры пропускают полностью."
        ),
        "es": (
            "Hay contenido (a menudo los datos de contacto) en el encabezado o pie de un "
            "DOCX — una parte fuera del cuerpo del documento que muchos analizadores omiten "
            "por completo."
        ),
        "nl": (
            "Cv-inhoud (vaak contactgegevens) staat in een DOCX-kop- of voettekst — een deel "
            "buiten het hoofddocument dat veel parsers volledig overslaan."
        ),
        "fr": (
            "Du contenu (souvent les coordonnées) se trouve dans un en-tête ou pied de page "
            "DOCX — une partie hors du corps du document que beaucoup d'analyseurs ignorent "
            "totalement."
        ),
    },
    "docx_text_box_content": {
        "en": (
            "Resume content lives inside a Word text box, nested inside a drawing anchor "
            "rather than the normal paragraph flow most parsers read."
        ),
        "de": (
            "Inhalte stehen in einem Word-Textfeld, eingebettet in einen Zeichnungsanker "
            "statt im normalen Absatzfluss, den die meisten Parser lesen."
        ),
        "uk": (
            "Вміст резюме розміщено в текстовому полі Word, вкладеному в графічний якір, а не "
            "у звичайному потоці абзаців, який читає більшість парсерів."
        ),
        "ru": (
            "Содержимое резюме размещено в текстовом поле Word, вложенном в графический якорь, "
            "а не в обычном потоке абзацев, который читает большинство парсеров."
        ),
        "es": (
            "Hay contenido dentro de un cuadro de texto de Word, anidado en un anclaje de "
            "dibujo en lugar del flujo normal de párrafos que leen la mayoría de analizadores."
        ),
        "nl": (
            "Cv-inhoud staat in een Word-tekstvak, genest in een tekeninganker in plaats van "
            "de normale alineastroom die de meeste parsers lezen."
        ),
        "fr": (
            "Du contenu se trouve dans une zone de texte Word, imbriquée dans une ancre de "
            "dessin plutôt que dans le flux normal de paragraphes que lisent les analyseurs."
        ),
    },
    "missing_contact_field": {
        "en": (
            "No email address and/or phone number could be found anywhere in the extracted "
            "text, even reading layout-aware, best case. Without a way to reach the "
            "candidate, this is typically an unrecoverable rejection regardless of formatting."
        ),
        "de": (
            "Weder E-Mail-Adresse noch Telefonnummer waren im extrahierten Text zu finden, "
            "auch nicht im besten Fall mit Layout-Berücksichtigung. Ohne Kontaktmöglichkeit "
            "ist das unabhängig von der Formatierung meist eine endgültige Absage."
        ),
        "uk": (
            "Ні електронної пошти, ні номера телефону не знайдено у видобутому тексті — навіть "
            "у найкращому випадку, з урахуванням верстки. Без способу зв'язатися з кандидатом "
            "це зазвичай безповоротна відмова, незалежно від форматування."
        ),
        "ru": (
            "Ни электронной почты, ни номера телефона не найдено в извлечённом тексте — даже в "
            "лучшем случае, с учётом вёрстки. Без способа связаться с кандидатом это обычно "
            "безвозвратный отказ, независимо от форматирования."
        ),
        "es": (
            "No se ha encontrado ni correo electrónico ni teléfono en el texto extraído, ni "
            "siquiera en el mejor caso con el diseño en cuenta. Sin forma de contactar al "
            "candidato, suele ser un rechazo irreversible al margen del formato."
        ),
        "nl": (
            "Er is geen e-mailadres of telefoonnummer gevonden in de geëxtraheerde tekst, "
            "zelfs niet in het beste geval met opmaak. Zonder manier om de kandidaat te "
            "bereiken is dit meestal een definitieve afwijzing, ongeacht de opmaak."
        ),
        "fr": (
            "Ni adresse e-mail ni numéro de téléphone n'ont été trouvés dans le texte extrait, "
            "même dans le meilleur cas tenant compte de la mise en page. Sans moyen de "
            "joindre le candidat, c'est généralement un rejet définitif."
        ),
    },
    "section_missing_under_naive_parsing": {
        "en": (
            "A resume section (Experience/Education/Skills) is recognized when the file is "
            "read layout-aware, but disappears entirely when read the way a naive, "
            "layout-blind parser would — evidence that formatting, not content, is putting "
            "this section at risk."
        ),
        "de": (
            "Ein Abschnitt (Berufserfahrung/Ausbildung/Kenntnisse) wird bei layoutbewusstem "
            "Lesen erkannt, verschwindet aber vollständig, wenn die Datei wie von einem "
            "layoutblinden Parser gelesen wird — die Formatierung, nicht der Inhalt, "
            "gefährdet diesen Abschnitt."
        ),
        "uk": (
            "Розділ резюме (Досвід/Освіта/Навички) розпізнається, коли файл читають з "
            "урахуванням верстки, але повністю зникає при читанні простим парсером, сліпим до "
            "верстки — отже, під загрозою цей розділ ставить форматування, а не вміст."
        ),
        "ru": (
            "Раздел резюме (Опыт/Образование/Навыки) распознаётся, когда файл читают с учётом "
            "вёрстки, но полностью исчезает при чтении простым парсером, слепым к вёрстке — "
            "значит, под угрозу этот раздел ставит форматирование, а не содержимое."
        ),
        "es": (
            "Una sección (Experiencia/Educación/Habilidades) se reconoce al leer el archivo "
            "teniendo en cuenta el diseño, pero desaparece por completo al leerlo como lo "
            "haría un analizador ciego al diseño — es el formato, no el contenido, lo que "
            "pone en riesgo esta sección."
        ),
        "nl": (
            "Een sectie (Werkervaring/Opleiding/Vaardigheden) wordt herkend bij opmaak-bewust "
            "lezen, maar verdwijnt volledig bij lezen zoals een opmaak-blinde parser doet — "
            "de opmaak, niet de inhoud, brengt deze sectie in gevaar."
        ),
        "fr": (
            "Une section (Expérience/Formation/Compétences) est reconnue lors d'une lecture "
            "tenant compte de la mise en page, mais disparaît entièrement à la lecture d'un "
            "analyseur aveugle à celle-ci — c'est la mise en forme, non le contenu, qui met "
            "cette section en péril."
        ),
    },
}


def rule_description(rule_id: str, language: str, fallback: str) -> str:
    """Return the translated description for a rule.

    ``fallback`` is the description carried by the Rule itself, used when a
    rule has no translation entry yet -- a new rule stays readable instead
    of showing a placeholder.
    """
    entry = RULE_DESCRIPTIONS.get(rule_id)
    if entry is None:
        return fallback
    return entry.get(language) or entry.get(DEFAULT_LANGUAGE) or fallback
