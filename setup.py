from setuptools import find_packages, setup

setup(
    name = "mcqgenerator",
    version= "0.0.1",
    author="Tal Giladi",
    install_requirements=["openai", "langchain", "streamlit","python-dotenv","PyPDF2"],
    packages=find_packages()
)