const supportedLangs = {
  en: "English",
  ar: "العربية",
  fr: "Français",
  es: "Español"
};

const translations = {
  site_title: {
    en: "NeuronForge AI", ar: "نيورون فورج AI", fr: "NeuronForge IA", es: "NeuronForge IA"
  },
  nav_home: {
    en: "Home", ar: "الرئيسية", fr: "Accueil", es: "Inicio"
  },
  nav_dashboard: {
    en: "Dashboard", ar: "لوحة التحكم", fr: "Tableau de bord", es: "Panel"
  },
  nav_products: {
    en: "Products", ar: "المنتجات الرقمية", fr: "Produits", es: "Productos"
  },
  nav_content: {
    en: "Content", ar: "مركز المحتوى", fr: "Contenu", es: "Centro de contenido"
  },
  nav_assistant: {
    en: "Your AI Assistant", ar: "مساعدك الذكي", fr: "Assistant IA", es: "Asistente IA"
  },
  nav_contact: {
    en: "Contact", ar: "تواصل معنا", fr: "Contact", es: "Contacto"
  },
  hero_title: {
    en: "Build smarter, faster, and autonomously.",
    ar: "ابنِ مستقبلًا أذكى، أسرع، وذاتياً.",
    fr: "Construisez plus intelligemment, plus rapidement et de manière autonome.",
    es: "Construye más inteligente, más rápido y de forma autónoma."
  },
  hero_desc: {
    en: "NeuronForge AI is your automated digital company that generates content, sells products, and manages your business—intelligently.",
    ar: "نيورون فورج AI هي شركتك الرقمية الذكية التي تنشئ المحتوى وتبيع المنتجات وتدير أعمالك... بذكاء.",
    fr: "NeuronForge IA est votre entreprise numérique automatisée qui génère du contenu, vend des produits et gère votre activité intelligemment.",
    es: "NeuronForge IA es tu empresa digital automatizada que genera contenido, vende productos y gestiona tu negocio de forma inteligente."
  },
  cta_start: {
    en: "Get Started", ar: "ابدأ الآن", fr: "Commencer", es: "Empezar"
  },
  feature_tools_title: {
    en: "AI Tools", ar: "أدوات الذكاء الاصطناعي", fr: "Outils IA", es: "Herramientas IA"
  },
  feature_tools_desc: {
    en: "Automated generators for ideas, books, posts, and more.",
    ar: "مولدات تلقائية للافكار والكتب والمنشورات والمزيد.",
    fr: "Générateurs automatiques pour idées, livres, publications et plus.",
    es: "Generadores automáticos de ideas, libros, publicaciones y más."
  },
  feature_products_title: {
    en: "Digital Products", ar: "المنتجات الرقمية", fr: "Produits numériques", es: "Productos digitales"
  },
  feature_products_desc: {
    en: "Sell smart books, guides, and services on autopilot.",
    ar: "بيع كتب وأدلة ذكية وخدمات دون تدخل.",
    fr: "Vendez des livres, guides et services intelligents en mode automatique.",
    es: "Vende libros, guías y servicios inteligentes de forma automática."
  },
  feature_assistant_title: {
    en: "Your AI Assistant", ar: "مساعد ذكي خاص بك", fr: "Votre assistant IA", es: "Tu asistente IA"
  },
  feature_assistant_desc: {
    en: "Your executive AI that helps you run and grow your business.",
    ar: "مساعدك التنفيذي الذكي لإدارة شركتك وتوسيعها.",
    fr: "Votre assistant IA exécutif qui vous aide à gérer et développer votre entreprise.",
    es: "Tu asistente ejecutivo IA que te ayuda a gestionar y hacer crecer tu negocio."
  },

  dashboard_title: {
    en: "NeuronForge AI - Dashboard", ar: "لوحة تحكم NeuronForge AI", fr: "NeuronForge IA - Tableau de bord", es: "NeuronForge IA - Panel"
  },
  dashboard_reports: {
    en: "Performance Reports", ar: "تقارير الأداء", fr: "Rapports de performance", es: "Informes de rendimiento"
  },
  dashboard_visitors: {
    en: "Visitors Today", ar: "الزوار اليوم", fr: "Visiteurs aujourd'hui", es: "Visitantes hoy"
  },
  dashboard_subscribers: {
    en: "Subscribers", ar: "عدد المشتركين", fr: "Abonnés", es: "Suscriptores"
  },
  dashboard_sales: {
    en: "Products Sold", ar: "المنتجات المباعة", fr: "Produits vendus", es: "Productos vendidos"
  },
  dashboard_revenue: {
    en: "Total Revenue", ar: "الإيرادات الإجمالية", fr: "Revenus totaux", es: "Ingresos totales"
  },
  dashboard_quick_commands: {
    en: "Quick Commands", ar: "أوامر سريعة", fr: "Commandes rapides", es: "Comandos rápidos"
  },
  dashboard_btn_content: {
    en: "Generate New Content", ar: "توليد محتوى جديد", fr: "Générer un nouveau contenu", es: "Generar nuevo contenido"
  },
  dashboard_btn_book: {
    en: "Create PDF Book", ar: "إنشاء كتاب PDF", fr: "Créer un livre PDF", es: "Crear libro PDF"
  },
  dashboard_btn_posts: {
    en: "Create Social Media Posts", ar: "إنشاء منشورات للسوشيال ميديا", fr: "Créer des publications sur les réseaux sociaux", es: "Crear publicaciones para redes sociales"
  },
  dashboard_btn_video: {
    en: "Generate Video", ar: "توليد فيديو تلقائي", fr: "Générer une vidéo", es: "Generar video"
  },
  dashboard_output: {
    en: "Command Results", ar: "نتائج الأوامر", fr: "Résultats des commandes", es: "Resultados de los comandos"
  },
  dashboard_output_wait: {
    en: "Press a button to start", ar: "اضغط زر لتبدأ", fr: "Appuyez sur un bouton pour commencer", es: "Presiona un botón para comenzar"
  },
  dashboard_social_accounts: {
    en: "Social Media Accounts", ar: "حسابات السوشيال ميديا", fr: "Comptes réseaux sociaux", es: "Cuentas de redes sociales"
  },
  connect_twitter: { en: "Connect Twitter", ar: "ربط تويتر", fr: "Connecter Twitter", es: "Conectar Twitter" },
  connect_instagram: { en: "Connect Instagram", ar: "ربط إنستغرام", fr: "Connecter Instagram", es: "Conectar Instagram" },
  connect_facebook: { en: "Connect Facebook", ar: "ربط فيسبوك", fr: "Connecter Facebook", es: "Conectar Facebook" },
  schedule_post: { en: "Schedule Post", ar: "جدولة المنشور", fr: "Programmer la publication", es: "Programar publicación" },
  btn_schedule: { en: "Schedule", ar: "جدولة", fr: "Programmer", es: "Programar" },

  assistant_title: {
    en: "Your AI Assistant", ar: "مساعدك الذكي", fr: "Assistant IA", es: "Asistente IA"
  },
  assistant_subtitle: {
    en: "Talk to your executive assistant", ar: "تحدث مع مساعدك التنفيذي", fr: "Parlez à votre assistant exécutif", es: "Habla con tu asistente ejecutivo"
  },
  assistant_input_placeholder: {
    en: "Type your request...", ar: "اكتب طلبك هنا...", fr: "Tapez votre demande...", es: "Escribe tu solicitud..."
  },
  assistant_btn_send: {
    en: "Send", ar: "إرسال", fr: "Envoyer", es: "Enviar"
  },
  assistant_response_title: {
    en: "Response:", ar: "الرد:", fr: "Réponse :", es: "Respuesta:"
  },
  assistant_response_wait: {
    en: "Waiting for response...", ar: "انتظر الرد...", fr: "En attente de réponse...", es: "Esperando respuesta..."
  }
};

let currentLang = localStorage.getItem("lang") || "en";

function buildLangSelector() {
  const select = document.getElementById("toggleLang");
  select.innerHTML = "";
  Object.entries(supportedLangs).forEach(([key, label]) => {
    const option = document.createElement("option");
    option.value = key;
    option.textContent = label;
    select.appendChild(option);
  });
  select.value = currentLang;
  select.onchange = function () {
    currentLang = this.value;
    localStorage.setItem("lang", currentLang);
    updateLanguage();
  };
}

function updateLanguage() {
  document.querySelectorAll("[data-i18n]").forEach(el => {
    const key = el.getAttribute("data-i18n");
    el.textContent = translations[key] && translations[key][currentLang] ? translations[key][currentLang] : "";
  });
  document.querySelectorAll("[data-i18n-placeholder]").forEach(el => {
    const key = el.getAttribute("data-i18n-placeholder");
    el.placeholder = translations[key] && translations[key][currentLang] ? translations[key][currentLang] : "";
  });

  document.body.dir = (currentLang === "ar" ? "rtl" : "ltr");
  document.documentElement.lang = currentLang;
}

window.onload = function () {
  buildLangSelector();
  updateLanguage();
};