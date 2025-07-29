const linkedAccounts = [];

function connectAccount(platform) {
  if (!linkedAccounts.includes(platform)) {
    linkedAccounts.push(platform);
    updateLinkedAccounts();
    alert({
      twitter: {
        en: "Twitter account connected!",
        ar: "تم ربط حساب تويتر!",
        fr: "Compte Twitter connecté !",
        es: "¡Cuenta de Twitter conectada!"
      },
      instagram: {
        en: "Instagram account connected!",
        ar: "تم ربط حساب إنستغرام!",
        fr: "Compte Instagram connecté !",
        es: "¡Cuenta de Instagram conectada!"
      },
      facebook: {
        en: "Facebook account connected!",
        ar: "تم ربط حساب فيسبوك!",
        fr: "Compte Facebook connecté !",
        es: "¡Cuenta de Facebook conectada!"
      }
    }[platform][currentLang]);
  }
}

function updateLinkedAccounts() {
  const div = document.getElementById("linked-accounts");
  div.innerHTML = linkedAccounts.length
    ? linkedAccounts.map(p => `<span>${{
        twitter: "Twitter",
        instagram: "Instagram",
        facebook: "Facebook"
      }[p]}</span>`).join(" | ")
    : `<span>${{
        en: "No accounts linked yet",
        ar: "لا يوجد حسابات مرتبطة بعد",
        fr: "Aucun compte lié pour l'instant",
        es: "No hay cuentas vinculadas todavía"
      }[currentLang]}</span>`;
}

function publishToSocial(content, type) {
  if (linkedAccounts.length === 0) {
    alert({
      en: "Please link your social accounts first!",
      ar: "يجب ربط حسابات السوشيال ميديا أولاً!",
      fr: "Veuillez d'abord lier vos comptes sociaux !",
      es: "¡Vincula primero tus cuentas sociales!"
    }[currentLang]);
    return;
  }
  linkedAccounts.forEach(platform => {
    console.log(`تم نشر ${type} على ${platform}: ${content}`);
  });
  alert({
    en: "Content has been published automatically to all linked accounts!",
    ar: "تم نشر المحتوى تلقائيًا على جميع الحسابات المرتبطة!",
    fr: "Le contenu a été publié automatiquement sur tous les comptes liés !",
    es: "¡El contenido se ha publicado automáticamente en todas las cuentas vinculadas!"
  }[currentLang]);
}