import os
from datetime import datetime

from flask import Flask, render_template_string, request, abort

app = Flask(__name__)

# ---------------------------------------------------------------------------
# VERİ: Gerçek bir veritabanı bağlamadan önce basit bir liste ile ilerliyoruz.
# İleride bunu bir DB tablosuna taşımak istersen alan isimlerini aynı tut.
# ---------------------------------------------------------------------------

KATEGORILER = ["Gündem", "Türkiye", "Dünya", "Ekonomi", "Spor", "Teknoloji"]

haberler = [
    {
        "id": 1,
        "baslik": "İttihahaber Canlıya Alındı!",
        "ozet": "Render ve GitHub altyapısı kullanılarak haber sitemiz başarıyla yayına girdi.",
        "detay": "Render ve GitHub altyapısı kullanılarak haber sitemiz başarıyla yayına girdi. "
                 "Artık tüm ziyaretçiler güncel haberlere bu adresten ulaşabilecek. Ekibimiz, "
                 "önümüzdeki dönemde siteye yeni bölümler ve özel haber dosyaları eklemeyi planlıyor.",
        "kategori": "Gündem",
        "tarih": "04 Ağustos 2026",
        "resim": "https://picsum.photos/seed/ittihahaber1/900/500",
        "manset": True,
    },
    {
        "id": 2,
        "baslik": "Yazılım ve Teknoloji Dünyasındaki Yenilikler",
        "ozet": "Python ve Flask gibi modern web çatıları ile geliştirilen projeler hız kesmeden büyüyor.",
        "detay": "Python ve Flask gibi modern web çatıları ile geliştirilen projeler hız kesmeden büyümeye "
                 "devam ediyor. Özellikle küçük ve orta ölçekli haber siteleri için hafif altyapılar tercih "
                 "sebebi olmaya devam ediyor.",
        "kategori": "Teknoloji",
        "tarih": "03 Ağustos 2026",
        "resim": "https://picsum.photos/seed/ittihahaber2/900/500",
        "manset": False,
    },
    {
        "id": 3,
        "baslik": "İstanbul'da Yeni Ulaşım Hattı Hizmete Girdi",
        "ozet": "Şehir içi ulaşımı rahatlatacak yeni hat, yoğun saatlerde yükü hafifletmeyi hedefliyor.",
        "detay": "Yetkililer, yeni hattın günlük binlerce yolcuya hizmet vermesinin beklendiğini açıkladı. "
                 "Projenin çevre ilçelere kademeli olarak genişletilmesi planlanıyor.",
        "kategori": "Türkiye",
        "tarih": "03 Ağustos 2026",
        "resim": "https://picsum.photos/seed/ittihahaber3/900/500",
        "manset": False,
    },
    {
        "id": 4,
        "baslik": "Küresel Piyasalarda Dikkatler Faiz Kararında",
        "ozet": "Yatırımcılar, önümüzdeki hafta açıklanacak faiz kararını yakından takip ediyor.",
        "detay": "Analistler, kararın hem döviz hem de borsa endeksleri üzerinde belirleyici olacağını "
                 "belirtiyor. Piyasalarda temkinli bir bekleyiş hâkim.",
        "kategori": "Ekonomi",
        "tarih": "02 Ağustos 2026",
        "resim": "https://picsum.photos/seed/ittihahaber4/900/500",
        "manset": False,
    },
    {
        "id": 5,
        "baslik": "Milli Takım Hazırlık Maçında Sahne Aldı",
        "ozet": "A Milli Takım, üst düzey bir performansla rakibini mağlup etti.",
        "detay": "Karşılaşmada özellikle ikinci yarıda oyuna hakim olan ekip, taraftarını sevindirdi. "
                 "Teknik direktör, kadro derinliğinden memnun olduğunu ifade etti.",
        "kategori": "Spor",
        "tarih": "02 Ağustos 2026",
        "resim": "https://picsum.photos/seed/ittihahaber5/900/500",
        "manset": False,
    },
    {
        "id": 6,
        "baslik": "Avrupa'da Enerji Politikalarında Yeni Dönem",
        "ozet": "Birlik üyesi ülkeler, ortak enerji stratejisinde yeni adımlar atmaya hazırlanıyor.",
        "detay": "Yetkililer, sürdürülebilir kaynaklara geçişin hızlandırılması yönünde ortak bir yol "
                 "haritası üzerinde çalıştıklarını açıkladı.",
        "kategori": "Dünya",
        "tarih": "01 Ağustos 2026",
        "resim": "https://picsum.photos/seed/ittihahaber6/900/500",
        "manset": False,
    },
]

