# TestSuiteGen

TestSuiteGen is a tool designed to automate the generation and evaluation of test suites.

## Infrastructure

Initially, the Test Suite Generator will generate a Test Suite.

This suite is executed and the suite itself, the execution results as well as the initial project files are feed into the Test Suite Evaluator.

The Evaluator generates a feedback about the Test Suite (like coverage, robustness and areas to improve).

This feedback is used to generate a new (and improved) Test Suite.

This process is iteratively repeated until a satisfactory Test Suite was generated and no significant improvements are identified. 

<p align="center">
  <img src="infrastructure.svg">
</p>

## Usage

The code was executed using the latest `Python 3.12` version.<br>Please make sure to enter you own Gemini API Key for Google AI Studio in the `.env` file (`GEMINI_API_KEY`).
