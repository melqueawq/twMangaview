let page = 0;
let w = $(window).width();
let h = $(window).height();

$(function () {
    reload();
    $(window).resize(function () {
        reload();
    });


    //
    //  touchevent
    //
    let touchpos, direction;
    $(window).on('touchstart', onTouchStart);
    $(window).on('touchend', onTouchEnd);
    $(window).on('mousedown', onTouchStart);
    $(window).on('mouseup', onTouchEnd);

    function onTouchStart(e) {
        touchpos = e.pageX;
    }

    function onTouchEnd(e) {
        if (touchpos - e.pageX < -70) {
            slide(1);
        } else if (touchpos - e.pageX > 70) {
            slide(-1);
        } else if (Math.abs(touchpos - e.pageX) < 20) {
            if (e.pageX < w / 6) {
                slide(1);
            } else if (e.pageX > w - w / 6) {
                slide(-1);
            }
        }
    }


    //
    //  slide page
    //
    function slide(vec = 1) {
        if ($('.page').is(animated)) {
            return;
        }

        let ope = "+="
        if (vec == 1) {
            if (page >= image_list.length - 1) {
                return
            }
            page += 1;
        } else {
            if (page <= 0) {
                return
            }
            page -= 1;
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

    //
    //  image reload
    //
    function reload() {
        w = $(window).width();
        $($(".page").get().reverse()).each(function (index, element) {
            if (page - 1 + index >= 0 && page - 1 + index < image_list.length) {
                $(element).html('<img src="' + image_list[page - 1 + index] + '">');
            }
            $(element).css('left', w - w * index);
        });
    }
})