# ---------------------------------------------------------------------------
# ORTAK STİL: Her iki sayfada da kullanılan CSS tek yerde tutuluyor.
# ---------------------------------------------------------------------------

ORTAK_STIL = """
<style>
:root{
    --red:#C8102E;
    --navy:#0F172A;
    --gold:#D4AF37;
    --bg:#f5f6fa;
}
*{box-sizing:border-box;}
body{
    background:var(--bg);
    font-family:'Inter',sans-serif;
    color:#1f2430;
}
h1,h2,h3,h4,.font-serif{
    font-family:'Playfair Display',serif;
}
a{text-decoration:none;}

/* ---- Üst şerit ---- */
.topbar{
    background:var(--navy);
    color:#cbd5e1;
    font-size:13px;
    padding:6px 0;
    letter-spacing:.3px;
}
.topbar a{color:#cbd5e1;}
.topbar a:hover{color:var(--gold);}

/* ---- Navbar / Masthead ---- */
.masthead{
    background:#fff;
    padding:18px 0 10px;
    text-align:center;
    border-bottom:3px double var(--gold);
}
.masthead .brand{
    font-family:'Playfair Display',serif;
    font-weight:800;
    font-size:40px;
    letter-spacing:1px;
    color:var(--navy);
}
.masthead .brand .star{color:var(--gold);}
.masthead .tagline{
    font-size:13px;
    color:#6b7280;
    letter-spacing:2px;
    text-transform:uppercase;
    margin-top:2px;
}
.navbar-kategori{
    background:var(--red)!important;
}
.navbar-kategori .nav-link{
    color:#fff!important;
    font-weight:600;
    letter-spacing:.4px;
}
.navbar-kategori .nav-link.active{
    color:var(--gold)!important;
    border-bottom:2px solid var(--gold);
}

/* ---- Son dakika şeridi ---- */
.breaking{
    background:#b00020;
    color:#fff;
    padding:9px 0;
    font-weight:600;
    overflow:hidden;
    white-space:nowrap;
    display:flex;
    align-items:center;
}
.breaking .etiket{
    background:var(--navy);
    padding:9px 14px;
    flex-shrink:0;
    letter-spacing:1px;
}
.breaking .kayan-alan{
    overflow:hidden;
    flex:1;
}
.breaking .kayan-alan span{
    display:inline-block;
    padding-left:100%;
    animation:kayan 26s linear infinite;
}
@keyframes kayan{
    0%{transform:translateX(0);}
    100%{transform:translateX(-100%);}
}

/* ---- Kartlar ---- */
.card{
    border:none;
    transition:.3s;
    border-radius:14px;
    overflow:hidden;
    background:#fff;
}
.card:hover{
    transform:translateY(-6px);
    box-shadow:0 15px 35px rgba(0,0,0,.15);
}
.card img{
    height:200px;
    object-fit:cover;
}
.badge-kategori{
    background:var(--red);
    color:#fff;
    font-size:11px;
    letter-spacing:.5px;
    text-transform:uppercase;
}

/* ---- Manşet (öne çıkan haber) ---- */
.manset-card{
    position:relative;
    border-radius:16px;
    overflow:hidden;
    color:#fff;
    min-height:380px;
    display:flex;
    align-items:flex-end;
}
.manset-card img{
    position:absolute;
    inset:0;
    width:100%;
    height:100%;
    object-fit:cover;
    z-index:0;
}
.manset-card .overlay{
    position:relative;
    z-index:1;
    width:100%;
    padding:28px;
    background:linear-gradient(0deg, rgba(15,23,42,.92) 0%, rgba(15,23,42,.1) 100%);
}
.manset-card h2{
    font-size:32px;
    margin-bottom:8px;
}

/* ---- Ayraç ---- */
.osmanli-ayrac{
    border:0;
    border-top:1px solid var(--gold);
    border-bottom:1px solid var(--gold);
    height:4px;
    margin:6px 0 28px;
}

/* ---- Sidebar ---- */
.sidebar-baslik{
    font-family:'Playfair Display',serif;
    font-weight:700;
    border-bottom:2px solid var(--red);
    padding-bottom:8px;
    margin-bottom:16px;
}
.cok-okunan{
    display:flex;
    gap:12px;
    padding:10px 0;
    border-bottom:1px solid #e5e7eb;
}
.cok-okunan .no{
    font-family:'Playfair Display',serif;
    font-size:26px;
    color:var(--gold);
    font-weight:800;
    line-height:1;
}
.cok-okunan a{color:var(--navy);font-weight:600;}
.cok-okunan a:hover{color:var(--red);}

/* ---- Footer ---- */
footer{
    background:var(--navy);
    color:#cbd5e1;
    padding:40px 0 20px;
    margin-top:70px;
}
footer h5{color:#fff;font-family:'Playfair Display',serif;}
footer a{color:#cbd5e1;}
footer a:hover{color:var(--gold);}
footer .alt-cizgi{
    border-top:1px solid #1e293b;
    margin-top:24px;
    padding-top:16px;
    font-size:13px;
    text-align:center;
    color:#64748b;
}
</style>
"""

