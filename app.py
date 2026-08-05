import os
import sqlite3
import base64
from datetime import datetime
from functools import wraps

from flask import (
    Flask, render_template_string, request, redirect,
    url_for, session, flash, get_flashed_messages
)

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "lutfen-bu-degeri-heroku-config-vars-icinde-degistir")

# --- AYARLAR ---
# ÖNEMLİ: Bu şifreyi Heroku/Render config vars kısmında ADMIN_PASSWORD olarak
# ayarlaman çok daha güvenli olur. Ayarlamazsan aşağıdaki varsayılan kullanılır.
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "ittihat2026")

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "news.db")

CATEGORIES = [
    "Gündem", "Teknoloji", "Ekonomi", "Bilim & Uzay", "Spor",
    "Çevre", "Kültür & Sanat", "Sağlık", "Otomotiv", "Dünya"
]

# --- İLK KURULUM İÇİN ÖRNEK HABERLER (sadece veritabanı boşsa eklenir) ---
SEED_NEWS = [
    {
        "title": "Yapay Zeka Teknolojilerinde Yeni Dönem: Tıp ve Mühendislikte Devrim",
        "category": "Teknoloji",
        "date": "4 Ağustos 2026",
        "image": "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=800&auto=format&fit=crop",
        "content": (
            "Yapay zeka teknolojilerinde yeni ve heyecan verici bir dönem resmi olarak başlıyor. "
            "Geliştirilen son dil modelleri ve derin öğrenme algoritmaları, özellikle tıp ile mühendislik alanlarında devrim niteliğinde çözümler sunuyor. "
            "Araştırmacılar, bu yeni nesil sistemlerin karmaşık hasta veri setlerini ve genetik haritaları sadece saniyeler içinde yüksek doğrulukla analiz edebildiğini belirtiyor. "
            "Teknoloji dünyasının önde gelen uluslararası isimleri, etik kuralların ve güvenlik önlemlerinin de algoritmalarla aynı hızla gelişmesi gerektiğinin altını çiziyor. "
            "Önümüzdeki aylarda bu gelişmiş teknolojilerin doğrudan entegre edildiği endüstriyel yazılımların piyasaya sürülmesi bekleniyor."
        ),
    },
    {
        "title": "Küresel Piyasalarda Faiz ve Enflasyon Dengesi Yeniden Şekilleniyor",
        "category": "Ekonomi",
        "date": "4 Ağustos 2026",
        "image": "https://images.unsplash.com/photo-1590283603385-17ffb3a7f29f?w=800&auto=format&fit=crop",
        "content": (
            "Küresel enflasyonla mücadele kapsamında dünya genelinde merkez bankalarının aldığı faiz kararları, piyasalarda yön arayışını hızlandırdı. "
            "Özellikle enerji ile gıda tedarik zincirlerinde yaşanan yapısal değişimler, ekonomik dengeleri köklü bir biçimde yeniden şekillendiriyor. "
            "Yatırımcılar belirsizlik ortamında güvenli liman olarak görülen varlıklara yönelirken, borsalarda teknoloji ve sanayi sektörleri bazında belirgin ayrışmalar gözlemleniyor. "
            "Uluslararası finans kuruluşları, önümüzdeki çeyrekte üretim maliyetlerinde kademeli bir dengelenme yaşanabileceğini öngörüyor. "
            "Piyasa aktörleri önümüzdeki hafta açıklanacak olan küresel büyüme ve istihdam verilerini yakından takip ediyor."
        ),
    },
    {
        "title": "Derin Uzayda Yaşam İzleri: Ötegezegenlerin Atmosferi İnceleniyor",
        "category": "Bilim & Uzay",
        "date": "3 Ağustos 2026",
        "image": "https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=800&auto=format&fit=crop",
        "content": (
            "James Webb Uzay Teleskobu, derin uzayda hayat belirtisi olabilecek niteliklere sahip yeni ötegezegenler keşfettiğini duyurdu. "
            "Güneş sistemi dışındaki bu gizemli gezegenlerin atmosferinde su buharı ve karbon bazlı organik moleküllere rastlandığı bildirildi. "
            "Gökbilimciler, bu buluşun evrende yalnız olup olmadığımız sorusuna bilimsel bir yanıt bulmak için bugüne kadarki en güçlü kanıt olduğunu ifade ediyor. "
            "NASA yetkilileri, elde edilen verilerin doğrulanması amacıyla ek spektral gözlemlerin yapılacağını ve projeye ayrılan fonların artırılacağını bildirdi. "
            "Araştırmanın kapsamlı sonuçlarının önümüzdeki günlerde dünyanın önde gelen uluslararası bilim dergilerinde yayınlanması planlanıyor."
        ),
    },
]


