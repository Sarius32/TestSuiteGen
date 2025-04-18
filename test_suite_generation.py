import json
import logging
import logging.handlers as handlers
import os
from time import sleep

import seedir
import subprocess

from google import genai
from google.genai import types
from datetime import datetime
from dotenv import load_dotenv
from typing_extensions import TypedDict

from constants import MODEL_NAME, LOGGING_LEVEL
from utils import clean_python_response

os.makedirs("logs", exist_ok=True)
LOGGER = logging.getLogger(__name__)
log_f = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
rf_handler = handlers.RotatingFileHandler(filename="logs/TestSuite.log", maxBytes=100 * 1024, backupCount=5)  # 100kB
stream_handler = logging.StreamHandler()
rf_handler.setFormatter(log_f), stream_handler.setFormatter(log_f)
LOGGER.addHandler(rf_handler), LOGGER.addHandler(stream_handler)
LOGGER.setLevel(LOGGING_LEVEL)

load_dotenv()


class Chat:
    def __init__(self, name: str, api_key: str, model_name: str, config: types.GenerateContentConfig):
        self.name = name
        self.client = genai.Client(api_key=api_key)

        LOGGER.info(f"Reading in project files ({self.name})...")
        with open("project/src/lexer.py", "r") as f:
            self.lex_str = f.read()
        with open("project/src/tokens.py", "r") as f:
            self.tok_str = f.read()

        self.chat = self.client.chats.create(model=model_name, config=config)


class TestGenChat(Chat):
    def __init__(self, api_key: str, model_name: str):
        sys_prompt = f"""

Your are a software tester, specialized on working with python projects.
Your goal is to write a test suite for the given python project using the python testing framework `unittest`!

The project has the following structure:
{seedir.seedir("project", printout=False)}

You will be provided all files in the src/ folder.
Additionally, feedback to the generated tests.py will be provided.

Your task is to improve the generated test suite based on the given feedback or generate the initial one.
Please ensure that any testsuite doesn't change the project structure (i.e. remove temporary testing data after the test execution).

For the given project files only answer with the contents of the tests.py file. Respond with Python code only.

""".strip()

        super().__init__("TS Generator", api_key, model_name,
                         types.GenerateContentConfig(system_instruction=sys_prompt))

    @staticmethod
    def _save_test_suite(content: str):
        with open("project/tests.py", "w") as tests_file:
            tests_file.write(clean_python_response(content))

        date, time = datetime.now().strftime("%Y-%m-%d/%H_%M_%S").split("/")
        os.makedirs(f"logs/suites/{date}", exist_ok=True)
        with open(f"logs/suites/{date}/tests_{time}.py", "w") as tests_log:
            LOGGER.debug(f"Saving suite to logs/suites/{date}/tests_{time}.py")
            tests_log.write(clean_python_response(content))

    def init_testsuite(self):
        LOGGER.info("Sending initial test suite request...")
        res = self.chat.send_message(message=f"These are the project file contents:"
                                             f" - lexer.py\n```python\n{self.lex_str}\n```\n"
                                             f" - tokens.py\n```python\n{self.tok_str}\n```\n")
        LOGGER.info("Received initial test suite!")
        self._save_test_suite(res.text)

    def redo_testsuite(self, feedback: str):
        LOGGER.info("Sending feedback for generation of new test suite...")
        res = self.chat.send_message(message="Your generated test suite was analysed. This is the feedback:\n\n"
                                             f"{feedback}\n\nPlease update the test suite accordingly."
                                             f"These are the project file contents:"
                                             f" - lexer.py\n```python\n{self.lex_str}\n```\n"
                                             f" - tokens.py\n```python\n{self.tok_str}\n```\n")
        LOGGER.info("Received updated test suite!")
        self._save_test_suite(res.text)


class TestEvalChat(Chat):
    class EvalResponse(TypedDict):
        score: int
        feedback: str

    def __init__(self, api_key: str, model_name: str):
        sys_prompt = f"""

Your are a software tester, specialized on working with python projects.
I will provide you a project as well as a proposed set of test cases.

The project has the following structure:
{seedir.seedir("project", printout=False)}

You will be provided all files in the src/ folder as well as the test suite in tests.py.
Additionally, I will provide you the output of the execution of the test suite.

It is important that you only analyse errors in the test suite.
Consider the project files to hold the correct behavior!

Please analyse the test suite for completeness and robustness and the execution.
You shall provide an overview whether the test suite is defined well, covers all decision branches and works correctly.

Please include a score from 0 (not working at all) to 100 (the test suite is complete, no improvements possible/needed).
Also provide a written feedback stating what might be wrong in the test suite (functionally like wrong imports or logically like uncovered decisions) in 2 to 10 sentences.

Only answer in JSON format as follows:
{{
    "score": your_score,
    "feedback": your_feedback
}}

        """.strip()

        super().__init__("TS Evaluator", api_key, model_name,
                         types.GenerateContentConfig(system_instruction=sys_prompt,
                                                     response_mime_type="application/json",
                                                     response_schema=self.EvalResponse))

    def analyse_testsuite(self, execution_output: str):
        with open("project/tests.py", "r") as f:
            tests_str = f.read()

        LOGGER.info("Sending test suite analyse request...")
        res = self.chat.send_message(message=execution_output + f"These are the project file contents:\n"
                                                                f" - lexer.py\n```python\n{self.lex_str}\n```\n"
                                                                f" - tokens.py\n```python\n{self.tok_str}\n```\n\n"
                                                                f"This is the content of the test suite:\n"
                                                                f" - tests.py\n```python\n{tests_str}```\n")
        data = json.loads(res.text)
        LOGGER.info("Received response to test suite analyse request!")
        LOGGER.debug("Analyse Score: " + str(data["score"]))
        LOGGER.debug("Analyse Feedback: " + data["feedback"])

        return data


def execute_testsuite():
    LOGGER.info("Starting execution of the generated test suite...")
    execution = subprocess.run(["python", "-m", "unittest"], capture_output=True, text=True, cwd="./project/")
    LOGGER.info("Execution of the generated test suite done!")
    LOGGER.debug("Test suite stdout:\n" + execution.stdout)
    LOGGER.debug("Test suite stderr:\n" + execution.stderr)

    return "The execution of the test suite yielded the following result:\n```\n" + execution.stdout + execution.stderr + "```\n"



if __name__ == "__main__":
    gen_chat = TestGenChat(os.getenv("GEMINI_API_KEY"), MODEL_NAME)
    eval_chat = TestEvalChat(os.getenv("GEMINI_API_KEY"), MODEL_NAME)

    gen_chat.init_testsuite()
    ts_output = execute_testsuite()
    stats = eval_chat.analyse_testsuite(ts_output)

    if stats["score"] > 90:
        LOGGER.info("Initial test suite analysed good enough already! No interation started")
    else:
        for iteration in range(10):
            LOGGER.info(f"+++ START OF ITERATION: {iteration + 1} +++")
            gen_chat.redo_testsuite(stats["feedback"])
            ts_output = execute_testsuite()
            stats = eval_chat.analyse_testsuite(ts_output)

            if stats["score"] > 90:
                LOGGER.info(f"Test suite score of {stats['score']} achieved! Stopping iteration.")
                break
            else:
                LOGGER.info(f"Test suite score of {stats['score']} achieved! Continuing iteration.")

            sleep(5)  # max. 15 requests per min allowed

    del gen_chat, eval_chat
