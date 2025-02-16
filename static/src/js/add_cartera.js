let registrandoInputTipoPunto;
let registrandoInputPunto;
let registrandoInputAlturaInstrumental;
let registrandoInputVistaMas;
let registrandoInputVistaMenos;
let registrandoInputCota;
let botonGuardarPunto;
let carteraId;
let cuerpoTablaPuntosCartera;
let filaAñadirPuntoInicial;
let guardarPuntoResultadoSpan;
let timeoutGuardarPuntoResultado;

const seleccionarTodosLosInputsFila = function (filaAñadirPunto) {
    registrandoInputTipoPunto = filaAñadirPunto.querySelector('.tipo-punto');
    registrandoInputPunto = filaAñadirPunto.querySelector('.punto');
    registrandoInputAlturaInstrumental = filaAñadirPunto.querySelector('.altura-instrumental');
    registrandoInputVistaMas = filaAñadirPunto.querySelector('.vista-mas');
    registrandoInputVistaMenos = filaAñadirPunto.querySelector('.vista-menos');
    registrandoInputCota = filaAñadirPunto.querySelector('.cota');

    registrandoInputAlturaInstrumental.value = '';
    registrandoInputVistaMas.value = '';
    registrandoInputVistaMenos.value = '';
    registrandoInputCota.value = '';

}

const botonGuardarPuntoHandleClick = function (event) {
    event.preventDefault();
    if (registrandoInputTipoPunto.value == 1) {
        guardarPuntoBM();
    } else if (registrandoInputTipoPunto.value == 2) {
        guardarPuntoDelta();
    } else if (registrandoInputTipoPunto.value == 3) {
        guardarPuntoCambio();
    }
}

const registrandoInputTipoPuntoHandleChange = function (event) {
    if (event.target.value == 2) {
        habilitarCamposRegistrandoDelta();
    } else if (event.target.value == 3) {
        habilitarCamposRegistrandoCambio();
    }
}

// Función para obtener el token CSRF
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

const guardarPuntoBM = function () {
    let formData = {
        punto: registrandoInputPunto.value,
        vista_mas: registrandoInputVistaMas.value,
        cota: registrandoInputCota.value
    };
    fetch(`/guardar-punto-bm/${carteraId}/`, {
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
                guardarPuntoResultadoSpan.textContent = data.message;
                timeoutGuardarPuntoResultado = setTimeout(() => {
                    guardarPuntoResultadoSpan.textContent = '';
                }, 5000);
                inhabilitarInputsPuntoRegistrado();
                asignarValoresInputPuntoBMGuardado(data.punto, data.alturaInstrumental, data.vistaMas, data.cota);
                renderNuevaFilaPunto();
            } else {
                guardarPuntoResultadoSpan.textContent = data.message;
                timeoutGuardarPuntoResultado = setTimeout(() => {
                    guardarPuntoResultadoSpan.textContent = '';
                }, 5000);
            }
        })
        .catch(error => {
            console.error("Error:", error);
            guardarPuntoResultadoSpan.textContent = data.message;
            timeoutGuardarPuntoResultado = setTimeout(() => {
                guardarPuntoResultadoSpan.textContent = '';
            }, 5000);
        });
}

const guardarPuntoDelta = function () {
    let formData = {
        punto: registrandoInputPunto.value,
        vista_menos: registrandoInputVistaMenos.value,
    };
    fetch(`/guardar-punto-delta/${carteraId}/`, {
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
                guardarPuntoResultadoSpan.textContent = data.message;
                timeoutGuardarPuntoResultado = setTimeout(() => {
                    guardarPuntoResultadoSpan.textContent = '';
                }, 5000);
                inhabilitarInputsPuntoRegistrado();
                asignarValoresInputPuntoDeltaGuardado(data.punto, data.alturaInstrumental, data.vistaMenos, data.cota);
                renderNuevaFilaPunto();
            } else {
                guardarPuntoResultadoSpan.textContent = data.message;
                timeoutGuardarPuntoResultado = setTimeout(() => {
                    guardarPuntoResultadoSpan.textContent = '';
                }, 5000);
            }
        })
        .catch(error => {
            console.error("Error:", error);
            guardarPuntoResultadoSpan.textContent = data.message;
            timeoutGuardarPuntoResultado = setTimeout(() => {
                guardarPuntoResultadoSpan.textContent = '';
            }, 5000);
        });
}

const guardarPuntoCambio = function () {
    let formData = {
        punto: registrandoInputPunto.value,
        vista_mas: registrandoInputVistaMas.value,
        vista_menos: registrandoInputVistaMenos.value,
    };
    fetch(`/guardar-punto-cambio/${carteraId}/`, {
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
                guardarPuntoResultadoSpan.textContent = data.message;
                timeoutGuardarPuntoResultado = setTimeout(() => {
                    guardarPuntoResultadoSpan.textContent = '';
                }, 5000);
                inhabilitarInputsPuntoRegistrado();
                asignarValoresInputPuntoCambioGuardado(data.punto, data.alturaInstrumental, data.vistaMas, data.vistaMenos, data.cota);
                renderNuevaFilaPunto();
            } else {
                guardarPuntoResultadoSpan.textContent = data.message;
                timeoutGuardarPuntoResultado = setTimeout(() => {
                    guardarPuntoResultadoSpan.textContent = '';
                }, 5000);
            }
        })
        .catch(error => {
            console.error("Error:", error);
            guardarPuntoResultadoSpan.textContent = data.message;
            timeoutGuardarPuntoResultado = setTimeout(() => {
                guardarPuntoResultadoSpan.textContent = '';
            }, 5000);
        });
}

