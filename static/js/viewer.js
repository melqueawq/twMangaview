let page = 0;
let w = $(window).width();
let h = $(window).height();

$(function () {
    //
    // slider
    //
    $(".slider").slider({
        max: image_list.length,
        min: 1,
        value: image_list.length,
        stop: function () {
            let diff = (image_list.length - $(this).slider('value')) - page;
            if (diff != 0) {
                page += diff;
                $(".page").fadeOut(200, function () {
                    reload();
                    $(".page").fadeIn(200);
                });
            }
        }
    });

    reload();
    $(window).resize(function () {
        reload();
    });


    //
    //  touchevent
    //
    let touchposx, touchposy;
    $(window).on("touchstart", onTouchStart);
    $(window).on("touchend", onTouchEnd);
    $(window).on("mousedown", onTouchStart);
    $(window).on("mouseup", onTouchEnd);

    function onTouchStart(e) {
        touchposx = e.pageX;
        touchposy = e.pageY;
    }

    function onTouchEnd(e) {
        if (e.pageY < 30 || e.pageY > h - 50) {
            return;
        }
        if (touchposx - e.pageX < -70) {
            slide(1);
        } else if (touchposx - e.pageX > 70) {
            slide(-1);
        } else if (Math.abs(touchposx - e.pageX) < 20) {
            if (e.pageX < w / 6) {
                slide(1);
            } else if (e.pageX > w - w / 6) {
                slide(-1);
            } else {
                menuToggle();
            }
        }
    }


    function menuToggle() {
        $("#menu").toggle("slide", {
            direction: "up",
            duration: 300
        });

        $("#sbar").toggle("slide", {
            direction: "down",
            duration: 300
        });
        $("#pageDisp").toggle("slide", {
            direction: "down",
            duration: 300
        });
    }

    //
    //  slide page
    //
    function slide(vec = 1) {
        if ($(".page").is(":animated")) {
            return -1;
        }

        let ope = "+="
        if (vec >= 1) {
            if (page >= image_list.length - 1) {
                return -1
            }
            page += 1;
        } else {
            if (page <= 0) {
                return -1
            }
            page -= 1;
            ope = "-="
        }

        $(".page").animate({
            "left": ope + w
        }, {
            duration: 300,
            complete: function () {
                reload();
            }
        });
        return 0
    }

    //
    //  image reload
    //
    function reload() {
        w = $(window).width();
        h = $(window).height();

        $(
            $(".page")
            .get()
            .reverse()
        ).each(function (index, element) {
            if (page - 1 + index >= 0 && page - 1 + index < image_list.length) {
                $(element).html('<img src="' + image_list[page - 1 + index] + '">');
            }
            let left = w - $(element).children("img").width();
            console.log(left);
            $(element).css("left", w - w * index + left / 2);
        });

        $("#pageDisp").html("" + (page + 1) + " / " + image_list.length);
        $(".slider").slider({
            value: (image_list.length - page)
        });

        if (w < h) {
            console.log("w < h");
            $(".page img")
                .css("width", "95%")
                .css("height", "auto");
        } else {
            console.log("w > h");
            $(".page img")
                .css("width", "auto")
                .css("height", "95vh");
        }
    }
})