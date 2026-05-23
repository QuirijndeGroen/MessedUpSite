document.addEventListener('DOMContentLoaded', () => {
  const addQuestionBtn = document.getElementById('add-question-btn');
  const formsetBody = document.getElementById('question-formset-body');
  const questionTemplate = document.getElementById('question-form-template');
  const totalFormsInput = document.querySelector('input[name$="-TOTAL_FORMS"]');

  if (!addQuestionBtn || !formsetBody || !questionTemplate || !totalFormsInput) {
    return;
  }

  addQuestionBtn.addEventListener('click', () => {
    const currentFormCount = parseInt(totalFormsInput.value, 10);
    const newRow = questionTemplate.content.firstElementChild.cloneNode(true);
    const rowHtml = newRow.innerHTML.replace(/__prefix__/g, currentFormCount);
    newRow.innerHTML = rowHtml;
    formsetBody.appendChild(newRow);
    totalFormsInput.value = currentFormCount + 1;
  });

  formsetBody.addEventListener('click', (event) => {
    const deleteButton = event.target.closest('.question-delete-btn');
    if (!deleteButton) {
      return;
    }

    const row = deleteButton.closest('.question-form-row');
    if (!row) {
      return;
    }

    const deleteInput = row.querySelector('input[name$="-DELETE"]');
    if (deleteInput) {
      deleteInput.checked = true;
    }
    row.style.display = 'none';
  });
});