# --------------------------------------------------------------------------
# VERİTABANI YARDIMCI FONKSİYONLARI
# --------------------------------------------------------------------------
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS news (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL,
            image TEXT,
            content TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)
    conn.commit()

    # Veritabanı boşsa örnek haberleri ekle (siteyi ilk açtığında boş görünmesin diye)
    count = conn.execute("SELECT COUNT(*) AS c FROM news").fetchone()["c"]
    if count == 0:
        for item in SEED_NEWS:
            conn.execute(
                "INSERT INTO news (title, category, date, image, content, created_at) "
                "VALUES (?, ?, ?, ?, ?, ?)",
                (item["title"], item["category"], item["date"], item["image"],
                 item["content"], datetime.now().isoformat())
            )
        conn.commit()

    conn.close()


init_db()


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("is_admin"):
            return redirect(url_for("admin_login"))
        return f(*args, **kwargs)
    return decorated


def file_to_data_uri(file_storage):
    """Yüklenen dosyayı, veritabanında saklanabilecek bir data-URI string'ine çevirir."""
    if not file_storage or file_storage.filename == "":
        return None
    data = file_storage.read()
    if not data:
        return None
    b64 = base64.b64encode(data).decode("utf-8")
    mimetype = file_storage.mimetype or "image/jpeg"
    return f"data:{mimetype};base64,{b64}"


# --------------------------------------------------------------------------
# ORTAK STİL (site + admin panelinde kullanılıyor)
# --------------------------------------------------------------------------
BASE_STYLE = """
<style>
    body { font-family: 'Inter', sans-serif; background-color: #f8f9fa; color: #212529; }
    .navbar-brand { font-weight: 800; letter-spacing: -0.5px; font-size: 1.6rem; color: #d90429 !important; }
    .hero-section { background: linear-gradient(135deg, #111 0%, #2b2d42 100%); color: white; padding: 4rem 0; margin-bottom: 3rem; }
    .news-card { transition: transform 0.2s, box-shadow 0.2s; border: none; border-radius: 12px; overflow: hidden; height: 100%; }
    .news-card:hover { transform: translateY(-5px); box-shadow: 0 10px 20px rgba(0,0,0,0.08); }
    .news-img { height: 220px; object-fit: cover; background: #e9ecef; }
    .category-badge { background-color: #ef233c; color: white; font-weight: 600; font-size: 0.75rem; padding: 0.4em 0.8em; border-radius: 6px; }
    .section-title { font-weight: 800; margin-bottom: 1.5rem; position: relative; padding-bottom: 0.5rem; }
    .section-title::after { content: ''; position: absolute; bottom: 0; left: 0; width: 60px; height: 4px; background-color: #d90429; border-radius: 2px; }
    .about-box { background: white; padding: 3rem; border-radius: 16px; box-shadow: 0 4px 15px rgba(0,0,0,0.04); }
    .contact-box { background: #2b2d42; color: white; padding: 3rem; border-radius: 16px; }
    footer { background-color: #111; color: #adb5bd; padding: 3rem 0; margin-top: 5rem; }
    .admin-card { background: white; border-radius: 14px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); padding: 2rem; }
    .thumb { width: 70px; height: 50px; object-fit: cover; border-radius: 6px; background: #e9ecef; }
</style>
"""

