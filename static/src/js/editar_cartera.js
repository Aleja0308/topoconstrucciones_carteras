let editandoInputTipoPunto;
let editandoInputPunto;
let editandoInputAlturaInstrumental;
let editandoInputVistaMas;
let editandoInputVistaMenos;
let editandoInputCota;
let botonEditarPunto;
let puntoId;
let editandoInputIdCarteraNivelacion;
let editarPuntoResultadoSpan;
let procesandoFetch = false;
let idCarteraNivelacion;


document.addEventListener('DOMContentLoaded', function () {
    editandoInputTipoPunto = document.querySelector('#id_tipo_punto');
    editandoInputPunto = document.querySelector('#id_punto');
    editandoInputAlturaInstrumental = document.querySelector('#id_altura_instrumental');
    editandoInputVistaMas = document.querySelector('#id_vista_mas');
    editandoInputVistaMenos = document.querySelector('#id_vista_menos');
    editandoInputCota = document.querySelector('#id_cota');
    editandoInputIdCarteraNivelacion = document.querySelector('#id_cartera_nivelacion');
    botonEditarPunto = document.querySelector('.boton-editar-punto');
    editarPuntoResultadoSpan = document.querySelector('.editar-punto-resultado');
    
    idCarteraNivelacion = editandoInputIdCarteraNivelacion.value;
    const urlPath = window.location.pathname; // Obtiene la ruta completa de la URL
    puntoId = urlPath.split('/')[2]; // Divide la URL por '/' y obtiene el tercer elemento (el ID de la cartera)

    editandoInputTipoPunto.onchange = () => handleEditandoInputTipoPuntoOnChange();
    botonEditarPunto.onclick = (event) => botonEditarPuntoHandleClick(event);
});

const handleEditandoInputTipoPuntoOnChange = function () {
    if (editandoInputTipoPunto.value == 2) {
        editandoInputVistaMas.classList.add("opacity-50", "cursor-not-allowed");
        editandoInputVistaMas.setAttribute("readonly", true);
        editandoInputVistaMas.value = null;
    } else if (editandoInputTipoPunto.value == 3) {
        editandoInputVistaMas.classList.remove("opacity-50", "cursor-not-allowed");
        editandoInputVistaMas.removeAttribute("readonly", true);
    }
}

const botonEditarPuntoHandleClick = function (event) {
    event.preventDefault();
    if (!procesandoFetch) {
        editarPuntoResultadoSpan.textContent = '';
        editarPuntoFetch();
    } else {
        editarPuntoResultadoSpan.textContent = 'Espera por favor, se está procesando el punto...';
    }
}

const editarPuntoFetch = function () {
    let formData;
    if (editandoInputTipoPunto.value == 1) {
        formData = {
            tipo_punto: editandoInputTipoPunto.value,
            punto: editandoInputPunto.value,
            vista_mas: editandoInputVistaMas.value,
            cota: editandoInputCota.value
        };
    } else if (editandoInputTipoPunto.value == 2){
        formData = {
            tipo_punto: editandoInputTipoPunto.value,
            punto: editandoInputPunto.value,
            vista_menos: editandoInputVistaMenos.value,
        };
    } else if(editandoInputTipoPunto.value == 3) {
        formData = {
            tipo_punto: editandoInputTipoPunto.value,
            punto: editandoInputPunto.value,
            vista_mas: editandoInputVistaMas.value,
            vista_menos: editandoInputVistaMenos.value,
        };
    }
    procesandoFetch = true;
    fetch(`/editar_punto/${puntoId}/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie("csrftoken") // Para seguridad
        },
        body: JSON.stringify(formData)
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                editarPuntoResultadoSpan.textContent = data.message;
                setTimeout(() => {
                    window.location = `/ver_cartera/${idCarteraNivelacion}/`;
                }, 1000)
            } else {
                editarPuntoResultadoSpan.textContent = data.message;
                procesandoFetch = false;
            }
        })
        .catch(error => {
            procesandoFetch = false;
            console.error("Error:", error);
            editarPuntoResultadoSpan.textContent = data.message;
            timeoutGuardarPuntoResultado = setTimeout(() => {
                editarPuntoResultadoSpan.textContent = '';
            }, 5000);
        });
}

const getCookie = function (name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        let cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            let cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === name + "=") {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}