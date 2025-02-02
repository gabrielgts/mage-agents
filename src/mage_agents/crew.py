
from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai.memory.long_term.long_term_memory import LongTermMemory
from crewai.memory.short_term.short_term_memory import ShortTermMemory
from crewai.memory.entity.entity_memory import EntityMemory
from crewai.memory.storage.ltm_sqlite_storage import LTMSQLiteStorage
from crewai.memory.storage.rag_storage import RAGStorage
from mage_agents.tools.calculator_tools import CalculatorTools
from crewai.knowledge.source.json_knowledge_source import JSONKnowledgeSource
#from mage_agents.tools.sec_tools import SEC10KTool, SEC10QTool
from dotenv import load_dotenv
import os
load_dotenv()

llm = LLM(model="ollama/llama3.2:3b", base_url="http://localhost:11434")

# Configuration for embeddings
embedder = {
	"provider": "ollama",
	"config": {
		"model": "nomic-embed-text",
		"ollama_base_url": "http://localhost:11434",
	},
}

magento_knowledge = JSONKnowledgeSource(
    file_paths=["magento_knowledge.json"]
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
				task=self.tasks_config["assistant"],
				knowledge_sources=[magento_knowledge]
			)
	
	def manager(self) -> Agent:
		return Agent(
			config=self.agents_config["manager"],
			llm=llm,
			verbose=True,
			allow_delegation=True,
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
			memory=False,
			# long_term_memory=LongTermMemory(
			# 	storage=LTMSQLiteStorage(
			# 		db_path="./data/long_term_memory_storage.db",
			# 	)
			# ),
			# short_term_memory=ShortTermMemory(
			# 	storage=RAGStorage(
			# 		type="short_term",
			# 	),
			# 	embedder_config=embedder,
			# 	path=f"./data/short_term_memory.db",
			# ),
			# entity_memory=EntityMemory(
			# 	storage=RAGStorage(
			# 		type="entities",
			# 	),
			# 	embedder_config=embedder,
			# 	path=f"./data/entity_memory.db",
			# ),
		)
