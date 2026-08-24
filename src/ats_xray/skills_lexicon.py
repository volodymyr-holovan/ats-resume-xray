"""A curated gazetteer of skills, with the spellings job adverts use.

Free-text keyword extraction without a gazetteer picks up whatever nouns
happen to be capitalised, which in a German advert means the company name,
the city, and "Mitarbeiter". A curated list is less clever and far more
accurate: a term is a skill because it is on the list, and every alias is
something a person decided to put there.

Aliases carry the spelling variants that actually occur -- the German name
next to the English one, the abbreviation next to the full form. Matching
is longest-alias-first, so "Microsoft SQL Server" is recognised as MSSQL
rather than as SQL plus noise.

Deliberately absent: single-letter and short common-word names. "R" and
"Go" are real technologies whose names collide with ordinary German and
English words often enough that including them would cost more in false
matches than they return in true ones. They are reachable through their
unambiguous spellings ("R-Programmierung", "Golang") instead.
"""

from dataclasses import dataclass

from .normalize import fold


@dataclass(frozen=True)
class Skill:
    id: str
    label: str
    category: str
    aliases: tuple[str, ...]


def _s(id_: str, label: str, category: str, *aliases: str) -> Skill:
    # The label is always an alias: the canonical spelling is the one most
    # likely to appear, and repeating it in every entry would be noise.
    return Skill(id_, label, category, (label, *aliases))


