from setuptools import setup, find_packages

with open("requirements.txt") as f:
    install_requires = f.read().strip().split("\n")

setup(
    name="aida_agent_app",
    version="1.0.0",
    description="AIDA AI Agent App for ERPNext - Intelligent onboarding and lead generation",
    author="AIDA AI",
    author_email="support@aida-ai.com",
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=install_requires,
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Framework :: Frappe",
        "Topic :: Office/Business",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
    ],
    keywords="erpnext frappe ai agent onboarding lead-generation",
    project_urls={
        "Documentation": "https://github.com/aida-ai/aida-taskforge-agent",
        "Source": "https://github.com/aida-ai/aida-taskforge-agent",
        "Tracker": "https://github.com/aida-ai/aida-taskforge-agent/issues",
    },
)