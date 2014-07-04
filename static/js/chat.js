$(function () {
  function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
  }

  function getUrlParam(name) {
    var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)");
    var r = window.location.search.substr(1).match(reg);
    if (r != null)
      return r[2];
      //return unescape(r[2]);
    return null;
  }

  $("form").submit(function (){
    //alert(decodeURI(getUrlParam("cname")));
    var msg = $("#input").val();
    $.post(
      '/channel/chat',
      {msg:msg, cname:decodeURI(getUrlParam("cname")), _xsrf:getCookie("_xsrf")},
      function (data) {
        $("#input").val('');
      });
    return false;
  });

  var updater = {
    poll: function(){
      $.ajax({url: "/longpolling",
        type: "POST",
        dataType: "json",
        data: {cname:decodeURI(getUrlParam("cname")), _xsrf:getCookie("_xsrf")},
        success: updater.onSuccess,
        error: updater.onError});
    },
    onSuccess: function(data, dataStatus){
      for (var p in data)
        console.log(p + ":" + data[p])
      try{
        if (data.msg != "") {
          if (data.badge) {
            var channel = "#" + data.cname
            var number = parseInt($(channel).text()) + 1;
            $(channel).html(number);
          } else {
		    $("#display").append(data.name + ": " + data.msg + "\n");
		  }
        }
      }
      catch(e){
        updater.onError(e);
        return;
      }
      updater.poll();
    },
    onError: function(e){
      if (e.message)
        console.log("Poll Error" + e.message);
      else
        console.log(e);
    }
  };

  updater.poll();
});