HEAD_ORTAK = """
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="Türkiye ve dünyadan güncel haberler">
<meta property="og:title" content="İttihahaber">
<meta property="og:description" content="Türkiye ve Dünya Haberleri">
<meta property="og:type" content="website">
<link rel="icon" href="data:,">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Playfair+Display:wght@600;700;800&display=swap" rel="stylesheet">
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
"""

# Üst kısım: topbar + masthead + kategori menüsü + son dakika şeridi.
# {aktif_kategori} her sayfada nav-link'in "active" sınıfını belirlemek için kullanılıyor.
UST_BOLUM = """
<div class="topbar">
    <div class="container d-flex justify-content-between">
        <span>{tarih}</span>
        <span><a href="#">Hakkımızda</a> &nbsp;|&nbsp; <a href="#">İletişim</a></span>
    </div>
</div>

<div class="masthead">
    <a href="/" class="brand">İttihahaber <span class="star">★</span></a>
    <div class="tagline">Fikr-i Hürriyet · Kalem-i Hakikat</div>
</div>

<nav class="navbar navbar-expand-lg navbar-kategori">
    <div class="container">
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#kategoriMenu">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="kategoriMenu">
            <ul class="navbar-nav">
                <li class="nav-item"><a class="nav-link {ana_aktif}" href="/">Ana Sayfa</a></li>
                {kategori_linkleri}
            </ul>
        </div>
    </div>
</nav>

<div class="breaking">
    <div class="etiket">SON DAKİKA</div>
    <div class="kayan-alan"><span>{kayan_basliklar}</span></div>
</div>
"""

ALT_BOLUM = """
<footer>
    <div class="container">
        <div class="row">
            <div class="col-md-4 mb-3">
                <h5>İttihahaber</h5>
                <p>Türkiye ve dünyadan güncel gelişmeleri tarafsız bir bakışla aktarıyoruz.</p>
            </div>
            <div class="col-md-4 mb-3">
                <h5>Kategoriler</h5>
                <p>{footer_kategoriler}</p>
            </div>
            <div class="col-md-4 mb-3">
                <h5>Bizi Takip Edin</h5>
                <p><a href="#">Twitter/X</a> · <a href="#">Instagram</a> · <a href="#">YouTube</a></p>
            </div>
        </div>
        <div class="alt-cizgi">© {yil} İttihahaber — Tüm hakları saklıdır.</div>
    </div>
</footer>
"""


