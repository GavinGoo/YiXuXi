// window.addEventListener('resize', function () {
//     var windowWidth = window.innerWidth || document.documentElement.clientWidth || document.body.clientWidth;

//     if (windowWidth <= 1200) {
//         $(".option").style.dis
//     } else {
//         resetSelect('desktopSelect');
//     }
// })

document.getElementById("content").addEventListener('resize', function () {
    this.style.resize = "vertical !important";
})

document.getElementById("article").addEventListener('resize', function () {
    this.style.resize = "vertical !important";
})

// 文本框自动伸长
// document.getElementById("content").addEventListener("input", function() {
//     // console.log('height =>'+this.scrollHeight);
//     this.style.height = "auto";
//     this.style.height = (this.scrollHeight) + "px";

//     // const { width, fontSize, fontFamily, fontWeight } = getComputedStyle(this);
//     // var multiple = (this.scrollHeight) / 200;
//     // this.style.fontSize = (fontSize / multiple) + "px";
//     // this.style.fontSize = "16px";
//     // console.log('fontsize =>'+this.style.fontSize);
// });

function extend_height() {
    var deepl_scrollHeight = $('.deepl')[0].scrollHeight;
    var gpt_scrollHeight = $('.gpt')[0].scrollHeight;
    var max_scrollHeight = (deepl_scrollHeight > gpt_scrollHeight) ? deepl_scrollHeight : gpt_scrollHeight
    if (max_scrollHeight == deepl_scrollHeight) {
        console.log('最长文本框为deepl：'+ max_scrollHeight);
        $('.gpt').animate({ height: deepl_scrollHeight }, 100);
        $('.deepl').animate({ height: deepl_scrollHeight }, 100);
        $('#content').animate({ height: deepl_scrollHeight }, 100);
    }
    else if (max_scrollHeight == gpt_scrollHeight) {
        console.log('最长文本框为gpt：'+ max_scrollHeight);
        $('.deepl').animate({ height: gpt_scrollHeight }, 100);
        $('.gpt').animate({ height: gpt_scrollHeight }, 100);
        $('#content').animate({ height: gpt_scrollHeight }, 100);
    }
}

$(".send-btn").click(function () {
    // 获取输入内容
    console.log('触发翻译！');
    $('.send-btn').attr('aria-busy', 'true');
    $('.deepl').attr('aria-busy', 'true');
    $('.gpt').attr('aria-busy', 'true');
    var text = $("#content").val();
    var source_language = $(".source").val();
    var target_language = $(".target").val();
    console.log('源语言：' + source_language);
    console.log('目标语言：' + target_language);
    if (text == "") {
        alert("请输入内容！");
        return;
    }else{
        // 创建一个Deferred对象
        var deeplDeferred = $.Deferred();
        var gptDeferred = $.Deferred();

        // let deeplx_content = $('.deepl');

        $.ajax({
            url: "/translate/deepl",
            data: {
                "send_message": text,
                "source_language": source_language,
                "target_language": target_language
            },
            type: "Post",
            dataType: "json",
            xhrFields: {
                onprogress: function (e) {
                    $('.send-btn').attr('aria-busy', 'false');
                    $('.deepl').attr('aria-busy', 'false');
                    let response = e.currentTarget.response;
                    // console.log('收到deepl译文：'+response);
                    // console.log(response);
                    if (response.startsWith("url_redirect:")){
                        window.location.href=response.split(":")[1];
                    } else {
                        deepl_response = response.replace(/\n/g, '<br>');
                        // gpt_response = gpt_response.replace(/\n/g, '<br>');

                        // deepl_response = response.replace(/\n/g, '<br>');
                        // var translation =  document.createElement('p');
                        // var transText =  document.createTextNode(response);
                        var deepl_translation = $('<p>').html(deepl_response);
                        // var gpt_translation = $('<p>').html(gpt_response);
                        $('.deepl').empty();
                        $('.deepl').append(deepl_translation);

                        // $('.gpt').empty();
                        // $('.gpt').append(gpt_translation);

                        // translation.createTextNode(response);
                        // translation.appendChild(transText);
                        // deeplx_content.append(translation);

                        // deeplx_content.innerHTML = '<p>' + response + '</p>';

                        // 自动滚动至最下面
                        // $(".deepl").scrollTop($(".deepl")[0].scrollHeight);

                        // 在每次响应时更新高度
                        updateHeight();
                        
                    }
                },
                onload: function() {
                    // 通知Deferred对象操作完成
                    deeplDeferred.resolve();
                }
                
            },
        }),

        // 自动延申文本框
        // extend_height();

        $.ajax({
            url: "/translate/gpt",
            data: {
                "send_message": text,
                "source_language": source_language,
                "target_language": target_language
            },
            type: "Post",
            dataType: "json",
            xhrFields: {
                onprogress: function (e) {
                    $('.send-btn').attr('aria-busy', 'false');
                    $('.gpt').attr('aria-busy', 'false');
                    let response = e.currentTarget.response;
                    // console.log('收到gpt译文：'+response);
                    // console.log(response);
                    if (response.startsWith("url_redirect:")){
                        window.location.href=response.split(":")[1];
                    } else {
                        gpt_response = response.replace(/\n/g, '<br>');
                        // var deepl_translation = $('<p>').html(deepl_response);
                        var gpt_translation = $('<p>').html(gpt_response);
                        $('.gpt').empty();
                        $('.gpt').append(gpt_translation);
                        // translation.createTextNode(response);
                        // translation.appendChild(transText);
                        // deeplx_content.append(translation);

                        // deeplx_content.innerHTML = '<p>' + response + '</p>';

                        // 自动滚动至最下面
                        // $(".gpt").scrollTop($(".gpt")[0].scrollHeight);

                        // 自动延申文本框
                        // extend_height();

                        // 在每次响应时更新高度
                        updateHeight();
                    }
                },
                onload: function() {
                    // 通知Deferred对象操作完成
                    gptDeferred.resolve();
                }
            },
        })

        // // 自动延申文本框
        // extend_height();

        function updateHeight() {
            var maxHeight = Math.max($('.deepl')[0].scrollHeight, $('.gpt')[0].scrollHeight);
            $('.deepl').animate({ height: maxHeight }, 250);
            // 修复滚动
            // $('.deepl').css('overflow', 'auto');
            $('.gpt').animate({ height: maxHeight }, 250);
            // $('.gpt').css('overflow', 'auto');
            $('#content').animate({ height: maxHeight }, 250);
            // $('#content').css('overflow', 'auto');

            $('.deepl').css({'resize': 'vertical' ,'overflow': 'auto'});
            $('.gpt').css({'resize': 'vertical' ,'overflow': 'auto'});
        }
    }

    
});

