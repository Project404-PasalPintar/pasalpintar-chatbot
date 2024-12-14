import os
import csv
from flask import Flask, request, jsonify
from groq import Groq, APIError
from dotenv import load_dotenv
import requests  # Import requests for general exception handling

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Konfigurasi API Key Groq dari environment variables
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise EnvironmentError("GROQ_API_KEY environment variable is not set.")

# Menggunakan 'Groq' untuk instansiasi klien API
client = Groq(api_key=api_key)  # Menggunakan 'Groq' jika 'Client' tidak tersedia

# Membaca file CSV dan memuat data ke dalam dictionary
def load_hukum_data(file_path):
    hukum_data = {}
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            pasal = row['pasal'].strip()
            deskripsi = row['deskripsi'].strip()
            hukum_data[pasal] = deskripsi
    return hukum_data

# Format data menjadi string
def format_hukum_data(hukum_data):
    formatted_data = []
    for pasal, deskripsi in hukum_data.items():
        formatted_data.append(f"Pasal {pasal}: {deskripsi}")
    return "\n".join(formatted_data)

# Load hukum data from CSV file
hukum_data = load_hukum_data('hukum_data.csv')
hukum_knowledge = format_hukum_data(hukum_data)

@app.route("/generate", methods=["POST"])
def chat():
    user_message = request.json.get("prompt", "").lower()

    conversation = [
        {
            "role": "system",
            "content": f"""
                Kamu adalah "PasalPintarAi", AI yang hanya menjawab pertanyaan seputar pasal, hukum dan pemerintah.
                Kamu tidak boleh memberikan jawaban tentang topik lain selain hukum dan pemerintah.
                Jika pertanyaannya tidak terkait dengan pasal atau pemerintah, jawab dengan 'Pertanyaan ini tidak terkait dengan pasal dan pemerintah.'.
                Berikut adalah beberapa pasal dan hukum yang dapat kamu gunakan:
                {hukum_knowledge}
                
                knowledge : Tim Developer PasalPintarAi adolah:
                    1. Alif Suryadi sebagai Machine Learning Engineer dan Backend Engineer. Fakta Menarik: Alif ahli dalam mengembangkan aplikasi semua platfrom.
                    2. Aldi Musneldi sebagai Frontend Engineer. Hanya manusia biasa, yang bisa bekerja keras :)
                    3. Hildiah Khairuniza Sebagai UI/UX Designer dan Support .Lebih diutamakan peran sebagai support
                    4. Dwi Andhara Valkyrie Sebagai UI/UX Designer dan Project Manager. Dia orang seorang wanita pekerja keras dan cantik

            """
        },
        {"role": "user", "content": user_message},
    ]

    try:
        response = client.chat.completions.create(
            messages=conversation,
            model="llama3-70b-8192",  # Ganti dengan model yang sesuai jika perlu
            temperature=0.5,
            max_tokens=1024,
            top_p=1,
            stop=None,
            stream=False,
        )

        response_content = response.choices[0].message.content.strip()
        return jsonify({
            "response": response_content
        })
    
    except APIError as e:  # Gunakan APIError untuk penanganan kesalahan API
        return jsonify({
            "error": f"API request failed: {e.message}"
        }), 400
    except Exception as e:
        return jsonify({"error": f"Terjadi kesalahan: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 8080)))
