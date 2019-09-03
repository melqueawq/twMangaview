$(function () {
    $('.favmit').on('click', function (event) {
        event.preventDefault();

        $.ajax({
            url: $(this).parent('form').attr('action'),
            type: 'post',
            data: $(this).parent('form').serialize()
        }).then(
            function () {
                $(this).html('お気に入りを解除する');
            },
            function () {
                alert('お気に入り登録に失敗しました。');
            }
        );
    });
})