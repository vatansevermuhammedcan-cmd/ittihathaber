from flask import Flask, render_template_string

app = Flask(__name__)

# --- HABER VERİTABANI ---
haberler = [
    {
        "id": 1,
        "baslik": "HALISAHA TAKIMININ YENİLMEZLİK SERİSİ 4 MAÇA ÇIKTI",
        "kategori": "Spor",
        "tarih": "04 Ağustos 2026",
        "resim_url": "https://images.unsplash.com/photo-1579952363873-27f3bade9f55?q=80&w=1000&auto=format&fit=crop",
        "ozet": "Kırmızı-Siyahlı fırtına dinmiyor. Takımımız 4. kez yenilgi yüzü görmedi.",
        "icerik": "Dün gece halı saha liginde adeta bir futbol resitali yaşandı. Efsanevi Milan formalarını kuşanan takımımız, sahadan 4. kez yenilgi yüzü görmeden ayrılmayı başardı.<br><br>Maça damga vuran isimlerin başında, rakip defansı ipe dizen ve attığı gollerle şov yapan <b>Yiğit</b> geldi. Kalede ise <b>İlker</b>, adeta etten bir duvar örerek rakibin en net pozisyonlarını mucizevi bir şekilde çıkardı ve galibiyetin mimarlarından oldu. Sahanın her yerinde basmadık yer bırakmayan <b>Muhammet</b> ise hem savunmada hem de hücumda gösterdiği olağanüstü performansla takımın dinamosu olduğunu bir kez daha kanıtladı.<br><br>Hücum hattındaki bitiricilik ve kaledeki efsanevi kurtarışlarla rakibe nefes aldırmayan takım, sahadan net bir skorla ayrılarak gelecek maçlar için rakiplerine gözdağı verdi."
    },
    {
        "id": 2,
        "baslik": "KÜRESEL SİYASETTE DEPREM: İSRAİL VE ÖZGÜR FİLİSTİN ORDUSU'NDAN SURİYE'NİN KUZEYİNDE TARİHİ ANLAŞMA",
        "kategori": "Siyaset",
        "tarih": "04 Ağustos 2026",
        "resim_url": "https://images.unsplash.com/photo-1529107386315-e1a2ed48a620?q=80&w=1000&auto=format&fit=crop",
        "ozet": "Dünya devletlerinin aylardır kapalı kapılar ardında beklediği sürpriz zirve gerçekleşti. Taraflar tarihi bir mutabakata imza attı.",
        "icerik": "Ortadoğu'da kartlar yeniden dağıtılıyor. Uzun süredir dünya başkentlerinde fısıltıyla konuşulan ve Washington'dan Moskova'ya kadar birçok küresel gücün yakından takip ettiği o tarihi an nihayet gerçekleşti. Suriye'nin kuzeyinde gizlilik içinde yürütülen diplomasi trafiği sonuç verdi ve İsrail üst düzey yetkilileri ile Özgür Filistin Ordusu kurmayları, haftalar süren müzakerelerin ardından tarihi bir antlaşmaya imza attı.<br><br>Anlaşmanın tam metni henüz yayınlanmamış olsa da, masada çekilen ve iki tarafın bayraklarının birbirine temas ettiği o sembolik kare, şimdiden 2026 yılına damgasını vurdu."
    },
    {
        "id": 3,
        "baslik": "AVRUPA FUTBOLUNDA DEFANS KRİZİ: YENİ NESİL STOPERLER ARANIYOR",
        "kategori": "Spor",
        "tarih": "03 Ağustos 2026",
        "resim_url": "https://images.unsplash.com/photo-1508344928928-7165b67de128?q=80&w=1000&auto=format&fit=crop",
        "ozet": "Dev kulüpler, veriye dayalı scout ekipleriyle dinamik bek ve stoper arayışına hız verdi.",
        "icerik": "Modern futbolda savunma kurgusu tamamen veri analizi üzerine inşa ediliyor. Özellikle İtalya Serie A ve Fransa Ligue 1 ekipleri; Singo, Semedo ve Agbadou gibi patlayıcı gücü yüksek beklerle, Davinson ve Skriniar gibi oyun kurabilen stoperlerin istatistiklerini mercek altına aldı.<br><br>Teknik direktörler artık sadece savunma yapan değil, topla çıkabilen ve oyunun yönünü değiştirebilen çok yönlü oyunculara milyonlarca euro harcamaya hazır."
    },
    {
        "id": 4,
        "baslik": "YAZILIMCILARIN YENİ GÖZDESİ: VERİTABANI BAĞLANTILI OTOMASYONLAR",
        "kategori": "Teknoloji",
        "tarih": "03 Ağustos 2026",
        "resim_url": "https://images.unsplash.com/photo-1555066931-4365d14bab8c?q=80&w=1000&auto=format&fit=crop",
        "ozet": "Python ve gelişmiş IDE ortamları, veri analizi süreçlerinde çığır açmaya devam ediyor.",
        "icerik": "Büyük veri yönetimi her geçen gün daha da karmaşıklaşırken, yazılım dünyası çözümü Python kütüphanelerinde buluyor. Geliştiriciler, Visual Studio ortamında yazdıkları scriptler sayesinde karmaşık Excel tablolarını saniyeler içinde devasa SQL veritabanlarına entegre etmeyi başarıyor.<br><br>Bu entegrasyonlar, şirketlerin raporlama sürelerini haftalardan dakikalara indirerek sektörde yepyeni bir standart belirliyor."
    },
    {
        "id": 5,
        "baslik": "FİTNESS DÜNYASINDA BİLİMSEL DÖNÜŞÜM: MİLİMETRİK HESAPLAMALAR",
        "kategori": "Yaşam",
        "tarih": "02 Ağustos 2026",
        "resim_url": "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?q=80&w=1000&auto=format&fit=crop",
        "ozet": "Vücut geliştirmede geleneksel yöntemler yerini spesifik antrenman splitlerine bıraktı.",
        "icerik": "Profesyonel vücut geliştirme disiplini artık sadece ağırlık kaldırmaktan ibaret değil. Uzmanlar, haftada 5 gün uygulanan izole kas grubu (split) antrenmanlarının, ancak milimetrik makro hesaplamalarıyla tam verim sağladığını kanıtladı.<br><br>Günlük kalori, protein ve kreatin alımının gramı gramına takip edildiği bu yeni dönem, sporcuların genetik sınırlarını zorlayarak hipertrofiyi (kas büyümesini) maksimize etmesine olanak tanıyor."
    },
    {
        "id": 6,
        "baslik": "İSTANBUL BOĞAZI'NDA ROMANTİZM: AVRUPA YAKASI'NIN GÖZDE MEKANLARI",
        "kategori": "Yaşam",
        "tarih": "02 Ağustos 2026",
        "resim_url": "https://images.unsplash.com/photo-1541336032412-2048a678540d?q=80&w=1000&auto=format&fit=crop",
        "ozet": "Özel günlerini unutulmaz kılmak isteyenler rotasını Boğaz'ın eşsiz ışıklarına çeviriyor.",
        "icerik": "İstanbul'un Avrupa Yakası, özellikle Sevgililer Günü gibi özel tarihlerde romantizmin başkenti olmaya devam ediyor. Bosphorus sularına yansıyan ışıklar eşliğinde yenilen lüks akşam yemekleri, çiftlerin en çok tercih ettiği konseptlerin başında geliyor.<br><br>Şeflerin özel tadım menüleri sunduğu yalı restoranları, aylar öncesinden yapılan rezervasyonlarla tamamen dolmuş durumda."
    }
]

