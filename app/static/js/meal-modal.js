const modalOverlay = document.getElementById('modalOverlay');
const closeBtn = document.getElementById('closeBtn');
const modalDayTitle = document.getElementById('modalDayTitle');
const modalMealTitle = document.getElementById('modalMealTitle');
const mealName = document.getElementById('mealName');
const mealTime = document.getElementById('mealTime');
const mealCalories = document.getElementById('mealCalories');
const mealIngredients = document.getElementById('mealIngredients');
const mealRecipe = document.getElementById('mealRecipe');

if (
  modalOverlay &&
  closeBtn &&
  modalDayTitle &&
  modalMealTitle &&
  mealName &&
  mealTime &&
  mealCalories &&
  mealIngredients &&
  mealRecipe
) {
  const formatIngredient = (ingredient) => {
    const quantity = ingredient.quantity ?? '';
    const unit = ingredient.unit ?? '';
    const name = ingredient.name ?? '';
    return [quantity, unit, name].filter(Boolean).join(' ').trim();
  };

  const renderIngredients = (ingredients) => {
    mealIngredients.innerHTML = '';

    if (!Array.isArray(ingredients) || ingredients.length === 0) {
      const emptyItem = document.createElement('li');
      emptyItem.className = 'ingredient-list__empty';
      emptyItem.textContent = 'No ingredients provided.';
      mealIngredients.appendChild(emptyItem);
      return;
    }

    ingredients.forEach((ingredient) => {
      const li = document.createElement('li');
      li.textContent = formatIngredient(ingredient);
      mealIngredients.appendChild(li);
    });
  };

  const showModal = () => {
    modalOverlay.classList.add('is-visible');
    modalOverlay.setAttribute('aria-hidden', 'false');
    closeBtn.focus();
  };

  const hideModal = () => {
    modalOverlay.classList.remove('is-visible');
    modalOverlay.setAttribute('aria-hidden', 'true');
  };

  closeBtn.addEventListener('click', hideModal);

  modalOverlay.addEventListener('click', (event) => {
    if (event.target === modalOverlay) {
      hideModal();
    }
  });

  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && modalOverlay.classList.contains('is-visible')) {
      hideModal();
    }
  });

  const updateModal = (day, mealtype, mealData) => {
    modalDayTitle.textContent = `Day ${day}`;
    modalMealTitle.textContent = mealtype === 'lunch' ? 'Lunch' : 'Dinner';

    const hasDetails = mealData && Object.keys(mealData).length > 0;

    mealName.textContent = hasDetails ? mealData.name ?? 'Untitled meal' : 'Not planned yet';
    mealTime.textContent = hasDetails && mealData.prep_time_minutes !== undefined ? mealData.prep_time_minutes : '—';
    mealCalories.textContent = hasDetails && mealData.calories_per_person !== undefined ? mealData.calories_per_person : '—';
    mealRecipe.textContent = hasDetails && mealData.recipe ? mealData.recipe : 'No recipe available yet.';

    renderIngredients(hasDetails ? mealData.ingredients : []);
  };

  const handleMealButtonClick = async (button) => {
    const { year, month, day, mealtype } = button.dataset;
    const url = `/api/day_details?year=${year}&month=${month}&day=${day}`;

    try {
      const response = await fetch(url);
      if (!response.ok) {
        throw new Error(response.statusText);
      }
      const data = await response.json();
      const mealData = mealtype === 'lunch' ? data.lunch : data.dinner;
      updateModal(day, mealtype, mealData);
      showModal();
    } catch (error) {
      console.error('Error while fetching meal details', error);
      updateModal(button.dataset.day, button.dataset.mealtype, {});
      showModal();
    }
  };

  document.querySelectorAll('.meal-button').forEach((button) => {
    button.addEventListener('click', () => handleMealButtonClick(button));
  });
}
