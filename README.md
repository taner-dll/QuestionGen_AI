# QuestionGen AI

OpenAI API kullanarak belirli bir ders, konu ve zorluk seviyesine göre çoktan seçmeli sorular üreten FastAPI tabanlı REST API projesi.

## Özellikler

- Yapılandırılmış JSON formatında soru üretimi
- Her soru için tam 5 seçenek
- Soru sayısı için 1-10 arası doğrulama
- Pydantic ile istek ve cevap doğrulama
- OpenAI API hataları için açıklayıcı HTTP cevapları
- Terminal ve dönen dosya loglaması
- Otomatik FastAPI Swagger dokümantasyonu

## Gereksinimler

- Python 3.14 veya üzeri
- OpenAI API anahtarı
- `uv` paket ve ortam yöneticisi

## Kurulum

### Windows

PowerShell ile proje klasörüne geçin:

```powershell
cd "D:\Python Projects\QuestionGen_AI"
```

### Fedora Linux

Python ve geliştirme araçlarını kurun:

```bash
sudo dnf install python3 python3-pip curl
```

`uv` paket yöneticisini kurun:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
source "$HOME/.local/bin/env"
```

Proje klasörüne geçin:

```bash
cd /path/to/QuestionGen_AI
```

> Proje Python 3.14 veya üzeri gerektirir. Fedora sisteminizde bu sürüm mevcut değilse Python 3.14 kurulumu veya uygun bir Python sürüm yöneticisi kullanın.

### Bağımlılıkları Kurma

Windows ve Fedora dahil tüm platformlarda, proje kök dizininde aşağıdaki komutu çalıştırın:

```bash
uv sync
```

## Ortam Değişkeni

Proje kök dizininde `.env` dosyası oluşturun:

```env
OPENAI_API_KEY=your_openai_api_key
```

API anahtarınızı kaynak koduna yazmayın ve Git'e göndermeyin. `.env` dosyası `.gitignore` içinde tanımlıdır.

## Uygulamayı Çalıştırma

### Windows PowerShell

```powershell
uv run uvicorn app.main:app --reload
```

### Fedora Linux

```bash
uv run uvicorn app.main:app --reload
```

API şu adreste çalışır:

```text
http://127.0.0.1:8000
```

Swagger arayüzü:

```text
http://127.0.0.1:8000/docs
```

Alternatif ReDoc arayüzü:

```text
http://127.0.0.1:8000/redoc
```

## Endpoint'ler

### Uygulama Durumu

```http
GET /
```

Örnek cevap:

```json
{
	"message": "Welcome to QuestionGen_AI!"
}
```

### Soru Üretme

```http
POST /generate-questions
Content-Type: application/json
```

İstek gövdesi:

```json
{
	"subject": "Mathematics",
	"topic": "Fractions",
	"difficulty": "easy",
	"questions_count": 2
}
```

Windows PowerShell ile örnek istek:

```powershell
$body = @{
		subject = "Mathematics"
		topic = "Fractions"
		difficulty = "easy"
		questions_count = 2
} | ConvertTo-Json

Invoke-RestMethod `
		-Uri "http://127.0.0.1:8000/generate-questions" `
		-Method Post `
		-ContentType "application/json" `
		-Body $body
```

Fedora Linux veya diğer Unix tabanlı sistemlerde `curl` ile örnek istek:

```bash
curl -X POST "http://127.0.0.1:8000/generate-questions" \
	-H "Content-Type: application/json" \
	-d '{
		"subject": "Mathematics",
		"topic": "Fractions",
		"difficulty": "easy",
		"questions_count": 2
	}'
```

Başarılı cevap örneği:

```json
{
	"questions": [
		{
			"question_text": "What is 1/2 + 1/4?",
			"options": [
				"1/4",
				"1/2",
				"3/4",
				"1",
				"2"
			],
			"correct_answer": "3/4",
			"explanation": "Convert 1/2 to 2/4 and add 1/4 to get 3/4."
		}
	]
}
```

## Hata Cevapları

- `422`: İstek gövdesi Pydantic doğrulamasından geçmedi.
- `502`: OpenAI API isteği başarısız oldu. API anahtarı, kota veya dış servis hatasını kontrol edin.
- `500`: Beklenmeyen sunucu hatası oluştu.

Hata ayrıntıları API cevabında ve sunucu loglarında görülebilir.

## Loglar

Uygulama logları şu dosyada tutulur:

```text
logs/app.log
```

Loglar aynı zamanda terminale yazılır. `app.log` dosyası 5 MB'a ulaştığında döndürülür ve en fazla üç eski log dosyası saklanır.

## Proje Yapısı

```text
QuestionGen_AI/
├── app/
│   ├── main.py                         # FastAPI uygulaması ve endpoint'ler
│   ├── models/
│   │   └── question.py                 # İstek ve cevap modelleri
│   └── services/
│       └── question_generator.py       # OpenAI soru üretme servisi
├── logs/
│   └── app.log                         # Uygulama logları
├── .env                                # Yerel API anahtarı, Git'e gönderilmez
├── pyproject.toml                      # Proje ve bağımlılık tanımları
├── uv.lock                             # Kilitlenmiş bağımlılık sürümleri
└── README.md                           # Proje dokümantasyonu
```

## Geliştirme Kontrolleri

Python dosyalarının sözdizimini kontrol etmek için:

```bash
uv run python -m compileall -q app
```

Uygulamanın import edilebildiğini kontrol etmek için:

```bash
uv run python -c "import app.main; print('app import: OK')"
```
