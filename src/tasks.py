from crewai import Task

class CompanyIntelligenceTasks:
    def research_task(self, agent, company_name):
        return Task(
            description=f"""Conduct a comprehensive web search for the company '{company_name}'. 
            Focus on finding:
            1. Overview and Mission
            2. Key Products/Services
            3. Leadership Team (CEO, CTO, etc.)
            4. Recent News or Press Releases
            5. Competitors""",
            expected_output="A detailed summary of the company's background, products, leadership, and recent activities.",
            agent=agent
        )

    def extraction_task(self, agent, context):
        return Task(
            description="""Analyze the research findings and extract the following entities:
            - **Products/Services**: List of main offerings.
            - **People**: Key executives and their roles.
            - **Locations**: HQ and major offices.
            - **Competitors**: Main market rivals.
            
            Format this as a structured list.""",
            expected_output="A structured list of extracted entities (Products, People, Locations, Competitors).",
            agent=agent,
            context=context # Results from research_task
        )

    def mapping_task(self, agent, context):
        return Task(
            description="""Using the extracted entities, map the relationships.
            - Who leads which division?
            - Which product competes with which competitor?
            - How do the locations relate to their operations?""",
            expected_output="A text description of the relationships and connections between the identified entities.",
            agent=agent,
            context=context # Results from extraction_task (and maybe research_task)
        )

    def reporting_task(self, agent, context):
        return Task(
            description="""Create a comprehensive Company Intelligence Report in Markdown format.
            Include:
            1. **Executive Summary**
            2. **Company Overview**
            3. **Key Entities** (Table format preferred)
            4. **Relationship Analysis**
            5. **Recent Developments**
            
            Ensure the tone is professional and suitable for business strategy planning.""",
            expected_output="A full markdown report file named 'company_intelligence_report.md'.",
            agent=agent,
            context=context, # All previous contexts
            output_file="company_intelligence_report.md"
        )
