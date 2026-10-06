const API_BASE_URL = "http://localhost:8000";

const ADMIN_TOKEN_STORAGE_KEY =
    "guia_pro_admin_token";


const loginState =
    document.getElementById("loginState");

const adminContent =
    document.getElementById("adminContent");

const loginForm =
    document.getElementById("loginForm");

const usernameInput =
    document.getElementById("adminUsername");

const passwordInput =
    document.getElementById("adminPassword");

const loginMessage =
    document.getElementById("loginMessage");

const pendingList =
    document.getElementById("pendingList");

const loadingState =
    document.getElementById("loadingState");

const emptyState =
    document.getElementById("emptyState");

const refreshButton =
    document.getElementById("refreshButton");

const adminMessage =
    document.getElementById("adminMessage");

const professionalsList =
    document.getElementById("professionalsList");

const professionalsLoadingState =
    document.getElementById(
        "professionalsLoadingState"
    );

const professionalsEmptyState =
    document.getElementById(
        "professionalsEmptyState"
    );

const adminProfileEditPanel =
    document.getElementById(
        "admin-profile-edit-panel"
    );

const adminProfileEditForm =
    document.getElementById(
        "admin-profile-edit-form"
    );

const adminEditTitle =
    document.getElementById(
        "admin-edit-title"
    );

const adminProfileDescription =
    document.getElementById(
        "admin-profile-description"
    );

const adminProfileYears =
    document.getElementById(
        "admin-profile-years"
    );

const adminProfileWhatsapp =
    document.getElementById(
        "admin-profile-whatsapp"
    );

const adminProfileInstagram =
    document.getElementById(
        "admin-profile-instagram"
    );

const adminProfileCategories =
    document.getElementById(
        "admin-profile-categories"
    );

const adminProfileLocations =
    document.getElementById(
        "admin-profile-locations"
    );

const adminProfileEditCancel =
    document.getElementById(
        "admin-profile-edit-cancel"
    );

const adminProfileEditMessage =
    document.getElementById(
        "admin-profile-edit-message"
    );

let editingProfessionalId = null;


/*
============================================================
TOKEN
============================================================
*/

function getAdminToken() {

    return sessionStorage.getItem(
        ADMIN_TOKEN_STORAGE_KEY
    );
}


function setAdminToken(token) {

    sessionStorage.setItem(
        ADMIN_TOKEN_STORAGE_KEY,
        token
    );
}


function clearAdminToken() {

    sessionStorage.removeItem(
        ADMIN_TOKEN_STORAGE_KEY
    );
}


/*
============================================================
LOGIN
============================================================
*/

