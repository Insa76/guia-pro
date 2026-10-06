
const API_BASE_URL = "http://localhost:8000";

const form = document.getElementById("registerForm");
const categorySelect = document.getElementById("category");
const locationSelect = document.getElementById("location");
const formMessage = document.getElementById("formMessage");
const submitButton = document.getElementById("submitButton");


function showMessage(message, type = "error") {
    formMessage.textContent = message;
    formMessage.className = `form-message ${type}`;
    formMessage.hidden = false;
}


function hideMessage() {
    formMessage.hidden = true;
    formMessage.textContent = "";
    formMessage.className = "form-message";
}


async function loadCategories() {
    try {
        const response = await fetch(
            `${API_BASE_URL}/api/categories`
        );

        if (!response.ok) {
            throw new Error("No se pudieron cargar los oficios.");
        }

        const categories = await response.json();

        categorySelect.innerHTML = `
            <option value="">Seleccioná tu oficio</option>
        `;

        categories
            .filter(category => category.is_active !== false)
            .forEach(category => {
                const option = document.createElement("option");

                option.value = category.id;
                option.textContent = category.name;

                categorySelect.appendChild(option);
            });

    } catch (error) {
        console.error(error);

        categorySelect.innerHTML = `
            <option value="">No se pudieron cargar los oficios</option>
        `;
    }
}


async function loadLocations() {
    try {
        const response = await fetch(
            `${API_BASE_URL}/api/locations`
        );

        if (!response.ok) {
            throw new Error("No se pudieron cargar las localidades.");
        }

        const locations = await response.json();

        locationSelect.innerHTML = `
            <option value="">Seleccioná tu localidad</option>
        `;

        locations
            .filter(location => location.is_active !== false)
            .forEach(location => {
                const option = document.createElement("option");

                option.value = location.id;

                option.textContent =
                    `${location.name}, ${location.province}`;

                locationSelect.appendChild(option);
            });

    } catch (error) {
        console.error(error);

        locationSelect.innerHTML = `
            <option value="">No se pudieron cargar las localidades</option>
        `;
    }
}


function getFormData() {
    const formData = new FormData(form);

    return {
        first_name: formData.get("first_name")?.trim(),
        last_name: formData.get("last_name")?.trim(),
        phone: formData.get("phone")?.trim(),
        whatsapp: formData.get("whatsapp")?.trim() || null,
        description: formData.get("description")?.trim() || null,
        years_experience:
            formData.get("years_experience")
                ? Number(formData.get("years_experience"))
                : null,
        instagram: formData.get("instagram")?.trim() || null,
        category_id: Number(formData.get("category_id")),
        location_id: Number(formData.get("location_id"))
    };
}


async function registerProfessional(data) {
    const response = await fetch(
        `${API_BASE_URL}/api/public/professionals/register`,
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        }
    );

    const result = await response.json();

    if (!response.ok) {
        throw new Error(
            result.detail || "No se pudo completar el registro."
        );
    }

    return result;
}


form.addEventListener("submit", async (event) => {
    event.preventDefault();

    hideMessage();

    submitButton.disabled = true;
    submitButton.textContent = "Enviando registro...";

    try {
        const data = getFormData();

        const result = await registerProfessional(data);

        showMessage(
            result.message ||
            "Registro recibido. Tu perfil quedará pendiente de revisión.",
            "success"
        );

        form.reset();

        await loadCategories();
        await loadLocations();

    } catch (error) {
        console.error(error);

        showMessage(
            error.message ||
            "Ocurrió un error al enviar el registro.",
            "error"
        );

    } finally {
        submitButton.disabled = false;
        submitButton.textContent = "Registrarme en Guia Pro";
    }
});


async function init() {
    await Promise.all([
        loadCategories(),
        loadLocations()
    ]);
}


init();

