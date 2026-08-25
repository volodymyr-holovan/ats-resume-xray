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
    "legend": {
        "en": "Boxes mark the exact area each finding refers to.",
        "de": "Die Rahmen markieren den genauen Bereich jedes Befunds.",
        "uk": "Рамки позначають точну ділянку, якої стосується кожне зауваження.",
        "ru": "Рамки отмечают точный участок, к которому относится каждое замечание.",
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
    "match_score_heading": {
        "en": "Match with this ad",
        "de": "Übereinstimmung mit dieser Anzeige",
        "uk": "Відповідність цій вакансії",
        "ru": "Соответствие этой вакансии",
        "es": "Encaje con esta oferta",
        "nl": "Match met deze vacature",
        "fr": "Correspondance avec cette offre",
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
    "match_partial_heading": {
        "en": "Partly covered",
        "de": "Teilweise abgedeckt",
        "uk": "Закрито частково",
        "ru": "Закрыто частично",
        "es": "Cubierto en parte",
        "nl": "Deels gedekt",
        "fr": "Partiellement couvert",
    },
    "match_missing_heading": {
        "en": "Not found in your CV",
        "de": "Nicht in Ihrem Lebenslauf gefunden",
        "uk": "Не знайдено у вашому резюме",
        "ru": "Не найдено в вашем резюме",
        "es": "No encontrado en tu CV",
        "nl": "Niet gevonden in je cv",
        "fr": "Introuvable dans votre CV",
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
    "upload_another": {
        "en": "Replace file",
        "de": "Datei ersetzen",
        "uk": "Замінити файл",
        "ru": "Заменить файл",
        "es": "Cambiar archivo",
        "nl": "Bestand vervangen",
        "fr": "Remplacer le fichier",
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
    "cap_reason_not_a_resume": {
        "en": "This does not look like a CV: no contact details and no recognisable sections were found, so there is nothing meaningful to score.",
        "de": "Das sieht nicht nach einem Lebenslauf aus: weder Kontaktdaten noch erkennbare Abschnitte gefunden, also gibt es nichts sinnvoll zu bewerten.",
        "uk": "Це не схоже на резюме: не знайдено ні контактних даних, ні впізнаваних розділів, тож оцінювати нема чого.",
        "ru": "Это не похоже на резюме: не найдено ни контактных данных, ни узнаваемых разделов, так что оценивать нечего.",
        "es": "Esto no parece un CV: no se han encontrado datos de contacto ni secciones reconocibles, así que no hay nada que puntuar.",
        "nl": "Dit lijkt geen cv: geen contactgegevens en geen herkenbare secties gevonden, dus er valt niets zinnigs te scoren.",
        "fr": "Cela ne ressemble pas à un CV : ni coordonnées ni sections reconnaissables, il n'y a donc rien à évaluer.",
    },
    "rating_not_a_resume": {
        "en": "Not a CV",
        "de": "Kein Lebenslauf",
        "uk": "Не резюме",
        "ru": "Не резюме",
        "es": "No es un CV",
        "nl": "Geen cv",
        "fr": "Pas un CV",
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


RULE_DESCRIPTIONS: dict[str, dict[str, str]] = {
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


RULE_DETAILS: dict[str, dict[str, str]] = {
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
}

RULE_FIXES: dict[str, dict[str, list[str]]] = {
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
            'Put your email and phone as plain text in the first three lines, directly under your name.',
            'Do not leave them only in a header, inside an image, or in a text box — those are the three places a parser is most likely to miss.',
            'Write them plainly: name@example.com and +49 151 2345678, not "name [at] example [dot] com".',
        ],
        "de": [
            'Setzen Sie E-Mail und Telefon als reinen Text in die ersten drei Zeilen, direkt unter Ihren Namen.',
            'Lassen Sie sie nicht nur in einer Kopfzeile, in einem Bild oder in einem Textfeld stehen — das sind die drei Orte, die ein Parser am ehesten übersieht.',
            'Schreiben Sie sie schlicht: name@example.com und +49 151 2345678, nicht "name [at] example [Punkt] com".',
        ],
        "uk": [
            'Напишіть пошту й телефон звичайним текстом у перших трьох рядках, одразу під вашим іменем.',
            'Не лишайте їх тільки в колонтитулі, всередині зображення чи в текстовому полі — саме ці три місця парсер пропускає найчастіше.',
            'Пишіть просто: name@example.com і +380 67 1234567, а не "name [собака] example [крапка] com".',
        ],
        "ru": [
            'Напишите почту и телефон обычным текстом в первых трёх строках, сразу под вашим именем.',
            'Не оставляйте их только в колонтитуле, внутри изображения или в текстовом поле — именно эти три места парсер пропускает чаще всего.',
            'Пишите просто: name@example.com и +7 900 1234567, а не "name [собака] example [точка] com".',
        ],
        "es": [
            'Pon tu correo y tu teléfono como texto plano en las tres primeras líneas, justo bajo tu nombre.',
            'No los dejes solo en un encabezado, dentro de una imagen o en un cuadro de texto: son los tres sitios que un analizador tiene más probabilidades de omitir.',
            'Escríbelos de forma sencilla: nombre@ejemplo.com y +34 600 123 456, no "nombre [arroba] ejemplo [punto] com".',
        ],
        "nl": [
            'Zet je e-mail en telefoonnummer als platte tekst in de eerste drie regels, direct onder je naam.',
            'Laat ze niet alleen in een koptekst, in een afbeelding of in een tekstvak staan — dat zijn de drie plekken die een parser het vaakst mist.',
            'Schrijf ze gewoon uit: naam@voorbeeld.nl en +31 6 12345678, niet "naam [apenstaartje] voorbeeld [punt] nl".',
        ],
        "fr": [
            'Indiquez votre e-mail et votre téléphone en texte brut dans les trois premières lignes, juste sous votre nom.',
            "Ne les laissez pas uniquement dans un en-tête, dans une image ou dans une zone de texte : ce sont les trois endroits qu'un analyseur rate le plus souvent.",
            'Écrivez-les simplement : nom@exemple.fr et +33 6 12 34 56 78, pas "nom [arobase] exemple [point] fr".',
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
}


def rule_detail(rule_id: str, language: str) -> str:
    """The longer explanation shown when a finding is expanded, or "" when
    a rule has none yet -- the caller simply shows nothing extra."""
    entry = RULE_DETAILS.get(rule_id)
    if entry is None:
        return ""
    return entry.get(language) or entry.get(DEFAULT_LANGUAGE) or ""


def rule_fixes(rule_id: str, language: str) -> list[str]:
    """Concrete steps for this finding, most direct first. Empty when a
    rule has no advice yet, which the caller renders as no fix list rather
    than an empty heading."""
    entry = RULE_FIXES.get(rule_id)
    if entry is None:
        return []
    return entry.get(language) or entry.get(DEFAULT_LANGUAGE) or []


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
