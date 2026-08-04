from flask import Flask, render_template_string

app = Flask(__name__)

# --- HABER VERİLERİ (Genişletilmiş, En Az 5-6 Cümlelik ve Tanınmış Kişi Alıntılı) ---
NEWS_ITEMS = [
    {
        "id": 1,
        "title": "Yapay Zeka Teknolojilerinde Yeni Dönem: Tıp ve Mühendislikte Devrim",
        "category": "Teknoloji",
        "date": "4 Ağustos 2026",
        "image": "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=800&auto=format&fit=crop",
        "content": (
            "Yapay zeka teknolojilerinde yeni ve heyecan verici bir dönem resmi olarak başlıyor. "
            "Geliştirilen son dil modelleri ve derin öğrenme algoritmaları, özellikle tıp ile mühendislik alanlarında devrim niteliğinde çözümler sunuyor. "
            "Araştırmacılar, bu yeni nesil sistemlerin karmaşık hasta veri setlerini ve genetik haritaları sadece saniyeler içinde yüksek doğrulukla analiz edebildiğini belirtiyor. "
            "Teknoloji dünyasının önde gelen uluslararası isimleri, etik kuralların ve güvenlik önlemlerinin de algoritmalarla aynı hızla gelişmesi gerektiğinin altını çiziyor. "
            "Ünlü teknoloji lideri Sam Altman konuyla ilgili yaptığı açıklamada, 'Yapay zeka insanlığın en büyük ve dönüştürücü araçlarından biri olacak; ancak denetim ve güvenlik mekanizmalarını asla göz ardı edemeyiz' ifadelerini kullandı. "
            "Önümüzdeki aylarda bu gelişmiş teknolojilerin doğrudan entegre edildiği endüstriyel yazılımların piyasaya sürülmesi bekleniyor."
        )
    },
    {
        "id": 2,
        "title": "Küresel Piyasalarda Faiz ve Enflasyon Dengesi Yeniden Şekilleniyor",
        "category": "Ekonomi",
        "date": "4 Ağustos 2026",
        "image": "https://images.unsplash.com/photo-1590283603385-17ffb3a7f29f?w=800&auto=format&fit=crop",
        "content": (
            "Küresel enflasyonla mücadele kapsamında dünya genelinde merkez bankalarının aldığı faiz kararları, piyasalarda yön arayışını hızlandırdı. "
            "Özellikle enerji ile gıda tedarik zincirlerinde yaşanan yapısal değişimler, ekonomik dengeleri köklü bir biçimde yeniden şekillendiriyor. "
            "Yatırımcılar belirsizlik ortamında güvenli liman olarak görülen varlıklara yönelirken, borsalarda teknoloji ve sanayi sektörleri bazında belirgin ayrışmalar gözlemleniyor. "
            "Uluslararası finans kuruluşları, önümüzdeki çeyrekte üretim maliyetlerinde kademeli bir dengelenme yaşanabileceğini öngörüyor. "
            "Ünlü ekonomist Nouriel Roubini gelişmeleri değerlendirerek, 'Küresel ekonomide temkinli ve kırılgan bir iyileşme sürecine giriyoruz, hükümetler mali disiplinden kesinlikle taviz vermemeli' açıklamasında bulundu. "
            "Piyasa aktörleri önümüzdeki hafta açıklanacak olan küresel büyüme ve istihdam verilerini yakından takip ediyor."
        )
    },
    {
        "id": 3,
        "title": "Derin Uzayda Yaşam İzleri: Ötegezegenlerin Atmosferi İnceleniyor",
        "category": "Bilim & Uzay",
        "date": "3 Ağustos 2026",
        "image": "https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=800&auto=format&fit=crop",
        "content": (
            "James Webb Uzay Teleskobu, derin uzayda hayat belirtisi olabilecek niteliklere sahip yeni ötegezegenler keşfettiğini duyurdu. "
            "Güneş sistemi dışındaki bu gizemli gezegenlerin atmosferinde su buharı ve karbon bazlı organik moleküllere rastlandığı bildirildi. "
            "Gökbilimciler, bu buluşun evrende yalnız olup olmadığımız sorusuna bilimsel bir yanıt bulmak için bugüne kadarki en güçlü kanıt olduğunu ifade ediyor. "
            "NASA yetkilileri, elde edilen verilerin doğrulanması amacıyla ek spektral gözlemlerin yapılacağını ve projeye ayrılan fonların artırılacağını bildirdi. "
            "Dünyaca ünlü astrofizikçi Neil deGrasse Tyson, 'Evrenin bize söyleyecek çok sözü var; bu keşif kozmik kimliğimizi ve evrendeki yerimizi anlamamızda bir dönüm noktasıdır' diyerek heyecanını paylaştı. "
            "Araştırmanın kapsamlı sonuçlarının önümüzdeki günlerde dünyanın önde gelen uluslararası bilim dergilerinde yayınlanması planlanıyor."
        )
    },
    {
        "id": 4,
        "title": "Avrupa Futbolunda Taktiksel Devrim ve Yüksek Tempolu Mücadele",
        "category": "Spor",
        "date": "3 Ağustos 2026",
        "image": "https://images.unsplash.com/photo-1508098682722-e99c43a406b2?w=800&auto=format&fit=crop",
        "content": (
            "Avrupa futbolunda yeni sezon heyecanı, taktiksel savaşların ve yüksek fiziksel temponun ön plana çıktığı nefes kesen karşılaşmalarla başladı. "
            "Kıtanın önde gelen elit kulüpleri, kadrolarını dinamik genç yetenekler ve tecrübeli uluslararası yıldızlarla güçlendirerek sahaya indi. "
            "İlk hafta maçlarında sergilenen tempolu oyun anlayışı ve bol gollü mücadeleler, tribünleri dolduran futbolseverlerden tam not aldı. "
            "Spor analistleri ve teknik direktörler, modern futbolda sadece teknik becerinin değil, üst düzey fiziksel dayanıklılığın başarının anahtarı olduğunu belirtiyor. "
            "Ünlü teknik direktör Pep Guardiola maç sonu demecinde, 'Artık kolay maç diye bir kavram kalmadı, her takım sahada fiziksel ve zihinsel olarak en üst seviyede mücadele etmek zorunda' değerlendirmesini yaptı. "
            "Turnuvanın lig aşaması, önümüzdeki haftalarda oynanacak kritik derbiler ve puan mücadeleleriyle kesintisiz devam edecek."
        )
    },
    {
        "id": 5,
        "title": "Yenilenebilir Enerji Üretiminde Tarihi Zirve: Yeşil Dönüşüm Hızlandı",
        "category": "Çevre",
        "date": "2 Ağustos 2026",
        "image": "https://images.unsplash.com/photo-1466611653911-95081537e5b7?w=800&auto=format&fit=crop",
        "content": (
            "İklim değişikliğiyle küresel mücadele kapsamında yenilenebilir enerji yatırımları dünya genelinde tarihi bir rekor seviyeye ulaştı. "
            "Rüzgar ve güneş enerjisi santrallerinin toplam elektrik üretimindeki payı, tarihte ilk kez geleneksel fosil yakıtları geride bıraktı. "
            "Çevre mühendisleri, özellikle gelişmiş batarya ve depolama teknolojilerinde yaşanan sıçramanın enerjide sürekliliği sağladığına dikkat çekiyor. "
            "Hükümetler, net sıfır karbon emisyonu hedefleri doğrultusunda sanayi kuruluşlarına yönelik teşvik paketlerini hızla genişletiyor. "
            "Birleşmiş Milletler Çevre Programı (UNEP) Genel Direktörü Inger Andersen, 'Temiz enerjiye geçiş artık ekonomik bir seçenek değil, gezegenimizin ortak geleceği için tek yoldur' diyerek küresel iş birliği çağrısında bulundu. "
            "Yeşil enerji projelerinin yeni istihdam alanları yaratma konusundaki ekonomik katkısı da her geçen gün daha görünür hale geliyor."
        )
    },
    {
        "id": 6,
        "title": "Uluslararası Film Festivali'nde Bağımsız Yapımların Yükselişi",
        "category": "Kültür & Sanat",
        "date": "2 Ağustos 2026",
        "image": "https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?w=800&auto=format&fit=crop",
        "content": (
            "Bu yıl düzenlenen Uluslararası Film Festivali'nde, büyük bütçeli stüdyo filmlerinin aksine insana ve topluma odaklanan bağımsız yapımlar büyük beğeni topladı. "
            "Dünyanın dört bir yanından gelen yönetmenler; göç, yabancılaşma ve dijital çağda modern insanın yalnızlığı gibi evrensel temaları ustalıkla işledi. "
            "Festival jürisi, özellikle genç senaristlerin cesur, klişelerden uzak ve yenilikçi anlatım dillerini övgüyle karşıladı. "
            "Sinema eleştirmenleri, bağımsız filmlerin dijital yayın platformları sayesinde artık dünya genelinde çok daha geniş kitlelere ulaştığını vurguluyor. "
            "Usta yönetmen Martin Scorsese festivalde yaptığı açılış konuşmasında, 'Sinema sadece boş zamanı eğlendiren bir içerik değil, insanlığın ortak vicdanına ayna tutan en güçlü sanattır' sözleriyle genç sinemacılara ilham verdi. "
            "Ödül kazanan seçkin filmlerin sonbahar aylarında uluslararası sinema salonlarında vizyona girmesi bekleniyor."
        )
    },
    {
        "id": 7,
        "title": "Tıp Dünyasında Yeni Ümit: Akıllı Nano-Taşıyıcılar ve Gen Tedavisi",
        "category": "Sağlık",
        "date": "1 Ağustos 2026",
        "image": "https://images.unsplash.com/photo-1532187863486-abf9dbad1b69?w=800&auto=format&fit=crop",
        "content": (
            "Gen tedavisi ve hücresel yenileme teknolojilerinde elde edilen son biyoteknolojik bulgular, kronik ve kalıcı hastalıkların tedavisinde yeni bir ümit oldu. "
            "Araştırmacılar, laboratuvar ortamında geliştirdikleri akıllı nano-taşıyıcılar sayesinde sağlıklı dokulara zarar vermeden doğrudan hasarlı hücreleri hedefleyebiliyor. "
            "Bu öncü yöntemin özellikle bağışıklık sistemi rahatsızlıkları ve belirli onkolojik vakalarda yüksek başarı oranları sunduğu açıklandı. "
            "Tıp dünyası, yürütülen klinik denemelerin hızlandırılmasıyla geleneksel ve yıpratıcı tedavi süreçlerinin köklü bir biçimde değişeceğini öngörüyor. "
            "Dünya Sağlık Örgütü (WHO) Baş Bilim İnsanı Dr. Jeremy Farrar, 'Biyoteknolojideki bu inovasyon sıçraması, önümüzdeki on yılda modern tıp tarihini yeniden yazabilir' açıklamasını yaptı. "
            "Tedavinin küresel çapta güvenlik ve etkinlik testlerinin tamamlanmasının ardından yaygın sağlık sistemlerine entegre edilmesi hedefleniyor."
        )
    },
    {
        "id": 8,
        "title": "Otomotivde Dönüşüm: Katı Hal Bataryalar ve Otonom Sürüş",
        "category": "Otomotiv",
        "date": "1 Ağustos 2026",
        "image": "https://images.unsplash.com/photo-1552519507-da3b142c6e3d?w=800&auto=format&fit=crop",
        "content": (
            "Yeni nesil elektrikli araçlar, önemli ölçüde uzatılmış batarya menzilleri ve yapay zeka destekli otonom sürüş özellikleri ile sektördeki rekabeti zirveye taşıyor. "
            "Otomotiv devleri, şarj süresini saatlerden dakikalara indiren ve yangın riskini sıfırlayan katı hal batarya teknolojilerini standart hale getirmek için yarışıyor. "
            "Akıllı şehir alt yapılarıyla tam entegre çalışan yeni nesil araçlar, trafik akışını ve enerji tüketimini gerçek zamanlı olarak optimize edebiliyor. "
            "Sektör analistleri, 2030 yılına kadar metropollerdeki bireysel ulaşımın çok büyük bir oranının sıfır emisyonlu akıllı araçlardan oluşacağını öngörüyor. "
            "Tesla CEO'su Elon Musk yeni batarya mimarisi hakkında yaptığı sunumda, 'Sürdürülebilir ulaştırmanın önündeki en büyük psikolojik engel olan menzil kaygısını tarihe gömüyoruz' ifadelerini kullandı. "
            "Tüketicilerin çevre dostu araçlara olan talebi, sağlanan vergi avantajları ve şarj istasyonu ağlarının genişlemesiyle artarak devam ediyor."
        )
    }
]

