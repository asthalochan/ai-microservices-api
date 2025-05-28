# apps/ai_article_writer/agents_and_logic.py

from crewai import Agent, Task, Crew
from apps.ai_article_writer.config import settings

# -------------------- Agents --------------------

planner = Agent(
    role="Content Planner",
    goal="Plan engaging and factually accurate content on a topic",
    backstory="You're responsible for planning informative, structured content for articles. Your job is to organize ideas and facts to help writers produce high-quality content.",
    allow_delegation=False,
    verbose=True
)

writer = Agent(
    role="Content Writer",
    goal="Write an insightful and accurate article using the planner's outline",
    backstory="You use the planner's outline to write a detailed, well-reasoned blog post with clear structure and valuable content.",
    allow_delegation=False,
    verbose=True
)

editor = Agent(
    role="Editor",
    goal="Review and polish the article for clarity, accuracy, and tone",
    backstory="As the editor, your job is to ensure the article meets professional standards, follows journalistic tone, and is ready for publication.",
    allow_delegation=False,
    verbose=True
)

# -------------------- Pipeline Function --------------------

def run_article_pipeline(topic: str) -> str:
    planning_task = Task(
        description=(
            f"Analyze the topic '{topic}' and generate a detailed outline with subtopics, key insights, audience focus, SEO keywords, and sources. "
            "Structure the plan clearly, no Markdown or HTML needed."
        ),
        expected_output="Content plan with outline, audience info, keywords, references.",
        agent=planner,
    )

    writing_task = Task(
        description=(
            "Write a full blog article (1000–1500 words) using <h2> and <p> tags. Include intro, 5–7 body sections, and a conclusion. "
            "Do not use Markdown or backticks. Output clean HTML only."
        ),
        expected_output="A well-structured HTML blog post with intro, sections, and conclusion.",
        agent=writer,
    )

    editing_task = Task(
        description=(
            "Edit the article for grammar, tone, and structure. Clean up any formatting issues. Output must be clean, final HTML."
        ),
        expected_output="Final edited HTML article ready for publishing.",
        agent=editor,
    )

    crew = Crew(
        agents=[planner, writer, editor],
        tasks=[planning_task, writing_task, editing_task],
        verbose=True
    )

    result = crew.kickoff(inputs={"topic": topic})

    # ✅ Extract actual output
    final_output = result.output if hasattr(result, "output") else str(result)

    # ✅ Clean up triple backticks if needed
    if final_output.strip().startswith("```") and final_output.strip().endswith("```"):
        final_output = "\n".join(final_output.strip().splitlines()[1:-1])

    return final_output.strip()
