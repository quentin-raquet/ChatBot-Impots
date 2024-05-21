# Chatbot déclaration d'impôts

This project is a Chatbot that uses the Mistral AI model to answer questions about French taxes. It uses a combination of the LangChain library, the Mistral AI model, and the Chroma vector store to process and answer questions.

## Example

Question: "Comment dois-je déclarer des gains issus du Bitcoin ?"

Chatbot answer with RAG: "Si vous avez réalisé des gains à partir de Bitcoin en 2023, vous devez les déclarer en tant que plus-values de cessions d'actifs numériques. Utilisez la déclaration n° 2086 et reportez la plus-value sur la case 3AN et la moins-value sur la case 3BN. Si vous souhaitez être imposé au barème progressif pour ces plus-values, cochez la case 3CN. Assurez-vous de joindre la déclaration n° 3916-3916 bis et de cocher la case 8UU si vous avez géré ces comptes à l'étranger."

Chatbot answer without RAG: "Les gains issus du Bitcoin doivent être déclarés dans la catégorie des plus-values de cession de biens meubles au titre des bénéfices non commerciaux (BNC) si vous êtes un particulier. Vous devez déclarer le montant brut de vos cessions et calculer l'impôt en fonction du barème progressif de l'impôt sur le revenu, après application d'un abattement pour durée de détention. Il est également important de noter que les plateformes d'échange de cryptomonnaies sont tenues de transmettre les informations relatives aux opérations de leurs utilisateurs à l'administration fiscale."


Question: "Dans quelle section dois-je déclarer des bénéfices issus d'une location meublée non professionel ?"

Chatbot answer with RAG: "Vous devez déclarer les bénéfices issus d'une location meublée non professionnelle dans la rubrique dédiée de la déclaration no 2042 C Pro et indiquer également l'adresse de la location principale. Si vous exercez une activité de location meublée saisonnière, ne remplissez pas la ligne « durée de l'exercice »."

Chatbot answer without RAG: "Les bénéfices issus d'une location meublée non professionnelle doivent être déclarés dans la catégorie des bénéfices industriels et commerciaux (BIC). Plus précisément, ils doivent être déclarés dans la section "régime réel" ou "micro-BIC" de la déclaration de revenus, en fonction du montant des recettes locatives."


## Setup

1. Clone the repository to your local machine.
2. Install the required Python packages by running `conda env create -f environment.yml` or `pip install -r requirements.txt` in your terminal.
3. Make sure you have the correct version of SQLite3 installed. If not, follow the instructions in the `requirements.txt` file to fix the issue.
4. Update the `config.yml` file with your specific configuration.

## Running the Project

1. Start the Flask server by running `python app.py` in your terminal.
2. Open your web browser and navigate to `http://localhost:5000` to interact with the chatbot.