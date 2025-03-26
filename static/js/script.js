document.addEventListener("DOMContentLoaded", function () {
    document
        .getElementById("exibir-carros")
        .addEventListener("click", function (event) {
            event.preventDefault();
            var tabela = document.getElementById("tabelaCarros");
            tabela.style.display = tabela.style.display === "none" ? "block" : "none";
        });

    document.querySelectorAll(".remover").forEach((button) => {
        button.addEventListener("click", function () {
            let idCarro = this.getAttribute("data-id");
            if (confirm(`Tem certeza que deseja excluir o carro com ID ${idCarro}?`)) {
                fetch("/deletar_carro", {
                    method: "DELETE",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({ id: idCarro }),
                })
                    .then((response) => response.json())
                    .then((data) => {
                        alert(data.mensagem);
                        location.reload();
                    })
                    .catch((error) => console.error("Erro:", error));
            }
        });
    });

    document.querySelectorAll(".alterar").forEach((button) => {
        button.addEventListener("click", function () {

            let idCarro = this.getAttribute("data-id");
            let placa = this.getAttribute("data-placa");
            let marca = this.getAttribute("data-marca");
            let modelo = this.getAttribute("data-modelo");
            let ano = this.getAttribute("data-ano");

            document.getElementById("idCarro").value = idCarro;
            document.getElementById("placa").value = placa;
            document.getElementById("marca").value = marca;
            document.getElementById("modelo").value = modelo;
            document.getElementById("ano").value = ano;

            document.getElementById("formEdicao").style.display = "block";
            document.getElementById("tabelaCarros").style.display = "none"; // Oculta a tabela

        });
    });

    document.getElementById("cancelarEdicao").addEventListener("click", function () {
        document.getElementById("formEdicao").style.display = "none";
        document.getElementById("tabelaCarros").style.display = "block";
    });


    document.getElementById("formAlterar").addEventListener("submit", function (event) {
        event.preventDefault();

        let idCarro = document.getElementById("idCarro").value;
        let placa = document.getElementById("placa").value;
        let marca = document.getElementById("marca").value;
        let modelo = document.getElementById("modelo").value;
        let ano = document.getElementById("ano").value;

        fetch("/alterar_carro", {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                id: idCarro,
                placa: placa,
                marca: marca,
                modelo: modelo,
                ano: ano,
            }),
        })
            .then((response) => response.json())
            .then((data) => {
                alert(data.mensagem);
                location.reload();
            })
            .catch((error) => console.error("Erro:", error));
    });
});
