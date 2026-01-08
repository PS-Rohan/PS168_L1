import argparse
from crewai import Crew, Process
from src.config import Config
from src.agents import CompanyIntelligenceAgents
from src.tasks import CompanyIntelligenceTasks

def main():
    parser = argparse.ArgumentParser(description="Company Intelligence Platform")
    parser.add_argument("--company", type=str, required=True, help="Name of the company to research")
    args = parser.parse_args()

    company_name = args.company

    # Validate Config
    try:
        Config.validate()
    except ValueError as e:
        print(f"Configuration Error: {e}")
        print("Please verify your .env file.")
        return

    print(f"Starting Company Intelligence Run for: {company_name}")

    # Initialize Agents and Tasks
    agents = CompanyIntelligenceAgents()
    tasks = CompanyIntelligenceTasks()

    # Create Agents
    researcher = agents.researcher_agent()
    extractor = agents.entity_extractor_agent()
    mapper = agents.relationship_mapper_agent()
    reporter = agents.report_writer_agent()

    # Create Tasks
    task1 = tasks.research_task(researcher, company_name)
    task2 = tasks.extraction_task(extractor, context=[task1])
    task3 = tasks.mapping_task(mapper, context=[task2])
    task4 = tasks.reporting_task(reporter, context=[task1, task2, task3])

    # Create Crew
    crew = Crew(
        agents=[researcher, extractor, mapper, reporter],
        tasks=[task1, task2, task3, task4],
        verbose=True,
        process=Process.sequential,
        memory=False # Disable memory to avoid local embedding model requirement (transformers/torch)
    )

    # Kickoff
    result = crew.kickoff()
    
    print("\n\n########################")
    print("## Intelligence Report Generated ##")
    print("########################\n")
    print(result)

if __name__ == "__main__":
    main()