HEAD = """
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap" rel="stylesheet">
""" + BASE_STYLE


# --------------------------------------------------------------------------
# ANA SİTE ŞABLONU
# --------------------------------------------------------------------------
HOME_TEMPLATE = """
<!DOCTYPE html>
<html lang="tr">
<head>
    """ + HEAD + """
    <title>İttihat Haber | Özgür ve Bağımsız Habercilik</title>
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark sticky-top shadow-sm">
        <div class="container">
            <a class="navbar-brand" href="/">İTTİHAT HABER</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto font-weight-semibold">
                    <li class="nav-item"><a class="nav-link active" href="#haberler">Haberler</a></li>
                    <li class="nav-item"><a class="nav-link" href="#hakkimizda">Hakkımızda</a></li>
                    <li class="nav-item"><a class="nav-link" href="#iletisim">İletişim</a></li>
                </ul>
            </div>
        </div>
    </nav>

    <header class="hero-section text-center">
        <div class="container">
            <h1 class="display-4 fw-bold mb-3">İttihat Haber</h1>
            <p class="lead text-light opacity-75 mx-auto" style="max-width: 700px;">
                Gündemi değiştiren, tarafsız, bağımsız ve özgür haberciliğin dijital merkezi.
            </p>
        </div>
    </header>

    <main class="container">
        <section id="haberler" class="mb-5">
            <h2 class="section-title">Günün Öne Çıkan Haberleri</h2>
            <div class="row g-4 mt-1">
                {% for news in news_list %}
                <div class="col-md-6 col-lg-4">
                    <div class="card news-card shadow-sm">
                        <img src="{{ news.image or 'https://images.unsplash.com/photo-1495020689067-958852a7765e?w=800&auto=format&fit=crop' }}" class="card-img-top news-img" alt="{{ news.title }}">
                        <div class="card-body d-flex flex-column p-4">
                            <div class="d-flex justify-content-between align-items-center mb-2">
                                <span class="category-badge">{{ news.category }}</span>
                                <small class="text-muted">{{ news.date }}</small>
                            </div>
                            <h5 class="card-title fw-bold my-2">{{ news.title }}</h5>
                            <p class="card-text text-secondary mb-4" style="font-size: 0.93rem; line-height: 1.6;">
                                {{ news.content }}
                            </p>
                        </div>
                    </div>
                </div>
                {% else %}
                <p class="text-muted">Henüz haber eklenmemiş.</p>
                {% endfor %}
            </div>
        </section>

        <section id="hakkimizda" class="my-5 pt-4">
            <div class="about-box">
                <h2 class="section-title">Hakkımızda</h2>
                <div class="row mt-4 align-items-center">
                    <div class="col-lg-8">
                        <h4 class="fw-bold mb-3">Biz Özgür ve Bağımsız Bir Haberciyiz</h4>
                        <p class="text-secondary lead fs-6" style="line-height: 1.8;">
                            <strong>İttihat Haber</strong> olarak en büyük ilkemiz, hiçbir gücün veya odağın etkisi altında kalmadan
                            tarafsız, doğru ve <strong>özgür habercilik</strong> yapmaktır.
                        </p>
                    </div>
                    <div class="col-lg-4 text-center mt-4 mt-lg-0">
                        <div class="p-4 bg-light rounded-4 border">
                            <h3 class="fw-bold text-danger mb-1">%100</h3>
                            <p class="mb-0 fw-semibold">Bağımsız & Özgür Medya</p>
                            <hr>
                            <h3 class="fw-bold text-danger mb-1">7/24</h3>
                            <p class="mb-0 fw-semibold">Kesintisiz Gündem Takibi</p>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <section id="iletisim" class="my-5 pt-4">
            <div class="contact-box">
                <div class="row">
                    <div class="col-lg-6 mb-4 mb-lg-0">
                        <h2 class="fw-bold mb-3">Bizimle İletişime Geçin</h2>
                        <p class="opacity-75 mb-4">
                            Görüşleriniz, haber ihbarlarınız veya iş birliği teklifleriniz için bizimle doğrudan iletişime geçebilirsiniz.
                        </p>
                        <div class="d-flex align-items-center mb-3">
                            <div class="bg-danger p-3 rounded-circle me-3"><strong>@</strong></div>
                            <div>
                                <small class="text-uppercase opacity-75 d-block">E-Posta Adresimiz</small>
                                <a href="mailto:ittihathaber@gmail.com" class="text-white fw-bold fs-5 text-decoration-none">ittihathaber@gmail.com</a>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    </main>

    <footer class="text-center">
        <div class="container">
            <h5 class="text-white fw-bold">İTTİHAT HABER</h5>
            <p class="small mb-2">Özgür, Bağımsız ve Tarafsız Dijital Haber Platformu</p>
            <p class="small mb-0 opacity-50">
                &copy; 2026 İttihat Haber. Tüm Hakları Saklıdır. |
                <a href="{{ url_for('admin_login') }}" class="text-white-50">Yönetim Paneli</a>
            </p>
        </div>
    </footer>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"""


