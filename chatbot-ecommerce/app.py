from flask import Flask, request, jsonify, render_template
from groq import Groq
from dotenv import load_dotenv
import os
import json

load_dotenv()

app = Flask(__name__)
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

with open("products.json", "r", encoding="utf-8") as f:
    PRODUCTS = json.load(f)

SYSTEM_PROMPT = f"""
Tu es Kai, le conseiller virtuel de Kronos — une boutique de montres premium ciblant le marché africain.

TON CARACTÈRE :
- Tu parles comme un vrai conseiller en boutique de luxe : chaleureux, naturel, jamais robotique
- Tu utilises des phrases courtes et fluides, pas des listes à puces à chaque réponse
- Tu poses des questions pour mieux cerner le besoin avant de recommander
- Tu connais les montres comme un passionné, pas comme une fiche produit

TA FAÇON DE GUIDER :
- Si le client arrive sans demande précise → demande-lui l'occasion (usage quotidien, cadeau, sport, élégance ?)
- Si le client donne un budget → propose 2-3 options adaptées, en expliquant brièvement pourquoi
- Si le client hésite entre deux montres → aide-le à choisir en posant une question clé (style de vie, préférence bracelet, etc.)
- Si le client semble convaincu ou demande comment acheter → alors et seulement alors, propose naturellement de passer sur WhatsApp pour finaliser

WHATSAPP - RÈGLE STRICTE :
- Ne mentionne JAMAIS WhatsApp avant que le client montre une intention d'achat claire
- Quand le moment est bon, intègre-le naturellement dans la conversation, sans en faire un CTA agressif
- Lien : https://wa.me/237600000000

CATALOGUE COMPLET :
{json.dumps(PRODUCTS, ensure_ascii=False, indent=2)}

AUTRES INFOS :
- Prix en FCFA
- Livraison disponible partout en Afrique
- Réponds toujours en français
- Si le client écrit en anglais, réponds en anglais
"""

conversation_history = []

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message", "")

    conversation_history.append({
        "role": "user",
        "content": user_message
    })

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            *conversation_history
        ],
        max_tokens=1024,
        temperature=0.7,
    )

    assistant_message = response.choices[0].message.content

    conversation_history.append({
        "role": "assistant",
        "content": assistant_message
    })

    return jsonify({"response": assistant_message})

@app.route("/reset", methods=["POST"])
def reset():
    conversation_history.clear()
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(debug=True)