def ust_bolum_render(aktif_kategori=None):
    """Üst bölümü (topbar, masthead, kategori menüsü, kayan şerit) doldurup döndürür."""
    kategori_linkleri = "".join(
        f'<li class="nav-item"><a class="nav-link {"active" if k == aktif_kategori else ""}" '
        f'href="/?kategori={k}">{k}</a></li>'
        for k in KATEGORILER
    )
    kayan_basliklar = "&nbsp;&nbsp;•&nbsp;&nbsp;".join(h["baslik"] for h in haberler)
    return UST_BOLUM.format(
        tarih=datetime.now().strftime("%d.%m.%Y"),
        ana_aktif="active" if aktif_kategori is None else "",
        kategori_linkleri=kategori_linkleri,
        kayan_basliklar=kayan_basliklar,
    )


def alt_bolum_render():
    footer_kategoriler = " · ".join(f'<a href="/?kategori={k}">{k}</a>' for k in KATEGORILER)
    return ALT_BOLUM.format(footer_kategoriler=footer_kategoriler, yil=datetime.now().year)


# ---------------------------------------------------------------------------
# SAYFALAR
# ---------------------------------------------------------------------------

ANA_SAYFA_HTML = """
<!DOCTYPE html>
<html lang="tr">
<head>
    {{ head|safe }}
    <title>İttihahaber - Güncel Haberler</title>
    {{ stil|safe }}
</head>
<body>
    {{ ust_bolum|safe }}

    <div class="container mt-4">
        {% if manset %}
        <a href="/haber/{{ manset.id }}" class="text-decoration-none text-dark">
            <div class="manset-card mb-5">
                <img src="{{ manset.resim }}" alt="{{ manset.baslik }}">
                <div class="overlay">
                    <span class="badge badge-kategori mb-2">{{ manset.kategori }}</span>
                    <h2>{{ manset.baslik }}</h2>
                    <p class="mb-0">{{ manset.ozet }}</p>
                </div>
            </div>
        </a>
        {% endif %}

        <div class="row">
            <div class="col-lg-8">
                <h3 class="font-serif mb-1">{{ baslik_metni }}</h3>
                <hr class="osmanli-ayrac">
                <div class="row">
                    {% for haber in liste %}
                    <div class="col-md-6 mb-4">
                        <a href="/haber/{{ haber.id }}" class="text-decoration-none text-dark">
                            <div class="card shadow-sm h-100">
                                <img src="{{ haber.resim }}" class="w-100" alt="{{ haber.baslik }}">
                                <div class="card-body">
                                    <span class="badge badge-kategori mb-2">{{ haber.kategori }}</span>
                                    <h5 class="card-title">{{ haber.baslik }}</h5>
                                    <p class="card-text text-muted small">{{ haber.ozet }}</p>
                                    <p class="card-text"><small class="text-muted">{{ haber.tarih }}</small></p>
                                </div>
                            </div>
                        </a>
                    </div>
                    {% else %}
                    <p class="text-muted">Bu kategoride henüz haber bulunmuyor.</p>
                    {% endfor %}
                </div>
            </div>

            <div class="col-lg-4">
                <div class="sidebar-baslik">Çok Okunanlar</div>
                {% for haber in cok_okunan %}
                <div class="cok-okunan">
                    <div class="no">{{ loop.index }}</div>
                    <a href="/haber/{{ haber.id }}">{{ haber.baslik }}</a>
                </div>
                {% endfor %}
            </div>
        </div>
    </div>

    {{ alt_bolum|safe }}
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"""