async function login(
    username,
    password
) {

    const response =
        await fetch(
            `${API_BASE_URL}/api/admin/auth/login`,
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json",
                },

                body: JSON.stringify({
                    username,
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

        throw new Error(
            data?.detail ||
            "No se pudo iniciar sesión."
        );
    }


    setAdminToken(
        data.access_token
    );
}


/*
============================================================
ESTADO DE LOGIN
============================================================
*/

function showLogin() {

    if (loginState) {
        loginState.hidden = false;
    }

    if (adminContent) {
        adminContent.hidden = true;
    }
}


function showAdminContent() {

    if (loginState) {
        loginState.hidden = true;
    }

    if (adminContent) {
        adminContent.hidden = false;
    }
}


function showLoginMessage(message) {

    if (!loginMessage) {
        return;
    }

    loginMessage.textContent =
        message;

    loginMessage.hidden =
        false;
}


function hideLoginMessage() {

    if (!loginMessage) {
        return;
    }

    loginMessage.hidden =
        true;

    loginMessage.textContent =
        "";
}


/*
============================================================
HEADERS
============================================================
*/

function getAdminHeaders() {

    const token =
        getAdminToken();

    if (!token) {

        throw new Error(
            "La sesión administrativa no está iniciada."
        );
    }


    return {
        "Content-Type": "application/json",

        "Authorization":
            `Bearer ${token}`,
    };
}


/*
============================================================
UTILIDADES
============================================================
*/

function escapeHtml(value) {

    if (
        value === null ||
        value === undefined
    ) {
        return "";
    }

    return String(value)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
}


function showMessage(
    message,
    type = "success"
) {

    adminMessage.textContent =
        message;

    adminMessage.className =
        `form-message ${type}`;

    adminMessage.hidden =
        false;
}


function hideMessage() {

    adminMessage.hidden =
        true;

    adminMessage.textContent =
        "";
}


/*
============================================================
RENDER PROFESIONAL
============================================================
*/

function renderProfessional(item) {

    const whatsappNumber =
        item.whatsapp ||
        item.phone ||
        "";

    const whatsappUrl =
        whatsappNumber
            ? `https://wa.me/${whatsappNumber.replace(/\D/g, "")}`
            : "#";


    return `
        <article class="profile-card admin-card">

            <div class="admin-card-header">

                <div>
                    <p class="eyebrow">
                        Solicitud #${item.verification_id}
                    </p>

                    <h2>
                        ${escapeHtml(item.first_name)}
                        ${escapeHtml(item.last_name)}
                    </h2>

                    <p class="admin-meta">
                        Profesional #${item.professional_id}
                    </p>
                </div>

                <span class="admin-status">
                    Pendiente
                </span>

            </div>


            <div class="admin-card-grid">

                <div>
                    <strong>Teléfono</strong>

                    <p>
                        ${escapeHtml(item.phone)}
                    </p>
                </div>


                <div>
                    <strong>WhatsApp</strong>

                    <p>
                        ${
                            item.whatsapp
                                ? `<a href="${whatsappUrl}" target="_blank" rel="noopener">
                                    ${escapeHtml(item.whatsapp)}
                                  </a>`
                                : "No informado"
                        }
                    </p>
                </div>


                <div>
                    <strong>Experiencia</strong>

                    <p>
                        ${
                            item.years_experience !== null
                                ? `${item.years_experience} años`
                                : "No informada"
                        }
                    </p>
                </div>


                <div>
                    <strong>Instagram</strong>

                    <p>
                        ${
                            item.instagram
                                ? escapeHtml(item.instagram)
                                : "No informado"
                        }
                    </p>
                </div>

            </div>


            <div class="admin-description">

                <strong>Descripción</strong>

                <p>
                    ${
                        item.description
                            ? escapeHtml(item.description)
                            : "Sin descripción."
                    }
                </p>

            </div>


            <div class="admin-method">

                <span>
                    Método:
                    <strong>
                        ${escapeHtml(item.method || "—")}
                    </strong>
                </span>

            </div>


            <div class="admin-actions">

                <button
                    type="button"
                    class="primary-button admin-approve"
                    data-id="${item.verification_id}"
                >
                    Aprobar
                </button>


                <button
                    type="button"
                    class="admin-reject"
                    data-id="${item.verification_id}"
                >
                    Rechazar
                </button>

            </div>

        </article>
    `;
}


/*
============================================================
EDICIÓN ADMINISTRATIVA
============================================================
*/

async function loadAdminProfileOptions() {

    const [
        categoriesResponse,
        locationsResponse
    ] = await Promise.all([
        fetch(`${API_BASE_URL}/api/categories`),
        fetch(`${API_BASE_URL}/api/locations`)
    ]);


    if (!categoriesResponse.ok) {
        throw new Error(
            "No se pudieron cargar los servicios."
        );
    }


    if (!locationsResponse.ok) {
        throw new Error(
            "No se pudieron cargar las zonas."
        );
    }


    const categories =
        await categoriesResponse.json();

    const locations =
        await locationsResponse.json();


    adminProfileCategories.innerHTML = "";

    categories.forEach(category => {

        const option =
            document.createElement("option");

        option.value =
            category.id;

        option.textContent =
            category.name;

        adminProfileCategories.appendChild(
            option
        );
    });


    adminProfileLocations.innerHTML = "";

    locations.forEach(location => {

        const option =
            document.createElement("option");

        option.value =
            location.id;

        option.textContent =
            `${location.name} · ${location.province}`;

        adminProfileLocations.appendChild(
            option
        );
    });
}


async function openAdminProfileEditor(
    professionalId
) {

    try {

        editingProfessionalId =
            professionalId;


        adminProfileEditMessage.hidden =
            true;


        await loadAdminProfileOptions();


        const response =
            await fetch(
                `${API_BASE_URL}/api/professionals/${professionalId}/profile`
            );


        let professional = null;

        try {
            professional =
                await response.json();
        } catch {
            professional = null;
        }


        if (!response.ok) {

            throw new Error(
                professional?.detail ||
                "No se pudo cargar el perfil."
            );
        }


        adminEditTitle.textContent =
            `Editar a ${professional.first_name} ${professional.last_name}`;


        adminProfileDescription.value =
            professional.description || "";


        adminProfileYears.value =
            professional.years_experience ?? "";


        adminProfileWhatsapp.value =
            professional.whatsapp || "";


        adminProfileInstagram.value =
            professional.instagram || "";


        const categoryIds =
            (professional.categories || [])
                .map(category =>
                    String(category.id)
                );


        Array.from(
            adminProfileCategories.options
        ).forEach(option => {

            option.selected =
                categoryIds.includes(
                    option.value
                );
        });


        const locationIds =
            (professional.locations || [])
                .map(location =>
                    String(location.id)
                );


        Array.from(
            adminProfileLocations.options
        ).forEach(option => {

            option.selected =
                locationIds.includes(
                    option.value
                );
        });


        adminProfileEditPanel.hidden =
            false;


        adminProfileEditPanel.scrollIntoView({
            behavior: "smooth",
            block: "start"
        });

    } catch (error) {

        showMessage(
            error.message ||
            "No se pudo abrir la edición.",
            "error"
        );
    }
}


async function saveAdminProfessionalProfile() {

    if (!editingProfessionalId) {
        return;
    }


    const categoryIds =
        Array.from(
            adminProfileCategories.selectedOptions
        )
        .map(option =>
            Number(option.value)
        );


    const locationIds =
        Array.from(
            adminProfileLocations.selectedOptions
        )
        .map(option =>
            Number(option.value)
        );


    const payload = {

        description:
            adminProfileDescription.value.trim() ||
            null,

        years_experience:
            adminProfileYears.value === ""
                ? null
                : Number(adminProfileYears.value),

        whatsapp:
            adminProfileWhatsapp.value.trim() ||
            null,

        instagram:
            adminProfileInstagram.value.trim() ||
            null,

        category_ids:
            categoryIds,

        location_ids:
            locationIds,
    };


    const submitButton =
        adminProfileEditForm.querySelector(
            'button[type="submit"]'
        );


    submitButton.disabled =
        true;

    submitButton.textContent =
        "Guardando...";


    adminProfileEditMessage.hidden =
        true;


    try {

        const response =
            await fetch(
                `${API_BASE_URL}/api/professionals/admin/${editingProfessionalId}`,
                {
                    method: "PATCH",

                    headers:
                        getAdminHeaders(),

                    body:
                        JSON.stringify(payload),
                }
            );


        let result = null;

        try {
            result =
                await response.json();
        } catch {
            result = null;
        }


        if (response.status === 401) {

            clearAdminToken();

            showLogin();

            throw new Error(
                "La sesión administrativa venció o no es válida."
            );
        }


        if (!response.ok) {

            throw new Error(
                result?.detail ||
                "No se pudo guardar el perfil."
            );
        }


        adminProfileEditMessage.textContent =
            "Los cambios se guardaron correctamente.";

        adminProfileEditMessage.className =
            "form-message success";

        adminProfileEditMessage.hidden =
            false;


        showMessage(
            "Perfil actualizado correctamente.",
            "success"
        );


        await loadProfessionals();


        setTimeout(() => {

            adminProfileEditPanel.hidden =
                true;

        }, 700);


    } catch (error) {

        adminProfileEditMessage.textContent =
            error.message ||
            "No se pudieron guardar los cambios.";

        adminProfileEditMessage.className =
            "form-message error";

        adminProfileEditMessage.hidden =
            false;

    } finally {

        submitButton.disabled =
            false;

        submitButton.textContent =
            "Guardar cambios";
    }
}


/*
============================================================
RENDER PROFESIONAL — ADMIN
============================================================
*/

function renderAdminProfessional(
    item
) {

    const statusLabel =
        item.is_active
            ? "Activo"
            : "Inactivo";


    const statusClass =
        item.is_active
            ? "active"
            : "inactive";


    const actionLabel =
        item.is_active
            ? "Desactivar"
            : "Activar";


    return `
        <article
            class="profile-card admin-card"
            data-professional-id="${item.id}"
        >

            <div class="admin-card-header">

                <div>

                    <p class="eyebrow">
                        Profesional #${item.id}
                    </p>

                    <h2>
                        ${escapeHtml(item.first_name)}
                        ${escapeHtml(item.last_name)}
                    </h2>

                </div>


                <span
                    class="admin-status admin-status-${statusClass}"
                >
                    ${statusLabel}
                </span>

            </div>


            <div class="admin-card-grid">

                <div>

                    <strong>
                        Teléfono
                    </strong>

                    <p>
                        ${escapeHtml(item.phone)}
                    </p>

                </div>


                <div>

                    <strong>
                        WhatsApp
                    </strong>

                    <p>
                        ${
                            item.whatsapp
                                ? escapeHtml(item.whatsapp)
                                : "No informado"
                        }
                    </p>

                </div>


                <div>

                    <strong>
                        Experiencia
                    </strong>

                    <p>
                        ${
                            item.years_experience !== null
                                ? `${item.years_experience} años`
                                : "No informada"
                        }
                    </p>

                </div>


                <div>

                    <strong>
                        Instagram
                    </strong>

                    <p>
                        ${
                            item.instagram
                                ? escapeHtml(item.instagram)
                                : "No informado"
                        }
                    </p>

                </div>

            </div>


            <div class="admin-actions">

                <a
                    href="./profile.html?id=${encodeURIComponent(item.id)}"
                    class="button secondary-button"
                    target="_blank"
                    rel="noopener noreferrer"
                >
                    Ver perfil
                </a>


                <button
                    type="button"
                    class="secondary-button admin-edit-professional"
                    data-id="${item.id}"
                >
                    Editar
                </button>


                <button
                    type="button"
                    class="primary-button admin-toggle-status"
                    data-id="${item.id}"
                    data-active="${item.is_active}"
                >
                    ${actionLabel}
                </button>

            </div>

        </article>
    `;
}
/*
============================================================
PROFESIONALES
============================================================
*/

async function loadProfessionals() {

    professionalsLoadingState.hidden =
        false;

    professionalsEmptyState.hidden =
        true;

    professionalsList.innerHTML =
        "";


    try {

        const response =
            await fetch(
                `${API_BASE_URL}/api/professionals/admin/list`,
                {
                    headers:
                        getAdminHeaders(),
                }
            );


        if (response.status === 401) {

            clearAdminToken();

            showLogin();

            throw new Error(
                "La sesión administrativa venció o no es válida."
            );
        }


        let professionals = null;

        try {
            professionals =
                await response.json();
        } catch {
            professionals = null;
        }


        if (!response.ok) {

            throw new Error(
                professionals?.detail ||
                "No se pudieron cargar los profesionales."
            );
        }


        if (!Array.isArray(professionals)) {

            throw new Error(
                "La respuesta del servidor no tiene el formato esperado."
            );
        }


        professionalsLoadingState.hidden =
            true;


        if (professionals.length === 0) {

            professionalsEmptyState.hidden =
                false;

            return;
        }


        professionalsList.innerHTML =
            professionals
                .map(renderAdminProfessional)
                .join("");


        attachProfessionalActions();


    } catch (error) {

        professionalsLoadingState.hidden =
            true;


        showMessage(
            error.message ||
            "No se pudieron cargar los profesionales.",
            "error"
        );
    }
}


/*
============================================================
ACCIONES DE PROFESIONALES
============================================================
*/

function attachProfessionalActions() {

    document
        .querySelectorAll(
            ".admin-toggle-status"
        )
        .forEach(button => {

            button.addEventListener(
                "click",
                async () => {

                    const professionalId =
                        Number(
                            button.dataset.id
                        );

                    const currentlyActive =
                        button.dataset.active ===
                        "true";


                    const newStatus =
                        !currentlyActive;


                    button.disabled =
                        true;

                    button.textContent =
                        "Guardando...";


                    try {

                        const response =
                            await fetch(
                                `${API_BASE_URL}/api/professionals/${professionalId}/status?is_active=${newStatus}`,
                                {
                                    method: "PATCH",

                                    headers:
                                        getAdminHeaders(),
                                }
                            );


                        let result = null;

                        try {
                            result =
                                await response.json();
                        } catch {
                            result = null;
                        }


                        if (
                            response.status ===
                            401
                        ) {

                            clearAdminToken();

                            showLogin();

                            throw new Error(
                                "La sesión administrativa venció o no es válida."
                            );
                        }


                        if (!response.ok) {

                            throw new Error(
                                result?.detail ||
                                "No se pudo cambiar el estado."
                            );
                        }


                        showMessage(
                            newStatus
                                ? "Profesional activado correctamente."
                                : "Profesional desactivado correctamente.",
                            "success"
                        );


                        await loadProfessionals();


                    } catch (error) {

                        showMessage(
                            error.message ||
                            "No se pudo cambiar el estado.",
                            "error"
                        );


                        button.disabled =
                            false;

                        button.textContent =
                            currentlyActive
                                ? "Desactivar"
                                : "Activar";
                    }

                }
            );

        });


    /*
    --------------------------------------------------------
    EDITAR PROFESIONAL
    --------------------------------------------------------
    */

    document
        .querySelectorAll(
            ".admin-edit-professional"
        )
        .forEach(button => {

            button.addEventListener(
                "click",
                () => {

                    const professionalId =
                        Number(
                            button.dataset.id
                        );


                    openAdminProfileEditor(
                        professionalId
                    );

                }
            );

        });
}


/*
============================================================
SOLICITUDES PENDIENTES
============================================================
*/

async function loadPending() {

    loadingState.hidden =
        false;

    emptyState.hidden =
        true;

    pendingList.innerHTML =
        "";


    try {

        const response =
            await fetch(
                `${API_BASE_URL}/api/admin/verifications/pending`,
                {
                    headers:
                        getAdminHeaders(),
                }
            );


        if (response.status === 401) {

            clearAdminToken();

            showLogin();

            throw new Error(
                "La sesión administrativa venció o no es válida."
            );
        }


        let pending = null;

        try {
            pending =
                await response.json();
        } catch {
            pending = null;
        }


        if (!response.ok) {

            throw new Error(
                pending?.detail ||
                "No se pudieron cargar las solicitudes."
            );
        }


        loadingState.hidden =
            true;


        if (
            !Array.isArray(pending) ||
            pending.length === 0
        ) {

            emptyState.hidden =
                false;

            return;
        }


        pendingList.innerHTML =
            pending
                .map(renderProfessional)
                .join("");


        attachPendingActions();


    } catch (error) {

        loadingState.hidden =
            true;


        showMessage(
            error.message ||
            "No se pudieron cargar las solicitudes.",
            "error"
        );
    }
}


/*
============================================================
ACCIONES DE SOLICITUDES
============================================================
*/

function attachPendingActions() {

    document
        .querySelectorAll(
            ".admin-approve"
        )
        .forEach(button => {

            button.addEventListener(
                "click",
                () => {

                    const verificationId =
                        Number(
                            button.dataset.id
                        );

                    approveVerification(
                        verificationId
                    );

                }
            );

        });


    document
        .querySelectorAll(
            ".admin-reject"
        )
        .forEach(button => {

            button.addEventListener(
                "click",
                () => {

                    const verificationId =
                        Number(
                            button.dataset.id
                        );

                    rejectVerification(
                        verificationId
                    );

                }
            );

        });
}


async function approveVerification(
    verificationId
) {

    try {

        const response =
            await fetch(
                `${API_BASE_URL}/api/admin/verifications/${verificationId}`,
                {
                    method: "PATCH",

                    headers:
                        getAdminHeaders(),

                    body: JSON.stringify({
                        status: "verified",
                    }),
                }
            );


        let result = null;

        try {
            result =
                await response.json();
        } catch {
            result = null;
        }


        if (response.status === 401) {

            clearAdminToken();

            showLogin();

            throw new Error(
                "La sesión administrativa venció o no es válida."
            );
        }


        if (!response.ok) {

            throw new Error(
                result?.detail ||
                "No se pudo aprobar la solicitud."
            );
        }


        showMessage(
            "Profesional verificado correctamente.",
            "success"
        );


        await loadPending();

        await loadProfessionals();


    } catch (error) {

        showMessage(
            error.message ||
            "No se pudo aprobar la solicitud.",
            "error"
        );
    }
}


async function rejectVerification(
    verificationId
) {

    try {

        const response =
            await fetch(
                `${API_BASE_URL}/api/admin/verifications/${verificationId}`,
                {
                    method: "PATCH",

                    headers:
                        getAdminHeaders(),

                    body: JSON.stringify({
                        status: "rejected",
                    }),
                }
            );


        let result = null;

        try {
            result =
                await response.json();
        } catch {
            result = null;
        }


        if (response.status === 401) {

            clearAdminToken();

            showLogin();

            throw new Error(
                "La sesión administrativa venció o no es válida."
            );
        }


        if (!response.ok) {

            throw new Error(
                result?.detail ||
                "No se pudo rechazar la solicitud."
            );
        }


        showMessage(
            "Solicitud rechazada.",
            "success"
        );


        await loadPending();


    } catch (error) {

        showMessage(
            error.message ||
            "No se pudo rechazar la solicitud.",
            "error"
        );
    }
}


/*
============================================================
LOGIN FORM
============================================================
*/

if (loginForm) {

    loginForm.addEventListener(
        "submit",
        async event => {

            event.preventDefault();

            hideLoginMessage();


            const username =
                usernameInput.value.trim();

            const password =
                passwordInput.value;


            if (!username || !password) {

                showLoginMessage(
                    "Ingresá usuario y contraseña."
                );

                return;
            }


            const submitButton =
                loginForm.querySelector(
                    'button[type="submit"]'
                );


            submitButton.disabled =
                true;

            submitButton.textContent =
                "Ingresando...";


            try {

                await login(
                    username,
                    password
                );


                showAdminContent();


                await loadPending();

                await loadProfessionals();


            } catch (error) {

                clearAdminToken();

                showLoginMessage(
                    error.message ||
                    "No se pudo iniciar sesión."
                );

            } finally {

                submitButton.disabled =
                    false;

                submitButton.textContent =
                    "Ingresar";
            }

        }
    );

}


/*
============================================================
REFRESCAR
============================================================
*/

if (refreshButton) {

    refreshButton.addEventListener(
        "click",
        async () => {

            hideMessage();

            await loadPending();

            await loadProfessionals();

        }
    );

}


/*
============================================================
CANCELAR EDICIÓN
============================================================
*/

if (adminProfileEditCancel) {

    adminProfileEditCancel.addEventListener(
        "click",
        () => {

            adminProfileEditPanel.hidden =
                true;

            editingProfessionalId =
                null;

            adminProfileEditMessage.hidden =
                true;
        }
    );

}


/*
============================================================
GUARDAR EDICIÓN
============================================================
*/

if (adminProfileEditForm) {

    adminProfileEditForm.addEventListener(
        "submit",
        async event => {

            event.preventDefault();

            await saveAdminProfessionalProfile();

        }
    );

}


/*
============================================================
INICIALIZACIÓN
============================================================
*/

async function initializeAdmin() {

    const token =
        getAdminToken();


    if (!token) {

        showLogin();

        return;
    }


    try {

        showAdminContent();


        await loadPending();

        await loadProfessionals();


    } catch {

        clearAdminToken();

        showLogin();
    }
}


initializeAdmin();