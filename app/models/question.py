from pydantic import BaseModel, Field
# Pydantic model sınıfı ve alan doğrulama yardımcıları içe aktarılır.

# API'ye gönderilecek soru üretme isteğinin veri modeli tanımlanır.
class QuestionGenerateRequest(BaseModel):
    # Soruların ait olduğu ana ders belirtilir.
    subject: str = Field(..., description="The subject for which questions need to be generated.")
    # Soruların üretileceği alt konu belirtilir.
    topic: str
    # Soruların zorluk seviyesi belirtilir.
    difficulty: str
    # İstenen soru sayısı doğrulanır ve sınırlandırılır.
    questions_count: int = Field(
        # Değer gönderilmezse bir soru üretilir.
        default=1,
        # En az bir soru üretilmesi zorunludur.
        ge=1,
        # En fazla on soru üretilmesine izin verilir.
        le=10,
        # Alanın amacı API dokümantasyonunda açıklanır.
        description="Number of questions to generate (between 1 and 10).",
    )
    
class Question(BaseModel):
    # Sorunun metni tutulur.
    question_text: str
    # Beş adet metin seçeneği zorunlu kılınır.
    options: list[str] = Field(min_length=5, max_length=5)
    # Doğru cevabın metni tutulur.
    correct_answer: str
    # Doğru cevabın açıklaması tutulur.
    explanation: str
    

class QuestionGenerateResponse(BaseModel):
    # Üretilen soru nesnelerinden oluşan liste tutulur.
    questions: list[Question]
    