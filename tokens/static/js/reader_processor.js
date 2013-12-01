var initialMessage;
var messageStarted;
var messageStopped;
var messageError;
var doProcess=true;

$(function() {
    initialMessage = $("#messageBox").text();
    messageStarted = $("#messageStarted").html();
    messageStopped = $("#messageStoped").html();
    messageError = $("#messageError").html();
});

String.prototype.format = String.prototype.f = function() {
    var s = this,
        i = arguments.length;

    while (i--) {
        s = s.replace(new RegExp('\\{' + i + '\\}', 'gm'), arguments[i]);
    }
    return s;
};

function process_error(error_data) {
    if (!doProcess) {
        return;
    }
    doProcess = false;

    setTimeout(function(){
        doProcess = true;
        $("#messageBox").text(initialMessage);
    }, 10000);

    $("#messageBox").html(messageError.format(error_data.error));
}

function process_token(token_data) {
    if (!doProcess) {
        return;
    }
    doProcess = false;
    setTimeout(function(){
        doProcess = true;
        $("#messageBox").text(initialMessage);
    }, 10000);

    $.ajax({
        url: processor_url,
        type: "POST",
        data: {
            reader: token_data.reader,
            token: token_data.token
        }
    })  //display message
        .done(function (data) {
            if (data.active) {
                $("#messageBox").html(messageStarted.format(data.person,
                    data.cable));
            } else {
                $("#messageBox").html(messageStopped.format(data.person,
                    data.cable));
            }
        })
        //display error message
        .fail(function (jqXHR, textStatus, errorThrown) {
            try {
                var template = "<p>{0}</p>";
                var msg_string = "";
                var json_data = $.parseJSON(jqXHR.responseText);
                $.each(json_data, function(k, v){
                    $.each(v, function(){
                        msg_string +=template.format(this);
                    })
                });
                $("#messageBox").html(messageError.format(msg_string));
            } catch(e) {
                $("#messageBox").html(messageError.format(errorThrown));
            }
        }).then();
}