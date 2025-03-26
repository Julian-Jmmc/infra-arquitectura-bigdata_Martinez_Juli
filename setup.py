from setuptools import setup, find_packages

setup(
    name="infra-arquitectura-bigdata_Martinez_Juli",
    version="3.0.0",
    author="Julian Jose Martinez Camacho",
    author_email="julian.martinezc@est.iudigital.edu.co",
    description="EA3 Proyecto Integrador: Enriquecimiento de Datos simulando una Plataforma de Big Data en la Nube. 🔍🚀",
    py_modules=["EA3_Enriquecimiento_de_Datos_simulando_una_Plataforma_de_Big_Data_en_la_Nube"],
    install_requires=[
        'requests',
        "pandas",
        "openpyxl"
    ]
)