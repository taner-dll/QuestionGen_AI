import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

# Loglama işlemlerini kullanabilmek için Python'un standart logging modülü içe aktarılır.
from fastapi import FastAPI, HTTPException
from openai import OpenAIError
# FastAPI uygulaması ve HTTP hata cevapları için gerekli sınıflar içe aktarılır.


from app.models.question import (
# İstek ve cevap gövdelerinde kullanılacak veri modelleri içe aktarılır.
    # Soru üretme isteğinin veri yapısını tanımlar.
    QuestionGenerateRequest,
    # Üretilen soruların cevap yapısını tanımlar.
    QuestionGenerateResponse,
)

from app.services.question_generator import (
# Soru üretme işlemini yapan servis fonksiyonu içe aktarılır.
    # OpenAI üzerinden soru üreten fonksiyon alınır.
    generate_questions,
)

app = FastAPI(
    title="QuestionGen_AI",
    # Uygulamanın dokümantasyonda gösterilecek adı belirlenir.
    description="A FastAPI application for generating questions using AI.",
    # Uygulamanın amacını açıklayan metin belirlenir.
    version="0.1.0",
)

# Proje kök dizini, app klasörünün bir üst dizini olarak belirlenir.
project_root = Path(__file__).resolve().parents[1]
# Log dosyalarının tutulacağı klasör yolu oluşturulur.
log_directory = project_root / "logs"
# Logs klasörü yoksa otomatik olarak oluşturulur.
log_directory.mkdir(exist_ok=True)
# Log dosyasının tam yolu belirlenir.
log_file = log_directory / "app.log"
# Uygulama logları hem terminale hem de dönen log dosyasına yazılır.
logging.basicConfig(
    # INFO ve üzerindeki kayıtların tutulması sağlanır.
    level=logging.INFO,
    # Log satırlarında zaman, seviye, logger adı ve mesaj gösterilir.
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    # Dosyanın büyümesini sınırlamak için dönen dosya yöneticisi kullanılır.
    handlers=[
        # En fazla 5 MB boyutunda app.log tutulur ve üç eski dosya saklanır.
        RotatingFileHandler(
            log_file,
            maxBytes=5 * 1024 * 1024,
            backupCount=3,
            encoding="utf-8",
        ),
        # Geliştirme sırasında logların terminalde de görünmesi sağlanır.
        logging.StreamHandler(),
    ],
)

# Bu modül için log kayıtlarını üretecek logger nesnesi hazırlanır.
logger = logging.getLogger(__name__)


@app.get("/")
    # Uygulamanın çalıştığını belirten karşılama mesajını döndürür.
async def read_root():
    return {"message": "Welcome to QuestionGen_AI!"}


@app.post("/generate-questions", response_model=QuestionGenerateResponse)
        # Doğrulanmış istek soru üretme servisine gönderilir.
def generate_questions_endpoint(request: QuestionGenerateRequest):
    try:
        # Hatanın ayrıntılı traceback bilgisi sunucu loguna yazılır.
        return generate_questions(request)
    except OpenAIError as error:
        logger.exception("OpenAI request failed")
            # OpenAI isteğinin başarısız olduğunu belirten HTTP durum kodu.
        raise HTTPException(
            # Orijinal hata zinciri korunur.
            status_code=502,
            detail=f"OpenAI API request failed: {error}",
        # Beklenmeyen hatanın traceback bilgisi sunucu loguna yazılır.
        ) from error
    except Exception as error:
        logger.exception("Question generation failed")
            # Sunucu tarafında beklenmeyen hata olduğunu belirten durum kodu.
        raise HTTPException(
            # Orijinal hata zinciri korunur.
            status_code=500,
            detail=f"Question generation failed: {error}",
        ) from error
