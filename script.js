document.getElementById('matchForm').addEventListener('submit', function(e) {
  e.preventDefault();
  const team1 = document.getElementById('team1').value.trim();
  const team2 = document.getElementById('team2').value.trim();

  const predictionUnder35 = (Math.random() * 100).toFixed(1);
  const predictionUnder45 = (Math.random() * 100).toFixed(1);

  document.getElementById('result').innerHTML = `
    <h3>${team1} vs ${team2}</h3>
    <p>Probabilité Under 3.5 buts : <strong>${predictionUnder35}%</strong></p>
    <p>Probabilité Under 4.5 buts : <strong>${predictionUnder45}%</strong></p>
  `;
});
