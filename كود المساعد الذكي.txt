async function sendRequest() {
  const input = document.getElementById("user-input").value.trim();
  const responseArea = document.getElementById("response-area");

  if (!input) {
    responseArea.textContent = {
      en: "Please write your request before sending.",
      ar: "الرجاء كتابة طلب قبل الإرسال.",
      fr: "Veuillez écrire votre demande avant d'envoyer.",
      es: "Por favor escribe tu solicitud antes de enviar."
    }[currentLang];
    return;
  }

  responseArea.textContent = {
    en: "Processing your request...",
    ar: "جاري معالجة طلبك...",
    fr: "Traitement de votre demande...",
    es: "Procesando tu solicitud..."
  }[currentLang];

  setTimeout(() => {
    let reply = "";
    if (input.includes("فيديو") || input.toLowerCase().includes("video")) {
      reply = {
        en: "A new motivational video has been prepared and will be published soon.",
        ar: "تم إعداد فيديو تحفيزي جديد وسيتم نشره خلال دقائق.",
        fr: "Une nouvelle vidéo de motivation a été préparée et sera publiée bientôt.",
        es: "Se ha preparado un nuevo vídeo motivacional y se publicará pronto."
      }[currentLang];
    } else if (input.includes("كتاب") || input.toLowerCase().includes("book")) {
      reply = {
        en: "A PDF book entitled 'Success and Self-Development' is being generated.",
        ar: "جارٍ توليد كتاب PDF بعنوان 'النجاح والتطوير الذاتي'.",
        fr: "Un livre PDF intitulé 'Succès et développement personnel' est en cours de génération.",
        es: "Se está generando un libro PDF titulado 'Éxito y desarrollo personal'."
      }[currentLang];
    } else if (input.includes("منشورات") || input.toLowerCase().includes("posts")) {
      reply = {
        en: "A set of social media posts has been created.",
        ar: "تم إنشاء مجموعة منشورات جاهزة للسوشيال ميديا.",
        fr: "Un ensemble de publications pour les réseaux sociaux a été créé.",
        es: "Se ha creado un conjunto de publicaciones para redes sociales."
      }[currentLang];
    } else if (input.includes("خطة محتوى") || input.toLowerCase().includes("content plan")) {
      reply = {
        en: "Here is a content plan for next week: Video, Book, Posts, Advertisement.",
        ar: "هذه خطة محتوى للأسبوع القادم: فيديو، كتاب، منشورات، إعلان.",
        fr: "Voici un plan de contenu pour la semaine prochaine : vidéo, livre, publications, publicité.",
        es: "Aquí tienes un plan de contenido para la próxima semana: vídeo, libro, publicaciones, anuncio."
      }[currentLang];
    } else {
      reply = {
        en: "Thank you for your request, we are working on it and will update you soon.",
        ar: "شكراً لطلبك، جاري العمل عليه وسأوافيك بالتحديثات قريباً.",
        fr: "Merci pour votre demande, nous y travaillons et vous tiendrons informé bientôt.",
        es: "Gracias por tu solicitud, estamos trabajando en ello y te informaremos pronto."
      }[currentLang];
    }
    responseArea.textContent = reply;
  }, 1500);
}