# --------------------------------------------------------------------------
# ADMIN ŞABLONLARI
# --------------------------------------------------------------------------
LOGIN_TEMPLATE = """
<!DOCTYPE html>
<html lang="tr">
<head>""" + HEAD + """<title>Yönetim Girişi | İttihat Haber</title></head>
<body>
    <div class="container" style="max-width: 420px; margin-top: 8rem;">
        <div class="admin-card">
            <h3 class="fw-bold mb-4 text-center">Yönetim Paneli Girişi</h3>
            {% if error %}
            <div class="alert alert-danger">{{ error }}</div>
            {% endif %}
            <form method="POST">
                <div class="mb-3">
                    <label class="form-label">Şifre</label>
                    <input type="password" name="password" class="form-control" autofocus required>
                </div>
                <button type="submit" class="btn btn-danger w-100 fw-bold">Giriş Yap</button>
            </form>
            <div class="text-center mt-3">
                <a href="{{ url_for('home') }}" class="text-muted small">&larr; Siteye dön</a>
            </div>
        </div>
    </div>
</body>
</html>
"""

PANEL_TEMPLATE = """
<!DOCTYPE html>
<html lang="tr">
<head>""" + HEAD + """<title>Yönetim Paneli | İttihat Haber</title></head>
<body>
    <nav class="navbar navbar-dark bg-dark mb-4">
        <div class="container">
            <a class="navbar-brand" href="{{ url_for('admin_panel') }}">İTTİHAT HABER — Yönetim</a>
            <div>
                <a href="{{ url_for('home') }}" class="btn btn-sm btn-outline-light me-2">Siteyi Görüntüle</a>
                <a href="{{ url_for('admin_logout') }}" class="btn btn-sm btn-danger">Çıkış Yap</a>
            </div>
        </div>
    </nav>
    <div class="container">
        {% with messages = get_flashed_messages() %}
            {% if messages %}
                {% for m in messages %}
                <div class="alert alert-warning">{{ m }}</div>
                {% endfor %}
            {% endif %}
        {% endwith %}

        <div class="d-flex justify-content-between align-items-center mb-3">
            <h3 class="fw-bold mb-0">Haberler ({{ news_list|length }})</h3>
            <a href="{{ url_for('admin_add') }}" class="btn btn-danger fw-bold">+ Yeni Haber Ekle</a>
        </div>

        <div class="admin-card p-3">
            <table class="table align-middle mb-0">
                <thead>
                    <tr>
                        <th>Görsel</th>
                        <th>Başlık</th>
                        <th>Kategori</th>
                        <th>Tarih</th>
                        <th class="text-end">İşlemler</th>
                    </tr>
                </thead>
                <tbody>
                    {% for news in news_list %}
                    <tr>
                        <td><img class="thumb" src="{{ news.image or 'https://images.unsplash.com/photo-1495020689067-958852a7765e?w=200&auto=format&fit=crop' }}"></td>
                        <td>{{ news.title }}</td>
                        <td><span class="category-badge">{{ news.category }}</span></td>
                        <td>{{ news.date }}</td>
                        <td class="text-end">
                            <a href="{{ url_for('admin_edit', news_id=news.id) }}" class="btn btn-sm btn-outline-secondary">Düzenle</a>
                            <form method="POST" action="{{ url_for('admin_delete', news_id=news.id) }}" style="display:inline;" onsubmit="return confirm('Bu haberi silmek istediğine emin misin?');">
                                <button type="submit" class="btn btn-sm btn-outline-danger">Sil</button>
                            </form>
                        </td>
                    </tr>
                    {% else %}
                    <tr><td colspan="5" class="text-muted text-center py-4">Henüz haber eklenmemiş.</td></tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </div>
</body>
</html>
"""

