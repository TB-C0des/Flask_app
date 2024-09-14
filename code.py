import os
from flask import Flask, request, jsonify
from groq import Groq

# Initialize Groq client
client = Groq(
    api_key="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"
)

# Initialize Flask app
app = Flask(__name__)

# Function to generate the hint
def generate_hint(question, complexity, answer):
    # Define prompt based on complexity
    if complexity == 'Easy':
        prompt = f"Explain the answer to this question briefly, in no more than two sentences:\n\nQuestion: {question}\nAnswer: {answer}"
    elif complexity == 'Medium':
        prompt = f"Provide a brief step-by-step approach to solving this question in no more than two sentences. Do not give the answer directly:\n\nQuestion: {question}\nAnswer: {answer}"
    elif complexity == 'Hard':
        prompt = f"Give a small hint to help the student make progress, but in no more than two sentences. Do not reveal the full answer:\n\nQuestion: {question}\nAnswer: {answer}"
    else:
        raise ValueError("Invalid complexity level! Choose from: Easy, Medium, Hard")
    
    # Call Groq API with the prompt
    completion = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {
                "role": "system",
                "content": prompt
            },
            {
                "role": "user",
                "content": question
            }
        ],
        temperature=1,
        max_tokens=1024,
        top_p=1,
        stream=True,
        stop=None,
    )

    # Aggregate the streamed response
    generated_response = ""
    for chunk in completion:
        generated_response += chunk.choices[0].delta.content or ""
    
    return generated_response

# Flask route to create API endpoint
@app.route('/generate-hint', methods=['POST'])
def generate_hint_endpoint():
    try:
        # Get parameters from the request body (JSON)
        data = request.json
        question = data.get('question')
        complexity = data.get('complexity')
        answer = data.get('answer')

        if not question or not complexity or not answer:
            return jsonify({'error': 'Missing required parameters'}), 400
        
        # Generate the hint using the function
        hint = generate_hint(question, complexity, answer)
        
        # Return the generated hint as a JSON response
        return jsonify({'hint': hint}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Run the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
