function simulateAsyncTask(text, delay = 1500) {
  return new Promise((resolve) => {
    setTimeout(() => resolve(text), delay);
  });
}

async function generateContent() {
  const output = document.getElementById("output-area");
  output.textContent = {
    en: "Generating new content...",
    ar: "جاري توليد محتوى جديد...",
    fr: "Génération d'un nouveau contenu...",
    es: "Generando nuevo contenido..."
  }[currentLang];
  const result = await simulateAsyncTask({
    en: "A weekly content plan has been successfully generated.",
    ar: "تم توليد خطة محتوى للأسبوع القادم بنجاح.",
    fr: "Un plan de contenu hebdomadaire a été généré avec succès.",
    es: "Se ha generado correctamente un plan de contenido semanal."
  }[currentLang]);
  output.textContent = result;
}

async function generateBook() {
  const output = document.getElementById("output-area");
  output.textContent = {
    en: "Creating PDF book...",
    ar: "جاري إنشاء كتاب PDF...",
    fr: "Création d'un livre PDF...",
    es: "Creando libro PDF..."
  }[currentLang];
  const result = await simulateAsyncTask({
    en: "A PDF book entitled 'Success Habits' is ready for publishing.",
    ar: "تم إنشاء كتاب PDF بعنوان 'عادات النجاح' جاهز للنشر.",
    fr: "Un livre PDF intitulé 'Les habitudes du succès' est prêt à être publié.",
    es: "El libro PDF titulado 'Hábitos de éxito' está listo para publicarse."
  }[currentLang]);
  output.textContent = result;
}

async function generatePosts() {
  const output = document.getElementById("output-area");
  output.textContent = {
    en: "Creating social media posts...",
    ar: "جاري إنشاء منشورات للسوشيال ميديا...",
    fr: "Création de publications pour les réseaux sociaux...",
    es: "Creando publicaciones para redes sociales..."
  }[currentLang];
  const result = await simulateAsyncTask({
    en: "5 posts are ready for publishing on Twitter and Instagram.",
    ar: "تم إنشاء 5 منشورات جاهزة للنشر على تويتر وإنستغرام.",
    fr: "5 publications sont prêtes à être publiées sur Twitter et Instagram.",
    es: "5 publicaciones están listas para publicar en Twitter e Instagram."
  }[currentLang]);
  output.textContent = result;
  publishToSocial(result, "منشور");
}

async function generateVideo() {
  const output = document.getElementById("output-area");
  output.textContent = {
    en: "Generating video...",
    ar: "جاري توليد فيديو تلقائي...",
    fr: "Génération de la vidéo...",
    es: "Generando vídeo..."
  }[currentLang];
  const result = await simulateAsyncTask({
    en: "A new motivational video has been generated and published.",
    ar: "تم توليد فيديو تحفيزي جديد وتم نشره تلقائيًا.",
    fr: "Une nouvelle vidéo de motivation a été générée et publiée automatiquement.",
    es: "Se ha generado y publicado automáticamente un nuevo vídeo motivacional."
  }[currentLang]);
  output.textContent = result;
  publishToSocial(result, "فيديو");
}

function schedulePost() {
  const time = document.getElementById('schedule-time').value;
  alert({
    en: `Post will be published at: ${time}`,
    ar: `سيتم نشر المنشور في الوقت: ${time}`,
    fr: `La publication sera programmée pour : ${time}`,
    es: `La publicación se programará para: ${time}`
  }[currentLang]);
}

document.getElementById("visitors-count").textContent = 342;
document.getElementById("subscribers-count").textContent = 125;
document.getElementById("sales-count").textContent = 27;
document.getElementById("revenue-amount").textContent = "$1,524";