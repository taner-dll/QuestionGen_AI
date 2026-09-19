# Ortam değişkenlerini okuyabilmek için standart os modülü içe aktarılır.
import os
# Proje kök dizinini güvenilir biçimde bulmak için Path sınıfı içe aktarılır.
from pathlib import Path

# .env dosyasını yüklemek için python-dotenv fonksiyonu içe aktarılır.
from dotenv import load_dotenv
# OpenAI istemcisini oluşturmak için OpenAI sınıfı içe aktarılır.
from openai import OpenAI

# İstek ve cevap modelleri servis fonksiyonunun tiplerini belirlemek için içe aktarılır.
from app.models.question import QuestionGenerateRequest, QuestionGenerateResponse

# Bu dosyanın iki üst dizini proje kök dizinini gösterir.
project_root = Path(__file__).resolve().parents[2]
# Proje kökündeki .env dosyası yüklenir ve eski ortam değeri güncellenir.
load_dotenv(project_root / ".env", override=True)

# OpenAI API anahtarı ortam değişkenlerinden alınır.
api_key = os.getenv("OPENAI_API_KEY")
# Anahtar yoksa yapılandırma hatası uygulama başlarken açıkça bildirilir.
if not api_key:
    # Eksik API anahtarını açıklayan hata oluşturulur.
    raise RuntimeError("OPENAI_API_KEY is missing from the project .env file")

# API anahtarı kullanılarak OpenAI istemcisi oluşturulur.
client = OpenAI(api_key=api_key)


# Gelen isteğe göre OpenAI'den yapılandırılmış sorular üreten fonksiyon tanımlanır.
def generate_questions(
    # Doğrulanmış ders, konu, zorluk ve soru sayısı bilgileri alınır.
    request: QuestionGenerateRequest,
    # Fonksiyonun doğrulanmış cevap modeli döndürmesi beklenir.
) -> QuestionGenerateResponse:

    # Modele gönderilecek soru üretme talimatları hazırlanır.
    # İstenen soru sayısı prompt içine yerleştirilir.
    prompt = f"""
Generate {request.questions_count} multiple-choice exam questions.

Subject: {request.subject}
Topic: {request.topic}
Difficulty: {request.difficulty}

Each question must have exactly 5 options in an array of strings.
Only one option must be correct.
Provide a short explanation for the correct answer.
"""

    # Responses API çağrılır ve çıktı Pydantic modeliyle ayrıştırılır.
    response = client.responses.parse(
        # Soru üretiminde kullanılacak model belirlenir.
        model="gpt-5-nano",
        # Hazırlanan prompt modele gönderilir.
        input=prompt,
        # Çıktının beklenen cevap şemasına uyması istenir.
        text_format=QuestionGenerateResponse,
    )

    # Ayrıştırılmış sorular endpoint'e geri döndürülür.
    return response.output_parsed # type: ignore
