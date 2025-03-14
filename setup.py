from setuptools import setup, find_packages

setup(
    name="infra-arquitectura-bigdata_Martinez_Julian",
    version="2.0.0",
    author="Julian Jose Martinez Camacho",
    author_email="julian.martinezc@est.iudigital.edu.co",
    description="EA2 Proyecto Integrador: Preprocesamiento y Limpieza de Datos simulando una Plataforma de Big Data en la Nube. 🔍🚀",
    py_modules=["EA2_Preprocesamiento_Limpieza_Datos_Simulando_Plataforma_BigData_Nube"],
    install_requires=[
        'requests',
        "pandas",
        "openpyxl"
    ]
)