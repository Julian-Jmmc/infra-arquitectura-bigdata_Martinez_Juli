from setuptools import setup, find_packages

setup(
    name="infra-arquitectura-bigdata_Martinez_Julian",
    version="0.0.1",
    author="Julian Jose Martinez Camacho",
    author_email="julian.martinezc@est.iudigital.edu.co",
    description="EA1 Proyecto integrador: Ingesta de datos desde un API a SQLite y Muestra en Excel.",
    py_modules=["EA1_Ingestión_Datos_API"],
    install_requires=[
        "requests",
        "pandas",
        "openpyxl" 
    ]
)