# --- HTML TASARIM ŞABLONLARI ---

base_html = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Evlad-ı Fatihanlar Haber</title>
    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { background-color: #f4f6f9; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
        /* Türk Bayrağı Tasarımlı Navbar */
        .navbar-turk { 
            background-color: #E30A17 !important; /* Gerçek Bayrak Kırmızısı */
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        .navbar-brand {
            color: #ffffff !important;
            font-size: 1.6rem;
            letter-spacing: 1px;
            display: flex;
            align-items: center;
        }
        .ay-yildiz {
            font-size: 2.2rem;
            margin-right: 12px;
            line-height: 1;
        }
        .offcanvas-header-turk {
            background-color: #E30A17;
            color: white;
        }
        
        .carousel-item { height: 450px; background-color: #000; border-radius: 8px; overflow: hidden; }
        .carousel-item img { object-fit: cover; height: 100%; width: 100%; opacity: 0.65; transition: opacity 0.3s; }
        .carousel-item:hover img { opacity: 0.5; }
        .carousel-caption { bottom: 15%; text-shadow: 2px 2px 5px rgba(0,0,0,0.9); }
        .carousel-caption h2 { font-size: 2.5rem; font-weight: 800; }
        
        .news-card { transition: transform 0.2s, box-shadow 0.2s; border-radius: 8px; overflow: hidden; border: none; }
        .news-card:hover { transform: translateY(-5px); box-shadow: 0 10px 20px rgba(0,0,0,0.15) !important; }
        .news-card img { height: 220px; object-fit: cover; }
        .card-title { font-weight: 700; color: #2c3e50; }
        
        .category-badge { background-color: #E30A17; color: white; padding: 5px 10px; font-weight: 600; border-radius: 4px; }
    </style>
</head>
<body>
    
    <!-- YAN MENÜ (OFFCANVAS) -->
    <div class="offcanvas offcanvas-start" tabindex="-1" id="kategoriMenusu" aria-labelledby="kategoriMenusuLabel">
        <div class="offcanvas-header offcanvas-header-turk">
            <h5 class="offcanvas-title fw-bold d-flex align-items-center" id="kategoriMenusuLabel">
                <span class="ay-yildiz fs-4 me-2">☪</span> Menü
            </h5>
            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="offcanvas" aria-label="Close"></button>
        </div>
        <div class="offcanvas-body p-0">
            <div class="list-group list-group-flush">
                <a href="/" class="list-group-item list-group-item-action py-3 fw-bold">🏠 Ana Sayfa</a>
                <a href="/kategori/Siyaset" class="list-group-item list-group-item-action py-3">🌍 Siyaset & Dünya</a>
                <a href="/kategori/Spor" class="list-group-item list-group-item-action py-3">⚽ Spor</a>
                <a href="/kategori/Teknoloji" class="list-group-item list-group-item-action py-3">💻 Teknoloji</a>
                <a href="/kategori/Yaşam" class="list-group-item list-group-item-action py-3">🌿 Yaşam & Sağlık</a>
            </div>
        </div>
    </div>

    <!-- ÜST BAR (NAVBAR) -->
    <nav class="navbar navbar-dark navbar-turk mb-5">
        <div class="container d-flex align-items-center">
            <!-- Hamburger Menü İkonu (3 Çizgi) -->
            <button class="navbar-toggler border-0 shadow-none me-3" type="button" data-bs-toggle="offcanvas" data-bs-target="#kategoriMenusu" aria-controls="kategoriMenusu">
                <span class="navbar-toggler-icon"></span>
            </button>
            
            <!-- Site Başlığı ve Logo -->
            <a class="navbar-brand fw-bold m-0" href="/">
                <span class="ay-yildiz">☪</span>
                EVLAD-I FATİHANLAR HABER
            </a>
        </div>
    </nav>

    <div class="container pb-5">
        {% block content %}{% endblock %}
    </div>

    <footer class="text-center py-4 mt-5 text-muted bg-white border-top">
        <div class="container">
            <p class="mb-0">© 2026 Evlad-ı Fatihanlar Haber. Tüm hakları saklıdır.</p>
        </div>
    </footer>

    <!-- Bootstrap JS -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"""

index_html = base_html.replace("{% block content %}{% endblock %}", """
    <!-- MANŞET ALANI (SLIDER) - Sadece ilk 3 haber döner -->
    <div id="haberManset" class="carousel slide mb-5 shadow-lg rounded" data-bs-ride="carousel">
        <div class="carousel-indicators">
            {% for haber in haberler[:3] %}
            <button type="button" data-bs-target="#haberManset" data-bs-slide-to="{{ loop.index0 }}" {% if loop.index0 == 0 %}class="active"{% endif %}></button>
            {% endfor %}
        </div>
        <div class="carousel-inner rounded">
            {% for haber in haberler[:3] %}
            <div class="carousel-item {% if loop.index0 == 0 %}active{% endif %}">
                <img src="{{ haber.resim_url }}" class="d-block w-100" alt="Haber Görseli">
                <div class="carousel-caption d-none d-md-block">
                    <span class="category-badge mb-3 d-inline-block">{{ haber.kategori }}</span>
                    <h2>{{ haber.baslik }}</h2>
                    <p class="fs-5 mb-4">{{ haber.ozet }}</p>
                    <a href="/haber/{{ haber.id }}" class="btn btn-light text-danger fw-bold px-4 py-2 rounded-pill">Haberi Oku &rarr;</a>
                </div>
            </div>
            {% endfor %}
        </div>
        <button class="carousel-control-prev" type="button" data-bs-target="#haberManset" data-bs-slide="prev">
            <span class="carousel-control-prev-icon"></span>
        </button>
        <button class="carousel-control-next" type="button" data-bs-target="#haberManset" data-bs-slide="next">
            <span class="carousel-control-next-icon"></span>
        </button>
    </div>

    <!-- HABER LİSTESİ (KARTLAR) - Tüm haberler burada listelenir -->
    <div class="d-flex align-items-center mb-4 border-bottom pb-2">
        <h3 class="fw-bold text-dark m-0">Son Dakika Gelişmeleri</h3>
    </div>
    <div class="row">
        {% for haber in haberler %}
        <div class="col-lg-4 col-md-6 mb-4">
            <div class="card h-100 shadow-sm news-card">
                <div class="position-relative">
                    <img src="{{ haber.resim_url }}" class="card-img-top" alt="...">
                    <span class="position-absolute top-0 start-0 m-3 category-badge" style="font-size: 0.8rem;">{{ haber.kategori }}</span>
                </div>
                <div class="card-body">
                    <h5 class="card-title">{{ haber.baslik }}</h5>
                    <p class="card-text text-muted" style="font-size: 0.95em;">{{ haber.ozet }}</p>
                </div>
                <div class="card-footer bg-white border-0 text-end pb-3">
                    <a href="/haber/{{ haber.id }}" class="btn btn-outline-danger btn-sm px-3 fw-bold">Devamını Oku</a>
                </div>
            </div>
        </div>
        {% endfor %}
    </div>
""")

detay_html = base_html.replace("{% block content %}{% endblock %}", """
    <div class="row justify-content-center">
        <div class="col-lg-9 bg-white p-5 rounded shadow-sm">
            <nav aria-label="breadcrumb">
                <ol class="breadcrumb">
                    <li class="breadcrumb-item"><a href="/" class="text-decoration-none text-danger fw-bold">Ana Sayfa</a></li>
                    <li class="breadcrumb-item"><a href="/kategori/{{ haber.kategori }}" class="text-decoration-none text-danger fw-bold">{{ haber.kategori }}</a></li>
                </ol>
            </nav>
            <h1 class="fw-bold mb-4 text-dark" style="font-size: 2.5rem;">{{ haber.baslik }}</h1>
            <div class="d-flex justify-content-between text-muted mb-4 border-bottom pb-3">
                <span><i class="bi bi-calendar"></i> {{ haber.tarih }}</span>
                <span class="badge bg-secondary p-2">{{ haber.kategori }}</span>
            </div>
            <img src="{{ haber.resim_url }}" class="img-fluid rounded mb-5 shadow-sm" alt="Haber Görseli" style="width: 100%; max-height: 550px; object-fit: cover;">
            <p class="lead fw-bold text-dark fs-4 mb-4" style="border-left: 4px solid #E30A17; padding-left: 15px;">{{ haber.ozet }}</p>
            <div class="fs-5 text-dark" style="line-height: 1.9; text-align: justify;">
                {{ haber.icerik|safe }}
            </div>
        </div>
    </div>
""")

# --- FLASK YÖNLENDİRİCİLER (ROUTES) ---

@app.route('/')
def ana_sayfa():
    return render_template_string(index_html, haberler=haberler)

@app.route('/haber/<int:haber_id>')
def haber_detay(haber_id):
    secilen_haber = next((h for h in haberler if h["id"] == haber_id), None)
    if secilen_haber:
        return render_template_string(detay_html, haber=secilen_haber)
    return "<div class='container text-center mt-5'><h1 class='fw-bold'>404</h1><h3>Haber bulunamadı!</h3><a href='/' class='btn btn-danger mt-3'>Ana Sayfaya Dön</a></div>", 404

@app.route('/kategori/<kategori_adi>')
def kategori_goster(kategori_adi):
    filtrelenmis_haberler = [h for h in haberler if h["kategori"].lower() == kategori_adi.lower()]
    html = base_html.replace("{% block content %}{% endblock %}", """
        <div class="d-flex align-items-center mb-4 border-bottom pb-2">
            <h3 class="fw-bold text-dark m-0"><span style="color: #E30A17;">{{ kategori_adi }}</span> Kategorisindeki Haberler</h3>
        </div>
        <div class="row">
            {% for haber in haberler %}
            <div class="col-lg-4 col-md-6 mb-4">
                <div class="card h-100 shadow-sm news-card">
                    <img src="{{ haber.resim_url }}" class="card-img-top" alt="...">
                    <div class="card-body">
                        <h5 class="card-title">{{ haber.baslik }}</h5>
                        <p class="card-text text-muted" style="font-size: 0.95em;">{{ haber.ozet }}</p>
                    </div>
                    <div class="card-footer bg-white border-0 text-end pb-3">
                        <a href="/haber/{{ haber.id }}" class="btn btn-outline-danger btn-sm px-3 fw-bold">Devamını Oku</a>
                    </div>
                </div>
            </div>
            {% else %}
            <div class="col-12 text-center py-5">
                <h4 class="text-muted">Bu kategoride henüz haber yayınlanmadı.</h4>
                <a href="/" class="btn btn-outline-danger mt-3">Ana Sayfaya Dön</a>
            </div>
            {% endfor %}
        </div>
    """)
    return render_template_string(html, haberler=filtrelenmis_haberler, kategori_adi=kategori_adi.capitalize())