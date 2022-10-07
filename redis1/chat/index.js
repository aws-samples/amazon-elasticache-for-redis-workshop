var app = require('express')();
var http = require('http').Server(app);
var io = require('socket.io')(http);
var Redis = require('ioredis');

app.get('/', function(req, res){ res.sendFile(__dirname + '/index.html');
});

http.listen(8080, function(){
   console.log('listening on *:8080');
});

//create pub sub
var pub = new Redis({
  host: "[Your Redis Cluster Endpoint]",
  port: 6379
});

var sub = new Redis({
  host: "[Your Redis Cluster Endpoint]",
  port: 6379
});
sub.subscribe("awsomechat");


io.sockets.on('connection', function (socket) {
    sub.on("message", function (channel, message) {
      console.log("get message");
      socket.send(message);
    });

    socket.on("message", function (msg) {
      console.log(msg);

      if(msg.type == "logIn"){
        pub.publish("awsomechat",msg.user + "님이 입장했습니다.");
      }

      else if(msg.type == "data"){
        pub.publish("awsomechat",msg.message);
      }
      
    });

    socket.on('disconnect', function () {
      sub.quit();
      pub.publish("awsomechat", socket.id+"님이 퇴장했습니다.");
    });
});