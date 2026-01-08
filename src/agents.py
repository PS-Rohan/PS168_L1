import litellm
from crewai import Agent, LLM
from crewai_tools import SerperDevTool
from .config import Config

class CompanyIntelligenceAgents:
    def __init__(self):
        self.serper_tool = SerperDevTool()
        # Configuring Ollama LLM using CrewAI native LLM
        # Using 'openai' provider for better compatibility and stability with Ollama
        self.llm = LLM(
            model=f"openai/{Config.OLLAMA_MODEL}",
            base_url=f"{Config.OLLAMA_BASE_URL}/v1",
            api_key="ollama" # generic key for local ollama
        )

    def researcher_agent(self):
        return Agent(
            role='Company Researcher',
            goal='Search the internet for detailed information about the target company.',
            backstory="""You are an expert intelligence gatherer. Your job is to scour the web 
            to find the most relevant and recent information about a company, including its 
            products, leadership, key news, and market standing.""",
            tools=[self.serper_tool],
            llm=self.llm,
            verbose=True
        )

    def entity_extractor_agent(self):
        return Agent(
            role='Entity Extraction Specialist',
            goal='Analyze research data to identify key entities like Products, Key People, and Competitors.',
            backstory="""You are a data analyst with a sharp eye for details. You take raw information 
            and structure it by identifying the core entities that define the company.""",
            llm=self.llm,
            verbose=True
        )

    def relationship_mapper_agent(self):
        return Agent(
            role='Relationship Analyst',
            goal='Map relationships between the extracted entities (e.g., Person A is CEO of Company X).',
            backstory="""You specialize in connecting the dots. You understand how people, products, 
            and markets are interconnected within the company's ecosystem.""",
            llm=self.llm,
            verbose=True
        )

    def report_writer_agent(self):
        return Agent(
            role='Intelligence Report Writer',
            goal='Compile all findings into a comprehensive, professional Markdown report.',
            backstory="""You are a technical writer known for creating clear, concise, and actionable 
            intelligence reports for executive briefings.""",
            llm=self.llm,
            verbose=True
        )
