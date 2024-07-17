# Deploy a Python (Flask) web app wih Langflow to Azure App Service - Sample Application

(https://docs.microsoft.com/en-us/azure/app-service/quickstart-python ). Para obtener instrucciones sobre cómo crear los recursos de Azure e implementar la aplicación en Azure, consulte el artículo de inicio rápido.
Sample applications are available for the other frameworks here:

1. Preferiblemente usar:
 --> python 3.12
 
2. clonar este repositorio:
--> git clone https://github.com/JsteveO/webapp-langflow-flask.git

3. Preferiblemente utilizar un entorno virtual:
 3.1. crear entorno virtual
 --> python -m venv .venv / python3 -m venv .venv
 3.2. activar entorno virtual
 --> source .venv/bin/activate

4. Instalar requerimientos del la webapp
   Excluir langflow para la instalación de los requerimientos en local. Para realizar push a azure se deja langflow en los requerimientos
   
--> pip install -r requirements

5. Instalar langflow:
 5.1 intentar primero con:
 --> pip install langflow -U
 5.2 solo si no funciona el anterior, desinstalar y reinstalar:
 --> pip uninstall langflow | pip uninstall langflow-base
 --> pip install langflow --pre --force-reinstall

SI SE DE DESEA EDITAR LOS FLUJOS ABRIR LANGFLOW:
 6. abir langflow: 
 --> langflow run / python3 -m langflow run

 7. si se va a modificar o crear un nuevo flujo con una ruta web o archivo diferente, es preferible crear una nueva collecion en astraDB.

 8. crear recurso en Azure y realizar el push. puede seguir los pasos desde la guia:
https://learn.microsoft.com/es-es/azure/app-service/quickstart-python?tabs=flask%2Cwindows%2Cazure-cli%2Cazure-cli-deploy%2Cdeploy-instructions-azportal%2Cterminal-bash%2Cdeploy-instructions-zip-azcli
 
 


