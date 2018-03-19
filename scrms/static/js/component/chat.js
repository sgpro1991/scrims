
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




function CHAT(USER_ID,USER_IMG,KEY,USERS,socket,csrf_token,noty,LANG,NOTY){







$('#dialog-chat').dialog({
      autoOpen: false,
      modal: true,
      //width:'100%',
      buttons:
      [
          {
            text: LANG[0].common[0].save,
            class:'btn btn-success',
            click: function (data) {
                if($('#id-dialog-param').attr('data-init') == 'create-group'){
                  CREATE_GROUP_SERVER()
                }
              }
          },{
            text:LANG[0].common[0].cancel,
            class:'btn btn-default',
            click: function () {
                $(this).dialog("close");
            }
          }
        ]
    });




function RENDER_USERS_ITEM(v,arg){

  if(v.status == true){
      var status = '<div class="avatar-icon avatar-icon-active">'
  }else{
      var status = '<div class="avatar-icon">'
  }



  if(v.count_msg != 0){
      var count_msg = '<b class="badge scrims_chat_count_message">'+v.count_msg+'</b>'
  }else{
      var count_msg = ''
  }



  if(v.last_msg != ''){
      if(v.last_msg_type == 'file'){
          last_msg = '<img class="scrims_chat_message_file img_types" style="width:10px;width: 15px;opacity: 0.5" src="/static/img/file.png">'
      }else{
          try{
            var last_msg = CryptoJS.AES.decrypt(v.last_msg, v.public_key).toString(CryptoJS.enc.Utf8).replace("<br>", "");
          }catch(e){
            var last_msg = CryptoJS.AES.decrypt(v.last_msg, KEY).toString(CryptoJS.enc.Utf8).replace("<br>", "");
          }if (last_msg == ''){
            var last_msg = CryptoJS.AES.decrypt(v.last_msg, KEY).toString(CryptoJS.enc.Utf8).replace("<br>", "");
          }
      }
  }else{
      var last_msg = ''
  }



  if(arg === true){

    $('#scrims_chat_contact_list').append(`<div class="row sideBar-body scrims_chat_companion" data-init="${v.id}" data-group="${v.group}">
        <div class="col-sm-2 col-xs-2 sideBar-avatar">
          ${status}
            <img src="${v.img}" width="50px" height="50px">
          </div>
        </div>
        <div class="col-sm-9 col-xs-9 sideBar-main">
          <div class="row">
            <div class="col-sm-8 col-xs-8 sideBar-name">
              <span class="name-meta">${v.name}</span>
              <div class="name-meta" style="color: #999;color: #999;overflow: hidden;width: 100%;text-overflow: ellipsis;">${last_msg}</div>
            </div>
            <div class="col-sm-3 col-xs-3 pull-right sideBar-time">
              <span class="time-meta pull-right">
            </span>
            ${count_msg}
            </div>
          </div>
        </div>
      </div>`)
  }else{
    $('#scrims_chat_contact_list').prepend(`<div class="row sideBar-body scrims_chat_companion" data-init="${v.id}" data-group="${v.group}">
        <div class="col-sm-2 col-xs-2 sideBar-avatar">
          ${status}
            <img src="${v.img}" width="50px" height="50px">
          </div>
        </div>
        <div class="col-sm-9 col-xs-9 sideBar-main">
          <div class="row">
            <div class="col-sm-8 col-xs-8 sideBar-name">
              <span class="name-meta">${v.name}</span>
              <div class="name-meta" style="color: #999;color: #999;overflow: hidden;width: 100%;text-overflow: ellipsis;">${last_msg}</div>
            </div>
            <div class="col-sm-3 col-xs-3 pull-right sideBar-time">
              <span class="time-meta pull-right">
            </span>
            ${count_msg}
            </div>
          </div>
        </div>
      </div>`)
  }
}














function RENDER_USERS(USERS){

  var mass = []

  $.each(USERS,function(k,v){

    //if(k>10){return false}

    if(v.count_msg != 0){
      mass.push(v)
    }else{
      RENDER_USERS_ITEM(v,true)
    }
  })

  $.each(mass,function(k,v){
      RENDER_USERS_ITEM(v,false)
  })

}
























RENDER_USERS(USERS)
  var width_window = $(window).width()
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

    if($('#scrims_chat_init').attr('data-group') == 'true'){
        var group = true
    }else{
        var group = false
    }



    SEND_MESSAGE(USER_ID, $('#scrims_chat_init').attr('data-init'), "file", body, USER_IMG, group)

    setTimeout(function(){
      $('.previewsContainer').empty()
    },4000)

  });















  myDropzone.on("addedfile", function(data) {
    $('.previewsContainer').fadeIn(10)
  });




















  function SELECT_GROUP(id){
      MAIN_AJAX_GET('/api/get-users-group/'+id+'/').then(function(result){

        $('#scrims_chat_heading').empty()
        var users  = []
        $.each(result,function(k,v){
            let user = USERS.filter(data => data.id==v)
            users.push(user)
        })

        $('#scrims_chat_canvas').attr('data-init',id)

        $('#scrims_chat_heading').append(`<div id="scrims_chat_init" class="col-sm-10 col-md-10 col-xs-10 heading-avatar" style="position:absolute;overflow:hidden; top:0;height: 50px;" data-init="${id}" data-public-key="123" data-group="true"></div>`)

        $.each(users,function(k,v){
          console.log(v)
            $('#scrims_chat_init').append(`<div  class="col-sm-1 col-md-1 col-xs-1 scrims_chat_companion heading-avatar " data-init="${id}" data-group="false">
                  <div class="heading-avatar-icon">
                    <a href="/personal/user/${v[0].id}/" class="heading-name-meta" style="text-align:center"><img src="${v[0].img}"></a>
                    </div>
                  </div>
            `)
        })
      GET_HISTORY(id,true)
      })
  }



















  function SELECT_COMPANION(id,group){
      if(group == 'true'){
        return SELECT_GROUP(id)
      }
      MAIN_AJAX_GET('/api/get-status/'+id+'/').then(function(result){
        if(result.status == true){
            var status = '<span  class="scrims_chat_status scrims_chat_status_online"></span>'
        }else{
            var status = '<span  class="scrims_chat_status scrims_chat_status_offline"></span>'
        }

          let user = USERS.filter(data => data.id==id)
          $('#scrims_chat_canvas').attr("data-init",id)
          $('#scrims_chat_heading').empty()
          $('#scrims_chat_heading').html(`<div id="scrims_chat_init" class="col-sm-2 col-md-1 col-xs-2 heading-avatar" data-init="${user[0].id}" data-public-key=${user[0].public_key} data-group="false">
                <div class="heading-avatar-icon">
                  <img src="${user[0].img}">
                  </div>
                  </div>
                  <div class="col-sm-4 col-xs-7 heading-name">
                  <a href="/personal/user/${user[0].id}/" class="heading-name-meta">${user[0].name}
                </a>

              </div>
              <div class="col-sm-1 col-xs-1 heading-name">
              ${status}
              </div>
              `)
            GET_HISTORY(id,false)
            if(width_window>700){
                  $('#scrims_chat_textarea').focus()
            }

    })
  }



