import os
from dotenv import load_dotenv
from flask import (Flask, redirect, render_template, request,
                   send_from_directory, url_for)
from langflow.load import run_flow_from_json

load_dotenv()

TWEAKS = {
  "ChatInput-f8JNS": {},
  "AstraVectorStoreComponent-bxDzZ": {},
  "ParseData-J2mbw": {},
  "Prompt-HcXo1": {},
  "ChatOutput-9kSDH": {},
  "SplitText-FAo0H": {},
  "AstraVectorStoreComponent-2nxDg": {},
  "OpenAIEmbeddings-zGZqu": {},
  "OpenAIEmbeddings-Q6Kn6": {},
  "OpenAIModel-s8KJW": {},
  "URL-1DR2E": {}
}

TWEAKS2 = {
  "ChatInput-qnwbS": {},
  "AstraVectorStoreComponent-pYhIM": {},
  "ParseData-nUn2x": {},
  "Prompt-2rvHS": {},
  "ChatOutput-QjwS2": {},
  "SplitText-1TiSH": {},
  "AstraVectorStoreComponent-DI7Dh": {},
  "OpenAIEmbeddings-4NHWq": {},
  "OpenAIEmbeddings-THR9U": {},
  "OpenAIModel-YSp6u": {},
  "File-96kbS": {}
}

app = Flask(__name__)


@app.route('/')
def index():
   print('Request for index page received')
   return render_template('home.html')

@app.route('/op')
def index2():
   print('Request for index page received')
   return render_template('hello.html')   

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/web', methods=['POST'])
def web():
    name = request.form.get('name')

    result = run_flow_from_json(flow="webapp/Vector Store RAG.json",
                            input_value=name,
                            fallback_to_env_vars=True, # False by default
                            tweaks=TWEAKS)

    if name:
        print('Request for hello page received with name=%s' % name)
        print(result)
        answer = result[0].outputs[0].results['message'].data['text']
        return render_template('home.html', name = name, answer = answer)
    else:
        print('Request for hello page received with no name or blank name -- redirecting')
        return redirect(url_for('index'))
    
@app.route('/pdf', methods=['POST'])
def pdf():
    name = request.form.get('name')

    result = run_flow_from_json(flow="webapp/Vector PDF.json",
                            input_value=name,
                            fallback_to_env_vars=True, # False by default
                            tweaks=TWEAKS2)

    if name:
        print('Request for hello page received with name=%s' % name)
        print(result)
        answer = result[0].outputs[0].results['message'].data['text']
        return render_template('hello.html', name = name, answer = answer)
    else:
        print('Request for hello page received with no name or blank name -- redirecting')
        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
