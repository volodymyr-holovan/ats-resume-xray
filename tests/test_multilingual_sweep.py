"""Ten professions in each of the seven languages, end to end.

Written after running live German postings through the parser found four
faults that adverts written for the tests had never exposed. These adverts
are constructed, but to each language's own posting conventions and with
deliberately varied shape: some label their blocks, some do not, one shouts,
several list benefits that must never be read as requirements.

What each advert has to produce: the right language, a non-empty requirement
list, at least one hard requirement, and no benefit among the keywords.
"""

import pytest

from ats_xray.langid import detect_language
from ats_xray.vacancy import parse_vacancy

# (profession, advert, a word from the benefits that must never be extracted)
ADVERTS: dict[str, list[tuple[str, str, str]]] = {
    "de": [
        ("koch", """Ihr Profil
- Abgeschlossene Ausbildung als Koch ist zwingend erforderlich
- Mindestens drei Jahre Erfahrung in der Gastronomie
- Kenntnisse der HACCP-Vorgaben und der Kalkulation
Wir bieten
- Ein Jobticket und kostenlose Verpflegung""", "jobticket"),
        ("reinigung", """Ihr Profil
- Erfahrung in der Unterhaltsreinigung ist zwingend erforderlich
- Sicherer Umgang mit Reinigungsmaschinen und Reinigungsmitteln
- Sorgfalt, Zuverlaessigkeit und gute Deutschkenntnisse
Wir bieten
- Dienstkleidung und ein Deutschlandticket""", "deutschlandticket"),
        ("pflege", """Ihr Profil
- Abgeschlossene Ausbildung als Pflegefachkraft
- Mindestens zwei Jahre Berufserfahrung in der Altenpflege
- Kenntnisse in der Wundversorgung und der Medikamentengabe
- Bereitschaft zum Schichtdienst wird vorausgesetzt""", "praemie"),
        ("fahrer", """Anforderungen
- Fuehrerschein Klasse CE ist zwingend erforderlich
- Gueltige Fahrerkarte und Module nach dem BKrFQG
- Erfahrung mit Ladungssicherung und Gefahrgut nach ADR""", "urlaubsgeld"),
        ("buchhaltung", """Das bringen Sie mit
- Kaufmaennische Ausbildung oder ein Studium der Betriebswirtschaft
- Mehrjaehrige Erfahrung in der Finanzbuchhaltung
- Sicherer Umgang mit DATEV und Excel
Unsere Benefits
- Ein Firmenwagen und ein Zuschuss zur Altersvorsorge""", "firmenwagen"),
        ("elektro", """Dich zeichnet aus
- Abgeschlossene elektrotechnische Ausbildung
- Erfahrung in der Elektroinstallation und im Schaltschrankbau
- Kenntnisse in der Steuerungstechnik sind von Vorteil""", "werkzeug"),
        ("erzieher", """Ihr Profil
- Staatlich anerkannte Ausbildung als Erzieher
- Kenntnisse des Bildungsplans werden vorausgesetzt
- Erfahrung in der Elternarbeit ist wuenschenswert
- Ein erweitertes Fuehrungszeugnis""", "fortbildungsbudget"),
        ("verkauf", """WIR SUCHEN VERSTAERKUNG
Ihr Profil
- Erfahrung im Einzelhandel und an der Kasse
- Freude an der Kundenberatung und an der Warenpraesentation
- Bereitschaft zur Samstagsarbeit""", "personalrabatt"),
        ("design", """Ihr Profil
- Ein Studium im Bereich Mediengestaltung oder eine vergleichbare Ausbildung
- Sicherer Umgang mit InDesign und Photoshop
- Erfahrung in der Typografie und im Corporate Design""", "homeoffice"),
        ("sicherheit", """Voraussetzungen
- Die Sachkundepruefung nach Paragraf 34a ist zwingend erforderlich
- Erfahrung im Objektschutz und in der Zutrittskontrolle
- Bereitschaft zum Schichtdienst und ein einwandfreies Fuehrungszeugnis""", "zuschlag"),
    ],
    "en": [
        ("chef", """Requirements
- A completed apprenticeship as a chef is required
- At least three years of experience in a professional kitchen
- Knowledge of HACCP and of kitchen costing
We offer
- A season ticket and free meals on shift""", "season"),
        ("cleaner", """What you bring
- Experience with commercial cleaning is required
- Confident handling of cleaning machines and cleaning agents
- Care, reliability and good English""", "uniform"),
        ("nurse", """Requirements
- A completed nursing qualification
- At least two years of experience in elderly care
- Knowledge of wound care and medication management
- Willingness to work shifts is required""", "bonus"),
        ("driver", """Requirements
- A category CE driving licence is required
- A valid driver card and periodic training
- Experience with load securing and with dangerous goods""", "pension"),
        ("accountant", """About you
- A completed commercial training or a degree in business administration
- Several years of experience in financial accounting
- Confident with Excel and with accounting software
What we offer
- A company car and a pension contribution""", "company car"),
        ("electrician", """Who you are
- A completed electrical apprenticeship
- Experience with electrical installation and switchgear
- Knowledge of control technology is a plus""", "tools"),
        ("teacher", """Requirements
- A completed degree and a passion for teaching
- Experience with lesson planning and with didactics
- Knowledge of the curriculum is required""", "training budget"),
        ("shop", """Requirements
- Experience in retail and at the till
- Enjoyment of customer service and of merchandising
- Willingness to work Saturdays""", "staff discount"),
        ("design", """Your profile
- A degree in media design or a comparable qualification
- Confident with InDesign and Photoshop
- Experience with typography and corporate design""", "remote work"),
        ("security", """Requirements
- A recognised security qualification is required
- Experience with premises protection and access control
- Willingness to work shifts and a clean criminal record""", "shift allowance"),
    ],
    "es": [
        ("cocinero", """Requisitos
- Formacion profesional como cocinero es imprescindible
- Al menos tres anos de experiencia en cocina profesional
- Conocimientos de APPCC y de escandallos
Ofrecemos
- Manutencion y un plus de transporte""", "transporte"),
        ("limpieza", """Requisitos
- Experiencia en limpieza de edificios es imprescindible
- Manejo de maquinaria de limpieza y de productos quimicos
- Rigor, fiabilidad y buen nivel de espanol""", "uniforme"),
        ("enfermera", """Requisitos
- Titulacion en enfermeria
- Al menos dos anos de experiencia en geriatria
- Conocimientos de curas y de administracion de medicacion
- Disponibilidad para turnos""", "incentivo"),
        ("conductor", """Requisitos
- Carnet de conducir categoria CE imprescindible
- Tarjeta de tacografo en vigor
- Experiencia con sujecion de cargas y mercancias peligrosas""", "dietas"),
        ("contable", """Tu perfil
- Formacion profesional administrativa o estudios de empresariales
- Varios anos de experiencia en contabilidad financiera
- Dominio de Excel y de software contable
Ofrecemos
- Coche de empresa y plan de pensiones""", "coche"),
        ("electricista", """Requisitos
- Formacion profesional en electricidad
- Experiencia en instalaciones electricas y cuadros
- Conocimientos de automatismos valorables""", "herramienta"),
        ("profesor", """Requisitos
- Titulacion universitaria y vocacion docente
- Experiencia en programacion didactica
- Conocimiento del curriculo es imprescindible""", "formacion continua"),
        ("dependiente", """Requisitos
- Experiencia en comercio y en caja
- Gusto por la atencion al cliente y por el escaparatismo
- Disponibilidad los sabados""", "descuento"),
        ("diseno", """Tu perfil
- Estudios de diseno grafico o titulacion equivalente
- Dominio de InDesign y Photoshop
- Experiencia en tipografia y en identidad corporativa""", "teletrabajo"),
        ("vigilante", """Requisitos
- Habilitacion de vigilante de seguridad imprescindible
- Experiencia en proteccion de instalaciones y control de accesos
- Disponibilidad para turnos""", "pluses"),
    ],
    "nl": [
        ("kok", """Functie-eisen
- Een afgeronde opleiding tot kok is vereist
- Minimaal drie jaar ervaring in een professionele keuken
- Kennis van HACCP en van calculatie
Wij bieden
- Een reiskostenvergoeding en maaltijden tijdens de dienst""", "reiskosten"),
        ("schoonmaak", """Functie-eisen
- Ervaring met bedrijfsschoonmaak is vereist
- Bekend met schoonmaakmachines en schoonmaakmiddelen
- Zorgvuldigheid, betrouwbaarheid en goede beheersing van het Nederlands""", "werkkleding"),
        ("verpleging", """Wat vragen wij
- Een afgeronde opleiding verpleegkunde
- Minimaal twee jaar ervaring in de ouderenzorg
- Kennis van wondzorg en van medicatie
- Bereidheid tot onregelmatige diensten is vereist""", "toeslag"),
        ("chauffeur", """Vereisten
- Rijbewijs categorie CE is verplicht
- Een geldige bestuurderskaart en code 95
- Ervaring met ladingzekering en met gevaarlijke stoffen""", "pensioen"),
        ("boekhouder", """Jouw profiel
- Een administratieve opleiding of bedrijfskunde
- Meerdere jaren ervaring in de financiele administratie
- Vaardig met Excel en met boekhoudsoftware
Wij bieden
- Een leaseauto en een pensioenregeling""", "leaseauto"),
        ("elektricien", """Functie-eisen
- Een afgeronde elektrotechnische opleiding
- Ervaring met elektrische installaties en schakelkasten
- Kennis van besturingstechniek is een pre""", "gereedschap"),
        ("leraar", """Vereisten
- Een afgeronde opleiding en plezier in lesgeven
- Ervaring met lesvoorbereiding en didactiek
- Kennis van het curriculum is vereist""", "opleidingsbudget"),
        ("verkoop", """Functie-eisen
- Ervaring in de detailhandel en achter de kassa
- Plezier in klantcontact en in de presentatie van artikelen
- Bereidheid om op zaterdag te werken""", "personeelskorting"),
        ("vormgever", """Jouw profiel
- Een opleiding grafische vormgeving of vergelijkbaar
- Vaardig met InDesign en Photoshop
- Ervaring met typografie en huisstijl""", "thuiswerken"),
        ("beveiliger", """Vereisten
- Een beveiligingsdiploma is verplicht
- Ervaring met objectbeveiliging en toegangscontrole
- Bereidheid tot onregelmatige diensten""", "onregelmatigheidstoeslag"),
    ],
    "fr": [
        ("cuisinier", """Profil recherche
- Un CAP cuisine est exige
- Au moins trois ans d'experience en cuisine professionnelle
- Connaissance de la methode HACCP et des couts matiere
Nous offrons
- Une prime de transport et les repas fournis""", "prime"),
        ("entretien", """Exigences
- Une experience du nettoyage industriel est exigee
- Maitrise des autolaveuses et des produits d'entretien
- Rigueur, fiabilite et bon niveau de francais""", "tenue"),
        ("infirmier", """Profil recherche
- Un diplome d'Etat d'infirmier
- Au moins deux ans d'experience en geriatrie
- Connaissance des soins de plaies et de l'administration des traitements
- Disponibilite pour le travail poste est exigee""", "indemnite"),
        ("chauffeur", """Exigences
- Le permis de conduire categorie CE est obligatoire
- Une carte conducteur en cours de validite et la FIMO
- Experience de l'arrimage et des matieres dangereuses""", "mutuelle"),
        ("comptable", """Votre profil
- Une formation en comptabilite ou en gestion
- Plusieurs annees d'experience en comptabilite generale
- Maitrise d'Excel et d'un logiciel comptable
Nous offrons
- Un vehicule de fonction et une mutuelle""", "vehicule"),
        ("electricien", """Profil recherche
- Une formation en electrotechnique
- Experience des installations electriques et des armoires
- La connaissance de l'automatisme est un atout""", "outillage"),
        ("enseignant", """Exigences
- Un diplome et le gout de la transmission
- Experience de la preparation des cours et de la didactique
- La connaissance des programmes est exigee""", "formation continue"),
        ("vendeur", """Profil recherche
- Experience de la vente et de la tenue de caisse
- Gout du conseil client et du merchandising
- Disponibilite le samedi""", "remise"),
        ("graphiste", """Votre profil
- Une formation en design graphique ou equivalente
- Maitrise d'InDesign et de Photoshop
- Experience de la typographie et de l'identite visuelle""", "teletravail"),
        ("securite", """Exigences
- La carte professionnelle est obligatoire
- Experience de la protection de site et du controle d'acces
- Disponibilite pour le travail poste""", "majoration"),
    ],
    "uk": [
        ("kukhar", """Вимоги
- Профільна освіта кухаря є обов'язковою
- Щонайменше три роки досвіду роботи на професійній кухні
- Знання HACCP та калькуляції страв
Ми пропонуємо
- Проїзний квиток та безкоштовне харчування""", "проїзний"),
        ("prybyral", """Вимоги
- Досвід роботи з прибирання приміщень є обов'язковим
- Впевнене поводження з прибиральними машинами та засобами
- Охайність, надійність та добре знання української""", "спецодяг"),
        ("medsestra", """Вимоги
- Закінчена медична освіта
- Щонайменше два роки досвіду роботи в геріатрії
- Знання з обробки ран та введення препаратів
- Готовність до змінного графіка є обов'язковою""", "премія"),
        ("vodiy", """Вимоги
- Посвідчення водія категорії CE є обов'язковим
- Чинна картка водія та відповідні модулі
- Досвід роботи з кріпленням вантажу та небезпечними вантажами""", "надбавка"),
        ("bukhhalter", """Ваш профіль
- Освіта у сфері обліку або економіки
- Кілька років досвіду роботи у фінансовому обліку
- Впевнене володіння Excel та обліковим програмним забезпеченням
Ми пропонуємо
- Службовий автомобіль та медичне страхування""", "автомобіль"),
        ("elektryk", """Вимоги
- Закінчена електротехнічна освіта
- Досвід роботи з електромонтажем та шафами керування
- Знання систем автоматизації буде перевагою""", "інструмент"),
        ("vchytel", """Вимоги
- Вища освіта та бажання навчати
- Досвід підготовки уроків та знання методики
- Знання навчальної програми є обов'язковим""", "навчання"),
        ("prodavets", """Вимоги
- Досвід роботи в роздрібній торгівлі та на касі
- Бажання консультувати клієнтів та викладати товар
- Готовність працювати в суботу""", "знижка"),
        ("dyzayner", """Ваш профіль
- Освіта у сфері графічного дизайну або рівноцінна
- Впевнене володіння InDesign та Photoshop
- Досвід роботи з типографікою та фірмовим стилем""", "віддалено"),
        ("okhoronets", """Вимоги
- Дозвіл на охоронну діяльність є обов'язковим
- Досвід охорони об'єктів та контролю доступу
- Готовність до змінного графіка""", "доплата"),
    ],
    "ru": [
        ("povar", """Требования
- Профильное образование повара обязательно
- Не менее трех лет опыта работы на профессиональной кухне
- Знание ХАССП и калькуляции блюд
Мы предлагаем
- Проездной билет и бесплатное питание""", "проездной"),
        ("uborka", """Требования
- Опыт работы по уборке помещений обязателен
- Уверенное обращение с уборочными машинами и средствами
- Аккуратность, надежность и хорошее знание русского""", "спецодежда"),
        ("medsestra", """Требования
- Законченное медицинское образование
- Не менее двух лет опыта работы в гериатрии
- Знание обработки ран и введения препаратов
- Готовность к сменному графику обязательна""", "премия"),
        ("voditel", """Требования
- Водительское удостоверение категории CE обязательно
- Действующая карта водителя и необходимые модули
- Опыт работы с креплением груза и опасными грузами""", "надбавка"),
        ("bukhgalter", """Ваш профиль
- Образование в области учета или экономики
- Несколько лет опыта работы в финансовом учете
- Уверенное владение Excel и учетной программой
Мы предлагаем
- Служебный автомобиль и медицинскую страховку""", "автомобиль"),
        ("elektrik", """Требования
- Законченное электротехническое образование
- Опыт работы с электромонтажом и шкафами управления
- Знание систем автоматизации будет преимуществом""", "инструмент"),
        ("uchitel", """Требования
- Высшее образование и желание учить
- Опыт подготовки уроков и знание методики
- Знание учебной программы обязательно""", "обучение"),
        ("prodavets", """Требования
- Опыт работы в розничной торговле и на кассе
- Желание консультировать клиентов и выкладывать товар
- Готовность работать в субботу""", "скидка"),
        ("dizayner", """Ваш профиль
- Образование в области графического дизайна или равноценное
- Уверенное владение InDesign и Photoshop
- Опыт работы с типографикой и фирменным стилем""", "удаленно"),
        ("okhrannik", """Требования
- Лицензия охранника обязательна
- Опыт охраны объектов и контроля доступа
- Готовность к сменному графику""", "доплата"),
    ],
}

CASES = [
    pytest.param(language, profession, advert, benefit, id=f"{language}-{profession}")
    for language, adverts in ADVERTS.items()
    for profession, advert, benefit in adverts
]


@pytest.mark.parametrize(("language", "profession", "advert", "benefit"), CASES)
def test_the_language_is_recognised(language, profession, advert, benefit):
    assert detect_language(advert) == language


@pytest.mark.parametrize(("language", "profession", "advert", "benefit"), CASES)
def test_requirements_come_out_with_at_least_one_hard_one(language, profession, advert, benefit):
    """An empty list is worse than a rough one: the reader has nothing to
    correct. A list with nothing required means the weighting is dead."""
    requirements = parse_vacancy(advert).requirements

    assert requirements, "no requirements at all"
    assert any(r.must for r in requirements), "nothing marked as required"


@pytest.mark.parametrize(("language", "profession", "advert", "benefit"), CASES)
def test_the_benefits_are_never_read_as_requirements(language, profession, advert, benefit):
    """The single most embarrassing failure this tool can produce: telling a
    candidate they lack the company's travel allowance."""
    labels = " ".join(r.label.lower() for r in parse_vacancy(advert).requirements)

    assert benefit.lower() not in labels
