const API_BASE_URL = "https://guia-pro.onrender.com";

const registerForm = document.getElementById(
  "professional-register-form"
);

const categorySelect = document.getElementById(
  "category_id"
);

const locationSelect = document.getElementById(
  "location_id"
);

const registerError = document.getElementById(
  "register-error"
);

const registerSuccess = document.getElementById(
  "register-success"
);

const submitButton = document.getElementById(
  "register-submit"
);


function showRegisterError(message) {
  registerError.textContent = message;
  registerError.classList.remove("hidden");
}


function hideRegisterError() {
  registerError.textContent = "";
  registerError.classList.add("hidden");
}


function showRegisterSuccess(message) {
  registerSuccess.textContent = message;
  registerSuccess.classList.remove("hidden");
}


function hideRegisterSuccess() {
  registerSuccess.textContent = "";
  registerSuccess.classList.add("hidden");
}


async function loadCategories() {
  const response = await fetch(
    `${API_BASE_URL}/api/categories`
  );

  let data = null;

  try {
    data = await response.json();
  } catch {}

  if (!response.ok) {
    throw new Error(
      typeof data?.detail === "string"
        ? data.detail
        : "No se pudieron cargar los oficios."
    );
  }

  const categories = Array.isArray(data)
    ? data
    : Array.isArray(data?.items)
      ? data.items
      : [];

  categorySelect.innerHTML = `
    <option value="">
      Seleccioná tu oficio
    </option>
  `;

  categories.forEach((category) => {
    const option = document.createElement("option");

    option.value = category.id;
    option.textContent = category.name;

    categorySelect.appendChild(option);
  });
}


async function loadLocations() {
  const response = await fetch(
    `${API_BASE_URL}/api/locations`
  );

  let data = null;

  try {
    data = await response.json();
  } catch {}

  if (!response.ok) {
    throw new Error(
      typeof data?.detail === "string"
        ? data.detail
        : "No se pudieron cargar las ciudades."
    );
  }

  const locations = Array.isArray(data)
    ? data
    : Array.isArray(data?.items)
      ? data.items
      : [];

  locationSelect.innerHTML = `
    <option value="">
      Seleccioná tu ciudad
    </option>
  `;

  locations.forEach((location) => {
    const option = document.createElement("option");

    option.value = location.id;
    option.textContent = location.name;

    locationSelect.appendChild(option);
  });
}


async function registerProfessional(event) {
  event.preventDefault();

  hideRegisterError();
  hideRegisterSuccess();

  const formData = new FormData(registerForm);

  const firstName = String(
    formData.get("first_name") || ""
  ).trim();

  const lastName = String(
    formData.get("last_name") || ""
  ).trim();

  const phone = String(
    formData.get("phone") || ""
  ).trim();

  const password = String(
    formData.get("password") || ""
  );

  const categoryId = Number(
    formData.get("category_id")
  );

  const locationId = Number(
    formData.get("location_id")
  );

  if (
    !firstName ||
    !lastName ||
    !phone ||
    !password ||
    !categoryId ||
    !locationId
  ) {
    showRegisterError(
      "Completá todos los campos."
    );
    return;
  }

  if (password.length < 6) {
    showRegisterError(
      "La contraseña debe tener al menos 6 caracteres."
    );
    return;
  }

  submitButton.disabled = true;
  submitButton.textContent = "Enviando solicitud...";

  try {
    const response = await fetch(
      `${API_BASE_URL}/api/professional/auth/register`,
      {
        method: "POST",

        headers: {
          "Content-Type": "application/json",
        },

        body: JSON.stringify({
          first_name: firstName,
          last_name: lastName,
          phone,
          password,
          category_id: categoryId,
          location_id: locationId,
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
          : "No se pudo enviar la solicitud."
      );
    }

    registerForm.reset();

    showRegisterSuccess(
      data?.message ||
      "Solicitud recibida. Tu perfil será revisado antes de ser activado."
    );

  } catch (error) {
    console.error(
      "[Professional Register] Error:",
      error
    );

    showRegisterError(
      error.message ||
      "Ocurrió un error al enviar la solicitud."
    );

  } finally {
    submitButton.disabled = false;
    submitButton.textContent = "Solicitar registro";
  }
}


async function initializeRegisterPage() {
  hideRegisterError();
  hideRegisterSuccess();

  try {
    await Promise.all([
      loadCategories(),
      loadLocations(),
    ]);

  } catch (error) {
    console.error(
      "[Professional Register] Initialization error:",
      error
    );

    showRegisterError(
      error.message ||
      "No se pudieron cargar los datos necesarios para registrarte."
    );
  }
}


registerForm.addEventListener(
  "submit",
  registerProfessional
);


initializeRegisterPage();