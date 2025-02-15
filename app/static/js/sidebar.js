const startPlanningBtn = document.getElementById('startPlanningBtn');
const planningModalOverlay = document.getElementById('planningModalOverlay');
const closePlanningBtn = document.getElementById('closePlanningBtn');

startPlanningBtn.addEventListener('click', () => {
  planningModalOverlay.style.display = 'block';
});
closePlanningBtn.addEventListener('click', () => {
  planningModalOverlay.style.display = 'none';
});
