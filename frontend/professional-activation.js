const API_BASE_URL = "https://guia-pro.onrender.com";

const loadingState = document.getElementById("loading-state");
const errorState = document.getElementById("error-state");
const errorText = document.getElementById("error-text");

const activationState = document.getElementById("activation-state");
const successState = document.getElementById("success-state");

const welcomeTitle = document.getElementById("welcome-title");

const activationForm = document.getElementById("activation-form");
const passwordInput = document.getElementById("password");
const passwordConfirmationInput = document.getElementById(
  "password-confirmation"
);

const activateButton = document.getElementById("activate-button");
const formMessage = document.getElementById("form-message");

const loginButton = document.getElementById("login-button");


let activationToken = null;
let professionalId = null;


function getActivationToken() {
  const params = new URLSearchParams(window.location.search);

  return params.get("token");
}


function showError(message) {
  loadingState.classList.add("hidden");
  activationState.classList.add("hidden");
  successState.classList.add("hidden");

  errorText.textContent = message;

  errorState.classList.remove("hidden");
}


function showActivationForm(data) {
  loadingState.classList.add("hidden");
  errorState.classList.add("hidden");
  successState.classList.add("hidden");

  professionalId = data.professional_id;

  welcomeTitle.textContent =
    `Hola, ${data.first_name}`;

  activationState.classList.remove("hidden");
}


function showSuccess() {
  loadingState.classList.add("hidden");
  errorState.classList.add("hidden");
  activationState.classList.add("hidden");

  successState.classList.remove("hidden");
}


function showFormMessage(message, type = "error") {
  formMessage.textContent = message;

  formMessage.className = `message ${type}`;
}


async function validateToken() {
  activationToken = getActivationToken();

  if (!activationToken) {
    showError(
      "No encontramos un token de activación en este enlace."
    );

    return;
  }

  try {
    const response = await fetch(
      `${API_BASE_URL}/api/professional/activation/validate?token=${encodeURIComponent(
        activationToken
      )}`
    );

    let data = null;

    try {
      data = await response.json();
    } catch {
      data = null;
    }

    if (!response.ok) {
      showError(
        data?.detail ||
          "El enlace de activación no es válido o ya venció."
      );

      return;
    }

    showActivationForm(data);

  } catch (error) {
    console.error(
      "[ProfessionalActivation] Error validating token:",
      error
    );

    showError(
      "No pudimos conectarnos con Guia Pro. Verificá que el sistema esté disponible e intentá nuevamente."
    );
  }
}


async function activateAccount(event) {
  event.preventDefault();

  const password = passwordInput.value;
  const passwordConfirmation =
    passwordConfirmationInput.value;

  showFormMessage("", "error");
  formMessage.classList.remove("error");
  formMessage.classList.remove("success");

  if (password.length < 8) {
    showFormMessage(
      "La contraseña debe tener al menos 8 caracteres."
    );

    return;
  }

  if (password !== passwordConfirmation) {
    showFormMessage(
      "Las contraseñas no coinciden."
    );

    return;
  }

  if (!activationToken) {
    showFormMessage(
      "El enlace de activación no es válido."
    );

    return;
  }

  activateButton.disabled = true;
  activateButton.textContent = "Activando...";

  try {
    const response = await fetch(
      `${API_BASE_URL}/api/professional/activation/activate`,
      {
        method: "POST",

        headers: {
          "Content-Type": "application/json",
        },

        body: JSON.stringify({
          token: activationToken,
          password,
        }),
      }
    );

    let data = null;

    try {
      data = await response.json();
    } catch {
      data = null;
    }

    if (!response.ok) {
      showFormMessage(
        data?.detail ||
          "No pudimos activar la cuenta."
      );

      activateButton.disabled = false;
      activateButton.textContent = "Activar mi cuenta";

      return;
    }

    showSuccess();

  } catch (error) {
    console.error(
      "[ProfessionalActivation] Error activating account:",
      error
    );

    showFormMessage(
      "No pudimos conectarnos con Guia Pro. Intentá nuevamente."
    );

    activateButton.disabled = false;
    activateButton.textContent = "Activar mi cuenta";
  }
}


loginButton.addEventListener("click", () => {
  window.location.href = "./professional-login.html";
});


activationForm.addEventListener(
  "submit",
  activateAccount
);


validateToken();