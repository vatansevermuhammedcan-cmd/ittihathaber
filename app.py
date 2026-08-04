from flask import Flask, render_template_string

app = Flask(__name__)

# Dinamik Altyapı: Haberleri bir liste içinde tutuyoruz
haberler = [
    {
        "id": 1, 
        "baslik": "İttihahaber Canlıya Alındı!", 
        "detay": "Render ve GitHub altyapısı kullanılarak haber sitemiz başarıyla yayına girdi. Artık tüm ziyaretçiler güncel haberlere bu adresten ulaşabilecek."
    },
    {
        "id": 2, 
        "baslik": "Yazılım ve Teknoloji Dünyasındaki Yenilikler", 
        "detay": "Python ve Flask gibi modern web çat arıları ile geliştirilen projeler hız kesmeden büyümeye devam ediyor."
    }
]

@app.route('/')
def ana_sayfa():
    html = """
    <!DOCTYPE html>
    <html lang="tr">
    <head>
        <meta charset="UTF-8">
        <title>İttihahaber - Güncel Haberler</title>
        <!-- Bootstrap CSS (Tasarımı Güçlendir) -->
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body class="bg-light">
        <nav class="navbar navbar-dark bg-dark shadow-sm">
            <div class="container">
                <a class="navbar-brand fw-bold" href="/">İttihahaber</a>
            </div>
        </nav>
        <div class="container mt-5">
            <h2 class="mb-4 text-dark border-bottom pb-2">Son Dakika Manşetler</h2>
            <div class="row">
                {% for haber in haberler %}
                    <div class="col-md-12 mb-3">
                        <div class="card shadow-sm border-0">
                            <div class="card-body">
                                <h4 class="card-title text-danger">{{ haber.baslik }}</h4>
                                <a href="/haber/{{ haber.id }}" class="btn btn-outline-dark btn-sm mt-2">Haberi Oku</a>
                            </div>
                        </div>
                    </div>
                {% endfor %}
            </div>
        </div>
    </body>
    </html>
    """
    return render_template_string(html, haberler=haberler)

@app.route('/haber/<int:id>')
def haber_detay(id):
    # İçerik ve Sayfa Zenginliği: ID'ye göre ilgili haberi buluyoruz
    haber = next((h for h in haberler if h["id"] == id), None)
    if not haber:
        return "Aradığınız haber bulunamadı.", 404

    html = """
    <!DOCTYPE html>
    <html lang="tr">
    <head>
        <meta charset="UTF-8">
        <title>{{ haber.baslik }}</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body class="bg-light">
        <div class="container mt-5" style="max-width: 800px;">
            <a href="/" class="btn btn-secondary mb-4">← Ana Sayfaya Dön</a>
            <div class="card shadow-sm p-4 border-0">
                <h1 class="text-danger mb-3">{{ haber.baslik }}</h1>
                <hr>
                <p class="lead mt-3" style="line-height: 1.8;">{{ haber.detay }}</p>
            </div>
        </div>
    </body>
    </html>
    """
    return render_template_string(html, haber=haber)

if __name__ == '__main__':
    app.run(debug=True)