SKILLS: tuple[Skill, ...] = (
    # --- programming languages -------------------------------------------
    _s("python", "Python", "language"),
    _s("csharp", "C#", "language", "c sharp", "csharp"),
    _s("cpp", "C++", "language", "cpp"),
    _s("java", "Java", "language"),
    _s("javascript", "JavaScript", "language", "js", "ecmascript"),
    _s("typescript", "TypeScript", "language", "ts"),
    _s("php", "PHP", "language"),
    _s("ruby", "Ruby", "language"),
    _s("kotlin", "Kotlin", "language"),
    _s("swift", "Swift", "language"),
    _s("scala", "Scala", "language"),
    _s("golang", "Go", "language", "golang", "go-entwicklung"),
    _s("rlang", "R", "language", "r-programmierung", "sprache r", "r language"),
    _s("rust", "Rust", "language"),
    _s("perl", "Perl", "language"),
    _s("abap", "ABAP", "language"),
    _s("matlab", "MATLAB", "language"),
    _s("vba", "VBA", "language", "visual basic for applications"),
    # --- shells and scripting --------------------------------------------
    _s("bash", "Bash", "language", "shell", "shellskripte", "shell scripting", "sh"),
    _s("powershell", "PowerShell", "language", "power shell"),
    # --- .NET -------------------------------------------------------------
    _s("dotnet", ".NET", "framework", "dotnet", ".net core", ".net framework", "net framework"),
    _s("aspnet", "ASP.NET", "framework", "asp net", "aspnet core"),
    _s("entityframework", "Entity Framework", "framework", "ef core", "entityframework"),
    _s("wpf", "WPF", "framework", "windows presentation foundation"),
    _s("blazor", "Blazor", "framework"),
    _s("xamarin", "Xamarin", "framework", "maui"),
    # --- web ---------------------------------------------------------------
    _s("html", "HTML", "web", "html5"),
    _s("css", "CSS", "web", "css3", "scss", "sass"),
    _s("react", "React", "web", "react.js", "reactjs"),
    _s("angular", "Angular", "web", "angularjs"),
    _s("vue", "Vue", "web", "vue.js", "vuejs"),
    _s("nodejs", "Node.js", "web", "nodejs", "node js"),
    _s("rest", "REST", "web", "rest-api", "restful", "rest api", "restful api"),
    _s("graphql", "GraphQL", "web"),
    _s("soap", "SOAP", "web"),
    _s("django", "Django", "web"),
    _s("flask", "Flask", "web"),
    _s("fastapi", "FastAPI", "web"),
    _s("spring", "Spring", "web", "spring boot", "springboot"),
    _s("streamlit", "Streamlit", "web"),
    # --- databases ---------------------------------------------------------
    _s("sql", "SQL", "database", "sql-kenntnisse", "structured query language"),
    _s("mysql", "MySQL", "database", "mariadb"),
    _s("postgresql", "PostgreSQL", "database", "postgres"),
    _s("mssql", "Microsoft SQL Server", "database", "ms sql", "mssql", "sql server", "t-sql", "tsql"),
    _s("oracledb", "Oracle Database", "database", "oracle db", "pl/sql", "plsql"),
    _s("mongodb", "MongoDB", "database", "mongo"),
    _s("redis", "Redis", "database"),
    _s("sqlite", "SQLite", "database"),
    _s("elasticsearch", "Elasticsearch", "database", "elastic search", "opensearch"),
    _s("bigquery", "BigQuery", "database", "google bigquery"),
    _s("snowflake", "Snowflake", "database"),
    _s("datamodeling", "Datenmodellierung", "database", "data modeling", "datenmodell", "datenbankdesign"),
    _s("etl", "ETL", "data", "etl-prozesse", "datenpipelines", "data pipeline", "elt"),
    # --- data and analytics ------------------------------------------------
    _s("pandas", "pandas", "data"),
    _s("numpy", "NumPy", "data"),
    _s("scikitlearn", "scikit-learn", "data", "sklearn", "scikit learn"),
    _s("tableau", "Tableau", "data"),
    _s("powerbi", "Power BI", "data", "powerbi", "microsoft power bi"),
    _s("excel", "Excel", "data", "microsoft excel", "ms excel", "pivot-tabellen"),
    _s("spark", "Apache Spark", "data", "pyspark", "spark"),
    _s("statistics", "Statistik", "data", "statistics", "deskriptive statistik", "statistische analyse"),
    _s("dataviz", "Datenvisualisierung", "data", "data visualization", "dashboards", "reporting"),
    _s("dataquality", "Datenqualität", "data", "data quality", "data cleaning", "datenbereinigung", "stammdatenpflege"),
    # --- AI / ML -----------------------------------------------------------
    _s("machinelearning", "Maschinelles Lernen", "ai", "machine learning", "ml", "maschinelles lernen"),
    _s("deeplearning", "Deep Learning", "ai", "neuronale netze", "neural networks", "tiefes lernen"),
    _s("llm", "Große Sprachmodelle", "ai", "large language models", "llm", "llms", "sprachmodelle"),
    _s("nlp", "NLP", "ai", "natural language processing", "computerlinguistik", "sprachverarbeitung"),
    _s("computervision", "Computer Vision", "ai", "bildverarbeitung", "bilderkennung"),
    _s("tensorflow", "TensorFlow", "ai", "keras"),
    _s("pytorch", "PyTorch", "ai"),
    _s("ai_general", "Künstliche Intelligenz", "ai", "artificial intelligence", "ki", "ai"),
    _s("aiagents", "KI-Agenten", "ai", "ai agents", "agentic", "ki agenten"),
    _s("ollama", "Ollama", "ai"),
    _s("rag", "RAG", "ai", "retrieval augmented generation"),
    _s("promptengineering", "Prompt Engineering", "ai", "prompting"),
    # --- infrastructure ----------------------------------------------------
    _s("linux", "Linux", "infra", "unix", "ubuntu", "debian", "red hat", "rhel", "centos", "suse"),
    _s("windowsserver", "Windows Server", "infra", "windows-server"),
    _s("docker", "Docker", "infra", "container", "containerisierung", "docker compose", "podman"),
    _s("kubernetes", "Kubernetes", "infra", "k8s", "openshift", "helm"),
    _s("ansible", "Ansible", "infra"),
    _s("terraform", "Terraform", "infra", "infrastructure as code", "iac"),
    _s("puppet", "Puppet", "infra", "chef", "saltstack"),
    _s("vmware", "VMware", "infra", "vsphere", "esxi", "virtualisierung", "virtualization"),
    _s("proxmox", "Proxmox", "infra"),
    _s("hyperv", "Hyper-V", "infra", "hyperv"),
    _s("truenas", "TrueNAS", "infra", "freenas", "nas", "nas-systeme"),
    _s("nginx", "Nginx", "infra", "apache", "webserver", "iis"),
    _s("aws", "AWS", "cloud", "amazon web services", "ec2", "s3"),
    _s("azure", "Azure", "cloud", "microsoft azure", "azure devops"),
    _s("gcp", "Google Cloud", "cloud", "gcp", "google cloud platform"),
    _s("cloud_general", "Cloud", "cloud", "cloud-technologien", "cloud computing"),
    _s("backup", "Backup", "infra", "datensicherung", "restore", "disaster recovery"),
    _s("monitoring", "Monitoring", "infra", "überwachung", "prometheus", "grafana", "nagios", "zabbix"),
    # --- networking --------------------------------------------------------
    _s("networking", "Netzwerk", "network", "netzwerke", "networking", "netzwerktechnik", "lan", "wan"),
    _s("tcpip", "TCP/IP", "network", "tcp ip"),
    _s("dns", "DNS", "network", "dhcp"),
    _s("vpn", "VPN", "network"),
    _s("firewall", "Firewall", "network", "firewalls", "fortigate", "pfsense"),
    _s("activedirectory", "Active Directory", "network", "ad", "ldap", "entra id", "azure ad"),
    _s("exchange", "Exchange", "network", "microsoft exchange", "outlook", "mail-server"),
    _s("m365", "Microsoft 365", "network", "office 365", "o365", "ms office", "microsoft office"),
    # --- tools and process -------------------------------------------------
    _s("git", "Git", "tool", "github", "gitlab", "bitbucket", "versionsverwaltung", "version control"),
    _s("cicd", "CI/CD", "method", "ci cd", "continuous integration", "continuous delivery", "jenkins", "github actions", "gitlab ci"),
    _s("jira", "Jira", "tool", "confluence", "atlassian"),
    _s("n8n", "n8n", "tool", "zapier", "make.com"),
    _s("sap", "SAP", "business", "sap erp", "s/4hana"),
    _s("salesforce", "Salesforce", "business", "crm"),
    _s("sharepoint", "SharePoint", "business"),
    _s("ticketsystem", "Ticketsystem", "business", "ticketing", "servicedesk", "service desk", "helpdesk", "otrs"),
    # --- methods -----------------------------------------------------------
    _s("scrum", "Scrum", "method", "agile", "agil", "kanban", "safe"),
    _s("devops", "DevOps", "method"),
    _s("itil", "ITIL", "method"),
    _s("testing", "Testing", "method", "softwaretest", "qualitätssicherung", "quality assurance", "qa", "testautomatisierung", "test automation"),
    _s("tdd", "TDD", "method", "test driven development", "unit tests", "unittests", "pytest"),
    _s("oop", "Objektorientierte Programmierung", "method", "object oriented programming", "oop", "objektorientierung"),
    _s("microservices", "Microservices", "method", "microservice", "mikroservices"),
    _s("designpatterns", "Design Patterns", "method", "entwurfsmuster", "clean code", "solid"),
    _s("requirements", "Anforderungsanalyse", "method", "requirements engineering", "anforderungsmanagement"),
    _s("documentation", "Dokumentation", "method", "technische dokumentation", "documentation"),
    _s("projectmanagement", "Projektmanagement", "method", "project management", "projektleitung"),
    _s("security", "IT-Sicherheit", "method", "it-security", "informationssicherheit", "cyber security", "cybersecurity", "datenschutz", "dsgvo", "gdpr"),
    _s("support", "Anwendersupport", "business", "user support", "1st level", "2nd level", "first level", "second level", "anwenderbetreuung"),
    _s("training", "Schulungen", "business", "schulung", "training", "einweisung", "workshops"),
    _s("automation", "Automatisierung", "method", "automation", "prozessautomatisierung", "process automation", "workflow automation"),
    _s("digitalisierung", "Digitalisierung", "business", "prozessdigitalisierung", "digital transformation"),
    # --- design and media --------------------------------------------------
    _s("uiux", "UI/UX", "design", "ux", "ui design", "usability"),
    _s("figma", "Figma", "design", "adobe xd", "sketch"),
    _s("photoshop", "Photoshop", "design", "adobe creative suite", "illustrator", "indesign", "grafikdesign"),
    _s("houdini", "Houdini", "design", "sidefx houdini", "3d-simulation"),
    _s("cad", "CAD", "design", "autocad", "solidworks", "catia"),
)

