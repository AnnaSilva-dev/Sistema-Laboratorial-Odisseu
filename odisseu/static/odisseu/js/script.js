const temaSalvo = localStorage.getItem("tema");

const btnClaro = document.getElementById("btn-tema-claro");
const btnEscuro = document.getElementById("btn-tema-escuro");
const btnTema = document.getElementById("btn-tema");

function aplicarTema(tema) {

    if (tema === "claro") {

        document.body.classList.remove("modo-escuro");
        document.body.classList.add("modo-claro");

    } else {

        document.body.classList.remove("modo-claro");
        document.body.classList.add("modo-escuro");

    }

    localStorage.setItem("tema", tema);

    atualizarBotoesTema();
}


function atualizarBotoesTema() {

    const temaAtual = localStorage.getItem("tema");

    if (btnClaro && btnEscuro) {

        const iconeTemaClaro = btnClaro.querySelector("i");
        const iconeTemaEscuro = btnEscuro.querySelector("i");

        if (temaAtual === "claro") {

            iconeTemaClaro.classList.replace("bi-circle", "bi-circle-fill");
            iconeTemaEscuro.classList.replace("bi-circle-fill", "bi-circle");

        } else {

            iconeTemaEscuro.classList.replace("bi-circle", "bi-circle-fill");
            iconeTemaClaro.classList.replace("bi-circle-fill", "bi-circle");

        }
    }


    if (btnTema) {

        const iconeTema = btnTema.querySelector("i");

        if (temaAtual === "claro") {

            iconeTema.classList.replace("bi-moon", "bi-sun");

        } else {

            iconeTema.classList.replace("bi-sun", "bi-moon");

        }
    }
}


if (temaSalvo === "claro") {

    aplicarTema("claro");

} else {

    aplicarTema("escuro");

}


if (btnClaro) {

    btnClaro.addEventListener("click", function () {

        aplicarTema("claro");

    });

}


if (btnEscuro) {

    btnEscuro.addEventListener("click", function () {

        aplicarTema("escuro");

    });

}


if (btnTema) {

    btnTema.addEventListener("click", function () {

        const temaAtual = localStorage.getItem("tema");

        if (temaAtual === "escuro") {

            aplicarTema("claro");

        } else {

            aplicarTema("escuro");

        }

    });

}

const paciente = document.querySelector("#paciente");

if (paciente) {
    new TomSelect(paciente, {
        placeholder: "Digite o nome do paciente",
        searchField: ["text"],
        create: false
    });
}
document.addEventListener("DOMContentLoaded", function () {

    // Pagina de exames
    document.querySelectorAll(".exames-all").forEach(function (grupo) {

        const mestre = grupo.querySelector(".selecionar_todos");
        const exames = grupo.querySelectorAll('input[name="exames"]');

        if (!mestre) return;

        mestre.addEventListener("change", function () {

            exames.forEach(function (exame) {
                exame.checked = mestre.checked;
            });

            grupo.classList.toggle(
                "grupo_selecionado",
                mestre.checked
            );
        });

        exames.forEach(function (exame) {

            exame.addEventListener("change", function () {

                const todosMarcados =
                    exames.length > 0 &&
                    Array.from(exames).every(function (exame) {
                        return exame.checked;
                    });

                mestre.checked = todosMarcados;

                grupo.classList.toggle(
                    "grupo_selecionado",
                    todosMarcados
                );
            });

        });

    });


    // pag de liberar resultados
    document.querySelectorAll(".grupo_paciente").forEach(function (grupo) {

        const mestre = grupo.querySelector(".selecionar_todos");
        const resultados = grupo.querySelectorAll('input[name="resultados"]');

        if (!mestre) return;

        mestre.addEventListener("change", function () {

            resultados.forEach(function (resultado) {
                resultado.checked = mestre.checked;
            });

            grupo.classList.toggle(
                "grupo_selecionado",
                mestre.checked
            );
        });

        resultados.forEach(function (resultado) {

            resultado.addEventListener("change", function () {

                const todosMarcados =
                    resultados.length > 0 &&
                    Array.from(resultados).every(function (resultado) {
                        return resultado.checked;
                    });

                mestre.checked = todosMarcados;

                grupo.classList.toggle(
                    "grupo_selecionado",
                    todosMarcados
                );
            });

        });

    });

});

const cpf = document.querySelector('.cpf');

if (cpf) {
    cpf.addEventListener('input', (e) => {
        let v = e.target.value.replace(/\D/g, '');
        v = v.replace(/^(\d{3})(\d)/, '$1.$2');
        v = v.replace(/^(\d{3})\.(\d{3})(\d)/, '$1.$2.$3');
        v = v.replace(/\.(\d{3})(\d)/, '.$1-$2');
        e.target.value = v.slice(0, 14);
    });
}

const cns = document.querySelector('.cns');

if (cns) {
    cns.addEventListener('input', (e) => {
        let v = e.target.value.replace(/\D/g, '').slice(0, 15);
        v = v.replace(/(\d{3})(\d)/, '$1 $2');
        v = v.replace(/(\d{3}) (\d{4})(\d)/, '$1 $2 $3');
        v = v.replace(/(\d{3}) (\d{4}) (\d{4})(\d)/, '$1 $2 $3 $4');
        e.target.value = v;
    });
}

const telefone = document.querySelector('.telefone');

if (telefone) {
    telefone.addEventListener('input', (e) => {
        let v = e.target.value.replace(/\D/g, '').slice(0, 11);

        if (v.length <= 2) {
            v = '(' + v;
        } 
        else if (v.length <= 7) {
            v = '(' + v.slice(0, 2) + ') ' + v.slice(2);
        } 
        else {
            v = '(' + v.slice(0, 2) + ') ' + v.slice(2, 7) + '-' + v.slice(7);
        }

        e.target.value = v;
    });
}

