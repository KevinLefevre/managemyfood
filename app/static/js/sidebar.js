const startPlanningBtn = document.getElementById('startPlanningBtn');
const planningModalOverlay = document.getElementById('planningModalOverlay');
const closePlanningBtn = document.getElementById('closePlanningBtn');
const sendChatBtn = document.getElementById('sendChatBtn');
const chatInput = document.getElementById('chatInput');
const chatArea = document.getElementById('chatArea');

if (startPlanningBtn && planningModalOverlay && closePlanningBtn) {
  const openPlanningModal = () => {
    planningModalOverlay.classList.add('is-visible');
    planningModalOverlay.setAttribute('aria-hidden', 'false');
    chatInput?.focus();
  };

  const closePlanningModal = () => {
    planningModalOverlay.classList.remove('is-visible');
    planningModalOverlay.setAttribute('aria-hidden', 'true');
    startPlanningBtn.focus();
  };

  startPlanningBtn.addEventListener('click', openPlanningModal);
  closePlanningBtn.addEventListener('click', closePlanningModal);

  planningModalOverlay.addEventListener('click', (event) => {
    if (event.target === planningModalOverlay) {
      closePlanningModal();
    }
  });

  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && planningModalOverlay.classList.contains('is-visible')) {
      closePlanningModal();
    }
  });

  const appendMessage = (message, author) => {
    if (!chatArea) {
      return;
    }

    const messageWrapper = document.createElement('div');
    messageWrapper.className = `chat-message chat-message--${author}`;
    messageWrapper.textContent = message;
    chatArea.appendChild(messageWrapper);
    chatArea.scrollTop = chatArea.scrollHeight;
  };

  const handleSendMessage = () => {
    if (!chatInput || chatInput.value.trim() === '') {
      return;
    }
    appendMessage(chatInput.value.trim(), 'user');
    chatInput.value = '';
  };

  sendChatBtn?.addEventListener('click', handleSendMessage);
  chatInput?.addEventListener('keydown', (event) => {
    if (event.key === 'Enter') {
      event.preventDefault();
      handleSendMessage();
    }
  });
}
