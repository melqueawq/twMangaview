let pagenum = 0;

let pages;

let reload = () => {
    Array.from(pages).reverse().forEach((element, index) => {
        if (index + pagenum >= 0 && index + pagenum < image_list.length) {
            element.innerHTML = "<img src=" + image_list[index + pagenum] + ">"
        } else {
            element.innerHTML = ""
        }
    });

    document.getElementById("pagenum").innerHTML = "<p>" + (pagenum + 1) + "/" + image_list.length + "</p>"

    document.documentElement.style.setProperty('--page-max', (image_list.length - 1).toString());
    document.documentElement.style.setProperty('--page-now', pagenum.toString());
}

window.onload = function () {
    pages = document.getElementsByClassName('page');
    reload();

    //ページクリック時のページめくり
    Array.from(pages).forEach((element, index) => {
        element.addEventListener("click", (event) => {
            if (index == 0) {
                pagenum += 2;
                if (pagenum >= image_list.length - 1) {
                    pagenum = image_list.length - 2;
                }
            } else {
                pagenum -= 2;
                if (pagenum < 0) {
                    pagenum = 0;
                }
            }
            reload();
        });
    });

    //シークバークリック時のページめくり
    document.getElementById("bar").addEventListener("click", (event) => {
        clickx = event.offsetX;
        blockx = event.srcElement.clientWidth;
        onePageWidth = 1.0 / parseFloat(image_list.length);
        clbl = parseFloat(clickx) / parseFloat(blockx);
        pagenum = image_list.length - Math.ceil(clbl / onePageWidth);
        reload();
    });
}