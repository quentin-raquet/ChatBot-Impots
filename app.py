import yaml
from flask import Flask, request, jsonify
from flask import render_template
from flask_cors import CORS
from src.RAG import build_rag
from src.vectorstore import build_vectorstore

app = Flask(__name__)
CORS(app)

# Load the configuration and build the RAG

with open("config.yml", "r") as f:
    config = yaml.safe_load(f)

build_vectorstore(config)
rag_chain = build_rag(config)

@app.route("/")
def main():
   return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    question = data.get("question")
    if question:
        answer = rag_chain.invoke(question)
        return jsonify({"answer": answer})
    else:
        return jsonify({"error": "No question provided"}), 400


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