// 回车触发翻译按钮 => 容易误触 还是不用了= =
// $("#content").keydown(function (e) {
//     if (e.keyCode === 13 && !e.shiftKey) {
//         e.preventDefault();
//         $("#send-btn").click();
//     }
// });

// 语言切换
$(".switch_lang").click(function () {
    var source_lang = $(".source").val();
    var target_lang = $(".target").val();
    // console.log('源语言：'+source_lang);
    // console.log('目标语言：'+target_lang);
    if(source_lang == 'auto'){
        alert("请手动选择源语言！");
    }else{
        $(".source").val(target_lang);
        $(".target").val(source_lang);
    }
})

// 复制功能
// 使Clipboard监听复制按钮的id"copy-btn"
new ClipboardJS('#copy-btn');
function copy() {
    var obj=event.srcElement;
    var content=obj.parentElement.nextElementSibling.textContent;   //获取button标签下面的pre标签里的文字内容
    // 对button标签注入Clipboard相关属性
    obj.setAttribute("data-clipboard-action","copy");
    obj.setAttribute("data-clipboard-text",content);
//          console.log(event.srcElement);
    console.log('复制内容 =>'+content);
    // 复制状态
    obj.innerHTML='';
    obj.innerHTML="已复制(•̀ᴗ•́)و";
    setTimeout(()=>{
        obj.innerHTML='';
        obj.innerHTML="复制";
    },2000);
};

// 粘贴功能
function paste() {
    // const pasteText = document.querySelector('#content');
    // pasteText.focus();
    // document.execCommand('paste');
    // 复制状态
    // obj.innerHTML='';
    // obj.innerHTML="已粘贴(•̀ᴗ•́)و";
    // setTimeout(()=>{
    //     obj.innerHTML='';
    //     obj.innerHTML="粘贴";
    // },2000);

    navigator.clipboard.readText().then((text) => {
        // console.log('从剪贴板中粘贴的文本内容：' + text);
        const pasteText = document.querySelector('#content');
        pasteText.innerHTML='';
        // 保险操作
        $('#content').empty();
        pasteText.innerHTML = text;

        // 自动延申文本框高度
        // pasteText.style.height = "auto";
        // pasteText.style.height = (pasteText.scrollHeight) + "px";
    });
}