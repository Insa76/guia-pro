const API_BASE_URL = "https://guia-pro.onrender.com";

const PROFESSIONAL_TOKEN_STORAGE_KEY =
  "guia_pro_professional_token";

const loginForm = document.getElementById(
  "professional-login-form"
);

const loginError = document.getElementById(
  "login-error"
);

const submitButton = document.getElementById(
  "login-submit"
);

function showLoginError(message) {
  loginError.textContent = message;
  loginError.classList.remove("hidden");
}

function hideLoginError() {
  loginError.textContent = "";
  loginError.classList.add("hidden");
}

async function loginProfessional(event) {
  event.preventDefault();

  hideLoginError();

  const formData = new FormData(loginForm);

  const phone = String(
    formData.get("phone") || ""
  ).trim();

  const password = String(
    formData.get("password") || ""
  );

  if (!phone || !password) {
    showLoginError(
      "Ingresá tu teléfono y contraseña."
    );
    return;
  }

  submitButton.disabled = true;
  submitButton.textContent = "Ingresando...";

  try {
    const response = await fetch(
      `${API_BASE_URL}/api/professional/auth/login`,
      {
        method: "POST",

        headers: {
          "Content-Type": "application/json",
        },

        body: JSON.stringify({
          phone,
          password,
        }),
      }
    );

    let data = null;

    try {
      data = await response.json();
    } catch {}

    if (!response.ok) {
      throw new Error(
        typeof data?.detail === "string"
          ? data.detail
          : "No se pudo iniciar sesión."
      );
    }

    if (!data?.access_token) {
      throw new Error(
        "El servidor no devolvió una sesión válida."
      );
    }

    sessionStorage.setItem(
      PROFESSIONAL_TOKEN_STORAGE_KEY,
      data.access_token
    );

    window.location.replace("professional.html");

  } catch (error) {
    console.error(
      "[Professional Login] Error:",
      error
    );

    showLoginError(
      error.message ||
      "Ocurrió un error al iniciar sesión."
    );

  } finally {
    submitButton.disabled = false;
    submitButton.textContent = "Ingresar";
  }
}

loginForm.addEventListener(
  "submit",
  loginProfessional
);