function PREVIOUS_MESSAGE(id,group){



      var limit = ($('.scrims_chat_msg_main').length)+($('.scrims_chat_msg_recive').length)

      if($('#scrims_chat_init').attr('data-group') == 'true'){
        var group = 1
      }else{
        var group = 0
      }

      MAIN_AJAX_GET('/api/get-history-about/?companion='+id+'&group='+group+'&limit='+limit).then(function(result){

        $('.message-previous').remove()

        PARSER_MSG_HISTORY(id,result,group)

      })

}



  function GET_HISTORY(id,group){
    if(group==true){
      var group = 1
    }else{
      var group = 0
    }

    MAIN_AJAX_GET('/api/get-history/?companion='+id+'&group='+group).then(function(result){
            $('#scrims_chat_canvas').empty()
            PARSER_MSG_HISTORY(id,result,group)
            $('#scrims_chat_textarea').val('')
            setTimeout(function(){
                    $('#scrims_chat_canvas').scrollTop($('#scrims_chat_canvas').prop('scrollHeight'))
            },10)

            $('.scrims_chat_companion').each(function() {
              if($(this).attr('data-init') == id){
                var count = parseInt($(this).find('.scrims_chat_count_message').remove())

                if($('.scrims_chat_count_message').length == 0){
                  $('.common-chat-count-message').html('')
                }else{
                  $('.common-chat-count-message').html(`<br><span id="common-chat-count-message-id" class="badge">${$('.scrims_chat_count_message').length}</span>`)
                }
              }
            })
        })

  }









  function PARSER_MSG_HISTORY(id,result,group){

    var messages_read = []

    $.each(result.reverse(),function(k,v){

        if(v.message=='recive'){
          messages_read.push(v.id) // статус прочитанных сообщений
          var cls_mess = 'receiver'
            if(group == 1){
              var decrypt = CryptoJS.AES.decrypt(v.body,$('#scrims_chat_init').attr('data-public-key')).toString(CryptoJS.enc.Utf8);
            }else{
              var decrypt = CryptoJS.AES.decrypt(v.body,KEY).toString(CryptoJS.enc.Utf8);
            }
          //var decrypt = CryptoJS.AES.decrypt(v.body,KEY).toString(CryptoJS.enc.Utf8);
          var img = '<img src="'+v.img+'" style="width:30px;height:30px;border-radius:50%;position:absolute;left:-50px;top: -25px;"/>'

        }else {
          var cls_mess = 'sender'
          var decrypt = CryptoJS.AES.decrypt(v.body,$('#scrims_chat_init').attr('data-public-key')).toString(CryptoJS.enc.Utf8);
          var img = '<img src="'+v.img+'" style="width:30px;height:30px;border-radius:50%;position:absolute;right:-50px;top: -25px;"/>'

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
                <div class="col-sm-12">
                ${img}
                </div>
              </div>

            </div>

          </div>`)
    })



    socket.emit("msg readed",{"id_msg":messages_read}) //!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


    if(result.length>=10){

          $('#scrims_chat_canvas').prepend(`<div class="row message-previous"  data-init="${id}" style="display:none">
            <div class="col-sm-12 previous">
              <b>
              ${LANG[0].chat[0].previous}
              <b>
            </div>
          </div>`)
        $('.message-previous').fadeIn('slow')
      }

      $('.message-body').fadeIn('slow')

      $('.message-previous').click(a => PREVIOUS_MESSAGE(id,group))
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





  function SEND_AJAX_MESSAGE(msg_object,group){

    var url = '/api/send-message/?group='+group
    if(msg_object.companion == ''){return false}//if not found recipient

    let data = $.ajax({
      url:url,
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










function SEND_MESSAGE(id_user,id_companion,type,message,img,group){

  console.log(id_companion)

  let msg = message.replace(/\n/g, "").replace(/\s/g, "")//strip \n
  if(msg === ''){return false}
  message = message.replace(/\n/g, "<br>")
  //smiles
  //message = message.replace(/=)/g, "<br>")

  var public_key = $('#scrims_chat_init').attr('data-public-key')


  let crypt_msg = CryptoJS.AES.encrypt(message,public_key).toString();
  let decrypt = CryptoJS.AES.decrypt(crypt_msg,public_key).toString(CryptoJS.enc.Utf8);


  console.log(crypt_msg,"------crypt-------",decrypt)

  let date = moment().format('YYYY-MM-DD HH:mm:ss')
  let msg_object = {"user":id_user,"companion":id_companion,"type":type,"body":crypt_msg,"date":date,"csrfmiddlewaretoken":csrf_token,"img":img}

  if (SEND_AJAX_MESSAGE(msg_object,Number(group))==false){return false}
  SCROLL_TO_BOTTOM()
  $('#scrims_chat_textarea').val('')

}


//smooth scroll to bottom when action(recive send) message
function SCROLL_TO_BOTTOM(){
  $('#scrims_chat_canvas').animate({scrollTop:$('#scrims_chat_canvas').prop('scrollHeight')},"slow")
}




function STATUS_CONECTED(data){
    var token = data.token.replace(' ','')


      if(data.status == 'on'){
        $('.scrims_chat_companion').each(function(){
          var id = $(this).attr('data-init')

          if(id == data.id_user){

            $(this).find('.avatar-icon').addClass('avatar-icon-active')
            $('#scrims_chat_contact_list').prepend('<div class="row sideBar-body scrims_chat_companion fade-'+id+'" data-init="'+id+'">'+$(this).html())
            $('.fade-'+id).effect('fade', { times:3 }, 300);

            $(this).remove()
          }
        })
      }
      if(data.status == 'off'){
        $('.scrims_chat_companion').each(function(){
          var id = $(this).attr('data-init')
          if(id == data.id_user){
            $(this).find('.avatar-icon').removeClass('avatar-icon-active')

            if(parseInt($(this).find('.scrims_chat_count_message').text()) > 0  ){

            }else{
              $('#scrims_chat_contact_list').append('<div class="row sideBar-body scrims_chat_companion" data-init="'+id+'">'+$(this).html())
              $(this).remove()
            }
          }
        })
      }



      SELECT_COMPANION_ACTION()
}


function READED_MSG(id_msg){
  MAIN_AJAX_GET('/api/read-msg/'+id_msg+'/').then(function(result){
    console.log(result)
    socket.emit("msg readed",{"id_msg":id_msg})
  })

}

























function PARSER_RECIVE_AND_SENDER_MESSAGE(data){
///// GROUPS
  if(data.group != ''){

      //Парсим сообщение группы которое пришло нам т.е. reciver
      if(data.companion.indexOf(USER_ID)!=-1){
        if($('#scrims_chat_canvas').attr('data-init') === data.group){

          let decrypt = CryptoJS.AES.decrypt(data.body,$('#scrims_chat_init').attr('data-public-key')).toString(CryptoJS.enc.Utf8);
          PARSER_WEBSOKET_MESSAGE(data,decrypt,'receiver')
          $('.heading-typing').fadeOut(200)
          SCROLL_TO_BOTTOM()
          READED_MSG(data.id_msg)

        }
      }else if(USER_ID === data.user ){
        let decrypt = CryptoJS.AES.decrypt(data.body,$('#scrims_chat_init').attr('data-public-key')).toString(CryptoJS.enc.Utf8);
        PARSER_WEBSOKET_MESSAGE(data,decrypt,'sender')
        SCROLL_TO_BOTTOM()
      }

      MESSAGE_NO_SEE(data,true)
      return false
  }


///// couple
  // Парсим сообщение которое пришло нам т.е. reciver
  if(data.companion === USER_ID && $('#scrims_chat_canvas').attr('data-init') === data.user){

    let decrypt = CryptoJS.AES.decrypt(data.body,KEY).toString(CryptoJS.enc.Utf8);
        PARSER_WEBSOKET_MESSAGE(data,decrypt,'receiver')
        $('.heading-typing').fadeOut(200)
        SCROLL_TO_BOTTOM()
        READED_MSG(data.id_msg)

  }  // Парсим сообщение которое мы отправили
  else if(data.user === USER_ID && $('#scrims_chat_canvas').attr('data-init') === data.companion){

        let decrypt = CryptoJS.AES.decrypt(data.body,$('#scrims_chat_init').attr('data-public-key')).toString(CryptoJS.enc.Utf8);
        PARSER_WEBSOKET_MESSAGE(data,decrypt,'sender')
        SCROLL_TO_BOTTOM()

   }
   MESSAGE_NO_SEE(data,false)
}



function PARSER_WEBSOKET_MESSAGE(data,decrypt,type){

  if(type == 'receiver'){
      var position = 'left'
      var galki =''
  }else{
    var position = 'right'
    var galki = `<span class="fa fa-check delivered_msg"></span><span class="fa fa-check reading_msg"></span>`
  }

  $('#scrims_chat_canvas').append(`<div id="id_msg_${data.id_msg}" class="row message-body scrims_chat_msg_${type}" data-init="${data.id_msg}">
          <div class="col-sm-12 message-main-${type}">
            <div class="${type}">
              <div class="message-text">
                ${decrypt}
              </div>
              <span class="message-time pull-right">
                ${moment().calendar()}
                ${galki}
              </span>
              <div class="col-sm-12">
              <img src="${data.img}" style="width:30px;height:30px;border-radius:50%;position:absolute;${position}:-50px;top: -25px;">
              </div>
            </div>
          </div>
      </div>`)

}



// if user not see recive message while no open contact or close chat
function MESSAGE_NO_SEE(data,group){

  console.log(data)

  if($('#scrims_chat').hasClass('scrims-chat-hide') == true){

    $('.common-chat-count-message').html(`<br><span id="common-chat-count-message-id" class="badge">${$('.scrims_chat_count_message').length}</span>`)
  }

  //if group
if(group == true){


  console.log(data.companion.indexOf(USER_ID),'------>')

  if (data.companion.indexOf(USER_ID)!=-1 && $('#scrims_chat_init').attr('data-init') != data.group){
    $('.scrims_chat_companion').each(function() {
      if($(this).attr('data-init') == data.group){
        //var count = parseInt($('.scrims_chat_count_message').text())
        var count = parseInt($(this).find('.scrims_chat_count_message').text())
        if(isNaN(count)==true){
          $(this).find(".pull-right").html('<div  class="badge scrims_chat_count_message shake-'+data.group+'">1</div>')
        }else{
          $(this).find(".pull-right").html('<div  class="badge scrims_chat_count_message shake-'+data.group+'">'+(count+1)+'</div>')

        }
        user = USERS.filter(a => a.id==data.group)
        noty(user[0].name, user[0].img, 'Отправил(а) вам') //-----------------------------------> lang

        $('#scrims_chat_contact_list').prepend('<div class="row sideBar-body scrims_chat_companion" data-init="'+data.group+'" data-group="true">'+$(this).html())
        $(this).remove()
        $('.shake-'+data.group).effect('shake', { times:3 }, 300);

      }
    })
    }
  }

    //if couple
  if (data.companion === USER_ID && $('#scrims_chat_canvas').attr('data-init') != data.user) {
        $('.scrims_chat_companion').each(function() {

          if($(this).attr('data-init') == data.user){
            //var count = parseInt($('.scrims_chat_count_message').text())
            var count = parseInt($(this).find('.scrims_chat_count_message').text())
            if(isNaN(count)==true){
              $(this).find(".pull-right").html('<div  class="badge scrims_chat_count_message shake-'+data.user+'">1</div>')
            }else{
              $(this).find(".pull-right").html('<div  class="badge scrims_chat_count_message shake-'+data.user+'">'+(count+1)+'</div>')

            }
            user = USERS.filter(a => a.id==data.user)
            noty(user[0].name, user[0].img, 'Отправил(а) вам') //-----------------------------------> lang

            $('#scrims_chat_contact_list').prepend('<div class="row sideBar-body scrims_chat_companion" data-init="'+data.user+'" data-group="false">'+$(this).html())
            $(this).remove()
            $('.shake-'+data.user).effect('shake', { times:3 }, 300);

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

  function hideKeyboard(element) {
      element.attr('readonly', 'readonly'); // Force keyboard to hide on input field.
      element.attr('disabled', 'true'); // Force keyboard to hide on textarea field.
      setTimeout(function() {
          element.blur();  //actually close the keyboard
          // Remove readonly attribute after keyboard is hidden.
          element.removeAttr('readonly');
          element.removeAttr('disabled');
      }, 100);
  }



  $('#scrims_chat_send').on('click',function(e){
      var img = $('#scrims_chat_init').find('img').attr('src')

      if($('#scrims_chat_init').attr('data-group') == 'true'){
          var group = true
      }else{
          var group = false
      }

      if(width_window<700){
          e.preventDefault();
          $('#scrims_chat_textarea').focus();
          SEND_MESSAGE( USER_ID, $('#scrims_chat_init').attr('data-init'), 'text',$('#scrims_chat_textarea').val(),USER_IMG,group)
      }else{
          SEND_MESSAGE( USER_ID, $('#scrims_chat_init').attr('data-init'), 'text',$('#scrims_chat_textarea').val(),USER_IMG,group)
      }
  })





 //ctr+enter send message
  $('#scrims_chat_textarea').bind('keypress', function(event) {
      if((event.keyCode == 10 || event.keyCode == 13) && event.ctrlKey) {

        if($('#scrims_chat_init').attr('data-group') == 'true'){
            var group = true
        }else{
            var group = false
        }
        var companion = $('#scrims_chat_init').attr('data-init')


        SEND_MESSAGE( USER_ID, companion,'text',$('#scrims_chat_textarea').val(),USER_IMG,group)

      }
  });



function AJAX(url,type,data){
  return $.ajax({
    url:url,
    type:type,
    dataType:'json',
    data:data,
  }).done(function(data){
  })
}



function CREATE_GROUP_SERVER(){

  users_group = []
  $('.invite').each(function(){
      if($(this).hasClass('active')==true){
        users_group.push($(this).attr('data-id'))
      }
  })
  $('#name_create_group').keydown(function(){
    $('#name_create_group').css({'box-shadow':''})
  })
  if($('#name_create_group').val() == '' ){
      $('#name_create_group').css({'box-shadow':'0 0 0 1px #f00'})
      $('#name_create_group').focus()
  }else if (users_group == ''){
      $('#dialog_list_users').css({'box-shadow':'0 0 0 1px #f00'})
  }else{
    users_group.push(USER_ID)
    let data = {
          'name':$('#name_create_group').val(),
          'csrfmiddlewaretoken':csrf_token,
          'users':users_group.join(','),
       }

         var a = AJAX('/api/create-group/','post', data)
         a.then(function(result){
          if(result.status == 'success'){
                console.log(result)

                NOTY(3000, 'success',LANG[0].success[0].success_create_group)

                $('#scrims_chat_contact_list').prepend(`<div class="row sideBar-body scrims_chat_companion" data-init="${result.init}" data-group="true">
                                                      <div class="col-sm-2 col-xs-2 sideBar-avatar">
                                                        <div class="avatar-icon avatar-icon-active">
                                                          <img src="" width="50px" height="50px">
                                                        </div>
                                                      </div>
                                                      <div class="col-sm-9 col-xs-9 sideBar-main">
                                                        <div class="row">
                                                          <div class="col-sm-8 col-xs-8 sideBar-name">
                                                            <span class="name-meta">${result.name}</span>
                                                            <div class="name-meta" style="color: #999;color: #999;overflow: hidden;width: 100%;text-overflow: ellipsis;"></div>
                                                          </div>
                                                          <div class="col-sm-3 col-xs-3 pull-right sideBar-time">
                                                            <span class="time-meta pull-right">
                                                          </span>

                                                          </div>
                                                        </div>
                                                      </div>
                                                    </div>`)
                $('#dialog-chat').dialog("close");
          }
          if(result.status == 'error'){
              if(result.reason == 'name exist'){
                $('#name_create_group').val('')
                NOTY(3000, 'error',LANG[0].error[0].error_group_exist)
              }

          }
        })

    }
}



function CREATE_GROUP(){
    $('#dialog-chat-content').empty()
    $('#dialog-chat-content').append(`<div id="id-dialog-param" data-init="create-group">
                                          <!--<label>${LANG[0].chat[0].name_group}</label>-->
                                          <input id="name_create_group" type="text" class="form-control" placeholder="${LANG[0].chat[0].name_group}" /><br>
                                          <label>${LANG[0].chat[0].invite}</label>
                                          <ul id="dialog_list_users" class="list-group"></ul>
                                          <br>
                                      </div>`)

    let users = USERS.filter(d => d.group==false)
    $.each(users,function(k,v){
        $('#dialog_list_users').append(`<li data-id="${v.id}" class="list-group-item invite">${v.name}</li>`)
    })

    ACTION_CLICK_GROUP_INVITE()
    $('#dialog-chat').dialog('option','title',LANG[0].chat[0].create_group );
    $('#dialog-chat').dialog('open')
  }

  function ACTION_CLICK_GROUP_INVITE(){
      $('.invite').click(function(){
        if($(this).hasClass('active') == true){
          $(this).removeClass('active')
        }else{
          $(this).addClass('active')
        }
        $('#dialog_list_users').css({'box-shadow':''})
   })
}




  $('#scrims_chat_create_group').on('click',function(){
    CREATE_GROUP()
  })


  $('#searchText').off('keydown')
  $('#searchText').on('keydown',function(e){

    if(e.keyCode == 13){
      $('.scrims_chat_companion:first').click()
      $('#scrims_chat_textarea').focus()
    }


    if($(this).val().length>2){
      MAIN_AJAX_GET('/api/search-users/'+$(this).val()+'/').then(function(users){
            $('#scrims_chat_contact_list').empty()
            RENDER_USERS(users)
      })
    }else{
      MAIN_AJAX_GET('/api/search-users/all/').then(function(users){
            $('#scrims_chat_contact_list').empty()
            RENDER_USERS(users)
      })
    }

  })


  function SELECT_COMPANION_ACTION(){
  $('.scrims_chat_companion').off('click')
  $('#scrims_chat_contact_list').on('click', '.scrims_chat_companion',function(){



    if($(this).hasClass('cleanstate_chat_companion') == true){return false}
    $('.scrims_chat_companion').removeClass('cleanstate_chat_companion')
    $(this).addClass('cleanstate_chat_companion');

    SELECT_COMPANION($(this).attr('data-init'),$(this).attr('data-group'))


    if(width_window<700){
        $('.conversation').addClass('active_chat_conversation')
    }

    $('#reply-to-chat').click(function(){
      $('#scrims_chat_canvas,#scrims_chat_heading').empty()
      $('.conversation').removeClass('active_chat_conversation')

    })


  })
}


$('#close-scrims-chat,.chat-close-open').click(function(){
  $('#scrims_chat').toggleClass('scrims-chat-hide')

  $('.chat-close-open').toggleClass('chat-close-open-active')

if($('#scrims_chat').hasClass('scrims-chat-hide')==true){
  if($('.scrims_chat_count_message').length == 0){
    $('.common-chat-count-message').html('')
  }else{
    $('.common-chat-count-message').html(`<br><span id="common-chat-count-message-id" class="badge">${$('.scrims_chat_count_message').length}</span>`)
  }
}

})



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
    socket.emit('user typing',{"user":USER_ID,"companion":$('#scrims_chat_init').attr('data-init')})
  }

  function TYPYNG_USR(data){


    if(data.companion === USER_ID && $('#scrims_chat_canvas').attr('data-init') === data.user){

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


  $('#scrims-upload').click(function(){
    $('.dz-hidden-input').click()
  })


//mobile actions







}//end chat