HABER_DETAY_HTML = """
<!DOCTYPE html>
<html lang="tr">
<head>
    {{ head|safe }}
    <title>{{ haber.baslik }}</title>
    {{ stil|safe }}
</head>
<body>
    {{ ust_bolum|safe }}

    <div class="container mt-4">
        <div class="row">
            <div class="col-lg-8">
                <a href="/" class="btn btn-outline-dark btn-sm mb-3">← Ana Sayfaya Dön</a>
                <div class="card shadow-sm border-0">
                    <img src="{{ haber.resim }}" class="w-100" style="max-height:420px;object-fit:cover;" alt="{{ haber.baslik }}">
                    <div class="card-body p-4">
                        <span class="badge badge-kategori mb-2">{{ haber.kategori }}</span>
                        <span class="text-muted small ms-2">{{ haber.tarih }}</span>
                        <h1 class="mt-2 mb-3" style="font-size:32px;">{{ haber.baslik }}</h1>
                        <hr class="osmanli-ayrac">
                        <p class="lead" style="line-height:1.9;">{{ haber.detay }}</p>
                        <div class="mt-4">
                            <span class="text-muted small">Paylaş:</span>
                            <a href="#" class="btn btn-sm btn-outline-secondary ms-2">Twitter/X</a>
                            <a href="#" class="btn btn-sm btn-outline-secondary">WhatsApp</a>
                        </div>
                    </div>
                </div>
            </div>

            <div class="col-lg-4">
                <div class="sidebar-baslik">İlgili Haberler</div>
                {% for h in ilgili %}
                <div class="cok-okunan">
                    <img src="{{ h.resim }}" style="width:64px;height:48px;object-fit:cover;border-radius:6px;">
                    <a href="/haber/{{ h.id }}">{{ h.baslik }}</a>
                </div>
                {% else %}
                <p class="text-muted small">Bu kategoride başka haber yok.</p>
                {% endfor %}
            </div>
        </div>
    </div>

    {{ alt_bolum|safe }}
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"""


@app.route('/')
def ana_sayfa():
    aktif_kategori = request.args.get('kategori')

    if aktif_kategori and aktif_kategori in KATEGORILER:
        liste = [h for h in haberler if h["kategori"] == aktif_kategori]
        manset = None
        baslik_metni = f"{aktif_kategori} Haberleri"
    else:
        manset = next((h for h in haberler if h.get("manset")), haberler[0])
        liste = [h for h in haberler if h["id"] != manset["id"]]
        baslik_metni = "Son Dakika Manşetler"

    cok_okunan = list(reversed(haberler))[:4]

    return render_template_string(
        ANA_SAYFA_HTML,
        head=HEAD_ORTAK,
        stil=ORTAK_STIL,
        ust_bolum=ust_bolum_render(aktif_kategori),
        alt_bolum=alt_bolum_render(),
        manset=manset,
        liste=liste,
        cok_okunan=cok_okunan,
        baslik_metni=baslik_metni,
    )


@app.route('/haber/<int:id>')
def haber_detay(id):
    haber = next((h for h in haberler if h["id"] == id), None)
    if not haber:
        abort(404)

    ilgili = [h for h in haberler if h["kategori"] == haber["kategori"] and h["id"] != id][:3]

    return render_template_string(
        HABER_DETAY_HTML,
        head=HEAD_ORTAK,
        stil=ORTAK_STIL,
        ust_bolum=ust_bolum_render(haber["kategori"]),
        alt_bolum=alt_bolum_render(),
        haber=haber,
        ilgili=ilgili,
    )


@app.errorhandler(404)
def sayfa_bulunamadi(e):
    sablon = f"""
    <!DOCTYPE html>
    <html lang="tr"><head>{HEAD_ORTAK}<title>Haber Bulunamadı</title>{ORTAK_STIL}</head>
    <body>
        {ust_bolum_render()}
        <div class="container mt-5 text-center py-5">
            <h1 class="font-serif">404</h1>
            <p class="text-muted">Aradığınız haber bulunamadı ya da kaldırılmış olabilir.</p>
            <a href="/" class="btn btn-outline-dark mt-3">Ana Sayfaya Dön</a>
        </div>
        {alt_bolum_render()}
    </body></html>
    """
    return sablon, 404


if __name__ == '__main__':
    # Render, PORT ortam değişkenini otomatik atar; yerelde 5000 kullanılır.
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