const renderNuevaFilaPunto = function () {
    const nuevaFilaPunto = filaAñadirPuntoInicial.cloneNode(true);
    const nuevoSelectTipoPunto = nuevaFilaPunto.querySelector('.tipo-punto');
    while (nuevoSelectTipoPunto.options.length > 0) {
        nuevoSelectTipoPunto.remove(0);
    }
    const nuevoOptionDelta = document.createElement('option');
    nuevoOptionDelta.value = 2;
    nuevoOptionDelta.textContent = "Delta";
    nuevoOptionDelta.selected = true;

    const nuevoOptionCambio = document.createElement('option');
    nuevoOptionCambio.value = 3;
    nuevoOptionCambio.textContent = "Cambio";

    nuevoSelectTipoPunto.appendChild(nuevoOptionDelta);
    nuevoSelectTipoPunto.appendChild(nuevoOptionCambio);

    cuerpoTablaPuntosCartera.appendChild(nuevaFilaPunto);
    seleccionarTodosLosInputsFila(nuevaFilaPunto);
    registrandoInputAlturaInstrumental.readOnly = true;
    registrandoInputCota.readOnly = true;
    habilitarCamposRegistrandoDelta();
    registrandoInputTipoPunto.onchange = (event) => registrandoInputTipoPuntoHandleChange(event);
}

const habilitarCamposRegistrandoDelta = function () {
    registrandoInputVistaMas.readOnly = true;
    registrandoInputVistaMenos.readOnly = false;
    registrandoInputVistaMas.classList.add('cursor-not-allowed', 'opacity-50');

}

const habilitarCamposRegistrandoCambio = function () {
    registrandoInputVistaMas.readOnly = false;
    registrandoInputVistaMenos.readOnly = false;
    registrandoInputVistaMas.classList.remove('cursor-not-allowed', 'opacity-50');
}

const inhabilitarInputsPuntoRegistrado = function () {
    registrandoInputTipoPunto.readOnly = true;
    registrandoInputPunto.readOnly = true;
    registrandoInputAlturaInstrumental.readOnly = true;
    registrandoInputVistaMas.readOnly = true;
    registrandoInputVistaMenos.readOnly = true;
    registrandoInputCota.readOnly = true;

    registrandoInputTipoPunto.onchange = null;
}

const asignarValoresInputPuntoBMGuardado = function (punto, alturaInstrumental, vistaMas, cota) {
    registrandoInputTipoPunto.value = 1;
    registrandoInputPunto.value = punto;
    registrandoInputAlturaInstrumental.value = alturaInstrumental;
    registrandoInputVistaMas.value = vistaMas;
    registrandoInputCota.value = cota;
}

const asignarValoresInputPuntoDeltaGuardado = function (punto, alturaInstrumental, vistaMenos, cota) {
    registrandoInputTipoPunto.value = 2;
    registrandoInputPunto.value = punto;
    registrandoInputAlturaInstrumental.value = alturaInstrumental;
    registrandoInputVistaMenos.value = vistaMenos;
    registrandoInputCota.value = cota;
}

const asignarValoresInputPuntoCambioGuardado = function (punto, alturaInstrumental, vistaMas, vistaMenos, cota) {
    registrandoInputTipoPunto.value = 3;
    registrandoInputPunto.value = punto;
    registrandoInputAlturaInstrumental.value = alturaInstrumental;
    registrandoInputVistaMas.value = vistaMas;
    registrandoInputVistaMenos.value = vistaMenos;
    registrandoInputCota.value = cota;
}

document.addEventListener('DOMContentLoaded', function () {
    cuerpoTablaPuntosCartera = document.querySelector('.cuerpo-tabla-puntos-cartera');
    filaAñadirPuntoInicial = document.querySelector('.fila-añadir-punto-inicial');
    botonGuardarPunto = document.querySelector('.boton-guardar-punto');
    guardarPuntoResultadoSpan = document.querySelector('.guardar-punto-resultado');
    const urlPath = window.location.pathname; // Obtiene la ruta completa de la URL
    carteraId = urlPath.split('/')[2]; // Divide la URL por '/' y obtiene el tercer elemento (el ID de la cartera)

    seleccionarTodosLosInputsFila(filaAñadirPuntoInicial);
    registrandoInputTipoPunto.onchange = (event) => registrandoInputTipoPuntoHandleChange(event);

    botonGuardarPunto.onclick = (event) => botonGuardarPuntoHandleClick(event);
});

