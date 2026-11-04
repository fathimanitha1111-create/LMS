/**
 * Online LMS - Quiz JavaScript
 */

document.addEventListener('DOMContentLoaded', function () {
  const quizForm = document.getElementById('quizForm');
  if (quizForm) {
    quizForm.addEventListener('submit', function (e) {
      const questions = document.querySelectorAll('.question-block');
      let answered = 0;
      questions.forEach(q => {
        const radios = q.querySelectorAll('input[type="radio"]:checked');
        if (radios.length > 0) answered++;
      });

      if (answered < questions.length) {
        if (!confirm(`You have answered ${answered} of ${questions.length} questions. Do you want to submit anyway?`)) {
          e.preventDefault();
        }
      }
    });
  }
});

