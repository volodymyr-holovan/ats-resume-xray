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
            "парсер — не таємничий бал, а реальне порівняння. Зауваження — це "
            "задокументовані типові збої ([джерела]({sources_url})), а не гарантія поведінки "
            "системи конкретного роботодавця."
        ),
        "ru": (
            "Загрузите резюме (PDF или DOCX), чтобы увидеть, что из него на самом деле "
            "извлекает парсер — не загадочный балл, а реальное сравнение. "
            "Замечания — это задокументированные типичные сбои ([источники]({sources_url})), "
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
    "score_caption": {
        "en": (
            "How much of this resume survives an automated read. This is **not** a "
            "keyword-match score against a job posting: that needs the posting and the "
            "employer's weighting, neither of which this tool has. Every number below is "
            "derived from evidence in your file, shown in full."
        ),
        "de": (
            "Wie viel von diesem Lebenslauf ein maschinelles Lesen übersteht. Das ist "
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
        "en": "Issues and fixes",
        "de": "Hinweise und Korrekturen",
        "uk": "Зауваження та виправлення",
        "ru": "Замечания и исправления",
        "es": "Observaciones y correcciones",
        "nl": "Opmerkingen en verbeteringen",
        "fr": "Remarques et corrections",
    },
    "no_findings": {
        "en": "No documented parsing risks triggered.",
        "de": "Keine dokumentierten Parsing-Risiken ausgelöst.",
        "uk": "Жодного задокументованого ризику розбору не виявлено.",
        "ru": "Ни одного задокументированного риска разбора не выявлено.",
        "es": "No se ha detectado ningún riesgo de análisis documentado.",
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
    "details_expander": {
        "en": "What this means and how to fix it",
        "de": "Was das bedeutet und wie Sie es beheben",
        "uk": "Що це означає і як це виправити",
        "ru": "Что это значит и как это исправить",
        "es": "Qué significa y cómo solucionarlo",
        "nl": "Wat dit betekent en hoe je het oplost",
        "fr": "Ce que cela signifie et comment le corriger",
    },
    "how_to_fix": {
        "en": "How to fix it",
        "de": "So beheben Sie es",
        "uk": "Як це виправити",
        "ru": "Как это исправить",
        "es": "Cómo solucionarlo",
        "nl": "Hoe je het oplost",
        "fr": "Comment le corriger",
    },
    "read_more": {
        "en": "Read more",
        "de": "Mehr dazu",
        "uk": "Докладніше",
        "ru": "Подробнее",
        "es": "Más información",
        "nl": "Meer lezen",
        "fr": "En savoir plus",
    },
    "severity_high": {
        "en": "HIGH RISK",
        "de": "HOHES RISIKO",
        "uk": "ВИСОКИЙ РИЗИК",
        "ru": "ВЫСОКИЙ РИСК",
        "es": "RIESGO ALTO",
        "nl": "HOOG RISICO",
        "fr": "RISQUE ÉLEVÉ",
    },
    "severity_medium": {
        "en": "MEDIUM RISK",
        "de": "MITTLERES RISIKO",
        "uk": "СЕРЕДНІЙ РИЗИК",
        "ru": "СРЕДНИЙ РИСК",
        "es": "RIESGO MEDIO",
        "nl": "GEMIDDELD RISICO",
        "fr": "RISQUE MOYEN",
    },
    "severity_low": {
        "en": "LOW RISK",
        "de": "GERINGES RISIKO",
        "uk": "НИЗЬКИЙ РИЗИК",
        "ru": "НИЗКИЙ РИСК",
        "es": "RIESGO BAJO",
        "nl": "LAAG RISICO",
        "fr": "RISQUE FAIBLE",
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
    "docx_layout_note": {
        "en": (
            "This DOCX was laid out with LibreOffice to produce pages; your own word "
            "processor may break lines slightly differently."
        ),
        "de": (
            "Dieses DOCX wurde mit LibreOffice gesetzt, um Seiten zu erzeugen; Ihr eigenes "
            "Textprogramm bricht Zeilen möglicherweise etwas anders um."
        ),
        "uk": "Цей DOCX було зверстано у LibreOffice, щоб отримати сторінки; ваш власний текстовий редактор може переносити рядки трохи інакше.",
        "ru": "Этот DOCX был свёрстан в LibreOffice, чтобы получить страницы; ваш текстовый редактор может переносить строки немного иначе.",
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
            "вміст, але не позиції на сторінці, тож його спершу треба зверстати. Зауваження "
            "вище лишаються чинними."
        ),
        "ru": (
            "Просмотр страниц для DOCX требует LibreOffice, которого здесь нет. DOCX хранит "
            "содержимое, но не позиции на странице, поэтому его сначала нужно сверстать. "
            "Замечания выше остаются в силе."
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
    "extraction_empty": {
        "en": "Nothing at all was recovered this way. Every word in the file sits somewhere this kind of reading cannot reach — a table, a text box, or a header.",
        "de": "Auf diesem Weg wurde überhaupt nichts gelesen. Jedes Wort der Datei steht an einer Stelle, die diese Art zu lesen nicht erreicht — in einer Tabelle, einem Textfeld oder einer Kopfzeile.",
        "uk": "Так не вдалося дістати нічого. Кожне слово у файлі лежить там, куди таке читання не дістає — у таблиці, текстовому полі або колонтитулі.",
        "ru": "Так не удалось извлечь ничего. Каждое слово в файле лежит там, куда такое чтение не достаёт — в таблице, текстовом поле или колонтитуле.",
        "es": "Por esta vía no se recuperó nada. Cada palabra del archivo está en un sitio al que esta forma de leer no llega: una tabla, un cuadro de texto o un encabezado.",
        "nl": "Zo is er helemaal niets uit gekomen. Elk woord in het bestand staat op een plek waar deze manier van lezen niet bij komt — een tabel, een tekstvak of een koptekst.",
        "fr": "Cette lecture n'a rien récupéré du tout. Chaque mot du fichier se trouve à un endroit qu'elle n'atteint pas : un tableau, une zone de texte ou un en-tête.",
    },
    "naive_expander": {
        "en": "Naive extraction — what a basic, layout-blind parser sees",
        "de": "Naive Extraktion — was ein einfacher, layoutblinder Parser sieht",
        "uk": "Наївний розбір — що бачить простий парсер, сліпий до верстки",
        "ru": "Наивный разбор — что видит простой парсер, слепой к вёрстке",
        "es": "Extracción ingenua — lo que ve un analizador ciego al diseño",
        "nl": "Naïeve extractie — wat een simpele, layoutblinde parser ziet",
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
        "es": "Contacto localizable",
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
        "fr": "S'analyse sans problème",

    },
    "rating_mostly": {
        "en": "Mostly parses, some risk",
        "de": "Weitgehend lesbar, mit Risiko",
        "uk": "Здебільшого читається, є ризик",
        "ru": "В основном читается, есть риск",
        "es": "Se analiza casi todo, con riesgo",
        "nl": "Grotendeels leesbaar, enig risico",
        "fr": "Analyse correcte, avec un risque",

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
        "nl": "E-mail en telefoon beide gevonden bij een eenvoudige, layoutblinde lezing",
        "fr": "E-mail et téléphone retrouvés par une lecture simple, aveugle à la mise en page",
    },
    "detail_contact_one": {
        "en": "Found: {found}. Not found: {missing}.",
        "de": "Gefunden: {found}. Nicht gefunden: {missing}.",
        "uk": "Знайдено: {found}. Не знайдено: {missing}.",
        "ru": "Найдено: {found}. Не найдено: {missing}.",
        "es": "Encontrado: {found}. No encontrado: {missing}.",
        "nl": "Gevonden: {found}. Niet gevonden: {missing}.",
        "fr": "Trouvé : {found}. Introuvable : {missing}.",

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
        "en": "All sections ({total}) survive layout-blind reading",
        "de": "Alle Abschnitte ({total}) überstehen ein layoutblindes Lesen",
        "uk": "Усі розділи ({total}) переживають читання, сліпе до верстки",
        "ru": "Все разделы ({total}) переживают чтение, слепое к вёрстке",
        "es": "Todas las secciones ({total}) sobreviven a la lectura ciega al diseño",
        "nl": "Alle secties ({total}) overleven layoutblind lezen",
        "fr": "Toutes les sections ({total}) survivent à la lecture aveugle à la mise en page",

    },
    "detail_sections_lost": {
        "en": "Layout-blind reading keeps {survived} of {total} sections (lost: {lost})",
        "de": "Layoutblindes Lesen bewahrt {survived} von {total} Abschnitten (verloren: {lost})",
        "uk": "Читання, сліпе до верстки, зберігає {survived} з {total} розділів (втрачено: {lost})",
        "ru": "Чтение, слепое к вёрстке, сохраняет {survived} из {total} разделов (потеряно: {lost})",
        "es": "La lectura ciega al diseño conserva {survived} de {total} secciones (perdidas: {lost})",
        "nl": "Layoutblind lezen behoudt {survived} van {total} secties (verloren: {lost})",
        "fr": "Sections conservées à la lecture aveugle à la mise en page : {survived} sur {total} (perdues : {lost})",

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
        "es": "Penalizaciones: {deductions}",
        "nl": "Aftrek: {deductions}",
        "fr": "Points retirés : {deductions}",

    },
    "cap_reason_one": {
        "en": "Capped at {cap}: {count} high-severity issue puts content at risk of being lost (before the cap: {uncapped})",
        "de": "Auf {cap} begrenzt: {count} schwerwiegender Hinweis gefährdet Inhalte (vor der Begrenzung: {uncapped})",
        "uk": "Обмежено до {cap}: {count} критичне зауваження ставить вміст під загрозу втрати (до обмеження: {uncapped})",
        "ru": "Ограничено до {cap}: {count} критическое замечание ставит содержимое под угрозу потери (до ограничения: {uncapped})",
        "es": "Limitado a {cap}: {count} observación grave pone el contenido en riesgo de perderse (antes del límite: {uncapped})",
        "nl": "Begrensd op {cap}: {count} ernstige opmerking zet inhoud op het spel (voor de begrenzing: {uncapped})",
        "fr": "Plafonné à {cap} : {count} remarque grave expose le contenu à un risque de perte (avant plafond : {uncapped})",

    },
    "cap_reason_few": {
        "uk": "Обмежено до {cap}: {count} критичні зауваження ставлять вміст під загрозу втрати (до обмеження: {uncapped})",
        "ru": "Ограничено до {cap}: {count} критических замечания ставят содержимое под угрозу потери (до ограничения: {uncapped})",
    },
    "cap_reason_many": {
        "en": "Capped at {cap}: {count} high-severity issues put content at risk of being lost (before the cap: {uncapped})",
        "de": "Auf {cap} begrenzt: {count} schwerwiegende Hinweise gefährden Inhalte (vor der Begrenzung: {uncapped})",
        "uk": "Обмежено до {cap}: {count} критичних зауважень ставлять вміст під загрозу втрати (до обмеження: {uncapped})",
        "ru": "Ограничено до {cap}: {count} критических замечаний ставят содержимое под угрозу потери (до ограничения: {uncapped})",
        "es": "Limitado a {cap}: {count} observaciones graves ponen el contenido en riesgo de perderse (antes del límite: {uncapped})",
        "nl": "Begrensd op {cap}: {count} ernstige opmerkingen zetten inhoud op het spel (voor de begrenzing: {uncapped})",
        "fr": "Plafonné à {cap} : {count} remarques graves exposent le contenu à un risque de perte (avant plafond : {uncapped})",

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
        "de": "[{zone}] \"{text}\" auf den Seiten {pages}",
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
        "ru": "Одна или несколько ячеек таблицы содержат текст резюме",
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
        "es": "La sección {sections} se detecta al leer teniendo en cuenta el diseño, pero falta en el análisis ingenuo",
        "nl": "Sectie {sections} wordt layoutbewust herkend, maar ontbreekt bij naïeve parsing",
        "fr": "La section {sections} est détectée avec la mise en page, mais absente à l'analyse naïve",
    },
    "evidence_sections_lost_many": {
        "en": "{sections} sections found layout-aware but missing under naive parsing",
        "de": "Abschnitte {sections} werden layoutbewusst erkannt, fehlen aber beim naiven Parsen",
        "uk": "Розділи {sections} розпізнано з урахуванням верстки, але при наївному розборі їх немає",
        "ru": "Разделы {sections} распознаны с учётом вёрстки, но при наивном разборе их нет",
        "es": "Las secciones {sections} se detectan al leer teniendo en cuenta el diseño, pero faltan en el análisis ingenuo",
        "nl": "Secties {sections} worden layoutbewust herkend, maar ontbreken bij naïeve parsing",
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
        "fr": "Open source",

    },
    "match_heading": {
        "en": "Match against a job ad",
        "de": "Abgleich mit einer Stellenanzeige",
        "uk": "Порівняння з вакансією",
        "ru": "Сравнение с вакансией",
        "es": "Comparación con una oferta",
        "nl": "Vergelijking met een vacature",
        "fr": "Comparaison avec une offre",
    },
    "match_intro": {
        "en": "Paste a job ad. The keywords are read out of it automatically; you can edit them before scoring.",
        "de": "Fügen Sie eine Stellenanzeige ein. Die Schlüsselwörter werden automatisch daraus gelesen; Sie können sie vor der Bewertung bearbeiten.",
        "uk": "Вставте опис вакансії. Ключові слова зчитуються з нього автоматично; перед оцінюванням їх можна відредагувати.",
        "ru": "Вставьте описание вакансии. Ключевые слова считываются из него автоматически; перед оценкой их можно отредактировать.",
        "es": "Pega una oferta de empleo. Las palabras clave se extraen automáticamente; puedes editarlas antes de puntuar.",
        "nl": "Plak een vacaturetekst. De trefwoorden worden er automatisch uit gelezen; je kunt ze vóór de beoordeling aanpassen.",
        "fr": "Collez une offre d'emploi. Les mots-clés en sont extraits automatiquement ; vous pouvez les modifier avant l'évaluation.",
    },
    "match_paste_label": {
        "en": "Job ad text",
        "de": "Text der Stellenanzeige",
        "uk": "Текст вакансії",
        "ru": "Текст вакансии",
        "es": "Texto de la oferta",
        "nl": "Vacaturetekst",
        "fr": "Texte de l'offre",
    },
    "match_paste_placeholder": {
        "en": "Paste the whole ad, including the tasks and the requirements.",
        "de": "Fügen Sie die gesamte Anzeige ein, einschließlich Aufgaben und Anforderungen.",
        "uk": "Вставте весь текст, разом із завданнями та вимогами.",
        "ru": "Вставьте весь текст, вместе с задачами и требованиями.",
        "es": "Pega el anuncio completo, con las tareas y los requisitos.",
        "nl": "Plak de volledige advertentie, inclusief taken en eisen.",
        "fr": "Collez l'annonce entière, tâches et exigences comprises.",
    },
    "match_keywords_expander": {
        "en": "Keywords found in the ad — edit before scoring",
        "de": "In der Anzeige gefundene Schlüsselwörter — vor der Bewertung bearbeiten",
        "uk": "Ключові слова, знайдені у вакансії — відредагуйте перед оцінюванням",
        "ru": "Ключевые слова, найденные в вакансии — отредактируйте перед оценкой",
        "es": "Palabras clave encontradas en la oferta — edítalas antes de puntuar",
        "nl": "Trefwoorden uit de vacature — pas ze aan vóór de beoordeling",
        "fr": "Mots-clés trouvés dans l'offre — modifiez-les avant l'évaluation",
    },
    "match_must_label": {
        "en": "Required (weighted 3x)",
        "de": "Erforderlich (3-fach gewichtet)",
        "uk": "Обов'язкові (вага 3x)",
        "ru": "Обязательные (вес 3x)",
        "es": "Obligatorios (peso 3x)",
        "nl": "Vereist (weegt 3x)",
        "fr": "Exigés (pondérés 3x)",
    },
    "match_nice_label": {
        "en": "Preferred (weighted 1x)",
        "de": "Wünschenswert (1-fach gewichtet)",
        "uk": "Бажані (вага 1x)",
        "ru": "Желательные (вес 1x)",
        "es": "Valorables (peso 1x)",
        "nl": "Gewenst (weegt 1x)",
        "fr": "Souhaités (pondérés 1x)",
    },
    "match_other_label": {
        "en": "Other requirements detected",
        "de": "Weitere erkannte Anforderungen",
        "uk": "Інші виявлені вимоги",
        "ru": "Другие обнаруженные требования",
        "es": "Otros requisitos detectados",
        "nl": "Overige herkende eisen",
        "fr": "Autres exigences détectées",
    },
    "match_add_hint": {
        "en": "Type a keyword and press Enter to add one the ad implied but did not spell out.",
        "de": "Tippen Sie ein Schlüsselwort und drücken Sie Enter, um eines zu ergänzen, das die Anzeige nur andeutet.",
        "uk": "Введіть слово і натисніть Enter, щоб додати те, на що вакансія лише натякає.",
        "ru": "Введите слово и нажмите Enter, чтобы добавить то, на что вакансия лишь намекает.",
        "es": "Escribe una palabra y pulsa Enter para añadir algo que la oferta solo insinúa.",
        "nl": "Typ een trefwoord en druk op Enter om iets toe te voegen dat de vacature alleen impliceert.",
        "fr": "Saisissez un mot-clé et appuyez sur Entrée pour ajouter ce que l'offre sous-entend.",
    },
    "match_evaluate_button": {
        "en": "Rate my match",
        "de": "Übereinstimmung bewerten",
        "uk": "Оцінити відповідність",
        "ru": "Оценить соответствие",
        "es": "Evaluar mi encaje",
        "nl": "Mijn match beoordelen",
        "fr": "Évaluer ma correspondance",
    },
    "match_score_caption": {
        "en": "Counts what appears in both texts. It cannot judge how well you did the work, only whether the ad's requirements are findable in your CV.",
        "de": "Zählt, was in beiden Texten vorkommt. Es beurteilt nicht, wie gut Sie gearbeitet haben, sondern nur, ob die Anforderungen der Anzeige in Ihrem Lebenslauf auffindbar sind.",
        "uk": "Рахує те, що є в обох текстах. Не оцінює, наскільки добре ви працювали, лише чи можна знайти вимоги вакансії у вашому резюме.",
        "ru": "Считает то, что есть в обоих текстах. Не оценивает, насколько хорошо вы работали, только можно ли найти требования вакансии в вашем резюме.",
        "es": "Cuenta lo que aparece en ambos textos. No juzga lo bien que trabajaste, solo si los requisitos de la oferta se encuentran en tu CV.",
        "nl": "Telt wat in beide teksten voorkomt. Het beoordeelt niet hoe goed jij je werk deed, alleen of de eisen uit de vacature in je cv te vinden zijn.",
        "fr": "Compte ce qui figure dans les deux textes. N'évalue pas la qualité de votre travail, seulement si les exigences de l'offre se trouvent dans votre CV.",
    },
    "match_rating_strong": {
        "en": "Strong match",
        "de": "Starke Übereinstimmung",
        "uk": "Висока відповідність",
        "ru": "Высокое соответствие",
        "es": "Encaje alto",
        "nl": "Sterke match",
        "fr": "Forte correspondance",
    },
    "match_rating_good": {
        "en": "Good match",
        "de": "Gute Übereinstimmung",
        "uk": "Добра відповідність",
        "ru": "Хорошее соответствие",
        "es": "Buen encaje",
        "nl": "Goede match",
        "fr": "Bonne correspondance",
    },
    "match_rating_partial": {
        "en": "Partial match",
        "de": "Teilweise Übereinstimmung",
        "uk": "Часткова відповідність",
        "ru": "Частичное соответствие",
        "es": "Encaje parcial",
        "nl": "Gedeeltelijke match",
        "fr": "Correspondance partielle",
    },
    "match_rating_weak": {
        "en": "Weak match",
        "de": "Geringe Übereinstimmung",
        "uk": "Низька відповідність",
        "ru": "Низкое соответствие",
        "es": "Encaje bajo",
        "nl": "Zwakke match",
        "fr": "Faible correspondance",
    },
    "match_met_heading": {
        "en": "Covered",
        "de": "Abgedeckt",
        "uk": "Є в резюме",
        "ru": "Есть в резюме",
        "es": "Cubierto",
        "nl": "Gedekt",
        "fr": "Couvert",
    },
    "match_missing_must_warning_many": {
        "en": "{count} required items could not be found in your CV.",
        "de": "{count} erforderliche Punkte konnten in Ihrem Lebenslauf nicht gefunden werden.",
        "uk": "У вашому резюме не знайдено {count} обов'язкових пунктів.",
        "ru": "{count} обязательных пунктов не найдено в вашем резюме.",
        "es": "No se encontraron {count} requisitos obligatorios en tu CV.",
        "nl": "{count} vereiste punten zijn niet in je cv gevonden.",
        "fr": "{count} critères obligatoires sont introuvables dans votre CV.",

    },
    "match_missing_must_warning_one": {
        "en": "{count} required item could not be found in your CV.",
        "de": "{count} erforderlicher Punkt konnte in Ihrem Lebenslauf nicht gefunden werden.",
        "uk": "У вашому резюме не знайдено {count} обов'язковий пункт.",
        "ru": "{count} обязательного пункта не найдено в вашем резюме.",
        "es": "No se encontró {count} requisito obligatorio en tu CV.",
        "nl": "{count} vereist punt is niet in je cv gevonden.",
        "fr": "{count} critère obligatoire est introuvable dans votre CV.",

    },
    "match_missing_must_warning_few": {
        "uk": "У вашому резюме не знайдено {count} обов'язкові пункти.",
        "ru": "{count} обязательных пункта не найдено в вашем резюме.",
    },
    "match_all_must_covered": {
        "en": "Every required item was found in your CV.",
        "de": "Alle erforderlichen Punkte wurden in Ihrem Lebenslauf gefunden.",
        "uk": "Усі обов'язкові пункти знайдено у вашому резюме.",
        "ru": "Все обязательные пункты найдены в вашем резюме.",
        "es": "Se encontraron todos los requisitos obligatorios en tu CV.",
        "nl": "Alle vereiste punten zijn in je cv gevonden.",
        "fr": "Toutes les exigences obligatoires figurent dans votre CV.",
    },
    "match_at_risk_heading": {
        "en": "Matches a parser might miss",
        "de": "Treffer, die ein Parser übersehen könnte",
        "uk": "Збіги, які парсер може не побачити",
        "ru": "Совпадения, которые парсер может не увидеть",
        "es": "Coincidencias que un analizador podría perder",
        "nl": "Treffers die een parser kan missen",
        "fr": "Correspondances qu'un analyseur pourrait manquer",
    },
    "match_at_risk_caption": {
        "en": "These matched only when the file was read layout-aware. A layout-blind parser would not see them, so the match would not count.",
        "de": "Diese passten nur beim layoutbewussten Lesen. Ein layoutblinder Parser sieht sie nicht, der Treffer würde also nicht zählen.",
        "uk": "Ці збіги знайдено лише при читанні з урахуванням верстки. Парсер, сліпий до верстки, їх не побачить, тож збіг не зарахується.",
        "ru": "Эти совпадения найдены только при чтении с учётом вёрстки. Парсер, слепой к вёрстке, их не увидит, и совпадение не засчитается.",
        "es": "Solo coincidieron al leer el archivo teniendo en cuenta el diseño. Un analizador ciego al diseño no las vería, así que no contarían.",
        "nl": "Deze kwamen alleen overeen bij layoutbewust lezen. Een layoutblinde parser ziet ze niet, dus de treffer zou niet meetellen.",
        "fr": "Elles n'ont correspondu qu'en lecture attentive à la mise en page. Un analyseur aveugle à la mise en page ne les verrait pas.",
    },
    "match_extras_heading": {
        "en": "In your CV but not asked for",
        "de": "Im Lebenslauf, nicht gefordert",
        "uk": "Є у резюме, але не вимагається",
        "ru": "Есть в резюме, но не требуется",
        "es": "En tu CV pero no solicitado",
        "nl": "Wel in je cv, niet gevraagd",
        "fr": "Dans votre CV mais non demandé",
    },
    "match_extras_caption": {
        "en": "Not a problem. Useful when you tailor the CV: these are the parts this particular ad does not reward.",
        "de": "Kein Problem. Nützlich beim Zuschneiden des Lebenslaufs: Diese Teile honoriert genau diese Anzeige nicht.",
        "uk": "Це не проблема. Корисно при адаптації резюме: саме ця вакансія цих пунктів не оцінює.",
        "ru": "Это не проблема. Полезно при адаптации резюме: именно эта вакансия эти пункты не оценивает.",
        "es": "No es un problema. Útil al adaptar el CV: son las partes que esta oferta concreta no valora.",
        "nl": "Geen probleem. Nuttig bij het toespitsen van je cv: deze onderdelen beloont juist deze vacature niet.",
        "fr": "Ce n'est pas un problème. Utile pour adapter le CV : cette offre précise ne valorise pas ces éléments.",
    },
    "match_no_requirements": {
        "en": "No requirements could be read out of this text. Add keywords by hand, or paste more of the ad.",
        "de": "Aus diesem Text ließen sich keine Anforderungen lesen. Ergänzen Sie Schlüsselwörter von Hand oder fügen Sie mehr der Anzeige ein.",
        "uk": "З цього тексту не вдалося зчитати жодної вимоги. Додайте ключові слова вручну або вставте більше тексту вакансії.",
        "ru": "Из этого текста не удалось считать ни одного требования. Добавьте ключевые слова вручную или вставьте больше текста вакансии.",
        "es": "No se pudo leer ningún requisito de este texto. Añade palabras clave a mano o pega más contenido de la oferta.",
        "nl": "Uit deze tekst zijn geen eisen te lezen. Voeg handmatig trefwoorden toe of plak meer van de vacature.",
        "fr": "Aucune exigence n'a pu être lue dans ce texte. Ajoutez des mots-clés à la main ou collez davantage de l'offre.",
    },
    "match_needs_cv": {
        "en": "Upload a CV above to compare it against this ad.",
        "de": "Laden Sie oben einen Lebenslauf hoch, um ihn mit dieser Anzeige zu vergleichen.",
        "uk": "Завантажте резюме вище, щоб порівняти його з цією вакансією.",
        "ru": "Загрузите резюме выше, чтобы сравнить его с этой вакансией.",
        "es": "Sube un CV arriba para compararlo con esta oferta.",
        "nl": "Upload hierboven een cv om het met deze vacature te vergelijken.",
        "fr": "Téléversez un CV ci-dessus pour le comparer à cette offre.",
    },
    "match_note_skill_stale": {
        "en": "Found, but the most recent dated entry using it ended {years} years ago.",
        "de": "Gefunden, aber der jüngste datierte Eintrag damit endete vor {years} Jahren.",
        "uk": "Знайдено. Років від останнього датованого запису з цим: {years}.",
        "ru": "Найдено. Лет от последней датированной записи с этим: {years}.",
        "es": "Encontrado, pero la entrada fechada más reciente que lo usa terminó hace {years} años.",
        "nl": "Gevonden, maar de recentste gedateerde vermelding ervan eindigde {years} jaar geleden.",
        "fr": "Trouvé, mais la dernière entrée datée qui l'utilise s'est terminée il y a {years} ans.",
    },
    "match_gains_heading": {
        "en": "What would raise this most",
        "de": "Was am meisten bringen würde",
        "uk": "Що підніме результат найбільше",
        "ru": "Что поднимет результат больше всего",
        "es": "Qué subiría más esta puntuación",
        "nl": "Wat dit het meest zou verhogen",
        "fr": "Ce qui ferait le plus monter la note",
    },
    "match_gains_caption": {
        "en": "Each line is what the score would gain if that one requirement were met. Required items are weighted three times preferred ones, so the order is not the order of the gaps list.",
        "de": "Jede Zeile zeigt, was die Bewertung gewinnen würde, wenn genau diese Anforderung erfüllt wäre. Pflichtpunkte zählen dreifach gegenüber gewünschten, die Reihenfolge ist also nicht die der Lückenliste.",
        "uk": "Кожен рядок — це те, що додасть оцінці виконання саме цієї вимоги. Обов'язкові пункти важать утричі більше за бажані, тож порядок тут не такий, як у списку прогалин.",
        "ru": "Каждая строка — это то, что добавит оценке выполнение именно этого требования. Обязательные пункты весят втрое больше желательных, поэтому порядок здесь не такой, как в списке пробелов.",
        "es": "Cada línea es lo que ganaría la puntuación si se cumpliera ese requisito. Los obligatorios pesan el triple que los preferentes, así que el orden no es el de la lista de carencias.",
        "nl": "Elke regel is wat de score erbij krijgt als juist die eis vervuld zou zijn. Vereiste punten wegen drie keer zo zwaar als gewenste, dus de volgorde is niet die van de lijst met hiaten.",
        "fr": "Chaque ligne indique ce que la note gagnerait si cette exigence était remplie. Les critères obligatoires pèsent trois fois plus que les souhaités : l'ordre n'est donc pas celui de la liste des manques.",
    },
    "match_gain_points": {
        "en": "+{points}",
        "de": "+{points}",
        "uk": "+{points}",
        "ru": "+{points}",
        "es": "+{points}",
        "nl": "+{points}",
        "fr": "+{points}",
    },
    "match_stale_heading": {
        "en": "Matched, but not lately",
        "de": "Getroffen, aber nicht mehr aktuell",
        "uk": "Збіглося, але давно не використовувалось",
        "ru": "Совпало, но давно не использовалось",
        "es": "Coincide, pero no recientemente",
        "nl": "Komt overeen, maar niet recent",
        "fr": "Correspond, mais pas récemment",
    },
    "match_stale_caption": {
        "en": "The advert asks for these and your CV has them — in an entry that ended years ago. That is a fair interview question, and a good line to refresh with something recent.",
        "de": "Die Anzeige verlangt diese Punkte und Ihr Lebenslauf hat sie — in einem Eintrag, der vor Jahren endete. Das ist eine faire Frage im Gespräch und eine gute Zeile, die man mit etwas Aktuellem auffrischt.",
        "uk": "Вакансія просить це, і у вашому резюме воно є — у записі, який завершився роками раніше. Це справедливе питання на співбесіді й хороший рядок, щоб освіжити чимось свіжішим.",
        "ru": "Вакансия просит это, и в вашем резюме оно есть — в записи, которая закончилась годы назад. Это справедливый вопрос на собеседовании и хорошая строка, чтобы освежить чем-то недавним.",
        "es": "La oferta pide esto y tu CV lo tiene, en una entrada que terminó hace años. Es una pregunta justa en una entrevista y una buena línea para refrescar con algo reciente.",
        "nl": "De vacature vraagt hierom en je cv heeft het — in een vermelding die jaren geleden eindigde. Dat is een eerlijke vraag in een gesprek en een goede regel om met iets recents op te frissen.",
        "fr": "L'offre demande cela et votre CV l'a — dans une entrée terminée il y a des années. C'est une question légitime en entretien, et une bonne ligne à rafraîchir avec quelque chose de récent.",
    },
    "match_note_skill_at_risk": {
        "en": "{skill} was found only in the layout-aware read.",
        "de": "{skill} wurde nur beim layoutbewussten Lesen gefunden.",
        "uk": "{skill} знайдено лише при читанні з урахуванням верстки.",
        "ru": "{skill} найдено только при чтении с учётом вёрстки.",
        "es": "{skill} solo apareció en la lectura consciente del diseño.",
        "nl": "{skill} werd alleen bij layoutbewust lezen gevonden.",
        "fr": "{skill} : trouvé uniquement en lecture attentive à la mise en page.",

    },
    "match_note_experience": {
        "en": "Your CV shows about {have} years; the ad asks for {want}.",
        "de": "Ihr Lebenslauf zeigt etwa {have} Jahre; gefordert: {want}.",
        "uk": "Років досвіду в резюме: близько {have}; у вакансії: {want}.",
        "ru": "Лет опыта в резюме: около {have}; в вакансии: {want}.",
        "es": "Tu CV muestra unos {have} años; la oferta pide {want}.",
        "nl": "Je cv toont ongeveer {have} jaar; de vacature vraagt {want} jaar.",
        "fr": "Votre CV indique environ {have} ans ; l'offre en demande {want}.",

    },
    "match_note_education_ok": {
        "en": "Your {have} covers the requested {want}.",
        "de": "Ihr Abschluss ({have}) deckt die geforderte Stufe ({want}) ab.",
        "uk": "Ваш рівень ({have}) покриває потрібний ({want}).",
        "ru": "Ваш уровень ({have}) покрывает требуемый ({want}).",
        "es": "Tu nivel ({have}) cubre el nivel solicitado ({want}).",
        "nl": "Je niveau ({have}) dekt het gevraagde niveau ({want}).",
        "fr": "Votre niveau ({have}) couvre le niveau demandé ({want}).",

    },
    "match_note_education_lower": {
        "en": "The ad asks for {want}; your CV shows {have}.",
        "de": "Die Anzeige verlangt {want}; Ihr Lebenslauf zeigt {have}.",
        "uk": "Вакансія вимагає рівня «{want}»; у резюме — «{have}».",
        "ru": "Вакансия требует уровня «{want}»; в резюме — «{have}».",
        "es": "La oferta pide {want}; tu CV muestra {have}.",
        "nl": "De vacature vraagt {want}; je cv toont {have}.",
        "fr": "L'offre demande {want} ; votre CV indique {have}.",
    },
    "match_note_education_missing": {
        "en": "No degree or completed training was found in your CV; the ad asks for {want}.",
        "de": "Im Lebenslauf wurde kein Abschluss gefunden; die Anzeige verlangt {want}.",
        "uk": "У резюме не знайдено освіти; вакансія вимагає: {want}.",
        "ru": "В резюме не найдено образования; вакансия требует: {want}.",
        "es": "No se encontró titulación en tu CV; la oferta pide {want}.",
        "nl": "In je cv is geen opleiding gevonden; de vacature vraagt {want}.",
        "fr": "Aucun diplôme n'a été trouvé dans votre CV ; l'offre demande {want}.",
    },
    "match_note_education_field": {
        "en": "The level fits, but the ad names {want} and your CV says {have}.",
        "de": "Die Stufe passt, aber die Anzeige nennt {want}, Ihr Lebenslauf {have}.",
        "uk": "Рівень підходить, але у вакансії — «{want}», а в резюме — «{have}».",
        "ru": "Уровень подходит, но в вакансии — «{want}», а в резюме — «{have}».",
        "es": "El nivel encaja, pero la oferta menciona {want} y tu CV dice {have}.",
        "nl": "Het niveau past, maar de vacature vermeldt {want} en je cv {have}.",
        "fr": "Le niveau convient, mais l'offre mentionne {want} et votre CV indique {have}.",

    },
    "match_note_language": {
        "en": "{lang}: your CV shows {have}, the ad asks for {want}.",
        "de": "{lang}: Ihr Lebenslauf zeigt {have}, die Anzeige verlangt {want}.",
        "uk": "{lang}: у резюме {have}, вакансія вимагає {want}.",
        "ru": "{lang}: в резюме {have}, вакансия требует {want}.",
        "es": "{lang}: tu CV muestra {have}, la oferta pide {want}.",
        "nl": "{lang}: je cv toont {have}, de vacature vraagt {want}.",
        "fr": "{lang} : votre CV indique {have}, l'offre demande {want}.",
    },
    "match_note_language_missing": {
        "en": "{lang} is asked for but no level was found in your CV.",
        "de": "{lang} wird verlangt, im Lebenslauf wurde aber kein Niveau gefunden.",
        "uk": "{lang} вимагається, але рівня в резюме не знайдено.",
        "ru": "{lang} требуется, но уровня в резюме не найдено.",
        "es": "Se pide {lang} pero no se encontró ningún nivel en tu CV.",
        "nl": "{lang} wordt gevraagd, maar in je cv is geen niveau gevonden.",
        "fr": "{lang} est demandé mais aucun niveau n'a été trouvé dans votre CV.",
    },
    "tagline": {
        "en": "See what a CV parser reads before an employer's does",
        "de": "Sehen Sie, was ein Lebenslauf-Parser liest, bevor es der eines Arbeitgebers tut",
        "uk": "Дізнайтеся, що читає парсер резюме, раніше за роботодавця",
        "ru": "Узнайте, что читает парсер резюме, раньше работодателя",
        "es": "Comprueba qué lee un analizador de CV antes que el de la empresa",
        "nl": "Zie wat een cv-parser leest, voordat die van een werkgever dat doet",
        "fr": "Voyez ce qu'un analyseur de CV lit avant celui d'un employeur",
    },
    "language_menu": {
        "en": "Language",
        "de": "Sprache",
        "uk": "Мова",
        "ru": "Язык",
        "es": "Idioma",
        "nl": "Taal",
        "fr": "Langue",
    },
    "zone_upload_title": {
        "en": "Your CV",
        "de": "Ihr Lebenslauf",
        "uk": "Ваше резюме",
        "ru": "Ваше резюме",
        "es": "Tu CV",
        "nl": "Je cv",
        "fr": "Votre CV",
    },
    "zone_upload_note": {
        "en": "PDF or DOCX. Nothing is stored: the file is read, analysed and deleted within seconds.",
        "de": "PDF oder DOCX. Nichts wird gespeichert: Die Datei wird gelesen, ausgewertet und binnen Sekunden gelöscht.",
        "uk": "PDF або DOCX. Нічого не зберігається: файл читається, аналізується і за секунди видаляється.",
        "ru": "PDF или DOCX. Ничего не сохраняется: файл читается, анализируется и через секунды удаляется.",
        "es": "PDF o DOCX. No se guarda nada: el archivo se lee, se analiza y se borra en segundos.",
        "nl": "PDF of DOCX. Er wordt niets bewaard: het bestand wordt gelezen, geanalyseerd en binnen seconden verwijderd.",
        "fr": "PDF ou DOCX. Rien n'est conservé : le fichier est lu, analysé puis supprimé en quelques secondes.",
    },
    "zone_document_note": {
        "en": "Your pages as the parser sees them. Boxes mark the exact area each finding refers to.",
        "de": "Ihre Seiten, wie der Parser sie sieht. Die Rahmen markieren den genauen Bereich jedes Befunds.",
        "uk": "Ваші сторінки очима парсера. Рамки позначають точну ділянку кожного зауваження.",
        "ru": "Ваши страницы глазами парсера. Рамки отмечают точный участок каждого замечания.",
        "es": "Tus páginas como las ve el analizador. Los recuadros marcan el área exacta de cada hallazgo.",
        "nl": "Je pagina's zoals de parser ze ziet. De kaders markeren precies het gebied van elke bevinding.",
        "fr": "Vos pages telles que l'analyseur les voit. Les cadres marquent la zone exacte de chaque constat.",
    },
    "zone_fixes_note": {
        "en": "Every finding, what it does to your file, and the steps that fix it.",
        "de": "Jeder Befund, seine Wirkung auf Ihre Datei und die Schritte, die ihn beheben.",
        "uk": "Кожне зауваження, що воно робить із вашим файлом, і кроки, які це виправляють.",
        "ru": "Каждое замечание, что оно делает с вашим файлом, и шаги, которые это исправляют.",
        "es": "Cada hallazgo, qué le hace a tu archivo y los pasos que lo corrigen.",
        "nl": "Elke bevinding, wat die met je bestand doet en de stappen die het oplossen.",
        "fr": "Chaque constat, son effet sur votre fichier et les étapes qui le corrigent.",
    },
    "jump_nav_label": {
        "en": "Zones",
        "de": "Bereiche",
        "uk": "Розділи",
        "ru": "Разделы",
        "es": "Secciones",
        "nl": "Zones",
        "fr": "Sections",
    },
    "jump_plan": {
        "en": "What to do",
        "de": "Was zu tun ist",
        "uk": "Що робити",
        "ru": "Что делать",
        "es": "Qué hacer",
        "nl": "Wat te doen",
        "fr": "Que faire",
    },
    "zone_plan_title": {
        "en": "What to do",
        "de": "Was zu tun ist",
        "uk": "Що робити",
        "ru": "Что делать",
        "es": "Qué hacer",
        "nl": "Wat te doen",
        "fr": "Que faire",
    },
    "zone_plan_note": {
        "en": "Everything above, as one list in the order worth doing it. Copy it and work down.",
        "de": "Alles von oben als eine Liste, in der Reihenfolge, in der es sich lohnt. Kopieren und abarbeiten.",
        "uk": "Усе вище — одним списком у тому порядку, у якому це варто робити. Скопіюйте й ідіть згори вниз.",
        "ru": "Всё выше — одним списком в том порядке, в котором это стоит делать. Скопируйте и идите сверху вниз.",
        "es": "Todo lo anterior en una sola lista, en el orden en que conviene hacerlo. Cópiala y ve bajando.",
        "nl": "Alles hierboven als één lijst, in de volgorde waarin het de moeite waard is. Kopieer en werk hem af.",
        "fr": "Tout ce qui précède en une seule liste, dans l'ordre où cela vaut la peine. Copiez-la et descendez.",
    },
    "plan_add": {
        "en": "Add {item} to your CV, in the entry where you actually used it — worth about {points} points on this advert.",
        "de": "Ergänzen Sie {item} im Lebenslauf, und zwar in dem Eintrag, in dem Sie es tatsächlich eingesetzt haben — etwa {points} Punkte bei dieser Anzeige.",
        "uk": "Додайте {item} до резюме — саме в той запис, де ви це справді робили. Це близько {points} балів для цієї вакансії.",
        "ru": "Добавьте {item} в резюме — именно в ту запись, где вы это действительно делали. Это около {points} баллов для этой вакансии.",
        "es": "Añade {item} a tu CV, en la entrada donde realmente lo usaste: vale unos {points} puntos en esta oferta.",
        "nl": "Voeg {item} toe aan je cv, in de vermelding waar je het echt hebt gebruikt — ongeveer {points} punten bij deze vacature.",
        "fr": "Ajoutez {item} à votre CV, dans l'entrée où vous vous en êtes réellement servi — environ {points} points sur cette offre.",
    },
    "plan_refresh": {
        "en": "Refresh {item} with something recent: the newest dated entry using it ended {years} years ago.",
        "de": "Frischen Sie {item} mit etwas Aktuellem auf: der jüngste datierte Eintrag damit endete vor {years} Jahren.",
        "uk": "Освіжіть {item} чимось свіжішим. Років від останнього датованого запису: {years}.",
        "ru": "Освежите {item} чем-то недавним. Лет от последней датированной записи: {years}.",
        "es": "Refresca {item} con algo reciente: la entrada fechada más nueva que lo usa terminó hace {years} años.",
        "nl": "Fris {item} op met iets recents: de nieuwste gedateerde vermelding ervan eindigde {years} jaar geleden.",
        "fr": "Rafraîchissez {item} avec quelque chose de récent : la dernière entrée datée qui l'utilise s'est terminée il y a {years} ans.",
    },
    "plan_header": {
        "en": "What to change in {name}",
        "de": "Was an {name} zu ändern ist",
        "uk": "Що змінити у файлі {name}",
        "ru": "Что изменить в файле {name}",
        "es": "Qué cambiar en {name}",
        "nl": "Wat te wijzigen in {name}",
        "fr": "Que changer dans {name}",
    },
    "plan_nothing": {
        "en": "Nothing to change. The file parses cleanly, and where an advert was pasted, everything it asked for was found.",
        "de": "Nichts zu ändern. Die Datei wird sauber gelesen, und wo eine Anzeige eingefügt wurde, war alles Verlangte vorhanden.",
        "uk": "Змінювати нічого. Файл читається чисто, а там, де вставлено вакансію, знайшлося все, що вона просила.",
        "ru": "Менять нечего. Файл читается чисто, а там, где вставлена вакансия, нашлось всё, что она просила.",
        "es": "Nada que cambiar. El archivo se analiza sin problemas y, donde se pegó una oferta, se encontró todo lo que pedía.",
        "nl": "Niets te wijzigen. Het bestand wordt schoon gelezen en waar een vacature is geplakt, is alles gevonden wat die vroeg.",
        "fr": "Rien à changer. Le fichier s'analyse sans problème et, là où une offre a été collée, tout ce qu'elle demandait a été trouvé.",
    },
    "plan_no_advert": {
        "en": "Paste a job advert in section 03 and this list also covers what that advert asks for.",
        "de": "Fügen Sie in Abschnitt 03 eine Stellenanzeige ein, dann deckt diese Liste auch deren Anforderungen ab.",
        "uk": "Вставте опис вакансії в розділі 03 — і цей список охопить також те, що просить вона.",
        "ru": "Вставьте описание вакансии в разделе 03 — и этот список охватит также то, что просит она.",
        "es": "Pega una oferta en la sección 03 y esta lista cubrirá también lo que esa oferta pide.",
        "nl": "Plak een vacature in sectie 03, dan dekt deze lijst ook wat die vacature vraagt.",
        "fr": "Collez une offre dans la section 03 et cette liste couvrira aussi ce qu'elle demande.",
    },
    "plan_copy_hint": {
        "en": "Use the copy button in the corner of the box.",
        "de": "Nutzen Sie die Kopierschaltfläche in der Ecke des Feldes.",
        "uk": "Скористайтеся кнопкою копіювання в кутку блоку.",
        "ru": "Воспользуйтесь кнопкой копирования в углу блока.",
        "es": "Usa el botón de copiar en la esquina del cuadro.",
        "nl": "Gebruik de kopieerknop in de hoek van het vak.",
        "fr": "Utilisez le bouton copier dans le coin de l'encadré.",
    },
    "jump_document": {
        "en": "Document",
        "de": "Dokument",
        "uk": "Документ",
        "ru": "Документ",
        "es": "Documento",
        "nl": "Document",
        "fr": "Document",
    },
    "jump_match": {
        "en": "Job match",
        "de": "Abgleich",
        "uk": "Вакансія",
        "ru": "Вакансия",
        "es": "Oferta",
        "nl": "Vacature",
        "fr": "Offre",
    },
    "jump_fixes": {
        "en": "Fixes",
        "de": "Korrekturen",
        "uk": "Виправлення",
        "ru": "Исправления",
        "es": "Correcciones",
        "nl": "Correcties",
        "fr": "Corrections",
    },
    "file_loaded": {
        "en": "{name} — {pages} page(s) read",
        "de": "{name} — {pages} Seite(n) gelesen",
        "uk": "{name} — прочитано сторінок: {pages}",
        "ru": "{name} — прочитано страниц: {pages}",
        "es": "{name} — {pages} página(s) leída(s)",
        "nl": "{name} — {pages} pagina('s) gelezen",
        "fr": "{name} — {pages} page(s) lue(s)",
    },
    "issue_tally": {
        "en": "{high} serious · {medium} moderate · {low} minor",
        "de": "schwerwiegend: {high} · mittel: {medium} · gering: {low}",
        "uk": "серйозні: {high} · середні: {medium} · незначні: {low}",
        "ru": "серьёзные: {high} · средние: {medium} · незначительные: {low}",
        "es": "graves: {high} · moderados: {medium} · leves: {low}",
        "nl": "ernstig: {high} · matig: {medium} · gering: {low}",
        "fr": "graves : {high} · moyens : {medium} · mineurs : {low}",

    },
    "empty_hint": {
        "en": "Once a file is loaded you will see its pages with the problem areas boxed, a readability score, and, if you paste a job ad, how much of that ad your CV covers.",
        "de": "Sobald eine Datei geladen ist, sehen Sie Ihre Seiten mit umrahmten Problemstellen, eine Lesbarkeitsbewertung und, wenn Sie eine Stellenanzeige einfügen, wie viel davon Ihr Lebenslauf abdeckt.",
        "uk": "Щойно файл завантажено, ви побачите сторінки з обведеними проблемними місцями, оцінку читабельності та, якщо вставите вакансію, наскільки резюме її покриває.",
        "ru": "Как только файл загружен, вы увидите страницы с обведёнными проблемными местами, оценку читаемости и, если вставите вакансию, насколько резюме её покрывает.",
        "es": "Cuando cargues un archivo verás sus páginas con las zonas problemáticas recuadradas, una puntuación de legibilidad y, si pegas una oferta, cuánto cubre tu CV.",
        "nl": "Zodra een bestand geladen is zie je de pagina's met omkaderde probleemgebieden, een leesbaarheidsscore en, als je een vacature plakt, hoeveel daarvan je cv dekt.",
        "fr": "Une fois un fichier chargé, vous verrez vos pages avec les zones problématiques encadrées, un score de lisibilité et, si vous collez une offre, ce que votre CV en couvre.",
    },
    "match_gaps_heading": {
        "en": "Not covered",
        "de": "Nicht abgedeckt",
        "uk": "Немає в резюме",
        "ru": "Нет в резюме",
        "es": "Sin cubrir",
        "nl": "Niet gedekt",
        "fr": "Non couvert",
    },
    "match_partly_tag": {
        "en": "partly",
        "de": "teilweise",
        "uk": "частково",
        "ru": "частично",
        "es": "en parte",
        "nl": "deels",
        "fr": "en partie",
    },
    "match_note_licence_missing": {
        "en": "The ad asks for a driving licence and none was found in your CV.",
        "de": "Die Anzeige verlangt einen Führerschein; im Lebenslauf wurde keiner gefunden.",
        "uk": "Вакансія вимагає посвідчення водія, у резюме його не знайдено.",
        "ru": "Вакансия требует водительское удостоверение, в резюме его не найдено.",
        "es": "La oferta pide carné de conducir y no se encontró ninguno en tu CV.",
        "nl": "De vacature vraagt een rijbewijs; in je cv is er geen gevonden.",
        "fr": "L'offre demande un permis de conduire, introuvable dans votre CV.",
    },
    "evidence_volunteering": {
        "en": "Listed under work experience: {text}",
        "de": "Unter Berufserfahrung aufgeführt: {text}",
        "uk": "Вказано в досвіді роботи: {text}",
        "ru": "Указано в опыте работы: {text}",
        "es": "Incluido en la experiencia laboral: {text}",
        "nl": "Vermeld onder werkervaring: {text}",
        "fr": "Indiqué dans l'expérience professionnelle : {text}",
    },
    "evidence_volunteering_starter": {
        "en": "Listed under work experience, beside little dated paid experience: {text}",
        "de": "Unter Berufserfahrung aufgeführt, neben wenig datierter Berufserfahrung: {text}",
        "uk": "Вказано в досвіді роботи поруч із невеликим датованим досвідом: {text}",
        "ru": "Указано в опыте работы рядом с небольшим датированным опытом: {text}",
        "es": "Incluido en la experiencia laboral, junto a poca experiencia fechada: {text}",
        "nl": "Vermeld onder werkervaring, naast weinig gedateerde ervaring: {text}",
        "fr": "Indiqué dans l'expérience professionnelle, à côté de peu d'expérience datée : {text}",
    },
    "evidence_gap": {
        "en": "Gaps: {count}. Longest: {start} – {end}, months: {months}.",
        "de": "Lücken: {count}. Längste: {start} – {end}, Monate: {months}.",
        "uk": "Перерв: {count}. Найдовша: {start} – {end}, місяців: {months}.",
        "ru": "Перерывов: {count}. Самый длинный: {start} – {end}, месяцев: {months}.",
        "es": "Huecos: {count}. El más largo: {start} – {end}, meses: {months}.",
        "nl": "Gaten: {count}. Langste: {start} – {end}, maanden: {months}.",
        "fr": "Périodes vides : {count}. La plus longue : {start} – {end}, mois : {months}.",
    },
    "evidence_date_backwards": {
        "en": "Ends before it starts: {text}",
        "de": "Endet vor dem Beginn: {text}",
        "uk": "Закінчується раніше, ніж починається: {text}",
        "ru": "Заканчивается раньше, чем начинается: {text}",
        "es": "Termina antes de empezar: {text}",
        "nl": "Eindigt voordat hij begint: {text}",
        "fr": "Se termine avant de commencer : {text}",
    },
    "evidence_date_future": {
        "en": "More than two years in the future: {text}",
        "de": "Mehr als zwei Jahre in der Zukunft: {text}",
        "uk": "Більш ніж на два роки вперед: {text}",
        "ru": "Более чем на два года вперёд: {text}",
        "es": "Más de dos años en el futuro: {text}",
        "nl": "Meer dan twee jaar in de toekomst: {text}",
        "fr": "Plus de deux ans dans le futur : {text}",
    },
    "evidence_first_person": {
        "en": "First-person forms outside the profile: {count}. For example: {text}",
        "de": "Ich-Formen außerhalb des Kurzprofils: {count}. Zum Beispiel: {text}",
        "uk": "Форм першої особи поза профілем: {count}. Наприклад: {text}",
        "ru": "Форм первого лица вне профиля: {count}. Например: {text}",
        "es": "Formas en primera persona fuera del perfil: {count}. Por ejemplo: {text}",
        "nl": "Ik-vormen buiten het profiel: {count}. Bijvoorbeeld: {text}",
        "fr": "Formes à la première personne hors du profil : {count}. Par exemple : {text}",
    },
    "evidence_outdated_details": {
        "en": "Fields found: {text}",
        "de": "Gefundene Angaben: {text}",
        "uk": "Знайдені поля: {text}",
        "ru": "Найденные поля: {text}",
        "es": "Campos encontrados: {text}",
        "nl": "Gevonden velden: {text}",
        "fr": "Champs trouvés : {text}",
    },
    "evidence_oldest_first": {
        "en": "Starts with {first} and ends with {last}.",
        "de": "Beginnt mit {first} und endet mit {last}.",
        "uk": "Починається з {first} і закінчується {last}.",
        "ru": "Начинается с {first} и заканчивается {last}.",
        "es": "Empieza por {first} y termina en {last}.",
        "nl": "Begint met {first} en eindigt met {last}.",
        "fr": "Commence par {first} et se termine par {last}.",
    },
    "finding_kind_convention": {
        "en": "CV CONVENTION",
        "de": "LEBENSLAUF-KONVENTION",
        "uk": "КОНВЕНЦІЯ РЕЗЮМЕ",
        "ru": "КОНВЕНЦИЯ РЕЗЮМЕ",
        "es": "CONVENCIÓN DEL CV",
        "nl": "CV-CONVENTIE",
        "fr": "CONVENTION DU CV",
    },
    "convention_not_scored": {
        "en": "This is about what the CV says, not how software reads it, so it does not change the score out of 100.",
        "de": "Es geht darum, was der Lebenslauf aussagt, nicht wie Software ihn liest — deshalb ändert es die Punktzahl von 100 nicht.",
        "uk": "Це про те, що каже резюме, а не про те, як його читає програма, тож на оцінку зі 100 не впливає.",
        "ru": "Это о том, что говорит резюме, а не о том, как его читает программа, поэтому на оценку из 100 не влияет.",
        "es": "Esto trata de lo que dice el CV, no de cómo lo lee el software, así que no cambia la puntuación sobre 100.",
        "nl": "Dit gaat over wat het cv zegt, niet over hoe software het leest, dus het verandert de score van 100 niet.",
        "fr": "Il s'agit de ce que dit le CV, pas de la façon dont un logiciel le lit : cela ne modifie donc pas la note sur 100.",
    },
}


VOCABULARY: dict[str, dict[str, str]] = {
    "email": {
        "en": "email address",
        "de": "E-Mail-Adresse",
        "uk": "електронна пошта",
        "ru": "электронная почта",
        "es": "correo electrónico",
        "nl": "e-mailadres",
        "fr": "adresse e-mail",
    },
    "phone": {
        "en": "phone number",
        "de": "Telefonnummer",
        "uk": "номер телефону",
        "ru": "номер телефона",
        "es": "número de teléfono",
        "nl": "telefoonnummer",
        "fr": "numéro de téléphone",
    },
    "header": {
        "en": "header",
        "de": "Kopfzeile",
        "uk": "верхній колонтитул",
        "ru": "верхний колонтитул",
        "es": "encabezado",
        "nl": "koptekst",
        "fr": "en-tête",
    },
    "footer": {
        "en": "footer",
        "de": "Fußzeile",
        "uk": "нижній колонтитул",
        "ru": "нижний колонтитул",
        "es": "pie de página",
        "nl": "voettekst",
        "fr": "pied de page",
    },
    "experience": {
        "en": "Experience",
        "de": "Berufserfahrung",
        "uk": "Досвід",
        "ru": "Опыт",
        "es": "Experiencia",
        "nl": "Werkervaring",
        "fr": "Expérience",
    },
    "education": {
        "en": "Education",
        "de": "Ausbildung",
        "uk": "Освіта",
        "ru": "Образование",
        "es": "Formación",
        "nl": "Opleiding",
        "fr": "Formation",
    },
    "skills": {
        "en": "Skills",
        "de": "Kenntnisse",
        "uk": "Навички",
        "ru": "Навыки",
        "es": "Competencias",
        "nl": "Vaardigheden",
        "fr": "Compétences",
    },
    "ausbildung": {
        "en": "vocational training",
        "de": "Ausbildung",
        "uk": "профтехосвіта",
        "ru": "профобразование",
        "es": "formación profesional",
        "nl": "beroepsopleiding",
        "fr": "formation professionnelle",
    },
    "bachelor": {
        "en": "Bachelor",
        "de": "Bachelor",
        "uk": "бакалавр",
        "ru": "бакалавр",
        "es": "grado",
        "nl": "bachelor",
        "fr": "licence",
    },
    "master": {
        "en": "Master",
        "de": "Master",
        "uk": "магістр",
        "ru": "магистр",
        "es": "máster",
        "nl": "master",
        "fr": "master",
    },
    "doctorate": {
        "en": "doctorate",
        "de": "Promotion",
        "uk": "докторський ступінь",
        "ru": "докторская степень",
        "es": "doctorado",
        "nl": "doctoraat",
        "fr": "doctorat",
    },
    "informatik": {
        "en": "computer science",
        "de": "Informatik",
        "uk": "інформатика",
        "ru": "информатика",
        "es": "informática",
        "nl": "informatica",
        "fr": "informatique",
    },
    "engineering": {
        "en": "engineering",
        "de": "Ingenieurwesen",
        "uk": "інженерія",
        "ru": "инженерия",
        "es": "ingeniería",
        "nl": "techniek",
        "fr": "ingénierie",
    },
    "mathematics": {
        "en": "mathematics",
        "de": "Mathematik",
        "uk": "математика",
        "ru": "математика",
        "es": "matemáticas",
        "nl": "wiskunde",
        "fr": "mathématiques",
    },
    "business": {
        "en": "business studies",
        "de": "Betriebswirtschaft",
        "uk": "менеджмент",
        "ru": "менеджмент",
        "es": "empresariales",
        "nl": "bedrijfskunde",
        "fr": "gestion",
    },
}
"""Internal identifiers that end up inside a translated sentence.

The findings and the score carry evidence as data -- which section was
lost, which contact detail was missing, which zone a repeated line sat in
-- and those values are the words the code uses, in English and lowercase.
They were being interpolated straight into every locale, so a German
reader was told "email gefunden, aber kein phone" and a Ukrainian one
"Знайдено email, але немає phone".

Translating at render time rather than at analysis time is what keeps the
analysis language-independent: the same Finding renders in seven
languages."""

TRANSLATED_PARAMS = frozenset(
    {"found", "missing", "zone", "have", "want", "lost", "section", "sections"}
)

RULE_LIST_PARAMS = frozenset({"deductions"})
"""Placeholders holding (rule id, penalty) pairs rather than text.

The score subtracts points per rule and has to say which rules, but it
runs before a language is chosen -- so it passes the pairs through and
they are named here, at render time, like every other token."""
"""Which placeholders hold vocabulary rather than free text.

Named explicitly so a font called "Master" or a keyword someone typed can
never be silently rewritten on its way to the screen."""


def term(token: str, language: str) -> str:
    """One vocabulary token in the reader's language, or the token itself."""
    entry = VOCABULARY.get(token)
    if entry is None:
        return token
    return entry.get(language) or entry.get(DEFAULT_LANGUAGE) or token


def _translate_params(params: dict, language: str) -> dict:
    translated = {}
    for name, value in params.items():
        if name in RULE_LIST_PARAMS:
            translated[name] = ", ".join(
                f"{rule_name(rule_id, language)} (-{penalty})" for rule_id, penalty in value
            )
            continue
        if name in TRANSLATED_PARAMS and isinstance(value, str):
            # A list of sections arrives already joined, so each piece is
            # translated and the separator is put back.
            translated[name] = ", ".join(term(part.strip(), language) for part in value.split(","))
        else:
            translated[name] = value
    return translated

def t(key: str, language: str, **kwargs) -> str:
    """Return the translated string, falling back to English when a language
    has no entry for it. Unknown keys surface as ``[key]`` rather than
    raising, so a typo shows up in the interface instead of taking the page
    down mid-render.
    """
    kwargs = _translate_params(kwargs, language)
    entry = TRANSLATIONS.get(key)
    if entry is None:
        return f"[{key}]"

    text = entry.get(language) or entry.get(DEFAULT_LANGUAGE, f"[{key}]")
    return text.format(**kwargs) if kwargs else text


PLURAL_FEW_LANGUAGES = frozenset({"uk", "ru"})
"""Languages with a distinct form for 2-4 alongside 1 and 5+."""


def _plural_form(count: int, language: str) -> str:
    """Which of one/few/many ``count`` takes in ``language``."""
    if language not in PLURAL_FEW_LANGUAGES:
        return "one" if count == 1 else "many"
    units, tens = count % 10, count % 100
    if units == 1 and tens != 11:
        return "one"
    if 2 <= units <= 4 and not 12 <= tens <= 14:
        return "few"
    return "many"


def tn(stem: str, count: int, language: str, **kwargs) -> str:
    """Translate a sentence whose wording depends on a count.

    English needs two forms, Ukrainian and Russian three, and picking
    between them in the calling code would mean writing the rule out again
    at every call site -- which is how "1 required item(s)" and "1 критична
    знахідка ставлять" got shipped. Callers pass the number; this picks the
    key.

    Falls back to ``stem_many`` when a language declares no form for the
    count, and to ``stem`` itself when there are no plural forms at all, so
    a key that never needed the machinery still resolves.
    """
    kwargs.setdefault("count", count)
    for candidate in (f"{stem}_{_plural_form(count, language)}", f"{stem}_many", stem):
        if candidate in TRANSLATIONS:
            return t(candidate, language, **kwargs)
    return f"[{stem}]"


RULE_NAMES: dict[str, dict[str, str]] = {
    "contact_only_as_link": {
        "en": "Contact only behind a link",
        "de": "Kontakt nur hinter einem Link",
        "uk": "Контакт лише за посиланням",
        "ru": "Контакт только за ссылкой",
        "es": "Contacto solo tras un enlace",
        "nl": "Contact alleen achter een link",
        "fr": "Contact seulement dans un lien",
    },
    "unrecognised_section_headings": {
        "en": "Headings a parser cannot place",
        "de": "Unbekannte Abschnittstitel",
        "uk": "Незнайомі заголовки розділів",
        "ru": "Незнакомые заголовки разделов",
        "es": "Títulos de sección no reconocidos",
        "nl": "Onbekende sectiekoppen",
        "fr": "Titres de section non reconnus",
    },
    "broken_characters": {
        "en": "Characters that break a word",
        "de": "Zeichen, die ein Wort zerbrechen",
        "uk": "Символи, що ламають слово",
        "ru": "Символы, ломающие слово",
        "es": "Caracteres que rompen la palabra",
        "nl": "Tekens die een woord breken",
        "fr": "Caractères qui cassent un mot",
    },
    "pdf_non_embedded_font": {
        "en": "Font not embedded",
        "de": "Schrift nicht eingebettet",
        "uk": "Шрифт не вбудовано",
        "ru": "Шрифт не встроен",
        "es": "Fuente no incrustada",
        "nl": "Lettertype niet ingesloten",
        "fr": "Police non intégrée",
    },
    "pdf_repeated_header_footer_content": {
        "en": "Header or footer repeats",
        "de": "Kopf- oder Fußzeile wiederholt sich",
        "uk": "Колонтитул повторюється",
        "ru": "Колонтитул повторяется",
        "es": "Encabezado o pie repetido",
        "nl": "Kop- of voettekst herhaalt zich",
        "fr": "En-tête ou pied répété",
    },
    "pdf_textless_image": {
        "en": "Image carries no text",
        "de": "Bild enthält keinen Text",
        "uk": "Зображення без тексту",
        "ru": "Изображение без текста",
        "es": "Imagen sin texto",
        "nl": "Afbeelding zonder tekst",
        "fr": "Image sans texte",
    },
    "docx_table_content": {
        "en": "Content inside a table",
        "de": "Inhalt in einer Tabelle",
        "uk": "Вміст усередині таблиці",
        "ru": "Содержимое внутри таблицы",
        "es": "Contenido dentro de una tabla",
        "nl": "Inhoud in een tabel",
        "fr": "Contenu dans un tableau",
    },
    "docx_header_footer_content": {
        "en": "Content in a header or footer",
        "de": "Inhalt in Kopf- oder Fußzeile",
        "uk": "Вміст у колонтитулі",
        "ru": "Содержимое в колонтитуле",
        "es": "Contenido en encabezado o pie",
        "nl": "Inhoud in kop- of voettekst",
        "fr": "Contenu en en-tête ou pied",
    },
    "docx_text_box_content": {
        "en": "Content inside a text box",
        "de": "Inhalt in einem Textfeld",
        "uk": "Вміст у текстовому полі",
        "ru": "Содержимое в текстовом поле",
        "es": "Contenido en un cuadro de texto",
        "nl": "Inhoud in een tekstvak",
        "fr": "Contenu dans une zone de texte",
    },
    "missing_contact_field": {
        "en": "No way to reach you",
        "de": "Keine Kontaktmöglichkeit",
        "uk": "Немає як з вами зв'язатися",
        "ru": "Нет способа с вами связаться",
        "es": "Sin forma de contacto",
        "nl": "Geen manier om je te bereiken",
        "fr": "Aucun moyen de vous joindre",
    },
    "section_missing_under_naive_parsing": {
        "en": "Section lost without the layout",
        "de": "Abschnitt geht ohne Layout verloren",
        "uk": "Розділ зникає без верстки",
        "ru": "Раздел исчезает без вёрстки",
        "es": "Sección perdida sin el diseño",
        "nl": "Sectie verdwijnt zonder opmaak",
        "fr": "Section perdue sans la mise en page",
    },
    "volunteering_listed_as_employment": {
        "en": "Volunteering listed as a job",
        "de": "Ehrenamt als Berufserfahrung",
        "uk": "Волонтерство як досвід роботи",
        "ru": "Волонтерство как опыт работы",
        "es": "Voluntariado como empleo",
        "nl": "Vrijwilligerswerk als baan",
        "fr": "Bénévolat présenté comme emploi",
    },
    "unexplained_gap": {
        "en": "Unexplained gap in the dates",
        "de": "Unerklärte Lücke im Lebenslauf",
        "uk": "Непояснена перерва в датах",
        "ru": "Необъяснённый перерыв в датах",
        "es": "Hueco sin explicar en las fechas",
        "nl": "Onverklaard gat in de data",
        "fr": "Période vide non expliquée",
    },
    "impossible_dates": {
        "en": "Dates that cannot be true",
        "de": "Unmögliche Datumsangaben",
        "uk": "Неможливі дати",
        "ru": "Невозможные даты",
        "es": "Fechas imposibles",
        "nl": "Onmogelijke data",
        "fr": "Dates impossibles",
    },
    "first_person_in_cv": {
        "en": "Written as sentences about I",
        "de": "Ich-Sätze im Lebenslauf",
        "uk": "Речення від першої особи",
        "ru": "Предложения от первого лица",
        "es": "Frases en primera persona",
        "nl": "Zinnen in de ik-vorm",
        "fr": "Phrases à la première personne",
    },
    "outdated_personal_details": {
        "en": "Outdated personal details",
        "de": "Veraltete persönliche Angaben",
        "uk": "Застарілі особисті дані",
        "ru": "Устаревшие личные данные",
        "es": "Datos personales obsoletos",
        "nl": "Verouderde persoonsgegevens",
        "fr": "Données personnelles superflues",
    },
    "oldest_entry_first": {
        "en": "Oldest job listed first",
        "de": "Älteste Station zuerst",
        "uk": "Найстаріша посада першою",
        "ru": "Самая старая должность первой",
        "es": "El empleo más antiguo primero",
        "nl": "Oudste baan bovenaan",
        "fr": "Poste le plus ancien en premier",
    },
}
"""A short name for each rule, for the places a reader meets one in
passing rather than in full.

The rule id is what the code calls it: lowercase, English, underscored.
That is right in a stack trace and wrong under a page image, where it read
as "Page 1 — section_missing_under_naive_parsing", and wrong again in the
score breakdown, which listed "Abzüge: docx_table_content (-25)" to a
German reader.

Short enough to sit inside a caption, and phrased as what is wrong rather
than as a category: "Content inside a table", not "Table content"."""


def _for_rule(table: dict[str, dict], rule_id: str, language: str, missing):
    """One rule's wording from one of the per-rule tables.

    The reader's language if it is there, English if it is not, and
    ``missing`` when the rule has no entry at all. Five tables are read this
    way and each had its own copy of those three lines, which made the
    fallback policy five decisions instead of one -- and the interesting
    thing about the policy is that it is uniform, since a half-translated
    interface is worse than an English one.

    What is not uniform is ``missing``, so that stays with each accessor:
    what to show for a rule nobody has written about yet differs by where it
    appears on the page, and each of them says why."""
    entry = table.get(rule_id) or {}
    return entry.get(language) or entry.get(DEFAULT_LANGUAGE) or missing


def rule_name(rule_id: str, language: str) -> str:
    """The reader's name for a rule, falling back to the id.

    A rule with no entry shows its id rather than an empty caption, which
    is ugly on purpose: the test suite fails on a missing name, so the only
    way to see one is to have added a rule and not this."""
    return _for_rule(RULE_NAMES, rule_id, language, rule_id)


RULE_DESCRIPTIONS: dict[str, dict[str, str]] = {
    "contact_only_as_link": {
        "en": "The only route to the candidate is a hyperlink — a LinkedIn or portfolio profile, or a mailto: — with no email address or phone number written out as text. The link text is what a parser reads; the address behind it lives in an annotation most extractors never open.",
        "de": "Der einzige Weg zur Bewerberin oder zum Bewerber ist ein Hyperlink — ein LinkedIn- oder Portfolio-Profil oder ein mailto: — ohne ausgeschriebene E-Mail-Adresse oder Telefonnummer. Ein Parser liest den Linktext; die Adresse dahinter steht in einer Anmerkung, die die meisten Extraktoren nie öffnen.",
        "uk": "Єдиний шлях до кандидата — гіперпосилання: профіль LinkedIn чи портфоліо або mailto: — без виписаної текстом адреси чи номера телефону. Парсер читає текст посилання; сама адреса лежить в анотації, яку більшість екстракторів ніколи не відкриває.",
        "ru": "Единственный путь к кандидату — гиперссылка: профиль LinkedIn или портфолио либо mailto: — без выписанного текстом адреса или номера телефона. Парсер читает текст ссылки; сам адрес лежит в аннотации, которую большинство экстракторов никогда не открывает.",
        "es": "La única vía hacia la persona candidata es un hipervínculo — un perfil de LinkedIn o de portafolio, o un mailto: — sin correo ni teléfono escritos como texto. Un analizador lee el texto del enlace; la dirección que hay detrás vive en una anotación que casi ningún extractor abre.",
        "nl": "De enige weg naar de kandidaat is een hyperlink — een LinkedIn- of portfolioprofiel, of een mailto: — zonder uitgeschreven e-mailadres of telefoonnummer. Een parser leest de linktekst; het adres erachter staat in een annotatie die de meeste extractors nooit openen.",
        "fr": "Le seul chemin vers la personne candidate est un lien — un profil LinkedIn ou de portfolio, ou un mailto: — sans adresse e-mail ni numéro écrits en toutes lettres. Un analyseur lit le texte du lien ; l'adresse derrière se trouve dans une annotation que presque aucun extracteur n'ouvre.",
    },
    "unrecognised_section_headings": {
        "en": "The document is organised under headings, but none of them is a heading a parser recognises. Software finds Experience and Education by their names; under invented labels the content is read as one undifferentiated block, and no history can be mapped to a role or a date.",
        "de": "Das Dokument ist in Abschnitte gegliedert, aber keine der Überschriften ist eine, die ein Parser kennt. Software findet Berufserfahrung und Ausbildung über ihre Namen; unter erfundenen Titeln wird der Inhalt als ein einziger Block gelesen, und kein Werdegang lässt sich einer Rolle oder einem Datum zuordnen.",
        "uk": "Документ поділено на розділи, але жоден заголовок не є тим, який парсер упізнає. Програма знаходить досвід і освіту за їхніми назвами; під вигаданими підписами вміст читається як один суцільний блок, і жоден запис не прив'язати ні до посади, ні до дати.",
        "ru": "Документ разделён на разделы, но ни один заголовок не из тех, что парсер узнаёт. Программа находит опыт и образование по их названиям; под придуманными подписями содержимое читается как один сплошной блок, и ни одну запись не привязать ни к должности, ни к дате.",
        "es": "El documento está organizado en secciones, pero ninguno de sus títulos es uno que un analizador reconozca. El software encuentra Experiencia y Formación por su nombre; bajo etiquetas inventadas el contenido se lee como un solo bloque y ningún historial puede asociarse a un puesto o a una fecha.",
        "nl": "Het document is ingedeeld met koppen, maar geen ervan is een kop die een parser herkent. Software vindt werkervaring en opleiding aan hun naam; onder verzonnen labels wordt de inhoud als één ongedeeld blok gelezen en is geen loopbaan aan een functie of datum te koppelen.",
        "fr": "Le document est organisé en sections, mais aucun de ses titres n'est un titre qu'un analyseur reconnaît. Un logiciel repère l'expérience et la formation à leur nom ; sous des libellés inventés, le contenu est lu comme un seul bloc et aucun parcours ne peut être rattaché à un poste ou à une date.",
    },
    "broken_characters": {
        "en": "A word contains characters that are not the letters they look like: a typographic ligature, an invisible soft hyphen or zero-width space, or a mix of Latin and Cyrillic. The word reads normally on screen and matches nothing a recruiter searches for.",
        "de": "Ein Wort enthält Zeichen, die nicht die Buchstaben sind, nach denen sie aussehen: eine typografische Ligatur, ein unsichtbares weiches Trennzeichen oder ein Nullbreiten-Leerzeichen, oder eine Mischung aus Latein und Kyrillisch. Am Bildschirm liest sich das Wort normal und trifft doch keine Suche.",
        "uk": "Слово містить символи, які не є тими літерами, на які схожі: типографська лігатура, невидимий м'який перенос чи пробіл нульової ширини, або суміш латиниці з кирилицею. На екрані слово читається нормально, а в пошуку не знаходиться.",
        "ru": "Слово содержит символы, которые не являются теми буквами, на которые похожи: типографская лигатура, невидимый мягкий перенос или пробел нулевой ширины, либо смесь латиницы с кириллицей. На экране слово читается нормально, а в поиске не находится.",
        "es": "Una palabra contiene caracteres que no son las letras que aparentan: una ligadura tipográfica, un guion suave o un espacio de ancho cero invisibles, o una mezcla de latino y cirílico. En pantalla la palabra se lee con normalidad y no aparece en ninguna búsqueda.",
        "nl": "Een woord bevat tekens die niet de letters zijn waar ze op lijken: een typografische ligatuur, een onzichtbaar zacht afbreekteken of spatie zonder breedte, of een mengeling van Latijn en Cyrillisch. Op het scherm leest het woord normaal en toch vindt geen zoekopdracht het.",
        "fr": "Un mot contient des caractères qui ne sont pas les lettres qu'ils semblent être : une ligature typographique, un trait d'union conditionnel ou une espace sans chasse invisibles, ou un mélange de latin et de cyrillique. À l'écran le mot se lit normalement et aucune recherche ne le trouve.",
    },
    "pdf_non_embedded_font": {
        "en": (
            "A font used in the PDF is not embedded and is not one of the 14 standard PDF "
            "base fonts. Non-embedded, non-standard fonts risk character-mapping issues "
            "that cause garbled or missing text during parsing."
        ),
        "de": (
            "Eine im PDF verwendete Schrift ist nicht eingebettet und gehört nicht zu den 14 "
            "PDF-Standardschriften. Bei solchen Schriften drohen Zeichenzuordnungsfehler, die "
            "beim Parsen zu verstümmeltem oder fehlendem Text führen."
        ),
        "uk": (
            "Шрифт, використаний у PDF, не вбудований і не належить до 14 стандартних "
            "шрифтів PDF. Такі шрифти можуть спричинити збій відповідності символів, через що "
            "текст при розборі спотворюється або зникає."
        ),
        "ru": (
            "Шрифт, использованный в PDF, не встроен и не входит в число 14 стандартных "
            "шрифтов PDF. Такие шрифты могут вызвать сбой соответствия символов, из-за чего "
            "текст при разборе искажается или пропадает."
        ),
        "es": (
            "Una fuente usada en el PDF no está incrustada ni es una de las 14 fuentes base "
            "estándar. Las fuentes no incrustadas corren el riesgo de provocar errores de correspondencia de "
            "caracteres que producen texto ilegible o ausente al analizar."
        ),
        "nl": (
            "Een in de PDF gebruikt lettertype is niet ingesloten en behoort niet tot de 14 "
            "standaard PDF-lettertypen. Bij zulke lettertypen dreigen fouten in de "
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
            "Вміст резюме розміщено в таблиці DOCX. Багато парсерів зводять рядки "
            "таблиці в один так, що плутається, яке значення до якої назви належить, або пропускають "
            "вміст таблиць повністю."
        ),
        "ru": (
            "Содержимое резюме размещено в таблице DOCX. Многие парсеры сворачивают строки "
            "таблицы в одну так, что путается, какое значение к какому названию относится, либо "
            "пропускают содержимое таблиц полностью."
        ),
        "es": (
            "Hay contenido del currículum dentro de una tabla DOCX. Muchos analizadores "
            "aplanan las filas de forma que se mezcla qué valor corresponde a qué etiqueta, "
            "o se saltan el contenido de las tablas por completo."
        ),
        "nl": (
            "Cv-inhoud staat in een DOCX-tabel. Veel parsers slaan tabelrijen zo plat dat "
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
            "Una sección (Experiencia/Formación/Competencias) se reconoce al leer el archivo "
            "teniendo en cuenta el diseño, pero desaparece por completo al leerlo como lo "
            "haría un analizador ciego al diseño — es el formato, no el contenido, lo que "
            "pone en riesgo esta sección."
        ),
        "nl": (
            "Een sectie (Werkervaring/Opleiding/Vaardigheden) wordt herkend bij layoutbewust "
            "lezen, maar verdwijnt volledig bij lezen zoals een layoutblinde parser doet — "
            "de opmaak, niet de inhoud, brengt deze sectie in gevaar."
        ),
        "fr": (
            "Une section (Expérience/Formation/Compétences) est reconnue lors d'une lecture "
            "tenant compte de la mise en page, mais disparaît entièrement à la lecture d'un "
            "analyseur aveugle à celle-ci — c'est la mise en forme, non le contenu, qui met "
            "cette section en péril."
        ),
    },
    "volunteering_listed_as_employment": {
        "en": "Volunteer work is listed under work experience. In a German or Ukrainian CV that section means paid employment, so a recruiter reads the entry as a job and then finds out it was not one.",
        "de": "Ehrenamtliche Tätigkeit steht unter Berufserfahrung. In einem deutschen Lebenslauf bedeutet diese Rubrik bezahlte Beschäftigung — wer ihn liest, hält den Eintrag für eine Stelle und stellt dann fest, dass es keine war.",
        "uk": "Волонтерство вказано в розділі досвіду роботи. В українському чи німецькому резюме цей розділ означає оплачувану зайнятість, тож рекрутер читає запис як посаду, а потім з'ясовує, що це не так.",
        "ru": "Волонтерство указано в разделе опыта работы. В немецком или украинском резюме этот раздел означает оплачиваемую занятость, поэтому рекрутер читает запись как должность, а потом выясняет, что это не так.",
        "es": "El voluntariado aparece en la experiencia laboral. En un CV alemán o ucraniano esa sección significa empleo remunerado, así que quien selecciona lee la entrada como un puesto y después descubre que no lo era.",
        "nl": "Vrijwilligerswerk staat onder werkervaring. In een Duits of Oekraïens cv betekent die rubriek betaald werk, dus een recruiter leest het als een baan en ontdekt daarna dat het er geen was.",
        "fr": "Le bénévolat figure dans l'expérience professionnelle. Dans un CV allemand ou ukrainien, cette rubrique désigne un emploi rémunéré : le recruteur lit l'entrée comme un poste, puis découvre que ce n'en était pas un.",
    },
    "unexplained_gap": {
        "en": "The dates leave months with nothing in them. German recruiters expect a CV without unexplained gaps, and read a silent one as something being left out.",
        "de": "Die Daten lassen Monate ohne Eintrag. In Deutschland wird ein lückenloser Lebenslauf erwartet, und eine unkommentierte Lücke wird so gelesen, als werde etwas verschwiegen.",
        "uk": "Між датами лишаються місяці без жодного запису. Німецькі рекрутери очікують резюме без непояснених перерв і читають мовчазну перерву як щось приховане.",
        "ru": "Между датами остаются месяцы без единой записи. Немецкие рекрутеры ожидают резюме без необъяснённых перерывов и читают молчаливый перерыв как что-то скрытое.",
        "es": "Las fechas dejan meses sin nada. En Alemania se espera un CV sin huecos sin explicar, y uno que calla se lee como algo que se oculta.",
        "nl": "De data laten maanden zonder invulling. Duitse recruiters verwachten een cv zonder onverklaarde gaten en lezen een zwijgend gat als iets dat wordt weggelaten.",
        "fr": "Les dates laissent des mois vides. En Allemagne, on attend un CV sans période inexpliquée, et un silence y est lu comme quelque chose que l'on tait.",
    },
    "impossible_dates": {
        "en": "A date range cannot be true: it ends before it starts, or it reaches years into the future. Software that works out years of experience from the dates discards the range entirely.",
        "de": "Ein Zeitraum kann so nicht stimmen: Er endet vor seinem Beginn oder reicht Jahre in die Zukunft. Software, die aus den Daten die Berufsjahre berechnet, verwirft ihn vollständig.",
        "uk": "Проміжок дат не може бути правдою: він закінчується раніше, ніж починається, або сягає на роки вперед. Програма, що рахує роки досвіду за датами, просто відкидає такий проміжок.",
        "ru": "Промежуток дат не может быть правдой: он заканчивается раньше, чем начинается, или уходит на годы вперёд. Программа, считающая годы опыта по датам, просто отбрасывает такой промежуток.",
        "es": "Un rango de fechas no puede ser cierto: termina antes de empezar o llega años hacia el futuro. El software que calcula los años de experiencia a partir de las fechas lo descarta por completo.",
        "nl": "Een periode kan niet kloppen: hij eindigt voordat hij begint, of reikt jaren de toekomst in. Software die jaren ervaring uit de data berekent, laat hem volledig vallen.",
        "fr": "Une période ne peut pas être vraie : elle se termine avant de commencer, ou s'étend des années dans le futur. Un logiciel qui calcule les années d'expérience à partir des dates l'écarte entièrement.",
    },
    "first_person_in_cv": {
        "en": "Entries are written as sentences about \"I\". A CV lists its entries as short fragments; first-person sentences belong in the profile at the top or in the cover letter.",
        "de": "Die Einträge sind als Ich-Sätze formuliert. Ein tabellarischer Lebenslauf nennt Stationen in Stichpunkten; Sätze in der Ich-Form gehören ins Kurzprofil oben oder ins Anschreiben.",
        "uk": "Записи сформульовано як речення від першої особи. Резюме подає записи короткими фразами; речення про себе доречні лише в профілі вгорі чи в супровідному листі.",
        "ru": "Записи сформулированы как предложения от первого лица. Резюме подаёт записи короткими фразами; предложения о себе уместны только в профиле вверху или в сопроводительном письме.",
        "es": "Las entradas están escritas como frases en primera persona. Un CV enumera sus entradas en fragmentos breves; las frases sobre uno mismo van en el perfil de arriba o en la carta de presentación.",
        "nl": "De onderdelen zijn geschreven als zinnen in de ik-vorm. Een cv noemt ze in korte fragmenten; zinnen over jezelf horen in het profiel bovenaan of in de sollicitatiebrief.",
        "fr": "Les entrées sont rédigées en phrases à la première personne. Un CV présente ses entrées en fragments courts ; les phrases sur soi vont dans le profil en tête ou dans la lettre de motivation.",
    },
    "outdated_personal_details": {
        "en": "The personal details include fields a German CV no longer needs: religion, marital status, children or parents. Religion is protected under the equal treatment law, and the rest are details most applicants no longer give.",
        "de": "Die persönlichen Daten enthalten Angaben, die ein deutscher Lebenslauf nicht mehr braucht: Konfession, Familienstand, Kinder oder Eltern. Die Religion ist nach dem AGG geschützt, und den Rest geben die meisten Bewerbenden nicht mehr an.",
        "uk": "В особистих даних є поля, які німецьке резюме більше не потребує: віросповідання, сімейний стан, діти чи батьки. Релігія захищена законом про рівне ставлення, а решту більшість кандидатів уже не вказує.",
        "ru": "В личных данных есть поля, которые немецкому резюме больше не нужны: вероисповедание, семейное положение, дети или родители. Религия защищена законом о равном обращении, а остальное большинство кандидатов уже не указывает.",
        "es": "Los datos personales incluyen campos que un CV alemán ya no necesita: religión, estado civil, hijos o padres. La religión está protegida por la ley de igualdad de trato, y el resto son datos que la mayoría ya no incluye.",
        "nl": "De persoonsgegevens bevatten velden die een Duits cv niet meer nodig heeft: geloof, burgerlijke staat, kinderen of ouders. Geloof is beschermd door de gelijkebehandelingswet, en de rest vermelden de meeste sollicitanten niet meer.",
        "fr": "Les données personnelles contiennent des champs dont un CV allemand n'a plus besoin : religion, situation familiale, enfants ou parents. La religion est protégée par la loi sur l'égalité de traitement, et la plupart des candidatures n'indiquent plus le reste.",
    },
    "oldest_entry_first": {
        "en": "Work experience runs from the oldest job to the newest. The expected order is the reverse, so that the first thing a recruiter reads is what the candidate does now.",
        "de": "Die Berufserfahrung beginnt mit der ältesten Station. Erwartet wird die umgekehrte Reihenfolge, damit man zuerst liest, was die Person heute tut.",
        "uk": "Досвід роботи йде від найстарішої посади до найновішої. Очікується зворотний порядок, щоб рекрутер першим прочитав, чим кандидат займається зараз.",
        "ru": "Опыт работы идёт от самой старой должности к самой новой. Ожидается обратный порядок, чтобы рекрутер первым прочитал, чем кандидат занимается сейчас.",
        "es": "La experiencia laboral va del empleo más antiguo al más reciente. Se espera el orden inverso, para que lo primero que se lea sea a qué se dedica la persona ahora.",
        "nl": "De werkervaring loopt van de oudste baan naar de nieuwste. De verwachte volgorde is omgekeerd, zodat een recruiter eerst leest wat de kandidaat nu doet.",
        "fr": "L'expérience professionnelle va du poste le plus ancien au plus récent. L'ordre attendu est l'inverse, pour que le recruteur lise d'abord ce que la personne fait aujourd'hui.",
    },
}


def rule_description(rule_id: str, language: str, fallback: str) -> str:
    """Return the translated description for a rule.

    ``fallback`` is the description carried by the Rule itself, used when a
    rule has no translation entry yet -- a new rule stays readable instead
    of showing a placeholder.
    """
    return _for_rule(RULE_DESCRIPTIONS, rule_id, language, fallback)


RULE_DETAILS: dict[str, dict[str, str]] = {
    "contact_only_as_link": {
        "en": "A person reading your CV clicks the link and finds you. Software does not click. It reads the words on the page, and the words say \"LinkedIn\" — the address itself sits in a separate layer of the file that most extractors never look at. So the contact field comes back empty, and an empty contact field is the one gap nothing else on the page can make up for.",
        "de": "Ein Mensch klickt den Link an und findet Sie. Software klickt nicht. Sie liest die Wörter auf der Seite, und dort steht \"LinkedIn\" — die Adresse selbst liegt in einer eigenen Ebene der Datei, die die meisten Extraktoren nie ansehen. Das Kontaktfeld bleibt also leer, und ein leeres Kontaktfeld ist die eine Lücke, die nichts anderes auf der Seite ausgleicht.",
        "uk": "Людина клікає посилання і знаходить вас. Програма не клікає. Вона читає слова на сторінці, а там написано «LinkedIn» — сама ж адреса лежить в окремому шарі файлу, куди більшість екстракторів не заглядає. Тож поле контакту лишається порожнім, а порожнє поле контакту — саме та прогалина, якої ніщо інше на сторінці не компенсує.",
        "ru": "Человек кликает ссылку и находит вас. Программа не кликает. Она читает слова на странице, а там написано «LinkedIn» — сам адрес лежит в отдельном слое файла, куда большинство экстракторов не заглядывает. Поле контакта остаётся пустым, а пустое поле контакта — та самая брешь, которую ничто другое на странице не восполняет.",
        "es": "Una persona hace clic en el enlace y te encuentra. El software no hace clic. Lee las palabras de la página, y las palabras dicen «LinkedIn»: la dirección está en una capa aparte del archivo que casi ningún extractor mira. El campo de contacto queda vacío, y un campo de contacto vacío es la única carencia que nada más en la página compensa.",
        "nl": "Een mens klikt op de link en vindt je. Software klikt niet. Die leest de woorden op de pagina, en daar staat \"LinkedIn\" — het adres zelf zit in een aparte laag van het bestand waar de meeste extractors nooit kijken. Het contactveld blijft dus leeg, en een leeg contactveld is het ene gat dat niets anders op de pagina goedmaakt.",
        "fr": "Une personne clique sur le lien et vous trouve. Un logiciel ne clique pas. Il lit les mots de la page, et ces mots disent « LinkedIn » : l'adresse elle-même est dans une couche à part du fichier que presque aucun extracteur ne consulte. Le champ de contact reste donc vide, et un champ de contact vide est le seul manque que rien d'autre sur la page ne rattrape.",
    },
    "unrecognised_section_headings": {
        "en": "Your file is laid out clearly and reads well. The problem is the labels. Software locates your history by looking for the word Experience, your qualifications by looking for Education — it has no other way in. \"My Journey\" is a better line than \"Experience\", and it is invisible: the entries underneath are read as loose text with nothing to say what they are. Keep your wording anywhere you like; put the plain word in the heading.",
        "de": "Ihre Datei ist klar aufgebaut und liest sich gut. Das Problem sind die Titel. Software findet Ihren Werdegang, indem sie nach dem Wort Berufserfahrung sucht, Ihre Abschlüsse über das Wort Ausbildung — einen anderen Zugang hat sie nicht. \"Was ich mitbringe\" ist die schönere Zeile und bleibt unsichtbar: die Einträge darunter werden als loser Text gelesen, ohne dass etwas sagt, was sie sind. Formulieren Sie, wie Sie mögen; in die Überschrift gehört das schlichte Wort.",
        "uk": "Ваш файл побудовано зрозуміло й читається добре. Проблема в підписах. Програма знаходить ваш шлях, шукаючи слово «Досвід», а кваліфікації — за словом «Освіта»; іншого входу в неї немає. «Мій шлях» — гарніший рядок, і він невидимий: записи під ним читаються як розсипаний текст, і ніщо не каже, що це таке. Формулюйте як хочете; у заголовок має піти просте слово.",
        "ru": "Ваш файл построен понятно и читается хорошо. Проблема в подписях. Программа находит ваш путь, ища слово «Опыт», а квалификации — по слову «Образование»; другого входа у неё нет. «Мой путь» — строка красивее, и она невидима: записи под ней читаются как рассыпанный текст, и ничто не говорит, что это такое. Формулируйте как хотите; в заголовок должно пойти простое слово.",
        "es": "Tu archivo está bien organizado y se lee bien. El problema son las etiquetas. El software localiza tu trayectoria buscando la palabra Experiencia y tus títulos buscando Formación: no tiene otra entrada. «Mi camino» es mejor frase que «Experiencia», y es invisible: lo que va debajo se lee como texto suelto, sin nada que diga qué es. Escribe como quieras; en el título pon la palabra sencilla.",
        "nl": "Je bestand is helder opgebouwd en leest prettig. Het probleem zijn de labels. Software vindt je loopbaan door te zoeken naar het woord Werkervaring en je diploma's via Opleiding — een andere ingang heeft die niet. \"Mijn pad\" is de mooiere regel en blijft onzichtbaar: wat eronder staat wordt als los tekst gelezen, zonder dat iets zegt wat het is. Formuleer zoals je wilt; in de kop hoort het gewone woord.",
        "fr": "Votre fichier est clairement organisé et se lit bien. Le problème, ce sont les libellés. Un logiciel repère votre parcours en cherchant le mot Expérience et vos diplômes en cherchant Formation : il n'a pas d'autre entrée. « Mon parcours » est une plus belle ligne, et elle est invisible : ce qui suit est lu comme du texte en vrac, sans rien pour dire ce que c'est. Formulez comme vous voulez ; dans le titre, mettez le mot simple.",
    },
    "broken_characters": {
        "en": "This is the fault that hides best, because the page looks perfect. A PDF exporter turns \"fi\" into the single character \"ﬁ\"; a justified paragraph leaves soft hyphens inside words; editing an old document with a second keyboard layout puts a Cyrillic о inside a Latin word. Every one of them reads correctly to you and matches nothing: a recruiter searching for the word will not find it, and neither will the filter that ranked the pile.",
        "de": "Das ist der Fehler, der sich am besten versteckt, weil die Seite perfekt aussieht. Ein PDF-Export macht aus \"fi\" das eine Zeichen \"ﬁ\"; ein Blocksatz hinterlässt weiche Trennzeichen mitten in Wörtern; wer ein altes Dokument mit einer zweiten Tastaturbelegung überarbeitet, setzt ein kyrillisches о in ein lateinisches Wort. Für Sie liest sich jedes davon richtig und trifft doch nichts: Wer das Wort sucht, findet es nicht — weder der Mensch noch der Filter, der den Stapel sortiert hat.",
        "uk": "Це вада, яка ховається найкраще, бо сторінка виглядає бездоганно. Експорт у PDF перетворює «fi» на один символ «ﬁ»; вирівнювання за шириною лишає м'які переноси всередині слів; правка старого документа з другою розкладкою ставить кириличну «о» в латинське слово. Кожне з них читається вам правильно і не збігається ні з чим: хто шукатиме це слово, не знайде його — ні людина, ні фільтр, що впорядкував стос.",
        "ru": "Это изъян, который прячется лучше всего, потому что страница выглядит безупречно. Экспорт в PDF превращает «fi» в один символ «ﬁ»; выравнивание по ширине оставляет мягкие переносы внутри слов; правка старого документа со второй раскладкой ставит кириллическую «о» в латинское слово. Каждое из них читается вам правильно и не совпадает ни с чем: кто будет искать это слово, не найдёт его — ни человек, ни фильтр, упорядочивший стопку.",
        "es": "Este es el fallo que mejor se esconde, porque la página se ve perfecta. Un exportador de PDF convierte «fi» en el carácter único «ﬁ»; un párrafo justificado deja guiones suaves dentro de las palabras; editar un documento antiguo con otra distribución de teclado mete una о cirílica en una palabra latina. Todos se leen bien para ti y no coinciden con nada: quien busque esa palabra no la encontrará, ni la persona ni el filtro que ordenó el montón.",
        "nl": "Dit is de fout die zich het best verstopt, want de pagina ziet er perfect uit. Een PDF-export maakt van \"fi\" het ene teken \"ﬁ\"; uitgevulde tekst laat zachte afbreektekens midden in woorden achter; een oud document bewerken met een tweede toetsenbordindeling zet een Cyrillische о in een Latijns woord. Voor jou leest elk ervan goed en toch matcht het niets: wie het woord zoekt vindt het niet, de mens niet en het filter dat de stapel sorteerde evenmin.",
        "fr": "C'est le défaut qui se cache le mieux, parce que la page a l'air parfaite. Un export PDF transforme « fi » en un seul caractère « ﬁ » ; un paragraphe justifié laisse des traits d'union conditionnels au milieu des mots ; retoucher un vieux document avec une deuxième disposition de clavier glisse un о cyrillique dans un mot latin. Chacun se lit correctement pour vous et ne correspond à rien : qui cherche ce mot ne le trouvera pas, ni la personne ni le filtre qui a trié la pile.",
    },
    "pdf_non_embedded_font": {
        "en": 'The PDF names a font but does not carry it. Whatever opens the file substitutes something else, and the substitute may map characters differently — which is how text that looks fine on your screen arrives as gibberish, or does not arrive at all.',
        "de": 'Das PDF nennt eine Schrift, enthält sie aber nicht. Das öffnende Programm ersetzt sie, und der Ersatz kann Zeichen anders zuordnen — so kommt Text, der auf Ihrem Bildschirm gut aussieht, als Zeichensalat oder gar nicht an.',
        "uk": 'PDF називає шрифт, але не містить його. Програма, що відкриває файл, підставляє інший, а підстановка може інакше зіставити символи — саме так текст, який на вашому екрані виглядає нормально, доходить спотвореним або не доходить узагалі.',
        "ru": 'PDF называет шрифт, но не содержит его. Программа, открывающая файл, подставляет другой, а подстановка может иначе сопоставить символы — именно так текст, который на вашем экране выглядит нормально, доходит искажённым или не доходит вовсе.',
        "es": 'El PDF nombra una fuente pero no la incluye. El programa que lo abre la sustituye, y el sustituto puede asignar los caracteres de otra forma: así es como un texto que se ve bien en tu pantalla llega ilegible, o no llega.',
        "nl": 'De PDF noemt een lettertype maar bevat het niet. Wat het bestand opent vervangt het, en de vervanger kan tekens anders toewijzen — zo komt tekst die er op jouw scherm goed uitziet als brij aan, of helemaal niet.',
        "fr": "Le PDF nomme une police sans l'inclure. Le programme qui l'ouvre la remplace, et le substitut peut associer les caractères autrement : c'est ainsi qu'un texte impeccable à l'écran arrive illisible, ou n'arrive pas.",
    },
    "pdf_repeated_header_footer_content": {
        "en": 'Text that repeats in the same spot on every page reads as page furniture, so parsers commonly strip it before looking at the content. That is the right call for page numbers. It is expensive if your phone number or email lives there and nowhere else.',
        "de": 'Text, der auf jeder Seite an derselben Stelle steht, wirkt wie Seitenbeiwerk, daher entfernen Parser ihn meist vor der Auswertung. Bei Seitenzahlen ist das richtig. Teuer wird es, wenn dort Ihre Telefonnummer oder E-Mail steht und sonst nirgends.',
        "uk": 'Текст, що повторюється на кожній сторінці в тому самому місці, сприймається як службовий, тож парсери зазвичай викидають його ще до аналізу вмісту. Для номерів сторінок це правильно. Дорого обходиться, якщо там ваш телефон чи пошта — і більше ніде.',
        "ru": 'Текст, повторяющийся на каждой странице в одном месте, воспринимается как служебный, поэтому парсеры обычно выбрасывают его ещё до анализа содержимого. Для номеров страниц это верно. Дорого обходится, если там ваш телефон или почта — и больше нигде.',
        "es": 'El texto que se repite en el mismo sitio de cada página parece decoración, así que los analizadores suelen eliminarlo antes de mirar el contenido. Con los números de página es lo correcto. Sale caro si ahí está tu teléfono o correo y en ningún otro sitio.',
        "nl": 'Tekst die op elke pagina op dezelfde plek terugkomt oogt als opvulling, dus parsers verwijderen die meestal vóór ze naar de inhoud kijken. Bij paginanummers is dat terecht. Het wordt duur als daar je telefoonnummer of e-mail staat en nergens anders.',
        "fr": "Un texte répété au même endroit sur chaque page passe pour de l'habillage, aussi les analyseurs le suppriment-ils souvent avant d'examiner le contenu. Pour un numéro de page, c'est justifié. Cela coûte cher si votre téléphone ou e-mail s'y trouve et nulle part ailleurs.",
    },
    "pdf_textless_image": {
        "en": 'A picture covers part of the page and no extracted text sits under it. If that picture is a name plate, a skills chart or a whole sidebar exported from a design tool, its words are not text at all and no parser will read them. If it is a portrait photo, nothing is lost.',
        "de": 'Ein Bild bedeckt einen Teil der Seite, und darunter liegt kein extrahierter Text. Ist es ein Namensschild, ein Diagramm oder eine ganze Seitenspalte aus einem Design-Tool, sind seine Wörter gar kein Text und kein Parser liest sie. Ist es ein Porträtfoto, geht nichts verloren.',
        "uk": 'Зображення закриває частину сторінки, і під ним немає видобутого тексту. Якщо це банер з іменем, діаграма навичок чи ціла бічна колонка з дизайн-редактора — слова на ньому взагалі не є текстом, і жоден парсер їх не прочитає. Якщо це портретне фото, нічого не втрачено.',
        "ru": 'Изображение закрывает часть страницы, и под ним нет извлечённого текста. Если это баннер с именем, диаграмма навыков или целая боковая колонка из дизайн-редактора — слова на нём вообще не текст, и ни один парсер их не прочитает. Если это портретное фото, ничего не потеряно.',
        "es": 'Una imagen cubre parte de la página y debajo no hay texto extraído. Si esa imagen es un rótulo con el nombre, un gráfico de competencias o una barra lateral entera exportada de una herramienta de diseño, sus palabras no son texto y ningún analizador las leerá. Si es una foto de retrato, no se pierde nada.',
        "nl": 'Een afbeelding bedekt een deel van de pagina en er ligt geen geëxtraheerde tekst onder. Is die afbeelding een naambanner, een vaardighedendiagram of een hele zijkolom uit een ontwerpprogramma, dan zijn de woorden erop geen tekst en leest geen enkele parser ze. Is het een portretfoto, dan gaat er niets verloren.',
        "fr": "Une image couvre une partie de la page et aucun texte extrait ne se trouve dessous. Si cette image est un bandeau de nom, un graphique de compétences ou toute une colonne latérale exportée d'un outil de design, ses mots ne sont pas du texte et aucun analyseur ne les lira. S'il s'agit d'une photo de portrait, rien n'est perdu.",
    },
    "docx_table_content": {
        "en": 'Tables are a tidy way to line up a two-column CV on screen, and a common way to scramble it on the way in. Many parsers flatten a table row into one line, so the label and the value from different columns end up welded together — or the table is skipped outright.',
        "de": 'Tabellen sind eine saubere Art, einen zweispaltigen Lebenslauf am Bildschirm auszurichten — und eine häufige Art, ihn beim Einlesen zu zerlegen. Viele Parser reduzieren eine Tabellenzeile auf eine einzige Zeile, sodass Bezeichnung und Wert aus verschiedenen Spalten verschweißt werden — oder die Tabelle wird ganz übersprungen.',
        "uk": 'Таблиці — охайний спосіб вирівняти двоколонкове резюме на екрані й водночас поширений спосіб зіпсувати його при читанні. Багато парсерів згортають рядок таблиці в один рядок тексту, і назва зі значенням із різних колонок зростаються — або таблицю пропускають узагалі.',
        "ru": 'Таблицы — аккуратный способ выровнять двухколоночное резюме на экране и одновременно распространённый способ испортить его при чтении. Многие парсеры сворачивают строку таблицы в одну строку текста, и название со значением из разных колонок срастаются — либо таблицу пропускают вовсе.',
        "es": 'Las tablas son una forma limpia de alinear un CV a dos columnas en pantalla, y una forma habitual de desordenarlo al leerlo. Muchos analizadores aplanan una fila en una sola línea, de modo que la etiqueta y el valor de columnas distintas quedan soldados — o la tabla se omite por completo.',
        "nl": 'Tabellen zijn een nette manier om een cv met twee kolommen uit te lijnen op het scherm, en een veelvoorkomende manier om het bij het inlezen te verhaspelen. Veel parsers slaan een tabelrij plat tot één regel, waardoor label en waarde uit verschillende kolommen aan elkaar vastzitten — of de tabel wordt helemaal overgeslagen.',
        "fr": "Les tableaux sont une manière propre d'aligner un CV sur deux colonnes à l'écran, et une manière courante de le brouiller à la lecture. Beaucoup d'analyseurs aplatissent une ligne de tableau en une seule ligne, soudant ainsi le libellé et la valeur de colonnes différentes — ou ignorent le tableau entièrement.",
    },
    "docx_header_footer_content": {
        "en": 'A Word header or footer is stored in its own part of the file, outside the document body. Readers that walk the body — which is most of them — never reach it. A quick check: press Ctrl+A in Word. Whatever does not highlight is roughly what a parser will not see.',
        "de": 'Eine Word-Kopf- oder Fußzeile liegt in einem eigenen Teil der Datei, außerhalb des Textkörpers. Programme, die den Textkörper durchlaufen — also die meisten — erreichen sie nie. Schnelltest: Strg+A in Word drücken. Was nicht markiert wird, sieht ein Parser ungefähr auch nicht.',
        "uk": 'Колонтитул Word зберігається в окремій частині файлу, поза тілом документа. Програми, що обходять тіло — а це більшість — до нього не дістаються. Швидка перевірка: натисніть Ctrl+A у Word. Те, що не виділилось, парсер приблизно так само не побачить.',
        "ru": 'Колонтитул Word хранится в отдельной части файла, вне тела документа. Программы, обходящие тело — а это большинство — до него не добираются. Быстрая проверка: нажмите Ctrl+A в Word. То, что не выделилось, парсер примерно так же не увидит.',
        "es": 'Un encabezado o pie de Word se guarda en su propia parte del archivo, fuera del cuerpo del documento. Los lectores que recorren el cuerpo — casi todos — nunca llegan ahí. Comprobación rápida: pulsa Ctrl+A en Word. Lo que no se resalte es más o menos lo que un analizador no verá.',
        "nl": 'Een Word-kop- of voettekst zit in een eigen deel van het bestand, buiten de hoofdtekst. Lezers die de hoofdtekst doorlopen — de meeste dus — komen er nooit. Snelle test: druk Ctrl+A in Word. Wat niet oplicht, ziet een parser ongeveer ook niet.',
        "fr": "Un en-tête ou pied de page Word est stocké dans sa propre partie du fichier, hors du corps du document. Les lecteurs qui parcourent le corps — la plupart — n'y accèdent jamais. Test rapide : appuyez sur Ctrl+A dans Word. Ce qui ne se surligne pas est à peu près ce qu'un analyseur ne verra pas.",
    },
    "docx_text_box_content": {
        "en": 'A text box is not part of the paragraph flow: Word stores it inside a drawing anchor, off to the side of the text a reader walks through. Sidebars built this way look deliberate and disappear completely, which is why they are among the most cited causes of a CV arriving half-empty.',
        "de": 'Ein Textfeld gehört nicht zum Absatzfluss: Word legt es in einem Zeichnungsanker ab, abseits des Textes, den ein Leser durchläuft. So gebaute Seitenspalten wirken durchdacht und verschwinden vollständig — deshalb zählen sie zu den meistgenannten Gründen, warum ein Lebenslauf halb leer ankommt.',
        "uk": 'Текстове поле не належить до потоку абзаців: Word тримає його в графічному якорі, збоку від тексту, який обходить програма читання. Бічні колонки, зроблені так, виглядають продумано і зникають повністю — через це вони серед найчастіше згадуваних причин, чому резюме доходить напівпорожнім.',
        "ru": 'Текстовое поле не относится к потоку абзацев: Word держит его в графическом якоре, в стороне от текста, который обходит программа чтения. Боковые колонки, сделанные так, выглядят продуманно и исчезают полностью — поэтому они среди самых частых причин, почему резюме доходит полупустым.',
        "es": 'Un cuadro de texto no forma parte del flujo de párrafos: Word lo guarda dentro de un anclaje de dibujo, al margen del texto que recorre un lector. Las barras laterales hechas así parecen intencionadas y desaparecen por completo, por eso están entre las causas más citadas de que un CV llegue medio vacío.',
        "nl": 'Een tekstvak hoort niet bij de alineastroom: Word bewaart het in een tekeninganker, naast de tekst die een lezer doorloopt. Zo gebouwde zijkolommen ogen doordacht en verdwijnen volledig — daarom staan ze bij de meest genoemde oorzaken van een half leeg aangekomen cv.',
        "fr": "Une zone de texte ne fait pas partie du flux de paragraphes : Word la range dans une ancre de dessin, à l'écart du texte qu'un lecteur parcourt. Les colonnes latérales construites ainsi paraissent voulues et disparaissent totalement — d'où leur place parmi les causes les plus citées d'un CV arrivé à moitié vide.",
    },
    "missing_contact_field": {
        "en": 'Neither an email address nor a phone number could be recovered, even reading the file at its best. Whatever else is right, an employer who cannot reach you cannot invite you — this is the one finding that makes the rest moot.',
        "de": 'Weder E-Mail-Adresse noch Telefonnummer waren zu finden, selbst beim bestmöglichen Lesen der Datei. Was sonst auch stimmt: Wer Sie nicht erreichen kann, kann Sie nicht einladen — dieser Befund macht alle anderen gegenstandslos.',
        "uk": "Не вдалося дістати ні електронну пошту, ні номер телефону — навіть при найкращому читанні файлу. Хоч би яким правильним було все інше, роботодавець, який не може з вами зв'язатися, не може вас запросити — саме це зауваження знецінює всі інші.",
        "ru": 'Не удалось получить ни адрес электронной почты, ни номер телефона — даже при наилучшем чтении файла. Каким бы хорошим ни было всё остальное, работодатель, который не может с вами связаться, не может вас пригласить — именно это замечание обесценивает все остальные.',
        "es": 'No se ha podido recuperar ni un correo electrónico ni un teléfono, ni siquiera leyendo el archivo en su mejor caso. Por bien que esté todo lo demás, quien no puede contactarte no puede invitarte: este hallazgo deja sin sentido a los demás.',
        "nl": 'Er kon geen e-mailadres en geen telefoonnummer worden achterhaald, zelfs niet bij de best mogelijke lezing. Wat er verder ook klopt: wie jou niet kan bereiken, kan jou niet uitnodigen — deze bevinding maakt de rest irrelevant.',
        "fr": "Ni adresse e-mail ni numéro de téléphone n'ont pu être retrouvés, même en lisant le fichier au mieux. Quoi que vaille le reste, un employeur qui ne peut pas vous joindre ne peut pas vous inviter — ce constat rend les autres sans objet.",
    },
    "section_missing_under_naive_parsing": {
        "en": 'Your file has this section, and reading it with the columns understood finds it. Reading it the plain way — left to right across the whole page, which is what a layout-blind parser does — merges your heading with whatever sits beside it, and the heading stops being a heading. The content is fine; the layout is what puts it at risk.',
        "de": 'Ihre Datei enthält diesen Abschnitt, und mit erkannten Spalten wird er gefunden. Beim schlichten Lesen — quer über die ganze Seite, wie es ein layoutblinder Parser tut — verschmilzt Ihre Überschrift mit dem, was daneben steht, und hört auf, eine Überschrift zu sein. Der Inhalt ist in Ordnung; das Layout gefährdet ihn.',
        "uk": 'Ваш файл містить цей розділ, і читання з урахуванням колонок його знаходить. Просте читання — зліва направо через усю сторінку, як робить парсер, сліпий до верстки — зливає ваш заголовок із тим, що стоїть поруч, і заголовок перестає бути заголовком. Зі вмістом усе гаразд; під загрозу його ставить верстка.',
        "ru": 'Ваш файл содержит этот раздел, и чтение с учётом колонок его находит. Простое чтение — слева направо через всю страницу, как делает парсер, слепой к вёрстке — сливает ваш заголовок с тем, что стоит рядом, и заголовок перестаёт быть заголовком. С содержимым всё в порядке; под угрозу его ставит вёрстка.',
        "es": 'Tu archivo tiene esta sección, y leerlo entendiendo las columnas la encuentra. Leerlo de forma simple — de izquierda a derecha por toda la página, como hace un analizador ciego al diseño — funde tu encabezado con lo que tenga al lado, y el encabezado deja de serlo. El contenido está bien; es el diseño lo que lo pone en riesgo.',
        "nl": 'Je bestand bevat deze sectie, en lezen met begrip van de kolommen vindt haar. Simpel lezen — van links naar rechts over de hele pagina, zoals een layoutblinde parser doet — smelt je kop samen met wat ernaast staat, en de kop is geen kop meer. De inhoud is prima; de opmaak brengt haar in gevaar.',
        "fr": "Votre fichier contient cette section, et une lecture qui comprend les colonnes la trouve. Une lecture simple — de gauche à droite sur toute la largeur, ce que fait un analyseur aveugle à la mise en page — fond votre intitulé avec ce qui l'entoure, et l'intitulé cesse d'en être un. Le contenu va bien ; c'est la mise en page qui le met en péril.",
    },
    "volunteering_listed_as_employment": {
        "en": "German career guidance is unusually firm about this: an Ehrenamt does not replace Berufserfahrung, and it belongs in its own section — Ehrenamtliches Engagement — after experience and education and before interests. Ukrainian guidance says the same of volunteering unless it was your full-time occupation. The reason is what the heading promises. Under work experience a recruiter counts years of paid work, and an unpaid role found there later reads as padding, however valuable it was. In its own section the same entry reads as character. Two exceptions are real. A career starter may list relevant volunteering as experience, because for them it is the practical experience there is — which is why, with little dated experience, this is reported as low. And a Freiwilliges Soziales Jahr or Bundesfreiwilligendienst is a paid, insured placement that counts as practice, so it is not reported at all. In Dutch, Spanish, French, English and Russian CVs volunteering under experience is accepted when it is relevant, and this check stays silent.",
        "de": "Die Karriereberatung ist hier ungewöhnlich eindeutig: Ein Ehrenamt ersetzt keine Berufserfahrung und gehört in eine eigene Rubrik — Ehrenamtliches Engagement — nach Berufserfahrung und Ausbildung, vor Hobbys und Interessen. Der Grund liegt in dem, was die Überschrift verspricht. Unter Berufserfahrung zählt man Jahre bezahlter Arbeit, und eine unbezahlte Tätigkeit, die sich dort später als solche herausstellt, wirkt wie aufgefüllt, so wertvoll sie war. In einer eigenen Rubrik liest sich derselbe Eintrag als Engagement. Zwei Ausnahmen sind echt. Wer gerade in den Beruf einsteigt, darf relevantes Ehrenamt unter Berufserfahrung nennen, denn es ist die Praxis, die es gibt — deshalb wird es bei wenig datierter Erfahrung nur als gering gemeldet. Und ein Freiwilliges Soziales Jahr oder ein Bundesfreiwilligendienst ist eine bezahlte, versicherte Tätigkeit, die als Praxis zählt; beides wird gar nicht gemeldet. In niederländischen, spanischen, französischen, englischen und russischen Lebensläufen ist Ehrenamt unter Berufserfahrung akzeptiert, wenn es relevant ist, und diese Prüfung schweigt.",
        "uk": "Німецькі кар'єрні поради тут незвично категоричні: Ehrenamt не замінює досвіду роботи й має стояти в окремому розділі — Ehrenamtliches Engagement — після досвіду й освіти, перед хобі. Українські поради кажуть те саме про волонтерство, якщо воно не було вашою основною зайнятістю. Причина в тому, що обіцяє заголовок. У розділі досвіду рекрутер рахує роки оплачуваної роботи, і неоплачувана роль, яка потім виявляється такою, виглядає як доповнення для обсягу, хоч би якою цінною вона була. В окремому розділі той самий запис читається як характер. Є два справжні винятки. Той, хто тільки починає кар'єру, може вказати релевантне волонтерство як досвід, бо для нього це і є практика, — тому за малого датованого досвіду знахідка має низьку важливість. А Freiwilliges Soziales Jahr чи Bundesfreiwilligendienst — оплачувана, застрахована служба, що зараховується як практика, тож про неї взагалі не повідомляється. У нідерландських, іспанських, французьких, англійських і російських резюме волонтерство в досвіді прийнятне, якщо воно релевантне, і ця перевірка мовчить.",
        "ru": "Немецкие карьерные советы здесь необычно категоричны: Ehrenamt не заменяет опыта работы и должен стоять в отдельном разделе — Ehrenamtliches Engagement — после опыта и образования, перед хобби. Украинские советы говорят то же о волонтерстве, если оно не было основной занятостью. Причина в том, что обещает заголовок. В разделе опыта рекрутер считает годы оплачиваемой работы, и неоплачиваемая роль, которая потом оказывается таковой, выглядит как добавленная для объёма, какой бы ценной она ни была. В отдельном разделе та же запись читается как характер. Есть два настоящих исключения. Тот, кто только начинает карьеру, может указать релевантное волонтерство как опыт, потому что для него это и есть практика, — поэтому при небольшом датированном опыте находка имеет низкую важность. А Freiwilliges Soziales Jahr или Bundesfreiwilligendienst — оплачиваемая, застрахованная служба, которая засчитывается как практика, поэтому о ней не сообщается вовсе. В нидерландских, испанских, французских, английских и русских резюме волонтерство в опыте приемлемо, если оно релевантно, и эта проверка молчит.",
        "es": "La orientación profesional alemana es inusualmente firme en esto: un Ehrenamt no sustituye a la experiencia laboral y va en su propia sección —Ehrenamtliches Engagement— después de la experiencia y la formación, antes de los intereses. La orientación ucraniana dice lo mismo del voluntariado, salvo que fuera tu ocupación principal. La razón es lo que promete el título. En experiencia laboral se cuentan años de trabajo remunerado, y un puesto no remunerado que después resulta serlo parece relleno, por valioso que fuera. En su propia sección, la misma entrada se lee como compromiso. Hay dos excepciones reales. Quien empieza su carrera puede incluir voluntariado relevante como experiencia, porque para esa persona es la práctica que tiene; por eso, con poca experiencia fechada, se indica como baja. Y un Freiwilliges Soziales Jahr o un Bundesfreiwilligendienst es una estancia remunerada y asegurada que cuenta como práctica, así que no se indica en absoluto. En los CV neerlandeses, españoles, franceses, ingleses y rusos el voluntariado en la experiencia se acepta si es relevante, y esta comprobación no dice nada.",
        "nl": "Duits loopbaanadvies is hierover opvallend stellig: een Ehrenamt vervangt geen werkervaring en hoort in een eigen rubriek — Ehrenamtliches Engagement — na werkervaring en opleiding, vóór hobby's. Oekraïens advies zegt hetzelfde over vrijwilligerswerk, tenzij het je hoofdbezigheid was. De reden is wat het kopje belooft. Onder werkervaring telt een recruiter jaren betaald werk, en een onbetaalde rol die dat later blijkt te zijn, leest als opvulling, hoe waardevol hij ook was. In een eigen rubriek leest hetzelfde onderdeel als karakter. Er zijn twee echte uitzonderingen. Wie net begint, mag relevant vrijwilligerswerk als ervaring vermelden, omdat het de praktijk is die er is — daarom wordt het bij weinig gedateerde ervaring als laag gemeld. En een Freiwilliges Soziales Jahr of Bundesfreiwilligendienst is een betaalde, verzekerde plaatsing die als praktijk telt; die wordt helemaal niet gemeld. In Nederlandse, Spaanse, Franse, Engelse en Russische cv's is vrijwilligerswerk onder werkervaring geaccepteerd als het relevant is, en deze controle zwijgt.",
        "fr": "Les conseils de carrière allemands sont inhabituellement fermes sur ce point : un Ehrenamt ne remplace pas l'expérience professionnelle et va dans sa propre rubrique — Ehrenamtliches Engagement — après l'expérience et la formation, avant les centres d'intérêt. Les conseils ukrainiens disent la même chose du bénévolat, sauf s'il était votre activité principale. La raison tient à ce que promet le titre. Sous l'expérience professionnelle, le recruteur compte des années de travail rémunéré, et un rôle non rémunéré qui s'avère tel plus tard ressemble à du remplissage, aussi précieux qu'il ait été. Dans sa propre rubrique, la même entrée se lit comme de l'engagement. Deux exceptions sont réelles. Une personne en début de carrière peut présenter un bénévolat pertinent comme expérience, car c'est la pratique dont elle dispose — c'est pourquoi, avec peu d'expérience datée, il est signalé comme faible. Et un Freiwilliges Soziales Jahr ou un Bundesfreiwilligendienst est un engagement rémunéré et assuré qui compte comme pratique, donc il n'est pas signalé du tout. Dans les CV néerlandais, espagnols, français, anglais et russes, le bénévolat dans l'expérience est accepté s'il est pertinent, et ce contrôle reste muet.",
    },
    "unexplained_gap": {
        "en": "The lückenloser Lebenslauf — a CV with no unexplained months — is a German expectation rather than a law, and a firm one. Career guidance puts the line at two to three months: eight to ten weeks between jobs is ordinary and needs nothing, while from three or four months a recruiter expects a line saying what happened. After finishing a qualification about six months of job searching is normal, and it is not counted here. A gap is not the problem; silence is. Parental leave, caring for a relative, illness, a period of reorientation, a language course, time spent looking for work — each is an acceptable answer written as its own dated line. Left blank, the recruiter supplies an explanation, and it is rarely a kind one. This check reports gaps of four months or more, because dates on a CV are imprecise and a year written alone covers twelve months.",
        "de": "Der lückenlose Lebenslauf ist in Deutschland kein Gesetz, aber eine feste Erwartung. Die Karriereberatung zieht die Grenze bei zwei bis drei Monaten: acht bis zehn Wochen zwischen zwei Stellen sind normal und brauchen keine Erklärung, ab drei bis vier Monaten erwartet man eine Zeile dazu. Nach einem Abschluss gelten etwa sechs Monate Stellensuche als üblich; sie werden hier nicht gezählt. Nicht die Lücke ist das Problem, sondern das Schweigen. Elternzeit, Pflege von Angehörigen, Krankheit, berufliche Neuorientierung, ein Sprachkurs, Zeit der Stellensuche — all das ist eine akzeptable Antwort, als eigene datierte Zeile. Bleibt die Stelle leer, denkt sich die lesende Person eine Erklärung aus, und selten eine wohlwollende. Gemeldet werden Lücken ab vier Monaten, weil Daten im Lebenslauf ungenau sind und eine Jahreszahl allein zwölf Monate umfasst.",
        "uk": "Lückenloser Lebenslauf — резюме без непояснених місяців — у Німеччині не закон, а тверде очікування. Кар'єрні поради проводять межу на двох-трьох місяцях: вісім-десять тижнів між роботами — звичайна річ і пояснень не потребує, а від трьох-чотирьох місяців рекрутер чекає рядка про те, що відбувалося. Після здобуття кваліфікації близько шести місяців пошуку роботи вважаються нормою, і тут вони не рахуються. Проблема не в перерві, а в мовчанні. Декретна відпустка, догляд за родичем, хвороба, період переорієнтації, мовний курс, пошук роботи — кожне з цього прийнятна відповідь, записана окремим датованим рядком. Якщо місце лишити порожнім, рекрутер сам вигадає пояснення, і рідко доброзичливе. Перевірка повідомляє про перерви від чотирьох місяців, бо дати в резюме неточні, а рік без місяця охоплює дванадцять місяців.",
        "ru": "Lückenloser Lebenslauf — резюме без необъяснённых месяцев — в Германии не закон, а твёрдое ожидание. Карьерные советы проводят границу на двух-трёх месяцах: восемь-десять недель между работами — обычное дело и объяснений не требует, а с трёх-четырёх месяцев рекрутер ждёт строки о том, что происходило. После получения квалификации около шести месяцев поиска работы считаются нормой, и здесь они не учитываются. Проблема не в перерыве, а в молчании. Декретный отпуск, уход за родственником, болезнь, период переориентации, языковой курс, поиск работы — каждое из этого приемлемый ответ, записанный отдельной датированной строкой. Если место оставить пустым, рекрутер сам придумает объяснение, и редко доброжелательное. Проверка сообщает о перерывах от четырёх месяцев, потому что даты в резюме неточны, а год без месяца охватывает двенадцать месяцев.",
        "es": "El lückenloser Lebenslauf —un CV sin meses sin explicar— no es una ley en Alemania, sino una expectativa firme. La orientación profesional pone el límite en dos o tres meses: ocho o diez semanas entre empleos son normales y no necesitan nada, mientras que a partir de tres o cuatro meses se espera una línea que diga qué pasó. Tras terminar una titulación, unos seis meses de búsqueda de empleo son lo habitual y aquí no se cuentan. El problema no es el hueco, sino el silencio. Un permiso parental, cuidar de un familiar, una enfermedad, un periodo de reorientación, un curso de idiomas, el tiempo buscando trabajo: todo es una respuesta aceptable escrita como línea fechada propia. Si queda en blanco, quien lee se inventa la explicación, y rara vez es amable. Se indican huecos de cuatro meses o más, porque las fechas de un CV son imprecisas y un año solo cubre doce meses.",
        "nl": "De lückenlose Lebenslauf — een cv zonder onverklaarde maanden — is in Duitsland geen wet, maar wel een stellige verwachting. Loopbaanadvies legt de grens bij twee à drie maanden: acht tot tien weken tussen twee banen is gewoon en vraagt niets, vanaf drie of vier maanden verwacht een recruiter een regel over wat er gebeurde. Na het afronden van een opleiding is ongeveer zes maanden zoeken normaal; die telt hier niet mee. Het gat is het probleem niet, het zwijgen wel. Ouderschapsverlof, zorg voor een familielid, ziekte, een periode van heroriëntatie, een taalcursus, tijd om werk te zoeken — elk is een aanvaardbaar antwoord als eigen gedateerde regel. Blijft het leeg, dan bedenkt de lezer zelf een verklaring, en zelden een vriendelijke. Gaten vanaf vier maanden worden gemeld, omdat data op een cv onnauwkeurig zijn en een jaartal alleen twaalf maanden beslaat.",
        "fr": "Le lückenloser Lebenslauf — un CV sans mois inexpliqué — n'est pas une loi en Allemagne, mais une attente ferme. Les conseils de carrière placent la limite à deux ou trois mois : huit à dix semaines entre deux emplois sont ordinaires et ne demandent rien, tandis qu'à partir de trois ou quatre mois on attend une ligne disant ce qui s'est passé. Après un diplôme, environ six mois de recherche d'emploi sont normaux et ne sont pas comptés ici. Le problème n'est pas la période vide, mais le silence. Un congé parental, s'occuper d'un proche, une maladie, une réorientation, un cours de langue, le temps passé à chercher un emploi : chacun est une réponse acceptable, écrite comme une ligne datée à part. Laissée vide, la personne qui lit invente l'explication, et rarement une bienveillante. Les périodes de quatre mois ou plus sont signalées, car les dates d'un CV sont imprécises et une année seule couvre douze mois.",
    },
    "impossible_dates": {
        "en": "Applicant tracking systems work out years of experience from the dates on each entry, and recruiters filter on that number. A range whose end comes before its start has no length, so the system either discards it or records nothing — and the experience it was meant to prove drops out of every search that filters by years. This tool behaves the same way: a backwards range adds nothing to the experience it counts against an advert. A date years in the future is almost always a typo, 2052 for 2025, and has the same effect. Both are easy to miss in your own CV, because the eye reads the year it expects. The check allows dates up to two years ahead, because a signed contract or a fixed-term role can legitimately end next year, and it ignores education, where an expected graduation date is normal.",
        "de": "Bewerbermanagementsysteme berechnen die Berufsjahre aus den Daten jeder Station, und danach wird gefiltert. Ein Zeitraum, dessen Ende vor dem Beginn liegt, hat keine Dauer — das System verwirft ihn oder erfasst nichts, und die Erfahrung, die er belegen sollte, fällt aus jeder Suche nach Berufsjahren heraus. Dieses Werkzeug verhält sich genauso: Ein rückwärts laufender Zeitraum zählt nicht zur Erfahrung, die mit einer Stellenanzeige verglichen wird. Ein Datum Jahre in der Zukunft ist fast immer ein Tippfehler, 2052 statt 2025, mit derselben Wirkung. Beides übersieht man im eigenen Lebenslauf leicht, weil das Auge die erwartete Jahreszahl liest. Daten bis zwei Jahre voraus werden zugelassen, weil ein unterschriebener Vertrag oder eine befristete Stelle berechtigt im nächsten Jahr enden kann, und die Ausbildung wird ausgenommen, wo ein voraussichtlicher Abschluss normal ist.",
        "uk": "Системи відбору кандидатів рахують роки досвіду за датами кожного запису, а рекрутери фільтрують за цим числом. Проміжок, що закінчується раніше, ніж починається, не має тривалості, тож система або відкидає його, або нічого не записує — і досвід, який він мав підтвердити, випадає з кожного пошуку за роками. Цей інструмент поводиться так само: зворотний проміжок нічого не додає до досвіду, який порівнюється з вакансією. Дата на роки вперед майже завжди друкарська помилка, 2052 замість 2025, і діє так само. Обидва випадки легко пропустити у власному резюме, бо око читає очікуваний рік. Перевірка допускає дати до двох років уперед, бо підписаний контракт чи строкова посада можуть законно закінчуватися наступного року, і не зважає на освіту, де очікувана дата закінчення — звичайна річ.",
        "ru": "Системы отбора кандидатов считают годы опыта по датам каждой записи, а рекрутеры фильтруют по этому числу. Промежуток, заканчивающийся раньше, чем начинается, не имеет длительности, поэтому система либо отбрасывает его, либо ничего не записывает — и опыт, который он должен был подтвердить, выпадает из каждого поиска по годам. Этот инструмент ведёт себя так же: обратный промежуток ничего не добавляет к опыту, который сравнивается с вакансией. Дата на годы вперёд почти всегда опечатка, 2052 вместо 2025, и действует так же. Оба случая легко пропустить в собственном резюме, потому что глаз читает ожидаемый год. Проверка допускает даты до двух лет вперёд, потому что подписанный контракт или срочная должность могут законно заканчиваться в следующем году, и не учитывает образование, где ожидаемая дата окончания — обычное дело.",
        "es": "Los sistemas de seguimiento de candidaturas calculan los años de experiencia a partir de las fechas de cada entrada, y se filtra por ese número. Un rango cuyo final va antes que su inicio no tiene duración, así que el sistema lo descarta o no registra nada, y la experiencia que debía demostrar desaparece de toda búsqueda por años. Esta herramienta hace lo mismo: un rango al revés no suma nada a la experiencia que compara con una oferta. Una fecha años en el futuro casi siempre es una errata, 2052 por 2025, con el mismo efecto. Ambas cosas se pasan por alto en el propio CV, porque el ojo lee el año que espera. Se admiten fechas hasta dos años por delante, porque un contrato firmado o un puesto temporal pueden terminar legítimamente el año siguiente, y se ignora la formación, donde una fecha prevista de titulación es normal.",
        "nl": "Sollicitatiesystemen berekenen jaren ervaring uit de data van elk onderdeel, en recruiters filteren op dat getal. Een periode die eindigt voordat hij begint, heeft geen duur, dus het systeem laat hem vallen of legt niets vast — en de ervaring die hij moest aantonen, valt uit elke zoekopdracht op jaren. Dit hulpmiddel doet hetzelfde: een achterstevoren periode telt niet mee in de ervaring die met een vacature wordt vergeleken. Een datum jaren in de toekomst is bijna altijd een typfout, 2052 voor 2025, met hetzelfde effect. Beide zie je in je eigen cv makkelijk over het hoofd, omdat het oog het verwachte jaar leest. Data tot twee jaar vooruit worden toegestaan, omdat een getekend contract of een tijdelijke functie terecht volgend jaar kan eindigen, en opleiding wordt overgeslagen, waar een verwachte afstudeerdatum normaal is.",
        "fr": "Les logiciels de recrutement calculent les années d'expérience à partir des dates de chaque entrée, et le filtrage se fait sur ce chiffre. Une période dont la fin précède le début n'a pas de durée : le système l'écarte ou n'enregistre rien, et l'expérience qu'elle devait prouver disparaît de toute recherche par années. Cet outil fait de même : une période à l'envers n'ajoute rien à l'expérience comparée à une offre. Une date située des années dans le futur est presque toujours une coquille, 2052 pour 2025, avec le même effet. Les deux passent facilement inaperçues dans son propre CV, car l'œil lit l'année qu'il attend. Les dates jusqu'à deux ans à l'avance sont admises, car un contrat signé ou un poste à durée déterminée peut légitimement se terminer l'année suivante, et la formation est ignorée, où une date de diplôme prévue est normale.",
    },
    "first_person_in_cv": {
        "en": "German guidance on the tabular Lebenslauf and US career-office guidance agree on this from opposite ends of the same format: under each entry you write fragments, not sentences, and never about yourself. \"Led a team of five\" rather than \"I led a team of five\"; \"Stationsleitung, Dienstplanung\" rather than \"Ich habe die Station geleitet\". The fragment is faster to scan, which is the whole purpose of a tabular CV, and the pronoun adds nothing — every line in it is about you already. Both make the same exception: a short profile of two to four sentences under your name may be written in the first person, and this check does not look there. The entries under experience, education and skills are counted.",
        "de": "Die deutsche Beratung zum tabellarischen Lebenslauf und die Karriereberatung in den USA sind sich hier einig: Unter jeder Station stehen Stichpunkte, keine ganzen Sätze, und schon gar keine über sich selbst. \"Stationsleitung, Dienstplanung\" statt \"Ich habe die Station geleitet\". Stichpunkte lassen sich schneller überfliegen, und genau dafür ist der tabellarische Lebenslauf da; das \"ich\" fügt nichts hinzu, denn jede Zeile handelt ohnehin von Ihnen. Beide machen dieselbe Ausnahme: Ein Kurzprofil von zwei bis vier Sätzen unter dem Namen darf in der Ich-Form stehen, und dort schaut diese Prüfung nicht hin. Gezählt werden die Einträge unter Berufserfahrung, Ausbildung und Kenntnissen.",
        "uk": "Німецькі поради щодо табличного Lebenslauf і поради американських кар'єрних центрів тут збігаються: під кожним записом пишуть короткі фрази, а не речення, і ніколи — про себе. «Керування командою з п'яти осіб» замість «Я керував командою з п'яти осіб». Фрази швидше проглядати, а саме для цього й існує табличне резюме; займенник нічого не додає, бо кожен рядок і так про вас. Обидві традиції роблять однаковий виняток: короткий профіль із двох-чотирьох речень під вашим іменем можна писати від першої особи, і туди ця перевірка не заглядає. Рахуються записи в розділах досвіду, освіти й навичок.",
        "ru": "Немецкие советы по табличному Lebenslauf и советы американских карьерных центров здесь совпадают: под каждой записью пишут короткие фразы, а не предложения, и никогда — о себе. «Руководство командой из пяти человек» вместо «Я руководил командой из пяти человек». Фразы быстрее просматривать, а именно для этого и существует табличное резюме; местоимение ничего не добавляет, потому что каждая строка и так о вас. Обе традиции делают одинаковое исключение: короткий профиль из двух-четырёх предложений под вашим именем можно писать от первого лица, и туда эта проверка не заглядывает. Учитываются записи в разделах опыта, образования и навыков.",
        "es": "La orientación alemana sobre el Lebenslauf tabular y la de los servicios de carrera de EE. UU. coinciden en esto: bajo cada entrada se escriben fragmentos, no frases, y nunca sobre uno mismo. \"Dirección de un equipo de cinco personas\" en lugar de \"Dirigí un equipo de cinco personas\". Los fragmentos se leen más rápido, que es para lo que existe un CV tabular, y el pronombre no aporta nada: cada línea ya habla de ti. Ambas hacen la misma excepción: un perfil breve de dos a cuatro frases bajo tu nombre puede ir en primera persona, y esta comprobación no mira ahí. Se cuentan las entradas de experiencia, formación y competencias.",
        "nl": "Duits advies over de tabellarische Lebenslauf en Amerikaans loopbaanadvies zijn het hierover eens: onder elk onderdeel schrijf je fragmenten, geen zinnen, en nooit over jezelf. \"Leiding aan een team van vijf\" in plaats van \"Ik gaf leiding aan een team van vijf\". Fragmenten scan je sneller, en daar is een tabellarisch cv voor; het \"ik\" voegt niets toe, want elke regel gaat al over jou. Beide maken dezelfde uitzondering: een kort profiel van twee tot vier zinnen onder je naam mag in de ik-vorm, en daar kijkt deze controle niet. De onderdelen onder werkervaring, opleiding en vaardigheden worden meegeteld.",
        "fr": "Les conseils allemands sur le Lebenslauf tabulaire et ceux des services carrière américains s'accordent sur ce point : sous chaque entrée, on écrit des fragments, pas des phrases, et jamais sur soi. « Direction d'une équipe de cinq personnes » plutôt que « J'ai dirigé une équipe de cinq personnes ». Un fragment se parcourt plus vite, ce qui est la raison d'être d'un CV tabulaire, et le pronom n'apporte rien : chaque ligne parle déjà de vous. Les deux font la même exception : un court profil de deux à quatre phrases sous votre nom peut être rédigé à la première personne, et ce contrôle n'y regarde pas. Les entrées d'expérience, de formation et de compétences sont comptées.",
    },
    "outdated_personal_details": {
        "en": "Religion, marital status, children and parents' names or professions were once a standard block at the top of a German CV. Since the Allgemeines Gleichbehandlungsgesetz of 2006 employers may not disadvantage applicants on grounds that include religion, and careful ones would rather not receive that information at all. Family details are not a protected ground in themselves, but they are no longer expected: guidance treats them as optional and most applicants now leave them out, so including them mainly dates the CV. None of this is an error, and you are free to keep them. The one real exception is religion when you apply to a church employer — a Caritas or Diakonie hospital, a church-run school — where it can be relevant. Date of birth, nationality and a photo are not reported here: they are optional as well, but still commonly given in Germany, and leaving them in is a choice rather than an oversight.",
        "de": "Konfession, Familienstand, Kinder sowie Namen oder Berufe der Eltern waren früher ein fester Block oben im deutschen Lebenslauf. Seit dem Allgemeinen Gleichbehandlungsgesetz von 2006 dürfen Arbeitgeber Bewerbende unter anderem wegen der Religion nicht benachteiligen, und sorgfältige Arbeitgeber möchten diese Angabe lieber gar nicht erst erhalten. Familiäre Angaben sind für sich genommen kein geschütztes Merkmal, werden aber nicht mehr erwartet: Die Beratung behandelt sie als freiwillig, und die meisten lassen sie inzwischen weg, sodass sie den Lebenslauf vor allem altmodisch wirken lassen. Ein Fehler ist nichts davon, und Sie dürfen die Angaben behalten. Die eine echte Ausnahme ist die Konfession bei einem kirchlichen Arbeitgeber — einem Krankenhaus der Caritas oder Diakonie, einer kirchlichen Schule —, wo sie relevant sein kann. Geburtsdatum, Staatsangehörigkeit und Foto werden hier nicht gemeldet: Sie sind ebenfalls freiwillig, werden in Deutschland aber weiterhin häufig angegeben, und sie stehen zu lassen ist eine Entscheidung, kein Versehen.",
        "uk": "Віросповідання, сімейний стан, діти, імена чи професії батьків колись були стандартним блоком угорі німецького резюме. Від ухвалення Allgemeines Gleichbehandlungsgesetz 2006 року роботодавці не можуть утискати кандидатів, зокрема через релігію, а обачні воліють узагалі не отримувати цих даних. Сімейні відомості самі по собі не є захищеною ознакою, але їх більше не очікують: поради вважають їх необов'язковими, і більшість кандидатів їх уже не вказує, тож вони передусім роблять резюме застарілим. Жодне з цього не є помилкою, і ви можете їх лишити. Єдиний справжній виняток — віросповідання, коли ви подаєтеся до церковного роботодавця: лікарні Caritas чи Diakonie, церковної школи, — там воно може мати значення. Дата народження, громадянство й фото тут не позначаються: вони теж необов'язкові, але в Німеччині їх досі часто вказують, і лишити їх — це вибір, а не недогляд.",
        "ru": "Вероисповедание, семейное положение, дети, имена или профессии родителей когда-то были стандартным блоком вверху немецкого резюме. С принятия Allgemeines Gleichbehandlungsgesetz 2006 года работодатели не могут ущемлять кандидатов, в том числе из-за религии, а осмотрительные предпочитают вовсе не получать этих данных. Семейные сведения сами по себе не являются защищённым признаком, но их больше не ожидают: советы считают их необязательными, и большинство кандидатов их уже не указывает, поэтому они прежде всего делают резюме устаревшим. Ничто из этого не является ошибкой, и вы можете их оставить. Единственное настоящее исключение — вероисповедание, если вы откликаетесь к церковному работодателю: больнице Caritas или Diakonie, церковной школе, — там оно может иметь значение. Дата рождения, гражданство и фото здесь не отмечаются: они тоже необязательны, но в Германии их по-прежнему часто указывают, и оставить их — это выбор, а не недосмотр.",
        "es": "La religión, el estado civil, los hijos y los nombres o profesiones de los padres eran antes un bloque fijo arriba en un CV alemán. Desde la Allgemeines Gleichbehandlungsgesetz de 2006, las empresas no pueden perjudicar a una candidatura, entre otros motivos, por su religión, y las cuidadosas prefieren no recibir ese dato en absoluto. Los datos familiares no son en sí un motivo protegido, pero ya no se esperan: la orientación los considera opcionales y la mayoría ya no los incluye, así que sobre todo envejecen el CV. Nada de esto es un error, y puedes conservarlos. La única excepción real es la religión cuando te presentas a un empleador eclesiástico —un hospital de Caritas o de Diakonie, un colegio religioso—, donde puede ser relevante. La fecha de nacimiento, la nacionalidad y la foto no se indican aquí: también son opcionales, pero en Alemania se siguen incluyendo con frecuencia, y dejarlos es una decisión, no un descuido.",
        "nl": "Geloof, burgerlijke staat, kinderen en namen of beroepen van ouders waren ooit een vast blok bovenaan een Duits cv. Sinds de Allgemeines Gleichbehandlungsgesetz van 2006 mogen werkgevers sollicitanten onder meer vanwege hun geloof niet benadelen, en zorgvuldige werkgevers ontvangen die informatie liever helemaal niet. Gezinsgegevens zijn op zich geen beschermde grond, maar ze worden niet meer verwacht: het advies noemt ze optioneel en de meeste sollicitanten laten ze weg, dus ze maken het cv vooral gedateerd. Niets hiervan is een fout, en je mag ze houden. De enige echte uitzondering is geloof als je solliciteert bij een kerkelijke werkgever — een ziekenhuis van Caritas of Diakonie, een kerkelijke school —, waar het relevant kan zijn. Geboortedatum, nationaliteit en foto worden hier niet gemeld: die zijn ook optioneel, maar worden in Duitsland nog vaak vermeld, en ze laten staan is een keuze, geen vergissing.",
        "fr": "La religion, la situation familiale, les enfants et les noms ou professions des parents formaient autrefois un bloc habituel en tête d'un CV allemand. Depuis l'Allgemeines Gleichbehandlungsgesetz de 2006, un employeur ne peut pas désavantager une candidature en raison notamment de la religion, et un employeur prudent préfère ne pas recevoir cette information du tout. Les données familiales ne sont pas en elles-mêmes un motif protégé, mais elles ne sont plus attendues : les conseils les jugent facultatives et la plupart des candidatures les omettent, si bien qu'elles datent surtout le CV. Rien de tout cela n'est une erreur, et vous pouvez les garder. La seule vraie exception est la religion lorsque vous postulez auprès d'un employeur confessionnel — un hôpital de Caritas ou de la Diakonie, une école confessionnelle —, où elle peut compter. La date de naissance, la nationalité et la photo ne sont pas signalées ici : elles sont facultatives aussi, mais encore souvent indiquées en Allemagne, et les laisser est un choix, pas un oubli.",
    },
    "oldest_entry_first": {
        "en": "Reverse chronological order — the current or most recent role at the top, earlier ones below — is the standard in German CVs and in the US format it came from. The reason is time: a recruiter decides in seconds, and what someone does now says more about them than what they did first. A CV that opens with an apprenticeship from fifteen years ago makes the reader dig to the bottom for the answer to the only question they had. The classic chronological Lebenslauf is not wrong, only dated, which is why this is reported as low. It is reported only when at least three dated jobs run consistently upwards, so a single side job listed out of order does not trigger it.",
        "de": "Die antichronologische Reihenfolge — aktuelle oder letzte Station oben, frühere darunter — ist im deutschen Lebenslauf Standard, übernommen aus dem amerikanischen Format. Der Grund ist Zeit: Über eine Bewerbung wird in Sekunden entschieden, und was jemand heute tut, sagt mehr als das, womit er angefangen hat. Ein Lebenslauf, der mit einer Ausbildung von vor fünfzehn Jahren beginnt, zwingt dazu, bis nach unten zu suchen, um die einzige Frage zu beantworten, die man hatte. Der klassische chronologische Lebenslauf ist nicht falsch, nur altmodisch — deshalb wird er als gering gemeldet. Gemeldet wird nur, wenn mindestens drei datierte Stationen durchgehend aufsteigen, damit ein einzelner falsch einsortierter Nebenjob nichts auslöst.",
        "uk": "Зворотний хронологічний порядок — поточна чи остання посада вгорі, попередні нижче — стандарт німецького резюме, запозичений з американського формату. Причина в часі: рекрутер ухвалює рішення за секунди, а те, чим людина займається зараз, каже про неї більше, ніж те, з чого вона починала. Резюме, що відкривається навчанням п'ятнадцятирічної давності, змушує шукати внизу відповідь на єдине запитання, яке було в рекрутера. Класичне хронологічне резюме не є помилкою, лише виглядає застарілим, тому знахідка має низьку важливість. Вона з'являється лише тоді, коли щонайменше три датовані посади послідовно йдуть угору, тож одна випадково переставлена підробітка її не викликає.",
        "ru": "Обратный хронологический порядок — текущая или последняя должность вверху, предыдущие ниже — стандарт немецкого резюме, заимствованный из американского формата. Причина во времени: рекрутер принимает решение за секунды, а то, чем человек занимается сейчас, говорит о нём больше, чем то, с чего он начинал. Резюме, открывающееся учёбой пятнадцатилетней давности, заставляет искать внизу ответ на единственный вопрос, который был у рекрутера. Классическое хронологическое резюме не является ошибкой, лишь выглядит устаревшим, поэтому находка имеет низкую важность. Она появляется только тогда, когда минимум три датированные должности последовательно идут вверх, так что одна случайно переставленная подработка её не вызывает.",
        "es": "El orden cronológico inverso —el puesto actual o más reciente arriba y los anteriores debajo— es el estándar en los CV alemanes y en el formato estadounidense del que procede. La razón es el tiempo: se decide en segundos, y lo que alguien hace ahora dice más que aquello con lo que empezó. Un CV que abre con una formación profesional de hace quince años obliga a buscar hasta abajo la respuesta a la única pregunta que había. El Lebenslauf cronológico clásico no está mal, solo anticuado, y por eso se indica como bajo. Solo se indica cuando al menos tres empleos fechados van de forma constante hacia arriba, para que un único trabajo secundario mal colocado no lo active.",
        "nl": "Omgekeerd chronologische volgorde — de huidige of laatste functie bovenaan, eerdere eronder — is de standaard in Duitse cv's en in het Amerikaanse formaat waar ze vandaan komt. De reden is tijd: een recruiter beslist in seconden, en wat iemand nu doet zegt meer dan waarmee hij begon. Een cv dat opent met een opleiding van vijftien jaar geleden laat de lezer tot onderaan zoeken naar het antwoord op de enige vraag die hij had. De klassieke chronologische Lebenslauf is niet fout, alleen gedateerd, en daarom wordt dit als laag gemeld. Het wordt alleen gemeld als ten minste drie gedateerde banen consequent oplopen, zodat één verkeerd geplaatste bijbaan het niet activeert.",
        "fr": "L'ordre antichronologique — le poste actuel ou le plus récent en haut, les précédents en dessous — est la norme des CV allemands et du format américain dont il vient. La raison est le temps : on décide en quelques secondes, et ce que quelqu'un fait aujourd'hui en dit plus que ce par quoi il a commencé. Un CV qui s'ouvre sur une formation d'il y a quinze ans oblige à chercher tout en bas la réponse à la seule question qu'on se posait. Le Lebenslauf chronologique classique n'est pas faux, seulement daté, d'où un signalement faible. Il n'est signalé que lorsqu'au moins trois emplois datés montent de manière constante, pour qu'un seul job d'appoint mal placé ne le déclenche pas.",
    },
}

RULE_FIXES: dict[str, dict[str, list[str]]] = {
    "contact_only_as_link": {
        "en": [
            "Write the address out in full in the first three lines: name@example.com and +49 170 1234567, as ordinary text under your name.",
            "Keep the profile link as well — it costs nothing and helps a human reader. It just cannot be the only route.",
            "Check it: open the file, select all, paste into a plain text editor. If your email is not in what you pasted, no parser will find it either.",
        ],
        "de": [
            "Schreiben Sie die Adresse in den ersten drei Zeilen aus: name@example.com und +49 170 1234567, als gewöhnlicher Text unter Ihrem Namen.",
            "Behalten Sie den Profil-Link ruhig — er kostet nichts und hilft menschlichen Lesenden. Er darf nur nicht der einzige Weg sein.",
            "Prüfen Sie es: Datei öffnen, alles markieren, in einen einfachen Texteditor einfügen. Steht Ihre E-Mail nicht darin, findet sie auch kein Parser.",
        ],
        "uk": [
            "Випишіть адресу повністю в перших трьох рядках: name@example.com і +380 67 1234567, звичайним текстом під вашим іменем.",
            "Посилання на профіль лишіть — воно нічого не коштує й допомагає людині. Просто воно не має бути єдиним шляхом.",
            "Перевірте: відкрийте файл, виділіть усе, вставте у простий текстовий редактор. Якщо вашої пошти там немає, її не знайде й жоден парсер.",
        ],
        "ru": [
            "Выпишите адрес полностью в первых трёх строках: name@example.com и +7 900 1234567, обычным текстом под вашим именем.",
            "Ссылку на профиль оставьте — она ничего не стоит и помогает человеку. Просто она не должна быть единственным путём.",
            "Проверьте: откройте файл, выделите всё, вставьте в простой текстовый редактор. Если вашей почты там нет, её не найдёт и никакой парсер.",
        ],
        "es": [
            "Escribe la dirección completa en las tres primeras líneas: nombre@ejemplo.com y +34 600 123 456, como texto normal bajo tu nombre.",
            "Deja también el enlace al perfil: no cuesta nada y ayuda a quien lee. Solo no puede ser la única vía.",
            "Compruébalo: abre el archivo, selecciona todo y pégalo en un editor de texto plano. Si tu correo no está ahí, ningún analizador lo encontrará.",
        ],
        "nl": [
            "Schrijf het adres voluit in de eerste drie regels: naam@voorbeeld.nl en +31 6 12345678, als gewone tekst onder je naam.",
            "Laat de profiellink gerust staan — die kost niets en helpt een menselijke lezer. Alleen mag het niet de enige weg zijn.",
            "Controleer het: open het bestand, selecteer alles, plak het in een kale teksteditor. Staat je e-mailadres er niet in, dan vindt geen parser het.",
        ],
        "fr": [
            "Écrivez l'adresse en toutes lettres dans les trois premières lignes : nom@exemple.com et +33 6 12 34 56 78, en texte ordinaire sous votre nom.",
            "Gardez aussi le lien vers le profil : il ne coûte rien et aide un lecteur humain. Il ne peut simplement pas être le seul chemin.",
            "Vérifiez : ouvrez le fichier, tout sélectionner, coller dans un éditeur de texte brut. Si votre e-mail n'y est pas, aucun analyseur ne le trouvera.",
        ],
    },
    "unrecognised_section_headings": {
        "en": [
            "Rename the headings to the plain words: Experience, Education, Skills. These are what software looks for, and a reader loses nothing by them.",
            "Keep your own phrasing as a line underneath the heading if you like it — it reads to a person and costs the parser nothing.",
            "Check it: search the file for the word Experience. If it is not there, no software reading it knows where your history begins.",
        ],
        "de": [
            "Benennen Sie die Überschriften in die schlichten Wörter um: Berufserfahrung, Ausbildung, Kenntnisse. Danach sucht Software, und Lesende verlieren nichts.",
            "Ihre eigene Formulierung können Sie als Zeile darunter behalten, wenn Sie daran hängen — Menschen lesen sie, den Parser kostet sie nichts.",
            "Prüfen Sie es: Suchen Sie in der Datei nach dem Wort Berufserfahrung. Steht es nicht darin, weiß keine Software, wo Ihr Werdegang beginnt.",
        ],
        "uk": [
            "Перейменуйте заголовки на прості слова: Досвід, Освіта, Навички. Саме їх шукає програма, а читач від цього нічого не втрачає.",
            "Власне формулювання лишіть рядком нижче, якщо воно вам дороге — людина його прочитає, а парсерові воно нічого не коштує.",
            "Перевірте: пошукайте у файлі слово «Досвід». Якщо його немає, жодна програма не знає, де починається ваш шлях.",
        ],
        "ru": [
            "Переименуйте заголовки в простые слова: Опыт, Образование, Навыки. Именно их ищет программа, а читатель от этого ничего не теряет.",
            "Собственную формулировку оставьте строкой ниже, если она вам дорога — человек её прочитает, а парсеру она ничего не стоит.",
            "Проверьте: поищите в файле слово «Опыт». Если его нет, никакая программа не знает, где начинается ваш путь.",
        ],
        "es": [
            "Renombra los títulos con las palabras sencillas: Experiencia, Formación, Competencias. Es lo que busca el software y quien lee no pierde nada.",
            "Conserva tu propia frase como línea debajo del título si te gusta: una persona la lee y al analizador no le cuesta nada.",
            "Compruébalo: busca la palabra Experiencia en el archivo. Si no está, ningún programa sabe dónde empieza tu trayectoria.",
        ],
        "nl": [
            "Hernoem de koppen naar de gewone woorden: Werkervaring, Opleiding, Vaardigheden. Daar zoekt software op, en een lezer verliest er niets mee.",
            "Houd je eigen formulering als regel eronder als je eraan hecht — een mens leest die, en de parser kost het niets.",
            "Controleer het: zoek in het bestand naar het woord Werkervaring. Staat het er niet, dan weet geen software waar je loopbaan begint.",
        ],
        "fr": [
            "Renommez les titres avec les mots simples : Expérience, Formation, Compétences. C'est ce que cherche un logiciel, et le lecteur n'y perd rien.",
            "Gardez votre propre formulation en ligne sous le titre si vous y tenez : une personne la lira, et l'analyseur n'en souffre pas.",
            "Vérifiez : cherchez le mot Expérience dans le fichier. S'il n'y est pas, aucun logiciel ne sait où commence votre parcours.",
        ],
    },
    "broken_characters": {
        "en": [
            "Delete the flagged word and retype it from scratch rather than editing it: a ligature or an invisible character survives most find-and-replace.",
            "Turn off automatic ligatures before exporting. In Word: Font → Advanced → Ligatures → None. In InDesign, uncheck Ligatures on the character panel.",
            "Check it: paste the file's text into a plain text editor and search for the word. If the search fails there, it will fail everywhere.",
        ],
        "de": [
            "Löschen Sie das gemeldete Wort und tippen Sie es neu, statt es zu bearbeiten: Eine Ligatur oder ein unsichtbares Zeichen übersteht die meisten Suchen-und-Ersetzen-Läufe.",
            "Schalten Sie automatische Ligaturen vor dem Export ab. In Word: Schriftart → Erweitert → Ligaturen → Keine. In InDesign den Haken bei Ligaturen entfernen.",
            "Prüfen Sie es: Text der Datei in einen einfachen Texteditor einfügen und nach dem Wort suchen. Scheitert die Suche dort, scheitert sie überall.",
        ],
        "uk": [
            "Видаліть позначене слово й наберіть його наново, а не редагуйте: лігатура чи невидимий символ переживає більшість замін через «знайти й замінити».",
            "Вимкніть автоматичні лігатури перед експортом. У Word: Шрифт → Додатково → Лігатури → Немає. В InDesign зніміть галочку «Лігатури».",
            "Перевірте: вставте текст файлу у простий текстовий редактор і пошукайте слово. Якщо пошук не спрацює там, він не спрацює ніде.",
        ],
        "ru": [
            "Удалите отмеченное слово и наберите его заново, а не редактируйте: лигатура или невидимый символ переживает большинство замен через «найти и заменить».",
            "Отключите автоматические лигатуры перед экспортом. В Word: Шрифт → Дополнительно → Лигатуры → Нет. В InDesign снимите галочку «Лигатуры».",
            "Проверьте: вставьте текст файла в простой текстовый редактор и поищите слово. Если поиск не сработает там, он не сработает нигде.",
        ],
        "es": [
            "Borra la palabra señalada y vuelve a escribirla desde cero en lugar de editarla: una ligadura o un carácter invisible sobrevive a casi cualquier buscar y reemplazar.",
            "Desactiva las ligaduras automáticas antes de exportar. En Word: Fuente → Avanzado → Ligaduras → Ninguna. En InDesign, desmarca Ligaduras.",
            "Compruébalo: pega el texto del archivo en un editor de texto plano y busca la palabra. Si la búsqueda falla ahí, fallará en todas partes.",
        ],
        "nl": [
            "Verwijder het gemarkeerde woord en typ het opnieuw in plaats van het te bewerken: een ligatuur of onzichtbaar teken overleeft de meeste zoek-en-vervangacties.",
            "Zet automatische ligaturen uit voor je exporteert. In Word: Lettertype → Geavanceerd → Ligaturen → Geen. In InDesign vink je Ligaturen uit.",
            "Controleer het: plak de tekst van het bestand in een kale teksteditor en zoek het woord. Lukt het zoeken daar niet, dan lukt het nergens.",
        ],
        "fr": [
            "Supprimez le mot signalé et retapez-le entièrement au lieu de le corriger : une ligature ou un caractère invisible survit à la plupart des rechercher-remplacer.",
            "Désactivez les ligatures automatiques avant l'export. Dans Word : Police → Avancé → Ligatures → Aucune. Dans InDesign, décochez Ligatures.",
            "Vérifiez : collez le texte du fichier dans un éditeur de texte brut et cherchez le mot. Si la recherche échoue là, elle échouera partout.",
        ],
    },
    "pdf_non_embedded_font": {
        "en": [
            'Re-export from Word with File → Save As → PDF, and under Options tick "PDF/A compliant" — that forces every font to be embedded.',
            'Switch the document to a common font (Arial, Calibri, Times New Roman, Georgia) and export again.',
            'Check it worked: open the PDF, then File → Properties → Fonts. Every entry should say "Embedded" or "Embedded Subset".',
        ],
        "de": [
            'Exportieren Sie neu aus Word: Datei → Speichern unter → PDF, und kreuzen Sie unter Optionen "PDF/A-kompatibel" an — das erzwingt das Einbetten aller Schriften.',
            'Stellen Sie das Dokument auf eine verbreitete Schrift um (Arial, Calibri, Times New Roman, Georgia) und exportieren Sie erneut.',
            'Prüfen Sie es: Öffnen Sie das PDF, dann Datei → Eigenschaften → Schriften. Bei jedem Eintrag sollte "Eingebettet" oder "Eingebettete Untergruppe" stehen.',
        ],
        "uk": [
            'Експортуйте з Word заново: Файл → Зберегти як → PDF, у Параметрах позначте "Сумісний з PDF/A" — це змусить вбудувати всі шрифти.',
            'Переведіть документ на поширений шрифт (Arial, Calibri, Times New Roman, Georgia) і експортуйте ще раз.',
            'Перевірте результат: відкрийте PDF, далі Файл → Властивості → Шрифти. Біля кожного має бути "Вбудований" або "Вбудована підмножина".',
        ],
        "ru": [
            'Экспортируйте из Word заново: Файл → Сохранить как → PDF, в Параметрах отметьте "Совместимый с PDF/A" — это заставит встроить все шрифты.',
            'Переведите документ на распространённый шрифт (Arial, Calibri, Times New Roman, Georgia) и экспортируйте ещё раз.',
            'Проверьте результат: откройте PDF, далее Файл → Свойства → Шрифты. У каждого должно быть "Встроенный" или "Встроенное подмножество".',
        ],
        "es": [
            'Vuelve a exportar desde Word con Archivo → Guardar como → PDF y, en Opciones, marca "Compatible con PDF/A": eso obliga a incrustar todas las fuentes.',
            'Cambia el documento a una fuente común (Arial, Calibri, Times New Roman, Georgia) y expórtalo de nuevo.',
            'Comprueba que funcionó: abre el PDF y ve a Archivo → Propiedades → Fuentes. Cada entrada debe decir "Incrustada" o "Subconjunto incrustado".',
        ],
        "nl": [
            'Exporteer opnieuw vanuit Word via Bestand → Opslaan als → PDF en vink bij Opties "PDF/A-compatibel" aan — dat dwingt insluiting van alle lettertypen af.',
            'Zet het document over op een gangbaar lettertype (Arial, Calibri, Times New Roman, Georgia) en exporteer opnieuw.',
            'Controleer het: open de PDF en ga naar Bestand → Eigenschappen → Lettertypen. Bij elk item hoort "Ingesloten" of "Ingesloten subset" te staan.',
        ],
        "fr": [
            'Réexportez depuis Word via Fichier → Enregistrer sous → PDF et cochez "Compatible PDF/A" dans les Options : cela force l\'incorporation de toutes les polices.',
            'Passez le document à une police courante (Arial, Calibri, Times New Roman, Georgia) et réexportez.',
            'Vérifiez : ouvrez le PDF, puis Fichier → Propriétés → Polices. Chaque entrée doit indiquer "Incorporée" ou "Sous-ensemble incorporé".',
        ],
    },
    "pdf_repeated_header_footer_content": {
        "en": [
            'Move your phone and email into the body of the CV, in the first few lines under your name.',
            'Leave only page numbers in the header and footer — nothing you would mind losing.',
            'Check it worked: select all the text in the PDF and paste it into a plain text editor. If your contact details are missing there, they are at risk.',
        ],
        "de": [
            'Verschieben Sie Telefon und E-Mail in den Fließtext des Lebenslaufs, in die ersten Zeilen unter Ihrem Namen.',
            'Lassen Sie in Kopf- und Fußzeile nur Seitenzahlen stehen — nichts, dessen Verlust schmerzt.',
            'Prüfen: gesamten Text im PDF markieren und in einen einfachen Texteditor einfügen. Fehlen dort Ihre Kontaktdaten, sind sie gefährdet.',
        ],
        "uk": [
            'Перенесіть телефон і пошту в основний текст резюме, у перші рядки під вашим іменем.',
            'У колонтитулах залиште тільки номери сторінок — нічого такого, що шкода втратити.',
            'Перевірте результат: виділіть увесь текст у PDF і вставте у простий текстовий редактор. Якщо контактів там немає — вони під загрозою.',
        ],
        "ru": [
            'Перенесите телефон и почту в основной текст резюме, в первые строки под вашим именем.',
            'В колонтитулах оставьте только номера страниц — ничего такого, что жаль потерять.',
            'Проверьте результат: выделите весь текст в PDF и вставьте в простой текстовый редактор. Если контактов там нет — они под угрозой.',
        ],
        "es": [
            'Lleva tu teléfono y correo al cuerpo del CV, en las primeras líneas bajo tu nombre.',
            'Deja en el encabezado y el pie solo los números de página: nada que te importe perder.',
            'Comprueba que funcionó: selecciona todo el texto del PDF y pégalo en un editor de texto plano. Si tus datos de contacto no aparecen, están en riesgo.',
        ],
        "nl": [
            'Verplaats je telefoonnummer en e-mail naar de tekst van het cv, in de eerste regels onder je naam.',
            'Laat in de kop- en voettekst alleen paginanummers staan — niets wat je zou missen.',
            'Controleer het: selecteer alle tekst in de PDF en plak die in een kale teksteditor. Ontbreken je contactgegevens daar, dan lopen ze gevaar.',
        ],
        "fr": [
            'Déplacez votre téléphone et votre e-mail dans le corps du CV, dans les premières lignes sous votre nom.',
            'Ne laissez que les numéros de page en en-tête et pied de page — rien dont la perte compte.',
            "Vérifiez : sélectionnez tout le texte du PDF et collez-le dans un éditeur de texte brut. Si vos coordonnées n'y sont pas, elles sont en péril.",
        ],
    },
    "pdf_textless_image": {
        "en": [
            'If the image is a name plate, a title bar or a skills chart, retype it as real text — that is the whole fix.',
            'If it is a portrait photo, it costs you no text. Keep it or not depending on the market: normal in Germany and much of Europe, usually left off in the US, UK and Ireland.',
            'Check which it is: open the PDF and press Ctrl+A. Anything that does not highlight is a picture, not text.',
        ],
        "de": [
            'Ist das Bild ein Namensschild, ein Titelbalken oder ein Kompetenzdiagramm, tippen Sie es als echten Text ab — das ist die ganze Lösung.',
            'Ist es ein Porträtfoto, kostet es keinen Text. Behalten oder nicht, je nach Markt: in Deutschland und weiten Teilen Europas üblich, in den USA, UK und Irland meist weggelassen.',
            'Prüfen, was es ist: PDF öffnen und Strg+A drücken. Was nicht markiert wird, ist ein Bild, kein Text.',
        ],
        "uk": [
            'Якщо це банер з іменем, титульна смуга чи діаграма навичок — наберіть це справжнім текстом, і проблему вичерпано.',
            'Якщо це портретне фото, жодного тексту через нього не втрачається. Лишати чи ні — залежить від ринку: у Німеччині та більшості Європи звично, у США, Британії та Ірландії зазвичай не додають.',
            'Перевірте, що саме там: відкрийте PDF і натисніть Ctrl+A. Усе, що не виділилось, — зображення, а не текст.',
        ],
        "ru": [
            'Если это баннер с именем, титульная полоса или диаграмма навыков — наберите это настоящим текстом, и проблема исчерпана.',
            'Если это портретное фото, никакого текста из-за него не теряется. Оставлять или нет — зависит от рынка: в Германии и большей части Европы привычно, в США, Британии и Ирландии обычно не добавляют.',
            'Проверьте, что именно там: откройте PDF и нажмите Ctrl+A. Всё, что не выделилось, — изображение, а не текст.',
        ],
        "es": [
            'Si la imagen es un rótulo con el nombre, una barra de título o un gráfico de competencias, vuelve a escribir su contenido como texto real: ahí acaba el problema.',
            'Si es una foto de retrato, no supone ninguna pérdida de texto. Mantenerla o no depende del mercado: habitual en Alemania y buena parte de Europa, normalmente se omite en EE. UU., Reino Unido e Irlanda.',
            'Comprueba cuál es: abre el PDF y pulsa Ctrl+A. Lo que no se resalte es una imagen, no texto.',
        ],
        "nl": [
            'Is de afbeelding een naambanner, titelbalk of vaardighedendiagram, typ het dan over als echte tekst — daarmee is het opgelost.',
            'Is het een portretfoto, dan kost het je geen tekst. Houden of niet hangt van de markt af: gebruikelijk in Duitsland en veel van Europa, in de VS, het VK en Ierland meestal weggelaten.',
            'Kijk wat het is: open de PDF en druk Ctrl+A. Alles wat niet oplicht is een afbeelding, geen tekst.',
        ],
        "fr": [
            "Si l'image est un bandeau de nom, une barre de titre ou un graphique de compétences, ressaisissez-la en vrai texte : le problème est réglé.",
            "S'il s'agit d'une photo de portrait, elle ne vous coûte aucun texte. La garder ou non dépend du marché : courante en Allemagne et dans une grande partie de l'Europe, généralement omise aux États-Unis, au Royaume-Uni et en Irlande.",
            "Vérifiez de quoi il s'agit : ouvrez le PDF et appuyez sur Ctrl+A. Tout ce qui ne se surligne pas est une image, pas du texte.",
        ],
    },
    "docx_table_content": {
        "en": [
            'Convert the table to plain text: click in it, then Table Layout → Convert to Text → separate with paragraph marks.',
            'Rebuild the alignment with tab stops or plain line breaks instead of a table.',
            'Keep tables only for genuinely tabular data. A two-column page layout is not tabular data.',
        ],
        "de": [
            'Wandeln Sie die Tabelle in Text um: hineinklicken, dann Tabellenlayout → In Text konvertieren → mit Absatzmarken trennen.',
            'Bauen Sie die Ausrichtung mit Tabstopps oder einfachen Zeilenumbrüchen statt mit einer Tabelle nach.',
            'Tabellen nur für echte Tabellendaten verwenden. Ein zweispaltiges Seitenlayout ist kein Tabelleninhalt.',
        ],
        "uk": [
            'Перетворіть таблицю на текст: клацніть у ній, далі Макет таблиці → Перетворити на текст → розділяти знаками абзацу.',
            'Відтворіть вирівнювання табуляціями або звичайними переносами рядків замість таблиці.',
            'Лишайте таблиці лише для справді табличних даних. Двоколонкова верстка сторінки — це не табличні дані.',
        ],
        "ru": [
            'Преобразуйте таблицу в текст: щёлкните в ней, далее Макет таблицы → Преобразовать в текст → разделять знаками абзаца.',
            'Воспроизведите выравнивание табуляциями или обычными переносами строк вместо таблицы.',
            'Оставляйте таблицы только для действительно табличных данных. Двухколоночная вёрстка страницы — это не табличные данные.',
        ],
        "es": [
            'Convierte la tabla en texto: haz clic dentro y ve a Disposición de tabla → Convertir en texto → separar con marcas de párrafo.',
            'Rehaz la alineación con tabuladores o saltos de línea normales en lugar de una tabla.',
            'Reserva las tablas para datos realmente tabulares. Una maquetación a dos columnas no es contenido tabular.',
        ],
        "nl": [
            'Zet de tabel om naar tekst: klik erin en ga naar Tabelindeling → Converteren naar tekst → scheiden met alineamarkeringen.',
            'Bouw de uitlijning opnieuw op met tabstops of gewone regeleinden in plaats van een tabel.',
            'Gebruik tabellen alleen voor echt tabellarische gegevens. Een pagina-indeling met twee kolommen is dat niet.',
        ],
        "fr": [
            'Convertissez le tableau en texte : cliquez dedans, puis Disposition du tableau → Convertir en texte → séparer par des marques de paragraphe.',
            "Refaites l'alignement avec des taquets de tabulation ou de simples sauts de ligne plutôt qu'un tableau.",
            "Réservez les tableaux aux données réellement tabulaires. Une mise en page à deux colonnes n'en est pas.",
        ],
    },
    "docx_header_footer_content": {
        "en": [
            'Move everything you need read into the document body — header and footer should hold nothing you would mind losing.',
            'Put your contact details in the first few lines under your name, as ordinary paragraphs.',
            'Check it worked: press Ctrl+A in Word. If text does not highlight, it is not in the body and a parser will likely miss it.',
        ],
        "de": [
            'Verschieben Sie alles, was gelesen werden soll, in den Textkörper — in Kopf- und Fußzeile gehört nichts, dessen Verlust schmerzt.',
            'Setzen Sie Ihre Kontaktdaten als normale Absätze in die ersten Zeilen unter Ihrem Namen.',
            'Prüfen: Strg+A in Word drücken. Was nicht markiert wird, steht nicht im Körper und wird von einem Parser wahrscheinlich übersehen.',
        ],
        "uk": [
            'Перенесіть у тіло документа все, що має бути прочитане — у колонтитулах не місце нічому, що шкода втратити.',
            'Розмістіть контакти звичайними абзацами в перших рядках під вашим іменем.',
            'Перевірте результат: натисніть Ctrl+A у Word. Якщо текст не виділився — він не в тілі документа, і парсер його, найімовірніше, не побачить.',
        ],
        "ru": [
            'Перенесите в тело документа всё, что должно быть прочитано — в колонтитулах не место ничему, что жаль потерять.',
            'Разместите контакты обычными абзацами в первых строках под вашим именем.',
            'Проверьте результат: нажмите Ctrl+A в Word. Если текст не выделился — он не в теле документа, и парсер его, скорее всего, не увидит.',
        ],
        "es": [
            'Lleva al cuerpo del documento todo lo que quieras que se lea: en el encabezado y el pie no debe quedar nada que te importe perder.',
            'Pon tus datos de contacto como párrafos normales en las primeras líneas bajo tu nombre.',
            'Comprueba que funcionó: pulsa Ctrl+A en Word. Si un texto no se resalta, no está en el cuerpo y es probable que un analizador lo pase por alto.',
        ],
        "nl": [
            'Verplaats alles wat gelezen moet worden naar de hoofdtekst — in kop- en voettekst hoort niets wat je zou missen.',
            "Zet je contactgegevens als gewone alinea's in de eerste regels onder je naam.",
            'Controleer het: druk Ctrl+A in Word. Licht tekst niet op, dan staat die niet in de hoofdtekst en mist een parser die waarschijnlijk.',
        ],
        "fr": [
            "Déplacez dans le corps du document tout ce qui doit être lu — l'en-tête et le pied de page ne doivent rien contenir dont la perte compte.",
            'Placez vos coordonnées en paragraphes ordinaires dans les premières lignes sous votre nom.',
            "Vérifiez : appuyez sur Ctrl+A dans Word. Si un texte ne se surligne pas, il n'est pas dans le corps et un analyseur le manquera probablement.",
        ],
    },
    "docx_text_box_content": {
        "en": [
            'Cut the text out of the box, paste it into the document as ordinary paragraphs, then delete the empty box.',
            'Replace a boxed sidebar with a normal heading followed by its content, in one column.',
            'Check it worked: press Ctrl+A in Word. Text still inside a box will not highlight.',
        ],
        "de": [
            'Schneiden Sie den Text aus dem Feld aus, fügen Sie ihn als normale Absätze ins Dokument ein und löschen Sie das leere Feld.',
            'Ersetzen Sie eine Seitenspalte im Textfeld durch eine normale Überschrift mit Inhalt darunter, einspaltig.',
            'Prüfen: Strg+A in Word drücken. Text, der noch im Feld steckt, wird nicht markiert.',
        ],
        "uk": [
            'Виріжте текст із поля, вставте його в документ звичайними абзацами, а порожнє поле видаліть.',
            'Замініть бічну колонку в текстовому полі на звичайний заголовок із вмістом під ним, в одну колонку.',
            'Перевірте результат: натисніть Ctrl+A у Word. Текст, що залишився в полі, не виділиться.',
        ],
        "ru": [
            'Вырежьте текст из поля, вставьте его в документ обычными абзацами, а пустое поле удалите.',
            'Замените боковую колонку в текстовом поле на обычный заголовок с содержимым под ним, в одну колонку.',
            'Проверьте результат: нажмите Ctrl+A в Word. Текст, оставшийся в поле, не выделится.',
        ],
        "es": [
            'Corta el texto del cuadro, pégalo en el documento como párrafos normales y borra el cuadro vacío.',
            'Sustituye una barra lateral en cuadro por un encabezado normal seguido de su contenido, a una sola columna.',
            'Comprueba que funcionó: pulsa Ctrl+A en Word. El texto que siga dentro de un cuadro no se resaltará.',
        ],
        "nl": [
            "Knip de tekst uit het vak, plak die als gewone alinea's in het document en verwijder het lege vak.",
            'Vervang een zijkolom in een tekstvak door een gewone kop met daaronder de inhoud, in één kolom.',
            'Controleer het: druk Ctrl+A in Word. Tekst die nog in een vak zit, licht niet op.',
        ],
        "fr": [
            'Coupez le texte de la zone, collez-le dans le document en paragraphes ordinaires, puis supprimez la zone vide.',
            'Remplacez une colonne latérale en zone de texte par un intitulé normal suivi de son contenu, sur une seule colonne.',
            'Vérifiez : appuyez sur Ctrl+A dans Word. Le texte encore dans une zone ne se surlignera pas.',
        ],
    },
    "missing_contact_field": {
        "en": [
            "Type your email and phone into the first three lines under your name, exactly as they are written: name@example.com and +49 151 2345678.",
            'Do not leave them only in a header, inside an image, or in a text box — those are the three places a parser is most likely to miss.',
            "Do not disguise them: \"name [at] example [dot] com\" defeats every parser, and the spam it saves you is not worth the application.",
        ],
        "de": [
            "Schreiben Sie E-Mail und Telefon in die ersten drei Zeilen unter Ihrem Namen, genau so, wie man sie schreibt: name@example.com und +49 151 2345678.",
            'Lassen Sie sie nicht nur in einer Kopfzeile, in einem Bild oder in einem Textfeld stehen — das sind die drei Orte, die ein Parser am ehesten übersieht.',
            "Verschleiern Sie sie nicht: \"name [at] example [Punkt] com\" scheitert an jedem Parser, und der ersparte Spam ist die Bewerbung nicht wert.",
        ],
        "uk": [
            "Напишіть пошту й телефон у перших трьох рядках під вашим іменем — так, як вони пишуться: name@example.com і +380 67 1234567.",
            'Не лишайте їх тільки в колонтитулі, всередині зображення чи в текстовому полі — саме ці три місця парсер пропускає найчастіше.',
            "Не маскуйте їх: «name [собака] example [крапка] com» не подолає жоден парсер, а зекономлений спам не вартий заявки.",
        ],
        "ru": [
            "Напишите почту и телефон в первых трёх строках под вашим именем — так, как они пишутся: name@example.com и +7 900 1234567.",
            'Не оставляйте их только в колонтитуле, внутри изображения или в текстовом поле — именно эти три места парсер пропускает чаще всего.',
            "Не маскируйте их: «name [собака] example [точка] com» не одолеет ни один парсер, а сэкономленный спам не стоит заявки.",
        ],
        "es": [
            "Escribe tu correo y tu teléfono en las tres primeras líneas bajo tu nombre, tal cual se escriben: nombre@ejemplo.com y +34 600 123 456.",
            'No los dejes solo en un encabezado, dentro de una imagen o en un cuadro de texto: son los tres sitios que un analizador tiene más probabilidades de omitir.',
            "No los disfraces: «nombre [arroba] ejemplo [punto] com» derrota a cualquier analizador, y el spam que te ahorras no vale la candidatura.",
        ],
        "nl": [
            "Zet je e-mailadres en telefoonnummer in de eerste drie regels onder je naam, precies zoals je ze schrijft: naam@voorbeeld.nl en +31 6 12345678.",
            'Laat ze niet alleen in een koptekst, in een afbeelding of in een tekstvak staan — dat zijn de drie plekken die een parser het vaakst mist.',
            "Verhul ze niet: \"naam [apenstaartje] voorbeeld [punt] nl\" strandt bij elke parser, en de bespaarde spam is de sollicitatie niet waard.",
        ],
        "fr": [
            "Écrivez votre e-mail et votre téléphone dans les trois premières lignes sous votre nom, tels quels : nom@exemple.com et +33 6 12 34 56 78.",
            "Ne les laissez pas uniquement dans un en-tête, dans une image ou dans une zone de texte : ce sont les trois endroits qu'un analyseur rate le plus souvent.",
            "Ne les déguisez pas : « nom [arobase] exemple [point] com » bloque tout analyseur, et le spam évité ne vaut pas la candidature.",
        ],
    },
    "section_missing_under_naive_parsing": {
        "en": [
            'Switch to a single-column layout. It is the one change that reliably fixes this, and it costs less visually than it sounds.',
            'If you keep two columns, make sure no heading shares a horizontal line with sidebar content — the merge happens line by line.',
            'Check it worked: copy everything out of your CV into a plain text editor and read it top to bottom. That is roughly what the parser sees.',
        ],
        "de": [
            'Wechseln Sie zu einem einspaltigen Layout. Das ist die eine Änderung, die das zuverlässig behebt, und sie kostet optisch weniger als es klingt.',
            'Wenn Sie zwei Spalten behalten, achten Sie darauf, dass keine Überschrift auf derselben Höhe wie Seitenspalteninhalt steht — verschmolzen wird zeilenweise.',
            'Prüfen: alles aus dem Lebenslauf in einen einfachen Texteditor kopieren und von oben nach unten lesen. Ungefähr so sieht es der Parser.',
        ],
        "uk": [
            'Перейдіть на одноколонкову верстку. Це єдина зміна, яка надійно це виправляє, і візуально вона коштує менше, ніж здається.',
            'Якщо лишаєте дві колонки, стежте, щоб жоден заголовок не стояв на одній горизонталі з вмістом бічної колонки — злиття відбувається саме порядково.',
            'Перевірте результат: скопіюйте все з резюме у простий текстовий редактор і прочитайте згори вниз. Приблизно так це бачить парсер.',
        ],
        "ru": [
            'Перейдите на одноколоночную вёрстку. Это единственное изменение, которое надёжно это исправляет, и визуально оно стоит меньше, чем кажется.',
            'Если оставляете две колонки, следите, чтобы ни один заголовок не стоял на одной горизонтали с содержимым боковой колонки — слияние происходит именно построчно.',
            'Проверьте результат: скопируйте всё из резюме в простой текстовый редактор и прочитайте сверху вниз. Примерно так это видит парсер.',
        ],
        "es": [
            'Pasa a una maquetación de una sola columna. Es el único cambio que lo arregla de forma fiable, y visualmente cuesta menos de lo que parece.',
            'Si mantienes dos columnas, asegúrate de que ningún encabezado comparta línea horizontal con contenido de la barra lateral: la fusión ocurre línea a línea.',
            'Comprueba que funcionó: copia todo el CV en un editor de texto plano y léelo de arriba abajo. Eso es más o menos lo que ve el analizador.',
        ],
        "nl": [
            'Stap over op één kolom. Dat is de ene wijziging die dit betrouwbaar oplost, en visueel kost het minder dan het klinkt.',
            'Houd je twee kolommen aan, zorg dan dat geen enkele kop op dezelfde hoogte staat als inhoud in de zijkolom — het samensmelten gebeurt regel voor regel.',
            'Controleer het: kopieer alles uit je cv naar een kale teksteditor en lees het van boven naar beneden. Dat is ongeveer wat de parser ziet.',
        ],
        "fr": [
            "Passez à une mise en page sur une seule colonne. C'est le seul changement qui règle cela de façon fiable, et visuellement il coûte moins qu'il n'y paraît.",
            "Si vous gardez deux colonnes, veillez à ce qu'aucun intitulé ne partage sa ligne horizontale avec le contenu de la colonne latérale : la fusion se fait ligne par ligne.",
            "Vérifiez : copiez tout le CV dans un éditeur de texte brut et lisez-le de haut en bas. C'est à peu près ce que voit l'analyseur.",
        ],
    },
    "volunteering_listed_as_employment": {
        "en": [
            "Add a section called Ehrenamtliches Engagement (or Волонтерство in a Ukrainian CV) after experience and education, and move the volunteer entries there with their dates.",
            "Keep each entry's organisation, role, dates and one line on what you did — the same shape as a job, so it reads as seriously as one.",
            "If you are just starting out and the volunteering is your most relevant practice, it may stay under experience — but put the word volunteer in the role title.",
        ],
        "de": [
            "Legen Sie nach Berufserfahrung und Ausbildung die Rubrik Ehrenamtliches Engagement an und verschieben Sie die ehrenamtlichen Einträge mit ihren Daten dorthin.",
            "Behalten Sie Organisation, Rolle, Zeitraum und eine Zeile zur Tätigkeit — im selben Aufbau wie eine Stelle, damit der Eintrag genauso ernst gelesen wird.",
            "Wenn Sie gerade einsteigen und das Ehrenamt Ihre relevanteste Praxis ist, darf es unter Berufserfahrung bleiben — dann aber mit \"ehrenamtlich\" in der Bezeichnung.",
        ],
        "uk": [
            "Створіть розділ «Волонтерство» після досвіду й освіти та перенесіть туди волонтерські записи разом із датами.",
            "Лишіть у кожному записі організацію, роль, дати й один рядок про те, що ви робили — у тому самому вигляді, що й посаду, щоб читався так само серйозно.",
            "Якщо ви тільки починаєте кар'єру і волонтерство — ваша найрелевантніша практика, його можна лишити в досвіді, але зі словом «волонтер» у назві ролі.",
        ],
        "ru": [
            "Создайте раздел «Волонтерство» после опыта и образования и перенесите туда волонтерские записи вместе с датами.",
            "Оставьте в каждой записи организацию, роль, даты и одну строку о том, что вы делали — в том же виде, что и должность, чтобы читалась так же серьёзно.",
            "Если вы только начинаете карьеру и волонтерство — ваша самая релевантная практика, его можно оставить в опыте, но со словом «волонтер» в названии роли.",
        ],
        "es": [
            "Crea una sección de voluntariado después de la experiencia y la formación, y mueve allí las entradas de voluntariado con sus fechas.",
            "Mantén en cada entrada la organización, el papel, las fechas y una línea sobre lo que hiciste, con la misma forma que un empleo, para que se lea con la misma seriedad.",
            "Si estás empezando y el voluntariado es tu práctica más relevante, puede quedarse en experiencia, pero con la palabra voluntario en el título del puesto.",
        ],
        "nl": [
            "Maak na werkervaring en opleiding een rubriek voor vrijwilligerswerk en verplaats de vrijwillige onderdelen daarheen, met hun data.",
            "Houd per onderdeel organisatie, rol, periode en één regel over wat je deed — in dezelfde vorm als een baan, zodat het even serieus gelezen wordt.",
            "Begin je net en is het vrijwilligerswerk je meest relevante praktijk, dan mag het onder werkervaring blijven — maar zet het woord vrijwilliger in de functienaam.",
        ],
        "fr": [
            "Créez une rubrique Bénévolat après l'expérience et la formation, et déplacez-y les entrées bénévoles avec leurs dates.",
            "Gardez pour chaque entrée l'organisme, le rôle, les dates et une ligne sur ce que vous faisiez — la même forme qu'un emploi, pour qu'elle soit lue aussi sérieusement.",
            "Si vous débutez et que ce bénévolat est votre pratique la plus pertinente, il peut rester dans l'expérience — mais avec le mot bénévole dans l'intitulé du rôle.",
        ],
    },
    "unexplained_gap": {
        "en": [
            "Add a dated line for each gap that says what filled it: parental leave, caring for a relative, a language course, reorientation, looking for work.",
            "Keep it to one line with the dates — the reason, not the story. The interview is where it gets explained.",
            "If the gap comes from how the dates are written, give month and year on both sides, so 2018 – 2019 is not read as covering less than it did.",
        ],
        "de": [
            "Fügen Sie für jede Lücke eine datierte Zeile ein, die sagt, was sie gefüllt hat: Elternzeit, Pflege von Angehörigen, Sprachkurs, berufliche Neuorientierung, Arbeitssuche.",
            "Belassen Sie es bei einer Zeile mit Zeitraum — der Grund, nicht die Geschichte. Erklärt wird im Vorstellungsgespräch.",
            "Entsteht die Lücke nur durch die Schreibweise, geben Sie auf beiden Seiten Monat und Jahr an, damit 2018 – 2019 nicht kürzer gelesen wird, als es war.",
        ],
        "uk": [
            "Додайте для кожної перерви датований рядок про те, що її заповнило: декретна відпустка, догляд за родичем, мовний курс, переорієнтація, пошук роботи.",
            "Обмежтеся одним рядком із датами — причиною, а не історією. Пояснювати будете на співбесіді.",
            "Якщо перерва виникає лише через спосіб запису дат, вказуйте місяць і рік з обох боків, щоб 2018 – 2019 не читалося коротшим, ніж було насправді.",
        ],
        "ru": [
            "Добавьте для каждого перерыва датированную строку о том, что его заполнило: декретный отпуск, уход за родственником, языковой курс, переориентация, поиск работы.",
            "Ограничьтесь одной строкой с датами — причиной, а не историей. Объяснять будете на собеседовании.",
            "Если перерыв возникает только из-за способа записи дат, указывайте месяц и год с обеих сторон, чтобы 2018 – 2019 не читалось короче, чем было на самом деле.",
        ],
        "es": [
            "Añade para cada hueco una línea fechada que diga qué lo ocupó: permiso parental, cuidado de un familiar, curso de idiomas, reorientación, búsqueda de empleo.",
            "Limítate a una línea con las fechas: el motivo, no la historia. Se explica en la entrevista.",
            "Si el hueco se debe a cómo están escritas las fechas, pon mes y año en ambos extremos, para que 2018 – 2019 no se lea como más corto de lo que fue.",
        ],
        "nl": [
            "Voeg voor elk gat een gedateerde regel toe die zegt wat het vulde: ouderschapsverlof, zorg voor een familielid, taalcursus, heroriëntatie, werk zoeken.",
            "Houd het bij één regel met de periode — de reden, niet het verhaal. In het gesprek komt de uitleg.",
            "Ontstaat het gat alleen door hoe de data geschreven zijn, geef dan aan beide kanten maand en jaar, zodat 2018 – 2019 niet korter gelezen wordt dan het was.",
        ],
        "fr": [
            "Ajoutez pour chaque période vide une ligne datée qui dit ce qui l'a occupée : congé parental, soin d'un proche, cours de langue, réorientation, recherche d'emploi.",
            "Tenez-vous-en à une ligne avec les dates — la raison, pas l'histoire. L'explication viendra en entretien.",
            "Si la période vide ne tient qu'à l'écriture des dates, indiquez mois et année des deux côtés, pour que 2018 – 2019 ne soit pas lu plus court que la réalité.",
        ],
    },
    "impossible_dates": {
        "en": [
            "Find the range shown in the evidence and check both ends against a contract, a payslip or a certificate.",
            "Write every range the same way, month and year on both sides — 03/2019 – 08/2022 — so a transposed digit is easy to spot.",
            "If a role has not ended, write present rather than a date in the future.",
        ],
        "de": [
            "Suchen Sie den Zeitraum aus dem Beleg und prüfen Sie beide Enden anhand von Vertrag, Gehaltsabrechnung oder Zeugnis.",
            "Schreiben Sie jeden Zeitraum gleich, mit Monat und Jahr auf beiden Seiten — 03/2019 – 08/2022 —, damit ein Zahlendreher sofort auffällt.",
            "Ist eine Stelle noch nicht beendet, schreiben Sie \"heute\" statt eines Datums in der Zukunft.",
        ],
        "uk": [
            "Знайдіть проміжок, наведений у доказі, і звірте обидва його кінці з договором, розрахунковим листком чи довідкою.",
            "Записуйте всі проміжки однаково, з місяцем і роком з обох боків — 03/2019 – 08/2022, — щоб переставлену цифру було легко помітити.",
            "Якщо робота ще триває, пишіть «дотепер», а не дату в майбутньому.",
        ],
        "ru": [
            "Найдите промежуток, приведённый в доказательстве, и сверьте оба его конца с договором, расчётным листком или справкой.",
            "Записывайте все промежутки одинаково, с месяцем и годом с обеих сторон — 03/2019 – 08/2022, — чтобы переставленную цифру было легко заметить.",
            "Если работа ещё продолжается, пишите «по настоящее время», а не дату в будущем.",
        ],
        "es": [
            "Busca el rango que aparece en la evidencia y comprueba ambos extremos con un contrato, una nómina o un certificado.",
            "Escribe todos los rangos igual, con mes y año en ambos lados —03/2019 – 08/2022—, para que un dígito cambiado salte a la vista.",
            "Si un puesto no ha terminado, escribe actualidad en lugar de una fecha futura.",
        ],
        "nl": [
            "Zoek de periode uit het bewijs op en controleer beide uiteinden aan de hand van een contract, loonstrook of getuigschrift.",
            "Schrijf elke periode op dezelfde manier, met maand en jaar aan beide kanten — 03/2019 – 08/2022 —, zodat een verwisseld cijfer direct opvalt.",
            "Is een functie nog niet afgelopen, schrijf dan heden in plaats van een datum in de toekomst.",
        ],
        "fr": [
            "Retrouvez la période indiquée dans la preuve et vérifiez ses deux bornes avec un contrat, une fiche de paie ou un certificat.",
            "Écrivez chaque période de la même façon, mois et année des deux côtés — 03/2019 – 08/2022 —, pour qu'un chiffre inversé saute aux yeux.",
            "Si un poste n'est pas terminé, écrivez aujourd'hui plutôt qu'une date future.",
        ],
    },
    "first_person_in_cv": {
        "en": [
            "Rewrite each sentence that starts with I as a fragment that starts with the verb: Led, Built, Managed.",
            "Cut the words that only connect the sentence — and, then, where I — and keep the facts and the numbers.",
            "Move anything that genuinely needs a sentence about you into the short profile at the top or into the cover letter.",
        ],
        "de": [
            "Formulieren Sie jeden Ich-Satz als Stichpunkt um, der mit dem Substantiv beginnt: Stationsleitung, Dienstplanung, Einarbeitung neuer Kolleginnen.",
            "Streichen Sie, was nur den Satz verbindet — und, dann, wobei ich —, und behalten Sie die Fakten und Zahlen.",
            "Was wirklich einen Satz über Sie braucht, gehört ins Kurzprofil oben oder ins Anschreiben.",
        ],
        "uk": [
            "Перепишіть кожне речення від першої особи як коротку фразу, що починається з іменника: «Керування командою», «Складання графіків».",
            "Приберіть слова, які лише зв'язують речення, — і, потім, де я, — і лишіть факти та цифри.",
            "Те, що справді потребує речення про вас, перенесіть у короткий профіль угорі чи в супровідний лист.",
        ],
        "ru": [
            "Перепишите каждое предложение от первого лица как короткую фразу, начинающуюся с существительного: «Руководство командой», «Составление графиков».",
            "Уберите слова, которые лишь связывают предложение, — и, потом, где я, — и оставьте факты и цифры.",
            "То, что действительно требует предложения о вас, перенесите в короткий профиль вверху или в сопроводительное письмо.",
        ],
        "es": [
            "Reescribe cada frase en primera persona como un fragmento que empiece por el sustantivo: Dirección del equipo, Planificación de turnos.",
            "Quita las palabras que solo enlazan la frase —y, luego, donde yo— y conserva los hechos y las cifras.",
            "Lo que de verdad necesite una frase sobre ti, llévalo al perfil breve de arriba o a la carta de presentación.",
        ],
        "nl": [
            "Herschrijf elke zin in de ik-vorm als fragment dat met het zelfstandig naamwoord begint: Teamleiding, Roosterplanning.",
            "Schrap wat alleen de zin verbindt — en, daarna, waarbij ik — en houd de feiten en de cijfers.",
            "Wat echt een zin over jezelf nodig heeft, hoort in het korte profiel bovenaan of in de sollicitatiebrief.",
        ],
        "fr": [
            "Réécrivez chaque phrase à la première personne en fragment qui commence par le nom : Direction d'équipe, Planification des horaires.",
            "Supprimez les mots qui ne font que lier la phrase — et, puis, où je — et gardez les faits et les chiffres.",
            "Ce qui a vraiment besoin d'une phrase sur vous va dans le court profil en tête ou dans la lettre de motivation.",
        ],
    },
    "outdated_personal_details": {
        "en": [
            "Delete the lines for religion, marital status, children and parents from your personal details.",
            "Keep what an employer genuinely needs: name, city, phone, email, and your work permit if that is a question for your application.",
            "If you are applying to a church employer, keeping your denomination is reasonable — for everyone else it can go.",
        ],
        "de": [
            "Löschen Sie die Zeilen zu Konfession, Familienstand, Kindern und Eltern aus den persönlichen Daten.",
            "Behalten Sie, was ein Arbeitgeber wirklich braucht: Name, Wohnort, Telefon, E-Mail und gegebenenfalls die Arbeitserlaubnis.",
            "Bei einer Bewerbung an einen kirchlichen Arbeitgeber ist die Konfession sinnvoll — für alle anderen kann sie weg.",
        ],
        "uk": [
            "Видаліть з особистих даних рядки про віросповідання, сімейний стан, дітей і батьків.",
            "Лишіть те, що роботодавцю справді потрібно: ім'я, місто, телефон, пошту й дозвіл на роботу, якщо для вашої заявки це питання.",
            "Якщо подаєтеся до церковного роботодавця, віросповідання можна лишити — для всіх інших його можна прибрати.",
        ],
        "ru": [
            "Удалите из личных данных строки о вероисповедании, семейном положении, детях и родителях.",
            "Оставьте то, что работодателю действительно нужно: имя, город, телефон, почту и разрешение на работу, если для вашего отклика это вопрос.",
            "Если откликаетесь к церковному работодателю, вероисповедание можно оставить — для всех остальных его можно убрать.",
        ],
        "es": [
            "Borra de tus datos personales las líneas de religión, estado civil, hijos y padres.",
            "Conserva lo que una empresa necesita de verdad: nombre, ciudad, teléfono, correo y el permiso de trabajo si es una cuestión en tu candidatura.",
            "Si te presentas a un empleador eclesiástico, mantener la confesión es razonable; para cualquier otro puede desaparecer.",
        ],
        "nl": [
            "Verwijder de regels over geloof, burgerlijke staat, kinderen en ouders uit je persoonsgegevens.",
            "Houd wat een werkgever echt nodig heeft: naam, woonplaats, telefoon, e-mail en je werkvergunning als dat een vraag is bij je sollicitatie.",
            "Solliciteer je bij een kerkelijke werkgever, dan is je geloofsovertuiging vermelden redelijk — voor alle anderen kan het weg.",
        ],
        "fr": [
            "Supprimez de vos données personnelles les lignes sur la religion, la situation familiale, les enfants et les parents.",
            "Gardez ce dont un employeur a vraiment besoin : nom, ville, téléphone, e-mail et votre autorisation de travail si c'est une question pour votre candidature.",
            "Si vous postulez auprès d'un employeur confessionnel, garder votre confession est raisonnable — pour tous les autres, elle peut partir.",
        ],
    },
    "oldest_entry_first": {
        "en": [
            "Reorder the entries under work experience so the current or most recent job comes first and the oldest last.",
            "Do the same within education, so the highest qualification sits at the top of its section.",
            "Keep the date format identical on every entry, so the new order is easy to check at a glance.",
        ],
        "de": [
            "Sortieren Sie die Berufserfahrung um: aktuelle oder letzte Station zuerst, die älteste zuletzt.",
            "Verfahren Sie in der Ausbildung genauso, damit der höchste Abschluss oben in der Rubrik steht.",
            "Halten Sie das Datumsformat in jedem Eintrag gleich, damit sich die neue Reihenfolge auf einen Blick prüfen lässt.",
        ],
        "uk": [
            "Переставте записи в досвіді роботи так, щоб поточна чи остання посада була першою, а найстаріша — останньою.",
            "Зробіть те саме в освіті, щоб найвища кваліфікація стояла вгорі свого розділу.",
            "Тримайте однаковий формат дат у кожному записі, щоб новий порядок можна було перевірити одним поглядом.",
        ],
        "ru": [
            "Переставьте записи в опыте работы так, чтобы текущая или последняя должность была первой, а самая старая — последней.",
            "Сделайте то же в образовании, чтобы самая высокая квалификация стояла вверху своего раздела.",
            "Держите одинаковый формат дат в каждой записи, чтобы новый порядок можно было проверить одним взглядом.",
        ],
        "es": [
            "Reordena la experiencia laboral para que el empleo actual o más reciente vaya primero y el más antiguo al final.",
            "Haz lo mismo en la formación, para que la titulación más alta quede arriba de su sección.",
            "Mantén el mismo formato de fecha en cada entrada, para que el nuevo orden se compruebe de un vistazo.",
        ],
        "nl": [
            "Zet de werkervaring om, zodat de huidige of laatste baan bovenaan staat en de oudste onderaan.",
            "Doe hetzelfde bij opleiding, zodat de hoogste opleiding bovenaan de rubriek staat.",
            "Houd het datumformaat in elk onderdeel gelijk, zodat de nieuwe volgorde in één oogopslag te controleren is.",
        ],
        "fr": [
            "Réordonnez l'expérience professionnelle pour que le poste actuel ou le plus récent vienne en premier et le plus ancien en dernier.",
            "Faites de même dans la formation, pour que le diplôme le plus élevé soit en haut de sa rubrique.",
            "Gardez le même format de date dans chaque entrée, pour que le nouvel ordre se vérifie d'un coup d'œil.",
        ],
    },
}


RULE_PLAN: dict[str, dict[str, str]] = {
    "pdf_non_embedded_font": {
        "en": "Embed every font the CV uses in the file itself, or rebuild the file in a common font.",
        "de": "Betten Sie jede im Lebenslauf verwendete Schrift in die Datei ein oder erzeugen Sie die Datei mit einer gängigen Schrift neu.",
        "uk": "Вбудуйте у файл кожен шрифт, який використовує резюме, або перезберіть файл звичайним шрифтом.",
        "ru": "Встройте в файл каждый шрифт, который использует резюме, или пересоберите файл обычным шрифтом.",
        "es": "Incrusta en el archivo todas las fuentes que usa el CV, o vuelve a generarlo con una fuente corriente.",
        "nl": "Sluit elk lettertype dat het cv gebruikt in het bestand zelf in, of maak het bestand opnieuw met een gangbaar lettertype.",
        "fr": "Intégrez dans le fichier chaque police utilisée par le CV, ou refaites le fichier avec une police courante.",
    },
    "pdf_repeated_header_footer_content": {
        "en": "Move the contact details out of the page header and footer into the body text, in the first lines under your name.",
        "de": "Verschieben Sie die Kontaktdaten aus Kopf- und Fußzeile in den Fließtext, in die ersten Zeilen unter Ihrem Namen.",
        "uk": "Перенесіть контактні дані з колонтитулів в основний текст, у перші рядки під вашим іменем.",
        "ru": "Перенесите контактные данные из колонтитулов в основной текст, в первые строки под вашим именем.",
        "es": "Saca los datos de contacto del encabezado y el pie de página y ponlos en el texto, en las primeras líneas bajo tu nombre.",
        "nl": "Haal de contactgegevens uit de kop- en voettekst en zet ze in de lopende tekst, in de eerste regels onder je naam.",
        "fr": "Sortez les coordonnées de l'en-tête et du pied de page et placez-les dans le texte, dans les premières lignes sous votre nom.",
    },
    "pdf_textless_image": {
        "en": "Replace the image with real text: type out what it shows as ordinary paragraphs.",
        "de": "Ersetzen Sie das Bild durch echten Text: Schreiben Sie seinen Inhalt als gewöhnliche Absätze aus.",
        "uk": "Замініть зображення справжнім текстом: наберіть те, що на ньому, звичайними абзацами.",
        "ru": "Замените изображение настоящим текстом: наберите то, что на нём, обычными абзацами.",
        "es": "Sustituye la imagen por texto real: escribe lo que muestra como párrafos normales.",
        "nl": "Vervang de afbeelding door echte tekst: typ uit wat erop staat als gewone alinea's.",
        "fr": "Remplacez l'image par du vrai texte : écrivez ce qu'elle montre en paragraphes ordinaires.",
    },
    "docx_table_content": {
        "en": "Take the content out of the table and write it as ordinary paragraphs, one entry per line.",
        "de": "Nehmen Sie den Inhalt aus der Tabelle heraus und schreiben Sie ihn als gewöhnliche Absätze, einen Eintrag pro Zeile.",
        "uk": "Винесіть вміст із таблиці й запишіть його звичайними абзацами, по одному запису в рядку.",
        "ru": "Вынесите содержимое из таблицы и запишите его обычными абзацами, по одной записи в строке.",
        "es": "Saca el contenido de la tabla y escríbelo como párrafos normales, una entrada por línea.",
        "nl": "Haal de inhoud uit de tabel en schrijf die als gewone alinea's, één vermelding per regel.",
        "fr": "Sortez le contenu du tableau et écrivez-le en paragraphes ordinaires, une entrée par ligne.",
    },
    "docx_header_footer_content": {
        "en": "Move everything that has to be read out of the page header and footer into the body of the document.",
        "de": "Verschieben Sie alles, was gelesen werden muss, aus Kopf- und Fußzeile in den Haupttext des Dokuments.",
        "uk": "Перенесіть усе, що має бути прочитане, з колонтитулів у тіло документа.",
        "ru": "Перенесите всё, что должно быть прочитано, из колонтитулов в тело документа.",
        "es": "Lleva al cuerpo del documento todo lo que deba leerse desde el encabezado y el pie de página.",
        "nl": "Verplaats alles wat gelezen moet worden uit de kop- en voettekst naar de hoofdtekst van het document.",
        "fr": "Déplacez dans le corps du document tout ce qui doit être lu depuis l'en-tête et le pied de page.",
    },
    "docx_text_box_content": {
        "en": "Take the text out of the text box and put it into the body of the document as ordinary paragraphs.",
        "de": "Nehmen Sie den Text aus dem Textfeld heraus und setzen Sie ihn als gewöhnliche Absätze in den Haupttext.",
        "uk": "Винесіть текст із текстового поля й розмістіть його в тілі документа звичайними абзацами.",
        "ru": "Вынесите текст из текстового поля и разместите его в теле документа обычными абзацами.",
        "es": "Saca el texto del cuadro de texto y ponlo en el cuerpo del documento como párrafos normales.",
        "nl": "Haal de tekst uit het tekstvak en zet die als gewone alinea's in de hoofdtekst van het document.",
        "fr": "Sortez le texte de la zone de texte et placez-le dans le corps du document en paragraphes ordinaires.",
    },
    "missing_contact_field": {
        "en": "Write your email address and phone number in the first three lines under your name, in their ordinary form: name@example.com and +49 151 2345678.",
        "de": "Schreiben Sie E-Mail-Adresse und Telefonnummer in die ersten drei Zeilen unter Ihrem Namen, in ihrer gewöhnlichen Form: name@example.com und +49 151 2345678.",
        "uk": "Напишіть адресу пошти й номер телефону в перших трьох рядках під вашим іменем, у звичайному вигляді: name@example.com і +380 67 1234567.",
        "ru": "Напишите адрес почты и номер телефона в первых трёх строках под вашим именем, в обычном виде: name@example.com и +7 900 1234567.",
        "es": "Escribe tu correo y tu teléfono en las tres primeras líneas bajo tu nombre, en su forma corriente: nombre@ejemplo.com y +34 600 123 456.",
        "nl": "Zet je e-mailadres en telefoonnummer in de eerste drie regels onder je naam, in hun gewone vorm: naam@voorbeeld.nl en +31 6 12345678.",
        "fr": "Écrivez votre adresse e-mail et votre numéro de téléphone dans les trois premières lignes sous votre nom, sous leur forme ordinaire : nom@exemple.com et +33 6 12 34 56 78.",
    },
    "section_missing_under_naive_parsing": {
        "en": "Lay the CV out in a single column, read top to bottom, with no side panel.",
        "de": "Legen Sie den Lebenslauf einspaltig an, von oben nach unten zu lesen, ohne Seitenspalte.",
        "uk": "Зробіть резюме одноколонковим, щоб воно читалося згори вниз, без бічної панелі.",
        "ru": "Сделайте резюме одноколоночным, чтобы оно читалось сверху вниз, без боковой панели.",
        "es": "Maqueta el CV a una sola columna, que se lea de arriba abajo, sin panel lateral.",
        "nl": "Zet het cv in één kolom, van boven naar beneden te lezen, zonder zijbalk.",
        "fr": "Mettez le CV sur une seule colonne, qui se lit de haut en bas, sans panneau latéral.",
    },
    "contact_only_as_link": {
        "en": "Write your email address and phone number out as text under your name, not only inside a link.",
        "de": "Schreiben Sie E-Mail-Adresse und Telefonnummer als Text unter Ihrem Namen aus, nicht nur innerhalb eines Links.",
        "uk": "Випишіть адресу пошти й номер телефону текстом під вашим іменем, а не лише всередині посилання.",
        "ru": "Выпишите адрес почты и номер телефона текстом под вашим именем, а не только внутри ссылки.",
        "es": "Escribe tu correo y tu teléfono como texto bajo tu nombre, no solo dentro de un enlace.",
        "nl": "Schrijf je e-mailadres en telefoonnummer als tekst onder je naam, niet alleen binnen een link.",
        "fr": "Écrivez votre adresse e-mail et votre numéro de téléphone en toutes lettres sous votre nom, pas seulement dans un lien.",
    },
    "unrecognised_section_headings": {
        "en": "Rename the section headings to the plain words: Experience, Education, Skills.",
        "de": "Benennen Sie die Abschnittsüberschriften in die schlichten Wörter um: Berufserfahrung, Ausbildung, Kenntnisse.",
        "uk": "Перейменуйте заголовки розділів на прості слова: Досвід, Освіта, Навички.",
        "ru": "Переименуйте заголовки разделов в простые слова: Опыт, Образование, Навыки.",
        "es": "Cambia los títulos de las secciones por las palabras corrientes: Experiencia, Formación, Competencias.",
        "nl": "Hernoem de kopjes naar de gewone woorden: Werkervaring, Opleiding, Vaardigheden.",
        "fr": "Renommez les titres de sections avec les mots simples : Expérience, Formation, Compétences.",
    },
    "broken_characters": {
        "en": "Retype the flagged word from scratch so no ligature, soft hyphen or letter from another alphabet is left inside it.",
        "de": "Tippen Sie das gemeldete Wort neu, sodass keine Ligatur, kein bedingter Trennstrich und kein Buchstabe aus einem anderen Alphabet darin bleibt.",
        "uk": "Наберіть позначене слово наново, щоб у ньому не лишилося ні лігатури, ні мʼякого переносу, ні літери з іншої абетки.",
        "ru": "Наберите отмеченное слово заново, чтобы в нём не осталось ни лигатуры, ни мягкого переноса, ни буквы из другого алфавита.",
        "es": "Vuelve a escribir desde cero la palabra señalada para que no quede en ella ninguna ligadura, guion opcional ni letra de otro alfabeto.",
        "nl": "Typ het gemarkeerde woord helemaal opnieuw, zodat er geen ligatuur, zacht afbreekstreepje of letter uit een ander alfabet in blijft staan.",
        "fr": "Retapez entièrement le mot signalé pour qu'il ne reste ni ligature, ni trait d'union conditionnel, ni lettre d'un autre alphabet.",
    },
    "volunteering_listed_as_employment": {
        "en": "Move the volunteer entries out of work experience into their own section after education, keeping their dates and roles.",
        "de": "Verschieben Sie die ehrenamtlichen Einträge aus der Berufserfahrung in eine eigene Rubrik nach der Ausbildung, mit Zeitraum und Rolle.",
        "uk": "Перенесіть волонтерські записи з досвіду роботи в окремий розділ після освіти, зберігши дати й ролі.",
        "ru": "Перенесите волонтерские записи из опыта работы в отдельный раздел после образования, сохранив даты и роли.",
        "es": "Saca las entradas de voluntariado de la experiencia laboral a su propia sección tras la formación, con sus fechas y funciones.",
        "nl": "Verplaats de vrijwillige onderdelen uit werkervaring naar een eigen rubriek na opleiding, met hun data en rollen.",
        "fr": "Sortez les entrées bénévoles de l'expérience professionnelle vers leur propre rubrique après la formation, avec leurs dates et rôles.",
    },
    "unexplained_gap": {
        "en": "Give every stretch of four months or more without an entry its own dated line saying what filled it.",
        "de": "Geben Sie jeder Zeit von vier Monaten oder mehr ohne Eintrag eine eigene datierte Zeile, die sagt, womit sie gefüllt war.",
        "uk": "Дайте кожному проміжку від чотирьох місяців без запису власний датований рядок про те, чим він був заповнений.",
        "ru": "Дайте каждому промежутку от четырёх месяцев без записи собственную датированную строку о том, чем он был заполнен.",
        "es": "Da a cada periodo de cuatro meses o más sin entrada su propia línea fechada que diga qué lo ocupó.",
        "nl": "Geef elke periode van vier maanden of langer zonder onderdeel een eigen gedateerde regel die zegt wat hem vulde.",
        "fr": "Donnez à chaque période de quatre mois ou plus sans entrée sa propre ligne datée indiquant ce qui l'a occupée.",
    },
    "impossible_dates": {
        "en": "Correct the date range that ends before it starts or lies years in the future, so every range runs forward and ends by today.",
        "de": "Korrigieren Sie den Zeitraum, der vor seinem Beginn endet oder Jahre in der Zukunft liegt, sodass jeder Zeitraum vorwärts läuft.",
        "uk": "Виправте проміжок дат, що закінчується раніше, ніж починається, або лежить на роки вперед, щоб кожен ішов від початку до кінця.",
        "ru": "Исправьте промежуток дат, который заканчивается раньше, чем начинается, или лежит на годы вперёд, чтобы каждый шёл от начала к концу.",
        "es": "Corrige el rango que termina antes de empezar o está años en el futuro, para que cada rango avance de principio a fin.",
        "nl": "Corrigeer de periode die eindigt voordat hij begint of jaren in de toekomst ligt, zodat elke periode vooruit loopt.",
        "fr": "Corrigez la période qui se termine avant de commencer ou se situe des années dans le futur, pour que chaque période aille vers l'avant.",
    },
    "first_person_in_cv": {
        "en": "Rewrite the entries under experience as short fragments that start with the verb, without sentences about yourself.",
        "de": "Formulieren Sie die Einträge unter Berufserfahrung als kurze Stichpunkte ohne Sätze in der Ich-Form.",
        "uk": "Перепишіть записи в досвіді роботи короткими фразами без речень від першої особи.",
        "ru": "Перепишите записи в опыте работы короткими фразами без предложений от первого лица.",
        "es": "Reescribe las entradas de experiencia como fragmentos breves, sin frases en primera persona.",
        "nl": "Herschrijf de onderdelen onder werkervaring als korte fragmenten, zonder zinnen in de ik-vorm.",
        "fr": "Réécrivez les entrées d'expérience en fragments courts, sans phrases à la première personne.",
    },
    "outdated_personal_details": {
        "en": "Remove religion, marital status, children and parents from your personal details, unless you are applying to a church employer.",
        "de": "Entfernen Sie Konfession, Familienstand, Kinder und Eltern aus den persönlichen Daten, außer bei einem kirchlichen Arbeitgeber.",
        "uk": "Приберіть з особистих даних віросповідання, сімейний стан, дітей і батьків, якщо не подаєтеся до церковного роботодавця.",
        "ru": "Уберите из личных данных вероисповедание, семейное положение, детей и родителей, если не откликаетесь к церковному работодателю.",
        "es": "Quita de tus datos personales la religión, el estado civil, los hijos y los padres, salvo si te presentas a un empleador eclesiástico.",
        "nl": "Haal geloof, burgerlijke staat, kinderen en ouders uit je persoonsgegevens, tenzij je bij een kerkelijke werkgever solliciteert.",
        "fr": "Retirez la religion, la situation familiale, les enfants et les parents de vos données personnelles, sauf pour un employeur confessionnel.",
    },
    "oldest_entry_first": {
        "en": "Reorder work experience so the current or most recent job is at the top and the oldest at the bottom.",
        "de": "Sortieren Sie die Berufserfahrung so, dass die aktuelle oder letzte Station oben steht und die älteste unten.",
        "uk": "Переставте досвід роботи так, щоб поточна чи остання посада була вгорі, а найстаріша — внизу.",
        "ru": "Переставьте опыт работы так, чтобы текущая или последняя должность была вверху, а самая старая — внизу.",
        "es": "Reordena la experiencia para que el empleo actual o más reciente quede arriba y el más antiguo abajo.",
        "nl": "Zet de werkervaring zo dat de huidige of laatste baan bovenaan staat en de oudste onderaan.",
        "fr": "Réordonnez l'expérience pour que le poste actuel ou le plus récent soit en haut et le plus ancien en bas.",
    },
}
"""What to do about a rule, said without naming any program.

The fix list under a finding walks the reader through one application:
which menu, which submenu, which checkbox. That is the right answer to
"how do I do this in Word", and the wrong thing to put in the plan, which
is copied out of the page and taken somewhere else -- to a different
editor, to a colleague, or into a model asked to rewrite the CV. A menu
path means nothing to any of them.

So each rule says here what the document should end up looking like, and
leaves the route there to whoever is holding the file. Both readers get
something they can act on: a person knows where the command lives in their
own editor, and a model editing the text can act on the end state
directly."""


def rule_detail(rule_id: str, language: str) -> str:
    """The longer explanation shown when a finding is expanded, or "" when
    a rule has none yet -- the caller simply shows nothing extra."""
    return _for_rule(RULE_DETAILS, rule_id, language, "")


def rule_fixes(rule_id: str, language: str) -> list[str]:
    """Concrete steps for this finding, most direct first. Empty when a
    rule has no advice yet, which the caller renders as no fix list rather
    than an empty heading."""
    return _for_rule(RULE_FIXES, rule_id, language, [])


def rule_plan(rule_id: str, language: str) -> str:
    """The plan's one-line instruction for a rule, or "" when it has none.

    Falls back to nothing rather than to the fix list: a caller that
    silently borrowed a menu path would put back exactly what this table
    exists to keep out of the copied block."""
    return _for_rule(RULE_PLAN, rule_id, language, "")


SOURCES_FILENAME = "research_sources.md"


def sources_path(language: str) -> str:
    """Repo-relative path to the sources file in this language.

    English lives at the repo root because that is where every existing link
    to it points; the translations sit in docs/ so the root stays readable.
    An unknown language falls back to English rather than producing a link
    to a file that was never written.
    """
    if language == DEFAULT_LANGUAGE or language not in UI_LANGUAGES:
        return SOURCES_FILENAME
    return f"docs/research_sources.{language}.md"
