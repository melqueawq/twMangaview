let page = 0;
let w = $(window).width();
let h = $(window).height();

$(function () {
    reload();
    $(window).resize(function () {
        reload();
    });

    $('html').click(function (e) {

        let x = e.pageX;
        console.log('x:' + x + " w:" + w);
        //次ページ

        if (x < w / 2) {
            if (page >= image_list.length - 1) {
                return
            }
            page += 1;
            slide(0);
        } else {
            if (page <= 0) {
                return
            }
            page -= 1;
            slide(1);
        }
    });
})

function slide(vec = 0) {
    let ope = "+="
    if (vec != 0) {
        ope = "-="
    }

    $('.page').animate({
        'left': ope + w
    }, {
        duration: 300,
        complete: function () {
            reload();
        }
    });
}

function reload() {
    w = $(window).width();
    $($(".page").get().reverse()).each(function (index, element) {
        if (page - 1 + index >= 0 && page - 1 + index < image_list.length) {
            $(element).html('<img src="' + image_list[page - 1 + index] + '">');
        }
        $(element).css('left', w - w * index);
    });
}