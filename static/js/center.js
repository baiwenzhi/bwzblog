csrfmiddlewaretoken = $("#csrfmiddlewaretoken").val();
function load_right(url) {
    $("#right_mb").show();
    $("#main-right").load(url, $.extend({}, {csrfmiddlewaretoken: csrfmiddlewaretoken}), function () {
        $("#right_mb").hide()
    })
}
function add_category() {
    var name = $("#category_name").val();
    if (name == "") {
        show_error("请填写分类名");
        return
    }
    $("#right_mb").show();
    $.post("/usercenter/add_category/", {
        csrfmiddlewaretoken: csrfmiddlewaretoken,
        name: $("#category_name").val()
    }, function (data) {
        if (data["is_succ"]) {
            load_right("/usercenter/categorys/")
        } else {
            show_error(data["msg"])
        }
    })
}
var delete_category = function (self, category_id) {
    $("#right_mb").show();
    $.post("/usercenter/del_category/", {csrfmiddlewaretoken: csrfmiddlewaretoken, id: category_id}, function (data) {
        if (data["is_succ"]) {
            $("#right_mb").hide();
            $(self).parent().parent().remove()
        } else {
            show_error(data["msg"])
        }
    })
};
var delete_blog = function (self, blog_id) {
    $("#right_mb").show();
    $.post("/usercenter/delete_blog/", {csrfmiddlewaretoken: csrfmiddlewaretoken, id: blog_id}, function (data) {
        if (data["is_succ"]) {
            $(self).parent().parent().remove();
            $("#right_mb").hide()
        } else {
            show_error(data["msg"])
        }
    })
};
var del_blog = function (myself, blog_id) {
    show_tip("正在删除");
    $.post("/usercenter/delete_blog/", {csrfmiddlewaretoken: csrfmiddlewaretoken, id: blog_id}, function (data) {
        if (data["is_succ"]) {
            $(myself).parent().parent().remove();
            hide_tip()
        } else {
            show_error(data["msg"])
        }
    })
};
var delete_comment = function (self, id) {
    $.post("/usercenter/del_comment/", {csrfmiddlewaretoken: csrfmiddlewaretoken, id: id}, function (data) {
        if (data["is_succ"]) {
            $(self).parent().parent().remove();
            $("#right_mb").hide()
        } else {
            show_error(data["msg"])
        }
    })
};
var delete_user = function (myself, user_id) {
    $("#right_mb").show();
    $.post("/usercenter/delete_user/", {csrfmiddlewaretoken: csrfmiddlewaretoken, id: user_id}, function (data) {
        if (data["is_succ"]) {
            $(myself).parent().prev().html(data["status"]);
            if (data["status"] == "") {
                $(myself).html("删除")
            } else {
                $(myself).html("取消删除")
            }
            $("#right_mb").hide()
        } else {
            show_error(data["msg"])
        }
    })
};
function save_blog(ifmarkdown) {
    var title = $("#title").val();
    if (title == "") {
        show_error("标题或摘要不能为空");
        return
    }
    if ($("#category_id").val() == "") {
        show_error("分类不能空");
        return
    }
    var content = ifmarkdown ? testEditor.getPreviewedHTML() : editor_a.getContent();
    var blogmd = ifmarkdown ? testEditor.getMarkdown() : "";
    $.post("/usercenter/edit/", {
        csrfmiddlewaretoken: csrfmiddlewaretoken,
        id: $("#blog_id").val(),
        title: title,
        taglist: $("#tag_id").val(),
        content: content,
        blogmd: blogmd,
        category_id: $("#category_id").val()
    }, function (data) {
        if (data["is_succ"]) {
            load_right("/usercenter/blogs/")
        } else {
            show_error(data["msg"])
        }
    })
}
function choose_by_category(self) {
    var category_id = $(self).val();
    if (category_id != "") {
        $(".blog_item").hide();
        $(".c_" + category_id).show()
    } else {
        $(".blog_item").show()
    }
}
function fav_blog(myself, blog_id) {
    var fav = $(myself).attr("fav");
    $.post("/fav_blog/", {csrfmiddlewaretoken: csrfmiddlewaretoken, id: blog_id, fav: fav}, function (data) {
        if (data["is_succ"]) {
            if (fav == 0) {
                $(myself).attr("fav", "1");
                $(myself).css("color", "#52CBA9");
                $(myself).html("设为推荐")
            } else {
                $(myself).attr("fav", "0");
                $(myself).css("color", "red");
                $(myself).html("取消推荐")
            }
        } else {
            show_error(data["msg"])
        }
    })
}
function bind_dialog_yes(fn, msg, a, b, c, d) {
    $("#cd-popup p").html(msg);
    $("#cd-popup li:first a").unbind("click");
    $("#cd-popup li:first a").on("click", function () {
        $("#cd-popup").removeClass("is-visible");
        fn(a, b, c, d)
    });
    $("#cd-popup").addClass("is-visible")
}
function show_edit_logo(self) {
    $(self).prev().show();
    $(self).hide();
    $(self).nextAll().show()
}
function cancle_edit_logo(self) {
    $(self).hide();
    $(self).prev().hide();
    $(self).prev().prev().show();
    $(self).prev().prev().prev().hide();
    $(self).prev().prev().prev().val("")
}
function PreviewImage(imgFile) {
    var filextension = imgFile.value.substring(imgFile.value.lastIndexOf("."), imgFile.value.length);
    filextension = filextension.toLowerCase();
    if ((filextension != ".jpg") && (filextension != ".gif") && (filextension != ".jpeg") && (filextension != ".png") && (filextension != ".bmp")) {
        show_error("格式不对");
        imgFile.focus()
    } else {
        var path;
        if (document.all) {
            imgFile.select();
            path = document.selection.createRange().text;
            document.getElementById("imgPreview").innerHTML = "";
            document.getElementById("imgPreview").style.filter = "progid:DXImageTransform.Microsoft.AlphaImageLoader(enabled='true',sizingMethod='scale',src=\"" + path + '")'
        } else {
            path = window.URL.createObjectURL(imgFile.files[0]);
            image = new Image();
            image.src = path;
            image.onload = function () {
                if (image.width > 500 || image.height > 500) {
                    show_error("图片格式太大，请上传500*500以下图片")
                } else {
                    document.getElementById("imgPreview").innerHTML = "<img src='" + path + "'/>"
                }
            }
        }
    }
}
function save_user_logo(self) {
    if (!/\.(gif|jpg|jpeg|png|GIF|JPG|PNG)$/.test($("#user_logo").val())) {
        show_error("图片格式不对");
        return false
    }
    show_tip("正在上传");
    $.ajaxFileUpload({
        type: "post",
        url: "/usercenter/save_logo/",
        fileElementId: "user_logo",
        dataType: "json",
        data: {csrfmiddlewaretoken: csrfmiddlewaretoken},
        success: function (data) {
            if (data["is_succ"]) {
                hide_tip();
                $(".log_img img").attr("src", data["img_url"]);
                cancle_edit_logo($(self).next())
            } else {
                show_error(data["msg"])
            }
        }
    })
}
function add_tag(self) {
    $(self).parent().next().show()
}
function cancle_add_tag(self) {
    $(self).parent().hide()
}
function add_tag_post(self) {
    var name = $(self).prev().val();
    if (name == "") {
        show_error("标签不能为空")
    } else {
        show_tip("正在提交");
        $.post("/usercenter/add_tag/", {csrfmiddlewaretoken: csrfmiddlewaretoken, name: name}, function (data) {
            if (data["is_succ"]) {
                hide_tip();
                cancle_add_tag(self);
                $("#tag_id").append("<option value='" + data["tag_id"] + "'>" + name + "</option")
            } else {
                show_error(data["msg"])
            }
        })
    }
}
$(function () {
    $("#menubar a").bind("click", function () {
        if ($(this).attr("url")) {
            $("#menubar .current-click").removeClass("current-click");
            load_right($(this).attr("url"));
            $(this).parent().addClass("current-click")
        }
    });
    $("#cd-popup").on("click", function (event) {
        console.log($(event.target));
        if ($(event.target).is("#cd-popup .cd-popup-close") || $(event.target).is(".cd-popup")) {
            event.preventDefault();
            $(this).removeClass("is-visible")
        }
    });
    $("#cd-popup li:last a").on("click", function (event) {
        $("#cd-popup").removeClass("is-visible")
    });
    $(document).keyup(function (event) {
        if (event.which == "27") {
            $("#cd-popup").removeClass("is-visible")
        }
    })
});
$(document).ready(function () {
    var hash = window.location.hash;
    if (hash != "") {
        $('#menubar a[href="' + hash + '"]').parent().addClass("current-click");
        url = hash.replace("#", "");
        load_right(url)
    }
});