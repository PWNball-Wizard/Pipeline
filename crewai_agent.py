"""
title: CrewAI Pipeline
author: open-webui
date: 2024-05-30
version: 1.1
license: MIT
description: Example pipeline integration for OpenWebUI using CrewAI.
requirements: crewai
"""

from typing import List, Union, Generator, Iterator
from pydantic import BaseModel
from crewai import Agent, Task, Crew, LLM

class Pipeline:

    class Valves(BaseModel):
        pass

    def __init__(self):
        self.valves = self.Valves()

        self.ollama_llm = LLM(
            model="ollama/llama3.2",
            base_url="http://host.docker.internal:11434",
            api_key="ollama"
        )

        self.researcher = Agent(
            role='Researcher',
            goal='Discover new insights',
            backstory="You're a world-class researcher working in a major data science company",
            verbose=True,
            allow_delegation=False,
            llm=self.ollama_llm
        )

        self.writer = Agent(
            role='Writer',
            goal='Create engaging content',
            backstory="You're a famous technical writer...",
            verbose=True,
            allow_delegation=False,
            llm=self.ollama_llm
        )

    async def on_startup(self):
        print(f"on_startup:{__name__}")

    async def on_shutdown(self):
        print(f"on_shutdown:{__name__}")

    def run(self, user_message: str) -> Union[str, Generator, Iterator]:
        print(f"[CrewAI] Recibiendo mensaje: {user_message}")

        task = Task(
            description=user_message,
            agent=self.researcher,
            expected_output="Detailed insights based on user's request"
        )

        crew = Crew(
            agents=[self.researcher, self.writer],
            tasks=[task],
            process="sequential"
        )

        result = crew.kickoff()
        print(f"[CrewAI] Respuesta generada: {result}")
        return result