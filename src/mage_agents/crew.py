
from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai.memory.long_term.long_term_memory import LongTermMemory
from crewai.memory.short_term.short_term_memory import ShortTermMemory
from crewai.memory.entity.entity_memory import EntityMemory
from crewai.memory.storage.ltm_sqlite_storage import LTMSQLiteStorage
from crewai.memory.storage.rag_storage import RAGStorage
from mage_agents.tools.calculator_tools import CalculatorTools
from mage_agents.tools.magento_tools import MagentoProductSearchTool, MagentoProductCreationTool, MagentoInventoryTool, MagentoOrderListTool
from crewai.knowledge.source.json_knowledge_source import JSONKnowledgeSource
from crewai.knowledge.storage.knowledge_storage import KnowledgeStorage

#from mage_agents.tools.sec_tools import SEC10KTool, SEC10QTool
from dotenv import load_dotenv
import os
load_dotenv()

llm = LLM(model=os.getenv("MODEL"), base_url=os.getenv("API_BASE"), temperature=0.2)

# Configuration for embeddings
embedder = {
	"provider": "ollama",
	"config": {
		"model": "nomic-embed-text:latest",
	},
}

magento_knowledge = JSONKnowledgeSource(
    file_paths=["adobe_commerce_knowledge_3.json"],
	collection_name="magento_knowledge",
	embedder=embedder,
	chunk_size=3000,
	chunk_overlap=200
)

# If you want to run a snippet of code before or after the crew starts, 
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class MageAgents():
	"""MageAgents crew"""

	# Learn more about YAML configuration files here:
	# Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
	# Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	# If you would like to add tools to your agents, you can learn more about it here:
	# https://docs.crewai.com/concepts/agents#agent-tools
	@agent
	def assistant(self) -> Agent:
			return Agent(
				config=self.agents_config["assistant"],
				llm=llm,
				verbose=False,
				knowledge_sources=[magento_knowledge],
				embedder=embedder,
				max_iter=2
			)
	
	def manager(self) -> Agent:
		return Agent(
			config=self.agents_config["manager"],
			llm=llm,
			verbose=True,
			allow_delegation=True,
			max_iter=2
		)

	# To learn more about structured task outputs, 
	# task dependencies, and task callbacks, check out the documentation:
	# https://docs.crewai.com/concepts/tasks#overview-of-a-task
	@task
	def assistant_task(self) -> Task:
		return Task(
			config=self.tasks_config["assistant_task"], 
			agent=self.assistant()
		)
	

	# Creating Tasks
	def search_product_task(self) -> Task: 
		return Task(
			config=self.tasks_config["search_product_task"], 
			agent=self.manager(),
			tools=[MagentoProductSearchTool()]
		)

	def create_product_task(self) -> Task:  
		return Task(
			config=self.tasks_config["create_product_task"], 
			agent=self.manager(),
			tools=[MagentoProductCreationTool()]
		)

	def update_stock_task(self) -> Task:
		return Task(
			config=self.tasks_config["update_stock_task"], 
			agent=self.manager(),                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       
			tools=[MagentoInventoryTool()]
		)

	def list_orders_task (self) -> Task:
		return Task(
			config=self.tasks_config["list_orders_task"], 
			agent=self.manager(),
			tools=[MagentoOrderListTool()]
		)


	@crew
	def crew(self) -> Crew:
		"""Creates the MageAgents crew"""
		# To learn how to add knowledge sources to your crew, check out the documentation:
		# https://docs.crewai.com/concepts/knowledge#what-is-knowledge

		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.hierarchical,
			manager_agent=self.manager(),
			verbose=True,
			memory=True,
			llm=llm,
			embedder=embedder,
		)
