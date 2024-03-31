import json
import random

from langchain import LLMChain, PromptTemplate
from langchain.chat_models import ChatOpenAI

from src.resume.models import AIBaseInfo
from src.config import OPENAI_API_KEY


def write_description(ai_base_info: AIBaseInfo):
    """
    Writes experience, project, involvement based on the information that users provide by OpenAI
    """
    skills = ""
    if ai_base_info.skills:
        skills = "Skills: " + ai_base_info.skills
    extra_rule = ""
    if ai_base_info.experience:
        extra_rule = f"The experience must start with `{ai_base_info.experience}`."
    format_rule = ""
    if ai_base_info.pre_experience:
        format_rule = f"The schema of experience to write should be different from the following experiences." \
                      f"\n {ai_base_info.pre_experience}"

    prompt_template = """
    I am writing about experiences in resume. 
    {type}: {title}

    {skills}

    Also here are rules that you must follow while write experience.
    - Each experience should include at least 5 words. 
    - Capitalize the first letter and end with a period for each experience.
    {extra_rule}
    You have to follow the below rules with 40%.
    - Add metrics to each experience when possible.
    {format_rule}

    Write experience professionally in more detail based on the above as the following schema.
    Including what technologies you used, how you did, what you did in more detail, write experience professionally.
    Also You can write experience integrating several experience. If so, you can write long experience.
    ["write experience", "write experience", ..., "write experience"]
    Result Example: ["Developed a website with React", "Developed a website with React", "Developed a website with React"]
    Write only experience. Also don't include special character. Let's think step by step.
    """

    # Gets a LLM
    llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY, temperature=1, model_name="gpt-4")
    prompt = PromptTemplate(
        template=prompt_template,
        input_variables=["type", "title", "skills", "extra_rule", "format_rule"]
    )

    # Gets a LLM Chain
    llm_chain = LLMChain(prompt=prompt, llm=llm)

    result = llm_chain.run(
        type=ai_base_info.type,
        title=ai_base_info.prompt,
        skills=skills,
        extra_rule=extra_rule,
        format_rule=format_rule
    )

    result = result.replace("\n", "")
    experiences = json.loads(result)
    random_number = random.randint(0, len(experiences) - 1)
    return experiences[random_number]
