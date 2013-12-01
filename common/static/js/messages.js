$(function() {

    $('.current-user').popover({
        placement: 'bottom',
        content: 'text',
        trigger: 'manual'
    }).popover('show');

    var messageId;
    var socket = new io.connect('http://localhost:8080',
        {rememberTransport: false});

    var markup =' \
        <div class="modal fade" id="myModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">\
            <div class="modal-dialog">\
            <div class="modal-content">\
              <div class="modal-header">\
                <button type="button" class="close" data-dismiss="modal" aria-hidden="true">&times;</button>\
                <h4 class="modal-title" id="myModalLabel">Сообщение</h4>\
              </div>\
              <div class="modal-body">\
                ...\
              </div>\
              <div class="modal-footer">\
                <button type="button" class="btn btn-default" data-dismiss="modal">Закрыть</button>\
                <button type="button" class="btn btn-primary process">OK</button>\
              </div>\
            </div><!-- /.modal-content -->\
          </div>\
        </div>';

    var $div = $(markup);
    $('body').append($div);

    function processFn() {
        $div.modal('hide');
        $.ajax({
            url: '/messages/mark_read/',
            type: "POST",
            data: {
                message: messageId
            }
        });
    }

    $div.find('button.process').on('click', processFn);

    $div.modal({
        show: false
    });

    socket.on('message', function (data) {
        if (data.type == 'message') {
            messageId = data.messageId;
            $div.find('.modal-body').html(data.message);
            $div.modal('show');
        }
    });

    socket.on('connect', function () {

        socket.json.send(
            {type: 'auth request',
             sessionid: 'dummy'
            });
    });
})
