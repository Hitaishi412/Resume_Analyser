document.addEventListener("DOMContentLoaded", function () {
  const analyzeBtn = document.getElementById('analyze-btn');
  const resumeInput = document.getElementById('resume');
  const jobDescInput = document.getElementById('job-description');
  const matchScore = document.getElementById('matchScore');
  const feedback = document.getElementById('feedback');
  const resultsContainer = document.getElementById('results');

  analyzeBtn.addEventListener('click', async function () {
    const jobDesc = jobDescInput.value.trim();

    if (!resumeInput.files.length || !jobDesc) {
      alert('Please upload a resume and enter a job description.');
      return;
    }

    const payload = { resume_text: resumeInput.files[0].name, jd_text: jobDesc };
    resultsContainer.style.display = 'block';
    matchScore.innerHTML = 'Analyzing...';
    feedback.innerHTML = '';

    try {
      const response = await fetch('http://localhost:5000/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      const data = await response.json();
      if (response.ok) {
        matchScore.innerHTML = `Match Score: <span class="highlight">${data.final_score.final_score}%</span>`;
        const missingSkills = data.skill_match.missing_skills.join(', ') || 'None';
        const suggestions = data.final_score.feedback.map(item => `<li>${item}</li>`).join('');
        feedback.innerHTML = `
          <p><span class="highlight">Missing Skills:</span> ${missingSkills}</p>
          <p><strong>Suggestions:</strong></p>
          <ul>${suggestions}</ul>
        `;
      } else {
        matchScore.innerHTML = '❌ Error analyzing the resume.';
        feedback.innerHTML = data.error || '';
      }
    } catch (err) {
      console.error('Fetch error:', err);
      matchScore.innerHTML = '❌ Server error.';
      feedback.innerHTML = 'Please try again later.';
    }
  });
});
