/**
 * Created by bwz on 15/11/8.
 */
csrfmiddlewaretoken = $('#csrfmiddlewaretoken').val();
function o_c_categorys(self,num){
    $(self).toggleClass('current-click');
    if($('#category').height()>0){
        $('#category').css('height','0');
        $(self).css('border-bottom','1px solid #85CCCB');
    }else{
        $('#category').css('height',num*39);
        $(self).css('border-bottom','0px solid #EFEFEF');
    }
}
$("#uptop").click(function () {
    $.scrollTo('html', 200);
});

function hide_tip(){
    $("#error_show").removeClass('error_show')
}
function show_error(msg){
    $('#right_mb').hide();
    $("#error_show span").html(msg)
    $('#error_show').removeClass('error_show_green')
    $("#error_show").addClass('error_show error_show_red')
    setTimeout(hide_tip,3000)
}
function show_tip(msg){
    $('#right_mb').hide()
    $("#error_show span").html(msg)
    $('#error_show').removeClass('error_show_red')
    $("#error_show").addClass('error_show error_show_green')
}
function sub_comment(){
    var nickname = $.trim($('#add_comment input[name=nickname]').val());
    var url = $.trim($('#add_comment input[name=url]').val());
    var content = $.trim($('#add_comment textarea[name=content]').val());
    if(nickname==''){
        show_error('昵称不能为空,var ss = content.match(/\[[\u4e00-\u9fa5]+]/g)')
        return
    }
    if (content==''){
        show_error('评论不能为空')
        return
    }
    content = content.replace(/\[/g,'<img src="/static/image/face/');
    content = content.replace(/\]/g,'.gif">');
    show_tip('正在发表评论')
    $.post('/sub_comment/',{
        csrfmiddlewaretoken:csrfmiddlewaretoken,
        nickname:nickname,
        url:url,
        content:content,
        blog_name:$("#blog_name").val(),
        parent_id:$("#parent_id").val()
    },function(data){
        if(data['is_succ']){
            hide_tip();
            $('#add_comment textarea[name=content]').val('')
            window.location.reload()
        }else{
            show_error(data['msg'])
        }
    })
}
function t_comment(parent_id,name){
    $('#parent_id').val(parent_id)
    $("#replay_p span").html(name)
    $("#replay_p").show()
    $.scrollTo('#add_comment',200)
}
function cancle_replay(){
    $('#parent_id').val('')
    $("#replay_p span").html('')
    $("#replay_p").hide()
}
function change_back(self) {
    if (!$(self).parent().hasClass('loading_ajax')){
        $(self).parent().addClass('loading_ajax')
        var heavyImage = new Image();
        var url = backgroundlist[parseInt(Math.random()*backgroundlist.length)]
        heavyImage.src = url ;
        heavyImage.onload = function() {
            $('body').css('background-image',"url("+url+")")
            $(self).parent().removeClass('loading_ajax')
        }
    }
}
$(function(){
    $("#error_show a").bind('click',function(){
        $(this).parent().removeClass('error_show')
    })

})