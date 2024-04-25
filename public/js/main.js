window.onload = function() {
    console.log("test");

    var scheme = window.location.protocol === 'https:' ? 'wss' : 'ws';
    var host = window.location.hostname;
    var port = window.location.port || (window.location.protocol === 'https:' ? 443 : 80);

    var websocket = scheme + '://' + host + ':' + port + '/ws';
    var ws;

    if (window.WebSocket) {
      ws = new WebSocket(websocket);
    }
    else if (window.MozWebSocket) {
      ws = new MozWebSocket(websocket);
    }
    else {
      console.log('WebSocket Not Supported');
      return;
    }

    ws.onmessage = function(event) {
        data_rcvd = JSON.parse(event.data);
        console.log(data_rcvd);
       switch(data_rcvd.action) {
            case 'update_time':
                var chat = document.getElementById('time_display');
                chat.innerHTML = '<h1>' + data_rcvd.time + '</h1>';
                break;

                break;
        }


      };
};