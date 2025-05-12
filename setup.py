from setuptools import setup, find_packages

setup(
    name="nvidia_sales_agent",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "async-timeout>=4.0.3",
        "python-dotenv>=1.0.0",
    ],
    author="NVIDIA Sales Agent Team",
    author_email="example@example.com",
    description="An intelligent sales agent for NVIDIA products using an agentic architecture",
    keywords="ai, sales, agent, nvidia, gpu",
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "nvidia-agent=main:main",
        ],
    },
)
