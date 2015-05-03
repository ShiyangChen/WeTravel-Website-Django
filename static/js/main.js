 $(function() {
        $("#comment-form").submit(function(){
            
           var comment_value = $("#comment-text").val();
       
             $(this).ajaxSubmit({
                type:"post",  //提交方式
                 dataType:"text", //数据类型
                url:"wetravel/comment_upload", //请求url
                 data: {
                 
                 'comment-text': comment-text,
               
                 },
                 success:function(data){ //提交成功的回调函数
                     loadNewContents()
                     $("#comment_value").val("");
                 }
             });
             return false; //不刷新页面
         });
     });


  //加载最新的评论
      function loadNewContents()
      {
          var lstContent = $("#lstContents");
          //lstContent.html("");
 
         
          $(this).ajaxSubmit({
              type: "post",  //提交方式
             dataType: "text", //数据类型
             url: "wetravel/comment_upload", //请求url
             data: {
                'comment-text': comment-text,
             },
             success: function (data) { //提交成功的回调函数
                 if(data.length >0)
                 {
                      $("#lstContents").html(data);
                  }
                               }
         });
     }