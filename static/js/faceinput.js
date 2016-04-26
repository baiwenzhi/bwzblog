/**
 * Created by bwz on 15/12/4.
 */
ss='[骷髅][擦汗][憨笑]'
$(document).ready(function(e) {
    ImgIputHandler.Init();
});
var ImgIputHandler={
    facePath:[
        {faceName:"微笑",facePath:"微笑.gif"},
        {faceName:"撇嘴",facePath:"撇嘴.gif"},
        {faceName:"色",facePath:"色.gif"},
        {faceName:"发呆",facePath:"发呆.gif"},
        {faceName:"得意",facePath:"得意.gif"},
        {faceName:"流泪",facePath:"流泪.gif"},
        {faceName:"害羞",facePath:"害羞.gif"},
        {faceName:"睡",facePath:"睡.gif"},
        {faceName:"闭嘴",facePath:"闭嘴.gif"},
        {faceName:"大哭",facePath:"大哭.gif"},
        {faceName:"尴尬",facePath:"尴尬.gif"},
        {faceName:"发怒",facePath:"发怒.gif"},
        {faceName:"调皮",facePath:"调皮.gif"},
        {faceName:"龇牙",facePath:"龇牙.gif"},
        {faceName:"惊讶",facePath:"惊讶.gif"},
        {faceName:"难过",facePath:"难过.gif"},
        {faceName:"酷",facePath:"酷.gif"},
        {faceName:"冷汗",facePath:"冷汗.gif"},
        {faceName:"抓狂",facePath:"抓狂.gif"},
        {faceName:"吐",facePath:"吐.gif"},
        {faceName:"偷笑",facePath:"偷笑.gif"},
        {faceName:"可爱",facePath:"可爱.gif"},
        {faceName:"白眼",facePath:"白眼.gif"},
        {faceName:"傲慢",facePath:"傲慢.gif"},
        {faceName:"饥饿",facePath:"饥饿.gif"},
        {faceName:"困",facePath:"困.gif"},
        {faceName:"惊恐",facePath:"惊恐.gif"},
        {faceName:"流汗",facePath:"流汗.gif"},
        {faceName:"憨笑",facePath:"憨笑.gif"},
        {faceName:"大兵",facePath:"大兵.gif"},
        {faceName:"奋斗",facePath:"奋斗.gif"},
        {faceName:"咒骂",facePath:"咒骂.gif"},
        {faceName:"疑问",facePath:"疑问.gif"},
        {faceName:"嘘",facePath:"嘘.gif"},
        {faceName:"晕",facePath:"晕.gif"},
        {faceName:"折磨",facePath:"折磨.gif"},
        {faceName:"衰",facePath:"衰.gif"},
        {faceName:"骷髅",facePath:"骷髅.gif"},
        {faceName:"敲打",facePath:"敲打.gif"},
        {faceName:"再见",facePath:"再见.gif"},
        {faceName:"擦汗",facePath:"擦汗.gif"},
        {faceName:"抠鼻",facePath:"抠鼻.gif"},
        {faceName:"鼓掌",facePath:"鼓掌.gif"},
        {faceName:"糗大了",facePath:"糗大了.gif"},
        {faceName:"坏笑",facePath:"坏笑.gif"},
        {faceName:"左哼哼",facePath:"左哼哼.gif"},
        {faceName:"右哼哼",facePath:"右哼哼.gif"},
        {faceName:"哈欠",facePath:"哈欠.gif"},
        {faceName:"鄙视",facePath:"鄙视.gif"},
        {faceName:"委屈",facePath:"委屈.gif"},
        {faceName:"快哭了",facePath:"快哭了.gif"},
        {faceName:"阴险",facePath:"阴险.gif"},
        {faceName:"亲亲",facePath:"亲亲.gif"},
        {faceName:"吓",facePath:"吓.gif"},
        {faceName:"可怜",facePath:"可怜.gif"},
        {faceName:"菜刀",facePath:"菜刀.gif"},
        {faceName:"西瓜",facePath:"西瓜.gif"},
        {faceName:"啤酒",facePath:"啤酒.gif"},
        {faceName:"篮球",facePath:"篮球.gif"},
        {faceName:"乒乓",facePath:"乒乓.gif"},
        {faceName:"拥抱",facePath:"拥抱.gif"},
        {faceName:"握手",facePath:"握手.gif"},
        {faceName:"得意地笑",facePath:"得意地笑.gif"},
        {faceName:"听音乐",facePath:"听音乐.gif"}
    ]
    ,
    Init:function(){
        var isShowImg=false;
        $(".imgBtn").click(function(){
            if(isShowImg==false){
                isShowImg=true;
                $(this).parent().prev().addClass('faceshow');
                if($(".faceDiv").children().length==0){
                    for(var i=0;i<ImgIputHandler.facePath.length;i++){
                        $(".faceDiv").append("<img title=\""+ImgIputHandler.facePath[i].faceName+"\" src=\"/static/image/face/"+ImgIputHandler.facePath[i].facePath+"\" />");
                    }
                    $(".faceDiv>img").click(function(){

                        isShowImg=false;
                        $(this).parent().removeClass('faceshow');
                        ImgIputHandler.insertAtCursor($(".Input_text")[0],"["+$(this).attr("title")+"]");
                    });
                }
            }else{
                isShowImg=false;
                $(this).parent().prev().removeClass('faceshow');
            }
        });
    },
    insertAtCursor:function(myField, myValue) {
    if (document.selection) {
        myField.focus();
        sel = document.selection.createRange();
        sel.text = myValue;
        sel.select();
    } else if (myField.selectionStart || myField.selectionStart == "0") {
        var startPos = myField.selectionStart;
        var endPos = myField.selectionEnd;
        var restoreTop = myField.scrollTop;
        myField.value = myField.value.substring(0, startPos) + myValue + myField.value.substring(endPos, myField.value.length);
        if (restoreTop > 0) {
            myField.scrollTop = restoreTop;
        }
        myField.focus();
        myField.selectionStart = startPos + myValue.length;
        myField.selectionEnd = startPos + myValue.length;
    } else {
        myField.value += myValue;
        myField.focus();
    }
}
}