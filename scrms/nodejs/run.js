var server = require('http').createServer();
var io = require('socket.io')(server);



io.on('connection', function(socket){

    // if user connect to chat

/*      console.log(socket)
      var cookie = socket.handshake.headers.cookie
      var regexp = /SCRIMS_TOKEN=.*;/;
      var str = cookie.match(regexp)
      try{
        io.emit('chat status', {"token":str[0].replace('SCRIMS_TOKEN=','').replace(';',''),"status":"on"});
      }catch(error){
        console.log(error)
      }
*/
    // end if user connect to chat

    socket.on('chat status', function(msg){
      console.log(msg)
      io.emit('chat status', msg);
    });


    socket.on('chat message', function(msg){
      console.log(msg)
      io.emit('chat message', msg);
    });

    socket.on('disconnect', function(){
      var cookie = socket.handshake.headers.cookie
      var regexp = /SCRIMS_TOKEN=.*;/;
      var str = cookie.match(regexp)
      try{
        io.emit('chat status', {"token":str[0].replace('SCRIMS_TOKEN=','').replace(';',''),"status":"off"});
      }catch(error){
        console.log(error)
      }

    });
});



server.listen(3000,'127.0.0.1');
