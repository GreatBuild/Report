import os
from utils.constants import page_break, FINAL_REPORT, CHAPTER_1, CHAPTER_2, CHAPTER_3, CHAPTER_4, CHAPTER_5, IMPLEMENTATION

def update_image_routes(content_md, level):
    if level == 0:
        relative_ref = 'src="../'
        alt_relative_ref = 'src="..\\'
        new_ref = 'src="./'
    elif level == 1:
        relative_ref = 'src="../../../'
        alt_relative_ref = 'src="..\\..\\..\\'
        new_ref = 'src="../'
    
    content_md = content_md.replace(relative_ref, new_ref)
    content_md = content_md.replace(alt_relative_ref, new_ref)
    
    return content_md


def combine_markdowns(output_file_obj):
    output_dir = os.path.dirname(output_file_obj.output_file_name)
    
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    ordered_files = [
        os.path.join(output_file_obj.source_dir, md_file) 
        for md_file in output_file_obj.order
        if os.path.exists(os.path.join(output_file_obj.source_dir, md_file))
    ]

    with open(output_file_obj.output_file_name, "w", encoding="utf-8") as outfile:
        if hasattr(output_file_obj, "header"):
            outfile.write(f"{output_file_obj.header}\n\n")

        for file_path in ordered_files:
            with open(file_path, "r", encoding="utf-8") as infile:
                content = infile.read()
                updated_content = update_image_routes(content, output_file_obj.level)
                outfile.write(updated_content)
                outfile.write(page_break)

def create_report(deliverable):
    if isinstance(deliverable, str):
        if deliverable == "TB1":
            deliverable = 1
        if deliverable == "TP":
            deliverable = 2
        if deliverable == "TB2":
            deliverable = 3
        if deliverable == "TF":
            deliverable = 4

    for i in range(deliverable):
        IMPLEMENTATION.order.append(f"Sprint{i+1}.md")

    if deliverable > 2:
        CHAPTER_5.order.append("ValidationInterviews.md")
        CHAPTER_5.order.append("About-the-Product.md")

    combine_markdowns(CHAPTER_1)
    combine_markdowns(CHAPTER_2)
    combine_markdowns(CHAPTER_3)
    combine_markdowns(CHAPTER_4)
    combine_markdowns(IMPLEMENTATION)
    combine_markdowns(CHAPTER_5)
    combine_markdowns(FINAL_REPORT)

    print(f"Archivos combinados en {FINAL_REPORT.output_file_name}")