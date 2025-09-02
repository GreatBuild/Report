import os
from utils.models import OutputFile, HeaderOutputFile

page_break = '\n\n<div style="page-break-before: always;"></div>\n\n'
report_source_dir = "report_sections"
chapters_source_dir = os.path.join(report_source_dir, "chapter_sections", "chapter")

FINAL_REPORT = OutputFile(
    source_dir = report_source_dir, 
    output_file_name="README.md",
    order = [
        "Carátula.md",
        "RegistroVersiones del Informe.md",
        "CollaborationInsights.md",
        "Contenido.md",
        "StudentOutcome.md",
        "Introducción.md",
        "RequirementsElicitation.md",
        "RequirementsSpecification.md",
        "ProductDesign.md",
        "ProductImplementation.md",
        "Conclusiones.md",
        "Bibliografia.md",
        "Anexos.md"
    ]
)

CHAPTER_1 = HeaderOutputFile(
    header= "# Capítulo I: Introducción",
    source_dir= chapters_source_dir + "1",
    output_file_name= os.path.join("report_sections", "Introducción.md"),
    order=[
        "StartupProfile.md",
        "SolutionProfile.md",
        "SegmentosObjetivo.md",
    ]
)

CHAPTER_2 = HeaderOutputFile(
    header="# Capítulo II: Requirements Elicitation & Analysis",
    source_dir=chapters_source_dir + "2",
    output_file_name=os.path.join("report_sections", "RequirementsElicitation.md"),
    order=[
        "Competidores.md",
        "Entrevistas.md",
        "Needfinding.md",
    ]
)

CHAPTER_3 = HeaderOutputFile(
    header="# Capítulo III: Requirements Specification",
    source_dir=chapters_source_dir + "3",
    output_file_name=os.path.join("report_sections", "RequirementsSpecification.md"),
    order=[
        "To-Be.md",
        "UserStories.md",
        "ImpactMapping.md",
        "ProductBacklog.md",
    ]
)

CHAPTER_4 = HeaderOutputFile(
    header="# Capítulo IV: Product Design",
    source_dir=chapters_source_dir + "4",
    output_file_name=os.path.join("report_sections", "ProductDesign.md"),
    order=[
        "StyleGuidelines.md",
        "InformationArchitecture.md",
        "LandingPage.md",
        "WebAppUX.md",
        "WebAppPrototyping.md",
        "DDDArchitecture.md",
        "OOPDesign.md",
        "DBDesign.md",
    ]
)

IMPLEMENTATION = HeaderOutputFile(
    header="## 5.2. Landing Page, Services & Applications Implementation",
    source_dir=os.path.join(chapters_source_dir + "5", "implementation_sections"),
    output_file_name=os.path.join("report_sections", "chapter_sections", "chapter5", "Implementation.md"),
    order=[
    ]
)

CHAPTER_5 = HeaderOutputFile(
    header="# Capítulo V: Product Implementation, Validation & Deployment",
    source_dir=chapters_source_dir + "5",
    output_file_name=os.path.join("report_sections", "ProductImplementation.md"),
    order=[
        "ConfigurationManagement.md",
        "Implementation.md"
        #,"Validation Interviews.md", "Video About-the-Product.md"
    ]
)