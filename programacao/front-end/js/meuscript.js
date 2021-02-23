$(function() { // quando o documento estiver pronto/carregado
    
    // função para exibir cachorros na tabela
    function exibir_cachorros() {
        $.ajax({
            url: 'http://localhost:5000/listar_cachorros',
            method: 'GET',
            dataType: 'json', // os dados são recebidos no formato json
            success: listar, // chama a função listar para processar o resultado
            error: function() {
                alert("erro ao ler dados, verifique o backend");
            }
        });
        function listar (cachorros) {
            var lin = "";
            // percorrer a lista de pessoas retornadas; 
            for (cachorro of cachorros) { //i vale a posição no vetor
                lin += `<tr>
                    <td> ${cachorro.nome}</td>
                    <td> ${cachorro.raca}</td>
                    <td> ${cachorro.porte}</td>  
                    <td> ${cachorro.pelagem}</td>
                </tr>`;
                
                // adiciona a linha no corpo da tabela
                $('#corpoTabelaCachorros').html(lin);
            }
        }
        mostrar_conteudo("tabelaCachorros");  
    }

    // função que mostra um conteúdo e esconde os outros
    function mostrar_conteudo(identificador) {
        // esconde todos os conteúdos
        $("#tabelaCachorros").addClass('invisible');
        $("#conteudoInicial").addClass('invisible');
        // torna o conteúdo escolhido visível
        $("#"+identificador).removeClass('invisible');      
    }

    // código para mapear o click do link Listar
    $("#linkListarCachorros").click(function() {
        exibir_cachorros();
    });
    
    // código para mapear click do link Inicio
    $("#linkInicio").click(function() {
        mostrar_conteudo("conteudoInicial");
    });

    // código para mapear click do botão incluir pessoa
    $('#btIncluirCachorros').click(function() {
        //pegar dados da tela
        var nome = $("#campoNome").val();
        var raca = $("#campoRaca").val();
        var porte = $("#campoPorte").val();
        var pelagem = $("#campoPelagem").val();
        // preparar dados no formato json
        var dados = JSON.stringify({ nome: nome, raca: raca, porte: porte, pelagem: pelagem });
        // fazer requisição para o back-end
        $.ajax({
            url: 'http://localhost:5000/incluir_cachorros',
            type: 'POST',
            dataType: 'json', // os dados são recebidos no formato json
            contentType: 'application/json', // tipo dos dados enviados
            data: dados, // estes são os dados enviados
            success: cachorroIncluido, // chama a função listar para processar o resultado
            error: erroAoIncluir
        });

        function cachorroIncluido (retorno) {
            if (retorno.resultado == "ok") { // a operação deu certo?
                // informar resultado de sucesso
                alert("Cachorro incluído com sucesso!");
                // limpar os campos
                $("#campoNome").val("");
                $("#campoRaca").val("");
                $("#campoPorte").val("");
                $("#campoPelagem").val("");
            } else {
                // informar mensagem de erro
                alert(retorno.resultado + ":" + retorno.detalhes);
            }            
        }
    
        function erroAoIncluir (retorno) {
            // informar mensagem de erro
            alert('Erro ao incluir!');
            // alert("ERRO: "+retorno.resultado + ":" + retorno.detalhes);
        }
    });

    // código a ser executado quando a janela de inclusão de pessoas for fechada
    $('#modalIncluirCachorros').on('hide.bs.modal', function (e) {
        // se a página de listagem não estiver invisível
        if (! $("#tabelaCachorros").hasClass('invisible')) {
            // atualizar a página de listagem
            exibir_cachorros();
        }
    });
    // a função abaixo é executada quando a página abre
    mostrar_conteudo("conteudoInicial");
});