
  function visibility(data,flag){
    if(flag == 0){
      $(".search_dropdown").hide();
    }
    else{
      var serbox = document.getElementById("skin_search");
      console.log("inside else");
      $(".dropdown_list").html(data);
      // if($("#skin_search").is(":focus")){
      if(serbox === document.activeElement){
        console.log("in focus");
        $(".search_dropdown").show();
      }
      $("#skin_search").on("focusout",()=>{
        console.log("out of focus");
        $(".search_dropdown").hide();
      })
    
    }

  }
$(document).ready(function(){
    var val,timer,response,flag;
  
    $("#skin_search").bind('keyup',function(){
      clearTimeout(timer);
      var search = $(this).val();

      if(search.length <3){
        flag = 0;
      }

      else if(search.length >= 3 && search != val){           

      timer = setTimeout(function(){
        val = search;
        console.log("Ajax query",val);
        var name_obj = {"skin_name":val}
      $.ajax({
      type: "POST",
      url: "/fetchsuggestions",
      data: JSON.stringify(name_obj),
      // dataType: "json",
      contentType: "application/json;charset=UTF-8",
      // <!-- beforeSend: function(){ -->
      //   <!-- $("#search-box").css("background","#FFF url(LoaderIcon.gif) no-repeat 165px"); -->
      // // <!-- }, 
      success: function(data){
        flag = 1;
        visibility(data,flag)
        console.log("print only on success")
        response = data;
        // $("#suggesstion-box").show();
        // $(".dropdown_list").html(response); 
        // $(".search_dropdown").show();
        // <!-- $("#search-box").css("background","#FFF"); -->
      }
      });
       
        },1000)
      }
      visibility(response,flag);

    });
  });
