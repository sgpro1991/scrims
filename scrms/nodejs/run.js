const server = require('http').createServer();
const io = require('socket.io')(server);
const request = require('request');
const host = '127.0.0.1:9898'





io.on('connection', function(socket){

    socket.join('chat');
      let cookie = socket.handshake.headers.cookie

      cookie.replace('/csrftoken/',' ')
      let regexp =  /SCRIMS_TOKEN=................................/;
      let str = cookie.match(regexp)
      try{
        let token = str[0].replace('SCRIMS_TOKEN=','').replace(';','').replace(' ','')
        request('http://'+host+'/api/status-chat/?token='+token+'&status=on', { json: false }, (err, res, body) => {
          if (err) { return console.log(err); }
          io.emit('chat status', {"token":token,"status":"on","id_user":body});
        });

      }catch(error){
        console.log(error)
      }





    socket.on('chat status', function(msg){
      let cookie = socket.handshake.headers.cookie
      cookie.replace('/csrftoken/',' ')
      let regexp =  /SCRIMS_TOKEN=................................/;
      let str = cookie.match(regexp)
      try{
        let token = str[0].replace('SCRIMS_TOKEN=','').replace(';','').replace(' ','')
        request('http://'+host+'/api/status-chat/?token='+token+'&status=on', { json: false }, (err, res, body) => {
          if (err) { return console.log(err); }
          //console.log(body)
          io.emit('chat status', {"token":token,"status":"on","id_user":body});
        });

      }catch(error){
        console.log(error)
      }
    });






    socket.on('chat message', function(msg){
      io.emit('chat message', msg);
    });



    socket.on('msg delivered', function(msg){
      //console.log(msg)
      io.emit('msg delivered', msg);
    });


    socket.on('msg readed', function(msg){
      io.emit('msg readed', msg);
    });


    socket.on('user typing', function(msg){
      io.emit('user typing', msg);
    });


    socket.on('disconnect', function(){

      let cookie = socket.handshake.headers.cookie
      let regexp = /SCRIMS_TOKEN=................................/;
      let str = cookie.match(regexp)

      try{
        let token = str[0].replace('SCRIMS_TOKEN=','').replace(';','').replace(' ','')
        request('http://'+host+'/api/status-chat/?token='+token+'&status=off', { json: false }, (err, res, body) => {
          if (err) { return console.log(err); }
          //console.log(body,"off")
          io.emit('chat status', {"token":token,"status":"off","id_user":body});
        });

      }catch(error){
        console.log(error)
      }


    });
});


server.listen(3000,'127.0.0.1');
