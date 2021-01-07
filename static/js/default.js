$(document).ready(function () {
    var namespace = "/fsic";
    var socket = io.connect("http://" + document.domain + ":" + location.port + namespace);

    socket.on("connect", function() {
        console.log("Connected");
    });

    socket.on("disconnect", function() {
        console.log("Disconnected");
    });

    socket.on("message-individual",function(message){
        console.log(message)
        if($("#usuario").html() == message.destino || $("#usuario").html() == message.fuente){
            $("#chat-output").append(
                "<div>" + message.contenido + " (" + message.fuente + ", " + message.fecha + ", " + message.lugar + ")" + "</div>"
            );
            $("#chat-output").scrollTop($("#chat-output")[0].scrollHeight);
        }
    });

    socket.on("contacto-seleccionado", function(message) {
        console.log(message)
        if($("#usuario").html() == message.destino || $("#usuario").html() == message.fuente){
            $("#chat-output").append(
                "<div>" + message.contenido + "</div>"
                );
            $("#chat-output").scrollTop($("#chat-output")[0].scrollHeight);
        }
    });

    $(".contacto_check").change(function(){
        if($(this).is(':checked')){
            console.log('Checked')
        } else{
            console.log('Unchecked')
        }
        var cantidad_seleccionados = $(".contacto_check:checked").length;
        var seleccionados = [];
        $("#chat-output").html("");
        if (cantidad_seleccionados == 0){
            
        }
        else{
            $(".contacto_check:checked").each(function(){
                seleccionados.push($(this).val());
            });
            socket.emit("contacto-seleccionado", [$("#usuario").html(), seleccionados]);
            console.log("solicitud historial");
        }
        $("#chat-input").val("");
        return false;
    });

    $("#clear-button").on("click", function () {
        $("#chat-input").val("");
    });

    $("#chat-form").on("submit", function () {
        var cantidad_seleccionados = $(".contacto_check:checked").length;
        var seleccionados = [];
        if (cantidad_seleccionados == 0){
            socket.emit("new-message", $("#chat-input").val());
        }
        else{
            $(".contacto_check:checked").each(function(){
                seleccionados.push($(this).val());
            });
            socket.emit("new-message-individual", [$("#chat-input").val(), $("#usuario").html(), seleccionados]);
            console.log("enviado mensaje ind");
        }
        $("#chat-input").val("");
        return false;
    });


});