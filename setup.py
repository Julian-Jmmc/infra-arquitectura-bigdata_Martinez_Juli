from setuptools import setup, find_packages

setup(
    name="infra-arquitectura-bigdata_Alexis_Machado",
    version="0.0.1",
    author="Jhon Alexis Machado Rodriguez",
    author_email="jmachadoa12@gmail.com",
    description="Convierte un JSON a Excel con Pandas y se ejecutará automáticamente con **GitHub Actions**. 🚀",
    py_modules=["EA1_Ingestión_Datos_API"],
    install_requires=[
        "requests",
        "pandas",
        "openpyxl" 
    ]
)