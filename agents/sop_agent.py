from typing import List
from pydantic import BaseModel
import re

class SOPSection(BaseModel):
    title: str
    content: str

class SOPDocument(BaseModel):
    business_name: str
    department: str
    author: str
    sections: List[SOPSection]

def generate_sop(business_name: str, department: str, author: str) -> SOPDocument:
    # Template sections for the SOP
    template = [
        SOPSection(
            title="Purpose",
            content=f"The purpose of this SOP is to outline the operational procedures for the {department} department at {business_name}."
        ),
        SOPSection(
            title="Scope",
            content="This procedure applies to all personnel and operations within the specified department."
        ),
        SOPSection(
            title="Responsibilities",
            content="The department manager is responsible for overseeing operations and ensuring compliance with this SOP."
        ),
        SOPSection(
            title="Procedure",
            content="1. Start each workday with a team check-in.\n2. Complete assigned tasks according to the department’s workflow.\n3. Log all completed work into the project management system."
        ),
        SOPSection(
            title="References",
            content="- Company Handbook\n- Departmental Guidelines"
        )
    ]

    return SOPDocument(
        business_name=business_name,
        department=department,
        author=author,
        sections=template
    )

def sop_to_text(sop: SOPDocument) -> str:
    # Convert SOPDocument into a readable text format
    lines = [
        f"Standard Operating Procedure",
        f"Business: {sop.business_name}",
        f"Department: {sop.department}",
        f"Author: {sop.author}",
        ""
    ]
    for section in sop.sections:
        lines.append(f"## {section.title}")
        lines.append(section.content)
        lines.append("")
    return "\n".join(lines)
