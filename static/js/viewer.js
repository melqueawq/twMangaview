let pagenum = 0;

let pages;

let reload = () => {
    console.log("reload");
    Array.from(pages).reverse().forEach((element, index) => {
        element.innerHTML = "<img src=" + image_list[index + pagenum] + ">"
    });

    document.getElementById("pagenum").innerHTML = "<p>" + (pagenum + 1) + "/" + image_list.length + "</p>"
}

window.onload = function () {
    pages = document.getElementsByClassName('page');
    console.log(pages);
    reload();


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
}