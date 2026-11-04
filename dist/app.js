const english = document.documentElement.lang.startsWith('en');
document.getElementById('year').textContent = new Date().getFullYear();
document.querySelectorAll('[data-mode]').forEach(a => a.addEventListener('click', () => { document.getElementById('mode').value = a.dataset.mode; }));
document.querySelectorAll('[data-sector]').forEach(a => a.addEventListener('click', () => {
  document.querySelector('select[name="Secteur"]').value = a.dataset.sector;
  document.getElementById('mode').selectedIndex = 0;
}));
document.getElementById('quote').addEventListener('submit', e => {
  e.preventDefault();
  const data = new FormData(e.currentTarget);
  const labels = {Nom:'Name',Entreprise:'Company',Courriel:'Email','Téléphone':'Phone',Besoin:'Service',Secteur:'Industry','Départ':'Pickup location',Destination:'Destination','Échéance':'Requested date and time','Référence achats':'Purchase reference','Réception':'Receiving contact','Conditions sur place':'Site conditions','Détails':'Details'};
  const subject = (english ? 'Transport request — ' : 'Demande de transport — ') + data.get('Entreprise') + ' — ' + data.get('Besoin');
  const rows = Array.from(data, ([key, value]) => (english ? labels[key] || key : key) + ' : ' + value).join('\n');
  const body = english ? 'Hello,\n\nI would like to discuss a transport with Transport routier spécialisé inc.\n\n' + rows + '\n\nPlease contact me to discuss feasibility and terms.' : 'Bonjour,\n\nJe souhaite discuter d’un transport avec Transport routier spécialisé inc.\n\n' + rows + '\n\nMerci de me contacter pour évaluer la faisabilité et les conditions.';
  window.location.href = 'mailto:info@TRspecialise.com?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(body);
  document.getElementById('status').textContent = english ? 'Your request is ready. Send it from your email application. If it does not open, email info@TRspecialise.com or call 450-374-4737.' : 'Votre demande est préparée. Envoyez-la depuis votre application de courriel. Si celle-ci ne s’ouvre pas, écrivez à info@TRspecialise.com ou appelez le 450-374-4737.';
});
const gallery = document.querySelector('.gallery-grid');
if (gallery) {
  const slides = [...gallery.querySelectorAll('figure')];
  let active = 0;
  setInterval(() => {
    if (document.hidden || slides.length < 2) return;
    active = (active + 1) % slides.length;
    gallery.scrollTo({
      left: slides[active].offsetLeft - slides[0].offsetLeft,
      behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'instant' : 'smooth'
    });
  }, 5000);
}