FORM_TEMPLATE = """
<!DOCTYPE html>
<html lang="tr">
<head>""" + HEAD + """<title>{{ 'Haberi Düzenle' if news else 'Yeni Haber Ekle' }} | İttihat Haber</title></head>
<body>
    <nav class="navbar navbar-dark bg-dark mb-4">
        <div class="container">
            <a class="navbar-brand" href="{{ url_for('admin_panel') }}">İTTİHAT HABER — Yönetim</a>
            <a href="{{ url_for('admin_panel') }}" class="btn btn-sm btn-outline-light">&larr; Listeye Dön</a>
        </div>
    </nav>
    <div class="container" style="max-width: 720px;">
        <div class="admin-card">
            <h3 class="fw-bold mb-4">{{ 'Haberi Düzenle' if news else 'Yeni Haber Ekle' }}</h3>
            <form method="POST" enctype="multipart/form-data">
                <div class="mb-3">
                    <label class="form-label">Başlık</label>
                    <input type="text" name="title" class="form-control" value="{{ news.title if news else '' }}" required>
                </div>
                <div class="row">
                    <div class="col-md-6 mb-3">
                        <label class="form-label">Kategori</label>
                        <select name="category" class="form-select">
                            {% for c in categories %}
                            <option value="{{ c }}" {% if news and news.category == c %}selected{% endif %}>{{ c }}</option>
                            {% endfor %}
                        </select>
                    </div>
                    <div class="col-md-6 mb-3">
                        <label class="form-label">Tarih</label>
                        <input type="text" name="date" class="form-control" placeholder="Örn: 5 Ağustos 2026"
                               value="{{ news.date if news else default_date }}">
                    </div>
                </div>

                <div class="mb-3">
                    <label class="form-label">Fotoğraf Yükle</label>
                    <input type="file" name="image" class="form-control" accept="image/*">
                    {% if news and news.image %}
                    <div class="mt-2">
                        <small class="text-muted d-block mb-1">Mevcut görsel (yeni yüklemezsen bu kalır):</small>
                        <img src="{{ news.image }}" class="thumb" style="width:120px;height:80px;">
                    </div>
                    {% endif %}
                </div>
                <div class="mb-3">
                    <label class="form-label">Ya da Görsel Linki (URL)</label>
                    <input type="text" name="image_url" class="form-control" placeholder="https://... (dosya yüklersen bu alan yok sayılır)">
                </div>

                <div class="mb-3">
                    <label class="form-label">Haber İçeriği</label>
                    <textarea name="content" class="form-control" rows="8" required>{{ news.content if news else '' }}</textarea>
                </div>

                <button type="submit" class="btn btn-danger fw-bold px-4">{{ 'Kaydet' if news else 'Haberi Yayınla' }}</button>
            </form>
        </div>
    </div>
</body>
</html>
"""


