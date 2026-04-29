document.addEventListener('DOMContentLoaded', () => {
  document.addEventListener('click', (event) => {
    const target = event.target;

    if (target.matches('.expand-button')) {
      const card = target.closest('.card');
      if (!card) return;
      card.querySelectorAll('.registrationlists').forEach((list) => list.classList.add('show'));
      target.style.display = 'none';
      return;
    }

    if (target.matches('.collapse-button')) {
      const card = target.closest('.card');
      if (!card) return;
      card.querySelectorAll('.registrationlists').forEach((list) => list.classList.remove('show'));
      const registerButton = card.querySelector('.expand-button');
      if (registerButton) registerButton.style.display = '';
    }
  });
});