# --- HTML TEMPLATE ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>İttihat Haber | Özgür ve Bağımsız Habercilik</title>
    <!-- Bootstrap 5 CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <!-- Google Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Inter', sans-serif; background-color: #f8f9fa; color: #212529; }
        .navbar-brand { font-weight: 800; letter-spacing: -0.5px; font-size: 1.6rem; color: #d90429 !important; }
        .hero-section { background: linear-gradient(135deg, #111 0%, #2b2d42 100%); color: white; padding: 4rem 0; margin-bottom: 3rem; }
        .news-card { transition: transform 0.2s, box-shadow 0.2s; border: none; border-radius: 12px; overflow: hidden; height: 100%; }
        .news-card:hover { transform: translateY(-5px); box-shadow: 0 10px 20px rgba(0,0,0,0.08); }
        .news-img { height: 220px; object-fit: cover; }
        .category-badge { background-color: #ef233c; color: white; font-weight: 600; font-size: 0.75rem; padding: 0.4em 0.8em; border-radius: 6px; }
        .section-title { font-weight: 800; margin-bottom: 1.5rem; position: relative; padding-bottom: 0.5rem; }
        .section-title::after { content: ''; position: absolute; bottom: 0; left: 0; width: 60px; height: 4px; background-color: #d90429; border-radius: 2px; }
        .about-box { background: white; padding: 3rem; border-radius: 16px; box-shadow: 0 4px 15px rgba(0,0,0,0.04); }
        .contact-box { background: #2b2d42; color: white; padding: 3rem; border-radius: 16px; }
        footer { background-color: #111; color: #adb5bd; padding: 3rem 0; margin-top: 5rem; }
    </style>
</head>
<body>

    <!-- NAVBAR -->
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

    <!-- HERO SECTION -->
    <header class="hero-section text-center">
        <div class="container">
            <h1 class="display-4 fw-bold mb-3">İttihat Haber</h1>
            <p class="lead text-light opacity-75 mx-auto" style="max-width: 700px;">
                Gündemi değiştiren, tarafsız, bağımsız ve özgür haberciliğin dijital merkezi. Gerçekleri olduğu gibi, en güncel açıklamalarla aktarıyoruz.
            </p>
        </div>
    </header>

    <!-- MAIN CONTENT -->
    <main class="container">
        
        <!-- HABERLER LİSTESİ -->
        <section id="haberler" class="mb-5">
            <h2 class="section-title">Günün Öne Çıkan Haberleri</h2>
            <div class="row g-4 mt-1">
                {% for news in news_list %}
                <div class="col-md-6 col-lg-4">
                    <div class="card news-card shadow-sm">
                        <img src="{{ news.image }}" class="card-img-top news-img" alt="{{ news.title }}">
                        <div class="card-body d-flex flex-column p-4">
                            <div class="d-flex justify-content-between align-items-center mb-2">
                                <span class="category-badge">{{ news.category }}</span>
                                <small class="text-muted">{{ news.date }}</small>
                            </div>
                            <h5 class="card-title fw-bold my-2">{{ news.title }}</h5>
                            <p class="card-text text-secondary mb-4" style="font-size: 0.95rem; line-height: 1.6;">
                                {{ news.content }}
                            </p>
                        </div>
                    </div>
                </div>
                {% end endfor if False else "" %}
                {% for news in news_list %}
                <div class="col-md-6 col-lg-4">
                    <div class="card news-card shadow-sm">
                        <img src="{{ news.image }}" class="card-img-top news-img" alt="{{ news.title }}">
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
                {% endfor %}
            </div>
        </section>

        <!-- HAKKIMIZDA BÖLÜMÜ -->
        <section id="hakkimizda" class="my-5 pt-4">
            <div class="about-box">
                <h2 class="section-title">Hakkımızda</h2>
                <div class="row mt-4 align-items-center">
                    <div class="col-lg-8">
                        <h4 class="fw-bold mb-3">Biz Özgür ve Bağımsız Bir Haberciyiz</h4>
                        <p class="text-secondary lead fs-6" style="line-height: 1.8;">
                            <strong>İttihat Haber</strong> olarak en büyük ilkemiz, hiçbir gücün veya odağın etkisi altında kalmadan 
                            tarafsız, doğru ve <strong>özgür habercilik</strong> yapmaktır. Medya dünyasındaki bilgi kirliliğine karşı 
                            durarak, okurlarımıza sadece teyit edilmiş verileri ve alanında uzman tanınmış kişilerin objektif açıklamalarını sunuyoruz.
                        </p>
                        <p class="text-secondary fs-6" style="line-height: 1.8;">
                            Haberin bir toplumun bilinci olduğuna inanıyor; teknoloji, ekonomi, bilim ve kültür gibi her alanda 
                            sansürsüz, evrensel gazetecilik etik değerlerine bağlı kalarak yayın hayatımızı sürdürüyoruz. 
                            Gerçekleri sorgulayan, araştıran ve halkın doğru bilgiye ulaşma hakkını savunan bağımsız bir yayın organı olmaktan gurur duyuyoruz.
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

        <!-- İLETİŞİM BÖLÜMÜ -->
        <section id="iletisim" class="my-5 pt-4">
            <div class="contact-box">
                <div class="row">
                    <div class="col-lg-6 mb-4 mb-lg-0">
                        <h2 class="fw-bold mb-3">Bizimle İletişime Geçin</h2>
                        <p class="opacity-75 mb-4">
                            Görüşleriniz, haber ihbarlarınız veya iş birliği teklifleriniz için bizimle doğrudan iletişime geçebilirsiniz. 
                            Özgür basının en büyük gücü okurlarıyla kurduğu güçlü bağdır.
                        </p>
                        <div class="d-flex align-items-center mb-3">
                            <div class="bg-danger p-3 rounded-circle me-3">
                                <strong>@</strong>
                            </div>
                            <div>
                                <small class="text-uppercase opacity-75 d-block">E-Posta Adresimiz</small>
                                <a href="mailto:ittihathaber@gmail.com" class="text-white fw-bold fs-5 text-decoration-none">ittihathaber@gmail.com</a>
                            </div>
                        </div>
                    </div>
                    <div class="col-lg-6">
                        <form>
                            <div class="mb-3">
                                <input type="text" class="form-control form-control-lg" placeholder="Adınız Soyadınız" required>
                            </div>
                            <div class="mb-3">
                                <input type="email" class="form-control form-control-lg" placeholder="E-Posta Adresiniz" required>
                            </div>
                            <div class="mb-3">
                                <textarea class="form-control form-control-lg" rows="3" placeholder="Mesajınız veya Haber İhbarınız..." required></textarea>
                            </div>
                            <button type="submit" class="btn btn-danger btn-lg w-100 fw-bold">Mesajı Gönder</button>
                        </form>
                    </div>
                </div>
            </div>
        </section>

    </main>

    <!-- FOOTER -->
    <footer class="text-center">
        <div class="container">
            <h5 class="text-white fw-bold">İTTİHAT HABER</h5>
            <p class="small mb-2">Özgür, Bağımsız ve Tarafsız Dijital Haber Platformu</p>
            <p class="small mb-0 opacity-50">&copy; 2026 İttihat Haber. Tüm Hakları Saklıdır. | İletişim: ittihathaber@gmail.com</p>
        </div>
    </footer>

    <!-- Bootstrap 5 JS -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML_TEMPLATE, news_list=NEWS_ITEMS)

if __name__ == "__main__":
    app.run(debug=True, port=5000)