# --------------------------------------------------------------------------
# ROTALAR — ANA SİTE
# --------------------------------------------------------------------------
@app.route("/")
def home():
    conn = get_db()
    rows = conn.execute("SELECT * FROM news ORDER BY id DESC").fetchall()
    conn.close()
    return render_template_string(HOME_TEMPLATE, news_list=rows)


# --------------------------------------------------------------------------
# ROTALAR — YÖNETİM PANELİ
# --------------------------------------------------------------------------
@app.route("/admin/giris", methods=["GET", "POST"])
def admin_login():
    error = None
    if request.method == "POST":
        password = request.form.get("password", "")
        if password == ADMIN_PASSWORD:
            session["is_admin"] = True
            return redirect(url_for("admin_panel"))
        error = "Şifre yanlış. Tekrar deneyin."
    return render_template_string(LOGIN_TEMPLATE, error=error)


@app.route("/admin/cikis")
def admin_logout():
    session.pop("is_admin", None)
    return redirect(url_for("admin_login"))


@app.route("/admin")
@login_required
def admin_panel():
    conn = get_db()
    rows = conn.execute("SELECT * FROM news ORDER BY id DESC").fetchall()
    conn.close()
    return render_template_string(PANEL_TEMPLATE, news_list=rows)


@app.route("/admin/ekle", methods=["GET", "POST"])
@login_required
def admin_add():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        category = request.form.get("category", "").strip() or "Gündem"
        date = request.form.get("date", "").strip() or datetime.now().strftime("%d %B %Y")
        content = request.form.get("content", "").strip()

        image_uri = file_to_data_uri(request.files.get("image"))
        if not image_uri:
            image_uri = request.form.get("image_url", "").strip() or None

        if not title or not content:
            flash("Başlık ve içerik alanları zorunludur.")
            return redirect(url_for("admin_add"))

        conn = get_db()
        conn.execute(
            "INSERT INTO news (title, category, date, image, content, created_at) VALUES (?, ?, ?, ?, ?, ?)",
            (title, category, date, image_uri, content, datetime.now().isoformat())
        )
        conn.commit()
        conn.close()
        return redirect(url_for("admin_panel"))

    return render_template_string(
        FORM_TEMPLATE, news=None, categories=CATEGORIES,
        default_date=datetime.now().strftime("%d %B %Y")
    )


@app.route("/admin/duzenle/<int:news_id>", methods=["GET", "POST"])
@login_required
def admin_edit(news_id):
    conn = get_db()
    news = conn.execute("SELECT * FROM news WHERE id = ?", (news_id,)).fetchone()
    if news is None:
        conn.close()
        flash("Haber bulunamadı.")
        return redirect(url_for("admin_panel"))

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        category = request.form.get("category", "").strip() or "Gündem"
        date = request.form.get("date", "").strip()
        content = request.form.get("content", "").strip()

        new_image_uri = file_to_data_uri(request.files.get("image"))
        image_url_field = request.form.get("image_url", "").strip()

        if new_image_uri:
            image_uri = new_image_uri
        elif image_url_field:
            image_uri = image_url_field
        else:
            image_uri = news["image"]

        conn.execute(
            "UPDATE news SET title=?, category=?, date=?, image=?, content=? WHERE id=?",
            (title, category, date, image_uri, content, news_id)
        )
        conn.commit()
        conn.close()
        return redirect(url_for("admin_panel"))

    conn.close()
    return render_template_string(
        FORM_TEMPLATE, news=news, categories=CATEGORIES, default_date=news["date"]
    )


@app.route("/admin/sil/<int:news_id>", methods=["POST"])
@login_required
def admin_delete(news_id):
    conn = get_db()
    conn.execute("DELETE FROM news WHERE id=?", (news_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("admin_panel"))


if __name__ == "__main__":
    app.run(debug=True, port=5000)
