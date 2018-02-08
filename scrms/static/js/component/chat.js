
/*
let p = 41
let g = 6

let a = 11
let A = Math.pow(g,a)%p //public
//alert(A)

let b = 19
let B = Math.pow(g,b)%p //public
//alert(B)

var s1 = Math.pow(B,a)%p
var s2 = Math.pow(A,b)%p


console.log(s1)
console.log(s2)
console.log(s1)
console.log(s2)
*/

function CHAT(USER_ID,KEY,USERS,socket,csrf_token,noty){

  Dropzone.autoDiscover = false;
  var myDropzone = new Dropzone("#dropzone-chat",);

  myDropzone.on("success", function(data) {
    setTimeout(function(){
      $('.previewsContainer').fadeOut(300)
    },3000)


    let images_type = ["jpg","JPG","gif","JPEG","png","PNG","tiff","GIF"]
    let jsn = JSON.parse(data.xhr.response)
    //console.log(jsn)

    if(images_type.indexOf(jsn.types)!= -1){
      var body = `<a href='${jsn.url}' target='blank'><img class='scrims_chat_message_file img_types' style='max-width:200px' src='${jsn.cache}'/></a>`
    }else if(jsn.types == 'pdf' || jsn.types == 'PDF' ){
      var body = `<div style='text-align:center'><a href='${jsn.url}' target='blank'><img class='scrims_chat_message_file img_types' style='width:80px' src='/static/img/file-pdf.png'/><br></a><span>${jsn.name}</span></div>`
    }else if(jsn.types == 'doc' || jsn.types == 'DOC' || jsn.types == 'DOC' || jsn.types == 'DOCX' ){
      var body = `<div style='text-align:center'><a href='${jsn.url}' target='blank'><img class='scrims_chat_message_file img_types' style='width:80px' src='/static/img/file-doc.png'/><br></a><span>${jsn.name}</span></div>`
    }else if(jsn.types == 'xls' || jsn.types == 'XLS' || jsn.types == 'csv' || jsn.types == 'CSV' ){
      var body = `<div style='text-align:center'><a href='${jsn.url}' target='blank'><img class='scrims_chat_message_file img_types' style='width:80px' src='/static/img/file-xls.png'/><br></a><span>${jsn.name}</span></div>`
    }else{
      var body = `<div style='text-align:center'><a href='${jsn.url}' target='blank'><img class='scrims_chat_message_file img_types' style='width:80px' src='/static/img/file.png'/><br></a><span>${jsn.name}</span></div>`
    }
      SEND_MESSAGE(USER_ID, parseInt($('#scrims_chat_init').attr('data-init')), "file", body)

    setTimeout(function(){
      $('.previewsContainer').empty()

    },4000)

  });

  myDropzone.on("addedfile", function(data) {
    $('.previewsContainer').fadeIn(10)
  });



  function SELECT_COMPANION(id){

      let user = USERS.filter(data => data.id==id)

      $('#scrims_chat_canvas').attr("data-init",id)
      $('#scrims_chat_heading').empty()
      $('#scrims_chat_heading').html(`<div id="scrims_chat_init" class="col-sm-2 col-md-1 col-xs-3 heading-avatar" data-init="${user[0].id}" data-public-key=${user[0].public_key}>
            <div class="heading-avatar-icon">
              <img src="${user[0].img}">
            </div>
            </div>
          <div class="col-sm-8 col-xs-7 heading-name">
            <a href="/personal/user/2/${user[0].id}" class="heading-name-meta">${user[0].name}
           </a>
          </div>
          `)

          GET_HISTORY(id)

          $('#scrims_chat_textarea').focus()
  }


  function PREVIOUS_MESSAGE(id){

    var limit = ($('.scrims_chat_msg_main').length)+($('.scrims_chat_msg_recive').length)

    MAIN_AJAX_GET('/api/get-history-about/?companion='+id+'&limit='+limit).then(function(result){

      $('.message-previous').remove()

      PARSER_MSG_HISTORY(id,result)

    })

  }



  function GET_HISTORY(id){

              MAIN_AJAX_GET('/api/get-history/?companion='+id).then(function(result){

                  $('#scrims_chat_canvas').empty()
                  PARSER_MSG_HISTORY(id,result)
                  $('#scrims_chat_textarea').val('')
                  setTimeout(function(){
                          $('#scrims_chat_canvas').scrollTop($('#scrims_chat_canvas').prop('scrollHeight'))
                  },10)

                  $('.scrims_chat_companion').each(function() {

                    if($(this).attr('data-init') == id){
                      //var count = parseInt($('.scrims_chat_count_message').text())

                      var count = parseInt($(this).find('.scrims_chat_count_message').remove())

                    }
                  })


              })
  }









  function PARSER_MSG_HISTORY(id,result){

            var messages_read = []



    $.each(result.reverse(),function(k,v){

        if(v.message=='recive'){
          messages_read.push(v.id) // статус прочитанных сообщений
          var cls_mess = 'receiver'
          var decrypt = CryptoJS.AES.decrypt(v.body,KEY).toString(CryptoJS.enc.Utf8);
        }else {
          var cls_mess = 'sender'
          var decrypt = CryptoJS.AES.decrypt(v.body,$('#scrims_chat_init').attr('data-public-key')).toString(CryptoJS.enc.Utf8);
        }

        let date = moment(v.date).calendar()

        if(v.delivered==true && cls_mess=='sender'){
            var check = '<span class="fa fa-check delivered_msg" style="color: rgb(79, 206, 59);"></span>'
        }else if(v.delivered==false && cls_mess=='sender'){
            var check = '<span class="fa fa-check delivered_msg"></span>'
        }else{
          var check = ''
        }


        //console.log(v.reading)
        if(v.reading==true && cls_mess=='sender'){
            messages_read.push(v.id)
            var read = '<span class="fa fa-check reading_msg" style="color: rgb(79, 206, 59);"></span>'
        }else if(v.reading==false && cls_mess=='sender'){
            var read = '<span class="fa fa-check reading_msg"></span>'
        }else{
          var read = ''
        }

        //console.log(read)

        $('#scrims_chat_canvas').prepend(`<div id="id_msg_${v.id}" class="row message-body scrims_chat_msg_${v.message}"  data-init="${v.id}" style="display:none">
            <div class="col-sm-12 message-main-${cls_mess}">
              <div class="${cls_mess}">
                <div class="message-text">
                  ${decrypt}
                </div>
                <span class="message-time pull-right">
                  ${moment(v.date).calendar()}
                  ${check}
                  ${read}
                </span>
              </div>
            </div>
          </div>`)
    })



    socket.emit("msg readed",{"id_msg":messages_read}) //!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


    if(result.length>=10){

          $('#scrims_chat_canvas').prepend(`<div class="row message-previous"  data-init="${id}" style="display:none">
            <div class="col-sm-12 previous">
              <b>
              Show Previous Message!
              <b>
            </div>
          </div>`)
        $('.message-previous').fadeIn('slow')
      }

      $('.message-body').fadeIn('slow')

      $('.message-previous').click(a => PREVIOUS_MESSAGE(id))
  }



  function MAIN_AJAX_GET(url){
    let data = fetch(url,{
        credentials: "same-origin"
      }).then(res => res.json())
        .catch(function(error) {
        console.log(error);
      })
      return(data)
  }





  function SEND_AJAX_MESSAGE(msg_object){

    if(isNaN(msg_object.companion) == true){return false}//if not found recipient
    let data = $.ajax({
      url:'/api/send-message/',
      type:'POST',
      dataType:"json",
      data:msg_object,
      success:function(data){
          socket.emit('chat message',data);
          socket.emit("msg delivered",{"id_msg":data.id_msg})
      },statusCode:{
        403:error => window.location.reload(),
        400:function(){
          return false
        }
      }
    })
    return data

  }










function SEND_MESSAGE(id_user,id_companion,type,message){

  let msg = message.replace(/\n/g, "").replace(/\s/g, "")//strip \n
  if(msg === ''){return false}
  message = message.replace(/\n/g, "<br>")
  //smiles
  //message = message.replace(/=)/g, "<br>")

  var public_key = $('#scrims_chat_init').attr('data-public-key')



  console.log(public_key)

  let crypt_msg = CryptoJS.AES.encrypt(message,public_key).toString();
  let decrypt = CryptoJS.AES.decrypt(crypt_msg,public_key).toString(CryptoJS.enc.Utf8);


  console.log(crypt_msg,"------crypt-------",decrypt)

  let date = moment().format('YYYY-MM-DD HH:mm:ss')
  //let msg_object = {"user":id_user,"companion":id_companion,"type":type,"body":message,"date":date,"csrfmiddlewaretoken":csrf_token}
  let msg_object = {"user":id_user,"companion":id_companion,"type":type,"body":crypt_msg,"date":date,"csrfmiddlewaretoken":csrf_token}

  if (SEND_AJAX_MESSAGE(msg_object)==false){return false}
  SCROLL_TO_BOTTOM()
  $('#scrims_chat_textarea').val('')

}


//smooth scroll to bottom when action(recive send) message
function SCROLL_TO_BOTTOM(){
  $('#scrims_chat_canvas').animate({scrollTop:$('#scrims_chat_canvas').prop('scrollHeight')},"slow")
}


function STATUS_CONECTED(data){
    var token = data.token.replace(' ','')
    //console.log(data.id_user,data.status)

      if(data.status == 'on'){
        $('.scrims_chat_companion').each(function(){
          var id = $(this).attr('data-init')
          if(id == data.id_user){
            $(this).find('.scrims_chat_status').removeClass('scrims_chat_status_offline').addClass('scrims_chat_status_online')
          }
        })
      }
      if(data.status == 'off'){
        $('.scrims_chat_companion').each(function(){
          var id = $(this).attr('data-init')
          if(id == data.id_user){
            $(this).find('.scrims_chat_status').removeClass('scrims_chat_status_online').addClass('scrims_chat_status_offline')
          }
        })
      }

}


function READED_MSG(id_msg){

  MAIN_AJAX_GET('/api/read-msg/'+id_msg+'/').then(function(result){
    console.log(result)
    socket.emit("msg readed",{"id_msg":id_msg})
  })

}


function PARSER_RECIVE_AND_SENDER_MESSAGE(data){



  // Парсим сообщение которое пришло нам т.е. reciver
  if(data.companion === USER_ID && parseInt($('#scrims_chat_canvas').attr('data-init')) === data.user){

    let decrypt = CryptoJS.AES.decrypt(data.body,KEY).toString(CryptoJS.enc.Utf8);


    $('#scrims_chat_canvas').append(`<div id="id_msg_${data.id_msg}" class="row message-body scrims_chat_msg_receiver" data-init="${data.id_msg}">
              <div class="col-sm-12 message-main-receiver">
                <div class="receiver">
                  <div class="message-text">
                    ${decrypt}
                  </div>
                  <span class="message-time pull-right">
                    ${moment().calendar()}
                  </span>
                </div>
              </div>
            </div>`)
          $('.heading-typing').fadeOut(200)

          SCROLL_TO_BOTTOM()
          READED_MSG(data.id_msg)


  }  // Парсим сообщение которое мы отправили
  else if(data.user === USER_ID && parseInt($('#scrims_chat_canvas').attr('data-init')) === data.companion){


        let decrypt = CryptoJS.AES.decrypt(data.body,$('#scrims_chat_init').attr('data-public-key')).toString(CryptoJS.enc.Utf8);

        $('#scrims_chat_canvas').append(`<div id="id_msg_${data.id_msg}" class="row message-body scrims_chat_msg_main" data-init="${data.id_msg}">
            <div class="col-sm-12 message-main-sender">
              <div class="sender">
                <div class="message-text">
                  ${decrypt}
                </div>
                <span class="message-time pull-right">
                  ${moment().calendar()}
                  <span class="fa fa-check delivered_msg"></span>
                  <span class="fa fa-check reading_msg"></span>
                </span>
              </div>
            </div>
          </div>`)
        SCROLL_TO_BOTTOM()

   }


   MESSAGE_NO_SEE(data)

}



// if user not see recive message while no open contact or close chat
function MESSAGE_NO_SEE(data){
  if (data.companion === USER_ID && parseInt($('#scrims_chat_canvas').attr('data-init')) != data.user) {
        $('.scrims_chat_companion').each(function() {

          if($(this).attr('data-init') == data.user){
            //var count = parseInt($('.scrims_chat_count_message').text())

            var count = parseInt($(this).find('.scrims_chat_count_message').text())

            if(isNaN(count)==true){
              $(this).find(".pull-right").html('<b  class="badge scrims_chat_count_message">1</b>')

            }else{
              $(this).find(".pull-right").html('<b  class="badge scrims_chat_count_message">'+(count+1)+'</b>')

            }

            user = USERS.filter(a => a.id==parseInt(data.user))
            noty(user[0].name, user[0].img, 'Отправил(а) вам') //-----------------------------------> lang
          }
        })
    }

}


function MSG_DELIVERED(data){
  $('#id_msg_'+data.id_msg).find('.delivered_msg').css({'color':'#4fce3b'})
}






function MSG_READED(data){

  if(Array.isArray(data.id_msg) == true){

    $.each(data.id_msg,function(k,v){
      $('#id_msg_'+v).find('.reading_msg').css({'color':'#4fce3b'})
    })

  }else{
      $('#id_msg_'+data.id_msg).find('.reading_msg').css({'color':'#4fce3b'})
  }


}



socket.on('chat message',data=>PARSER_RECIVE_AND_SENDER_MESSAGE(data))
socket.on('chat status',data=>STATUS_CONECTED(data))
socket.on('msg delivered',data=>MSG_DELIVERED(data))
socket.on('msg readed',data=>MSG_READED(data))




//actions
  //click on "send icon" send message




  $('#scrims_chat_send').on('click',function(){
      SEND_MESSAGE(USER_ID,parseInt($('#scrims_chat_init').attr('data-init')),'text',$('#scrims_chat_textarea').val())
  })

 //ctr+enter send message
  $('#scrims_chat_textarea').bind('keypress', function(event) {
      if((event.keyCode == 10 || event.keyCode == 13) && event.ctrlKey) {
        SEND_MESSAGE( USER_ID, parseInt($('#scrims_chat_init').attr('data-init')), 'text',$('#scrims_chat_textarea').val() )
      }
  });

  $('#searchText').off('keydown')
  $('#searchText').on('keydown',function(e){

    if(e.keyCode == 13){
      $('.scrims_chat_companion:first').click()
    }

    var data = $(this).val()
    function filtration(text){
      var a = text.slice(0,data.length)
      return (a.toLowerCase())
    }


    var users = USERS.filter(a => filtration(a.search[0]) == data.toLowerCase() || filtration(a.search[1]) == data.toLowerCase() || filtration(a.search[2]) == data.toLowerCase())
    if(users == ''){
      var users = USERS.filter(a => filtration(a.name) == data.toLowerCase())
    }
    $('#scrims_chat_contact_list').empty()

    $.each(users,function(k,v){
        $('#scrims_chat_contact_list').append(`<div class="row sideBar-body scrims_chat_companion" data-init="${v.id}">
                <span class="scrims_chat_status scrims_chat_status_offline"></span>
                <span class="scrims_chat_status"></span>
                <div class="col-sm-3 col-xs-3 sideBar-avatar">
                  <div class="avatar-icon">
                      <img src="${v.img}" width="50" height="50">
                  </div>
                </div>
                <div class="col-sm-9 col-xs-9 sideBar-main">
                  <div class="row">
                    <div class="col-sm-8 col-xs-8 sideBar-name">
                      <span class="name-meta">${v.name}
                    </span>
                    </div>
                    <div class="col-sm-4 col-xs-4 pull-right sideBar-time">
                      <span class="time-meta pull-right">
                    </span>
                    </div>
                  </div>
                </div>
              </div>`)
    })

    SELECT_COMPANION_ACTION()

  })


  function SELECT_COMPANION_ACTION(){
  $('.scrims_chat_companion').off('click')
  $('.scrims_chat_companion').on('click',function(){
    if($(this).hasClass('cleanstate_chat_companion') == true){return false}
    $('.scrims_chat_companion').removeClass('cleanstate_chat_companion')
    $(this).addClass('cleanstate_chat_companion');

    SELECT_COMPANION($(this).attr('data-init'))
  })
}

SELECT_COMPANION_ACTION()
//end actions


/* позволяет делать тайминги при вызове ф-ций */
function debounce(func, wait, immediate) {
	var timeout;
	return function() {
		var context = this, args = arguments;
		var later = function() {
			timeout = null;
			if (!immediate) func.apply(context, args);
		};
		var callNow = immediate && !timeout;
		clearTimeout(timeout);
		timeout = setTimeout(later, wait);
		if (callNow) func.apply(context, args);
	};
};


  function TYPYNG_MSG(){
    socket.emit('user typing',{"user":USER_ID,"companion":parseInt($('#scrims_chat_init').attr('data-init'))})
  }

  function TYPYNG_USR(data){


    if(data.companion === USER_ID && parseInt($('#scrims_chat_canvas').attr('data-init')) === data.user){

      $('.heading-typing').fadeIn(200)
      clearTimeout(timerId);
      var timerId = setTimeout(function(){
            $('.heading-typing').fadeOut(200)
        },8000)
      }


  }

  socket.on('user typing',data=>TYPYNG_USR(data))


  $('#scrims_chat_textarea').on('input change', debounce(TYPYNG_MSG, 220));


  function getCookie(name) {
    var matches = document.cookie.match(new RegExp(
      "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
    ));
    return matches ? decodeURIComponent(matches[1]) : undefined;
  }


  $(window).on("blur focus", function(e) {
    socket.emit('chat status',{"token":getCookie("SCRIMS_TOKEN"),"status":"on"})
  })


  $('.fa-upload').click(function(){
    $('.dz-hidden-input').click()
  })



}//end chat