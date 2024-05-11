from flask import Flask, jsonify, request
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from transformers import BertTokenizer, TFBertModel
from database import execute_query  # Importing execute_query function from database.py

app = Flask(__name__)

tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = TFBertModel.from_pretrained('bert-base-uncased')


def get_embeddings(texts, batch_size=32):
    embeddings = []

    for i in range(0, len(texts), batch_size):
        inputs = tokenizer(texts[i:i + batch_size],
                           return_tensors='tf',
                           truncation=True,
                           padding=True)
        outputs = model(inputs)
        batch_embeddings = outputs.last_hidden_state[:, 0, :].numpy()
        embeddings.append(batch_embeddings)

    return np.vstack(embeddings)


@app.route('/match', methods=['POST'])
def match():
    # Use execute_query function to fetch data from the database
    cvs_query = "SELECT * FROM freelancers_cv"
    projects_query = "SELECT * FROM projects"

    cvs_df = pd.DataFrame(execute_query(cvs_query))
    projects_df = pd.DataFrame(execute_query(projects_query))

    project_texts = projects_df['requirements'].tolist()
    project_embeddings = get_embeddings(project_texts)

    cv_texts = cvs_df['cv_text'].tolist()
    cv_embeddings = get_embeddings(cv_texts)

    similarity_scores = cosine_similarity(project_embeddings, cv_embeddings)

    top_cvs = np.argsort(-similarity_scores, axis=1)[:, :5]

    response = []
    for i, project in enumerate(projects_df['project'].tolist()):
        response.append({
            'project':
            project,
            'top_cvs': [cvs_df.iloc[cv_idx]['ID'] for cv_idx in top_cvs[i]]
        })

    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True)
