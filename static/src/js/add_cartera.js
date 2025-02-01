let inputsTipoPunto;
let inputsPunto;
let inputsAlturaInstrumental;
let inputsVistaMas;
let inputsVistaMenos;
let inputsCota;
let puntoRegistrandose = 0;
let botonGuardarPunto;
let carteraId;

const seleccionarTodosLosInputs = function () {
    inputsTipoPunto = document.querySelectorAll('.tipo-punto');
    inputsPunto = document.querySelectorAll('.punto');
    inputsAlturaInstrumental = document.querySelectorAll('.altura-instrumental');
    inputsVistaMas = document.querySelectorAll('.vista-mas');
    inputsVistaMenos = document.querySelectorAll('.vista-menos');
    inputsCota = document.querySelectorAll('.cota');
}

const botonGuardarPuntoHandleClick = function (event) {
    event.preventDefault();
    if (inputsTipoPunto[puntoRegistrandose].value == 1){
        guardarPuntoBM();
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
        punto: inputsPunto[puntoRegistrandose].value,
        vista_mas: inputsVistaMas[puntoRegistrandose].value,
        cota: inputsCota[puntoRegistrandose].value
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
            alert(data.message);
        })
        .catch(error => {
            console.error("Error:", error);
            alert("Error al guardar el punto BM");
        });
}

document.addEventListener('DOMContentLoaded', function () {
    console.log("Carga el JS");
    seleccionarTodosLosInputs();
    botonGuardarPunto = document.querySelector('.boton-guardar-punto');
    const urlPath = window.location.pathname; // Obtiene la ruta completa de la URL
    carteraId = urlPath.split('/')[2]; // Divide la URL por '/' y obtiene el tercer elemento (el ID de la cartera)
    botonGuardarPunto.onclick = (event) => botonGuardarPuntoHandleClick(event);
});