SKILLS_BY_ID: dict[str, Skill] = {skill.id: skill for skill in SKILLS}

AMBIGUOUS_ALIASES = frozenset({"go", "r", "ef core"})
"""Spellings that are never treated as a skill mention even though they are
the real name of one. "Go live" and "R&D" are ordinary phrases, and a
requirements list that gained the Go language from a launch date would be
wrong in a way the reader cannot easily spot. These skills stay reachable
through their unambiguous aliases."""

ALIAS_TO_ID: dict[str, str] = {}
for _skill in SKILLS:
    for _alias in _skill.aliases:
        _folded = fold(_alias)
        if not _folded or _folded in AMBIGUOUS_ALIASES:
            continue
        # First writer wins: an alias listed under two skills belongs to the
        # one that declared it first, and a silent reassignment here would be
        # very hard to notice later.
        ALIAS_TO_ID.setdefault(_folded, _skill.id)

MAX_ALIAS_WORDS = max(len(alias.split()) for alias in ALIAS_TO_ID)


def label_for(skill_id: str) -> str:
    skill = SKILLS_BY_ID.get(skill_id)
    return skill.label if skill else skill_id


def category_for(skill_id: str) -> str:
    skill = SKILLS_BY_ID.get(skill_id)
    return skill.category if skill else "other"


def find_skills(text: str) -> list[str]:
    """Skill ids mentioned in ``text``, in order of first appearance.

    Scans longest phrase first so that "Microsoft SQL Server" is consumed
    whole instead of leaving a stray "SQL" behind, and marks the words it
    consumed so one mention cannot count twice.
    """
    from .normalize import same_word

    words = text and fold(text).split() or []
    consumed = [False] * len(words)
    found: list[str] = []

    for size in range(MAX_ALIAS_WORDS, 0, -1):
        for start in range(len(words) - size + 1):
            if any(consumed[start : start + size]):
                continue
            window = words[start : start + size]
            skill_id = _lookup(window, same_word)
            if skill_id is None:
                continue
            for index in range(start, start + size):
                consumed[index] = True
            if skill_id not in found:
                found.append(skill_id)

    return found


def _lookup(window: list[str], same_word) -> str | None:
    """Resolve one window of words to a skill id.

    Tries the exact spelling first, because that is both the common case
    and the safe one. Only single words fall back to inflection-tolerant
    comparison: allowing it on every phrase would make long aliases match
    far too loosely.
    """
    phrase = " ".join(window)
    exact = ALIAS_TO_ID.get(phrase)
    if exact is not None:
        return exact
    if len(window) != 1:
        return None
    for alias, skill_id in ALIAS_TO_ID.items():
        if " " not in alias and same_word(alias, phrase):
            return skill_id
    return None
