$(function() {
  $(".favmit").on("click", function(event) {
    event.preventDefault();

    let a = this;
    $.ajax({
      url: $(this)
        .parent("form")
        .attr("action"),
      type: "post",
      data: $(this)
        .parent("form")
        .serialize(),
      dataType: "json"
    }).then(
      function(json_data) {
        if (json_data["result"]) {
          $(a).html("お気に入りを解除する");
        } else {
          $(a).html("お気に入りに追加する");
        }
      },
      function() {
        alert("お気に入り登録に失敗しました。");
      }
    );
  });
});
