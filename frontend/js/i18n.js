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
  nav_home: { en: "Home", ar: "الرئيسية", fr: "Accueil", es: "Inicio" },
  nav_dashboard: { en: "Dashboard", ar: "لوحة التحكم", fr: "Tableau de bord", es: "Panel" },
  nav_assistant: { en: "AI Assistant", ar: "المساعد الذكي", fr: "Assistant IA", es: "Asistente IA" },
  hero_title: {
    en: "Build smarter, faster, and autonomously.",
    ar: "ابنِ مستقبلًا أذكى، أسرع، وذاتياً.",
    fr: "Construisez plus intelligemment, plus rapidement et de manière autonome.",
    es: "Construye más inteligente, más rápido y de forma autónoma."
  },
  hero_desc: {
    en: "NeuronForge AI is an open-source automation toolkit that discovers trends, writes scripts, produces videos, and publishes to YouTube — on a schedule.",
    ar: "نيورون فورج AI هو نظام أوتوماتيك مفتوح المصدر يكتشف الترندات ويكتب السكريبتات وينتج الفيديوهات وينشرها على يوتيوب — حسب جدول زمني.",
    fr: "NeuronForge IA est une boîte à outils open-source qui découvre les tendances, rédige des scripts, produit des vidéos et publie sur YouTube selon un calendrier.",
    es: "NeuronForge IA es un conjunto de herramientas de código abierto que descubre tendencias, escribe guiones, produce vídeos y publica en YouTube según un calendario."
  },
  cta_start: { en: "Open Dashboard", ar: "افتح لوحة التحكم", fr: "Ouvrir le tableau de bord", es: "Abrir panel" },
  feature_tools_title: { en: "Trend Discovery", ar: "اكتشاف الترندات", fr: "Découverte de tendances", es: "Descubrimiento de tendencias" },
  feature_tools_desc: {
    en: "Pulls trending topics from Google Trends, Reddit, and YouTube RSS — all free.",
    ar: "يجلب المواضيع الرائجة من Google Trends و Reddit و YouTube RSS — كلها مجانية.",
    fr: "Récupère les tendances depuis Google Trends, Reddit et YouTube RSS — tout gratuit.",
    es: "Obtiene temas de tendencia de Google Trends, Reddit y YouTube RSS — todo gratis."
  },
  feature_products_title: { en: "Video Factory", ar: "مصنع الفيديو", fr: "Usine de vidéos", es: "Fábrica de vídeos" },
  feature_products_desc: {
    en: "Scripts via LLM, free Edge TTS narration, stock footage, captions, FFmpeg assembly.",
    ar: "سكريبتات من LLM وصوت مجاني بـ Edge TTS ومقاطع ستوك وتسميات توضيحية ودمج بـ FFmpeg.",
    fr: "Scripts via LLM, narration gratuite Edge TTS, séquences de stock, sous-titres, montage FFmpeg.",
    es: "Guiones vía LLM, narración gratuita Edge TTS, metraje de stock, subtítulos, montaje FFmpeg."
  },
  feature_assistant_title: { en: "Auto Upload", ar: "رفع تلقائي", fr: "Téléversement auto", es: "Subida automática" },
  feature_assistant_desc: {
    en: "Publishes to YouTube via the official API, schedules runs, tracks what's been posted.",
    ar: "ينشر على يوتيوب عبر الـ API الرسمي ويجدول التشغيل ويتتبع ما تم نشره.",
    fr: "Publie sur YouTube via l'API officielle, planifie l'exécution et suit ce qui a été publié.",
    es: "Publica en YouTube vía la API oficial, programa ejecuciones y rastrea lo publicado."
  },

  dashboard_title: { en: "NeuronForge AI - Dashboard", ar: "لوحة تحكم NeuronForge AI", fr: "NeuronForge IA - Tableau de bord", es: "NeuronForge IA - Panel" },
  dashboard_api_status: { en: "Backend Status", ar: "حالة الخلفية", fr: "État du backend", es: "Estado del backend" },
  dashboard_channels: { en: "Configured Channels", ar: "القنوات المُعدّة", fr: "Chaînes configurées", es: "Canales configurados" },
  dashboard_quick_commands: { en: "Manual Run", ar: "تشغيل يدوي", fr: "Exécution manuelle", es: "Ejecución manual" },
  dashboard_select_channel: { en: "Channel:", ar: "القناة:", fr: "Chaîne :", es: "Canal:" },
  dashboard_btn_run_now: { en: "Generate & Upload", ar: "ولّد وانشر", fr: "Générer et publier", es: "Generar y publicar" },
  dashboard_btn_dry_run: { en: "Dry Run (no upload)", ar: "تشغيل تجريبي (بدون نشر)", fr: "Test (sans publication)", es: "Prueba (sin publicar)" },
  dashboard_recent_runs: { en: "Recent Runs", ar: "آخر عمليات التشغيل", fr: "Exécutions récentes", es: "Ejecuciones recientes" },
  dashboard_output: { en: "Output Log", ar: "سجل المخرجات", fr: "Journal de sortie", es: "Registro de salida" },
  dashboard_output_wait: { en: "Press a button to start", ar: "اضغط زر لتبدأ", fr: "Appuyez sur un bouton pour commencer", es: "Presiona un botón para comenzar" },
  runs_col_when: { en: "When", ar: "الوقت", fr: "Quand", es: "Cuándo" },
  runs_col_channel: { en: "Channel", ar: "القناة", fr: "Chaîne", es: "Canal" },
  runs_col_topic: { en: "Topic", ar: "الموضوع", fr: "Sujet", es: "Tema" },
  runs_col_status: { en: "Status", ar: "الحالة", fr: "Statut", es: "Estado" },
  runs_col_url: { en: "Video URL", ar: "رابط الفيديو", fr: "URL vidéo", es: "URL del vídeo" },
  loading: { en: "Loading…", ar: "جاري التحميل…", fr: "Chargement…", es: "Cargando…" },
  backend_online: { en: "Online", ar: "متصل", fr: "En ligne", es: "En línea" },
  backend_offline: { en: "Offline — start the backend (see README)", ar: "غير متصل — شغّل الخلفية (راجع README)", fr: "Hors ligne — démarrez le backend (voir README)", es: "Desconectado — inicia el backend (ver README)" },

  assistant_title: { en: "AI Assistant", ar: "المساعد الذكي", fr: "Assistant IA", es: "Asistente IA" },
  assistant_subtitle: { en: "Ask the backend to generate content ideas", ar: "اطلب من الخلفية توليد أفكار محتوى", fr: "Demandez au backend de générer des idées", es: "Pide al backend que genere ideas" },
  assistant_input_placeholder: { en: "e.g. Give me 5 YouTube Shorts ideas about AI news in Arabic", ar: "مثال: هاتلي 5 أفكار شورتس عن أخبار الذكاء الاصطناعي بالعربي", fr: "ex. Donne-moi 5 idées de Shorts sur l'IA en français", es: "ej. Dame 5 ideas de Shorts sobre IA en español" },
  assistant_btn_send: { en: "Send", ar: "إرسال", fr: "Envoyer", es: "Enviar" },
  assistant_response_title: { en: "Response:", ar: "الرد:", fr: "Réponse :", es: "Respuesta:" },
  assistant_response_wait: { en: "Waiting for request…", ar: "في انتظار الطلب…", fr: "En attente de requête…", es: "Esperando solicitud…" }
};

let currentLang = localStorage.getItem("lang") || "en";

function buildLangSelector() {
  const select = document.getElementById("toggleLang");
  if (!select) return;
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

function t(key) {
  return (translations[key] && translations[key][currentLang]) || key;
}

function updateLanguage() {
  document.querySelectorAll("[data-i18n]").forEach(el => {
    const key = el.getAttribute("data-i18n");
    el.textContent = t(key);
  });
  document.querySelectorAll("[data-i18n-placeholder]").forEach(el => {
    const key = el.getAttribute("data-i18n-placeholder");
    el.placeholder = t(key);
  });

  document.body.dir = (currentLang === "ar" ? "rtl" : "ltr");
  document.documentElement.lang = currentLang;
}

window.addEventListener("DOMContentLoaded", function () {
  buildLangSelector();
  updateLanguage();
});
