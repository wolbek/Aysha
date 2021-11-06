// Give search results when enter key is pressed
$("#searchcontent").on("keydown", function (event) {
    if (event.which == 13) {
        var searchcontent = $(this).val();
        $(".list-items").remove();
        $("#searchcontent").blur();
        $.ajax({
            method: "GET",
            url: "../api/completedorderlist",
            data: {
                searchcontent: searchcontent
            },
            success: function (data) {
                console.log(data)
                $(".orderlist").remove()
                $.each(data, function (index, order) {
                    $(".content-table").append($("<tr>").append(
                        $("<td>").text(order.id),
                        $("<td>").text(order.customer_firstname),
                        $("<td>").text(order.customer_lastname),
                        $("<td>").text(order.product_label),
                        $("<td>").text(order.product_size),
                        $("<td>").text(order.buy_quantity),
                        $("<td>").text(formatDate(order.order_date)),
                        $("<td>").text(order.to_address),
                        $("<td>").text("₹" + order.price),
                        $("<td>").text("Delivered on " + formatDate(order.delivered_date)),
                    ).addClass("orderlist")).hide();
                    $(".content-table").fadeIn(300);
                })

            }
        })

    }
})
// To format date to dd/mm/yyyy
function formatDate(date) {
    var d = new Date(date),
        month = '' + (d.getMonth() + 1),
        day = '' + d.getDate(),
        year = d.getFullYear();

    if (month.length < 2)
        month = '0' + month;
    if (day.length < 2)
        day = '0' + day;

    return [day, month, year].join('/');
}

// Result list when you type something in search bar
$("#searchcontent").on("click keyup", function (event) {

    if ($(this).val() == "") {
        $(".list-items").remove();
    }
    else if (event.which != 13) {
        var searchcontent = $(this).val();
        $.ajax({
            method: "GET",
            url: "../api/completedorderlist",
            data: {
                searchcontent: searchcontent
            },
            success: function (data) {
                // console.log(data)        
                $(".list-items").remove();
                $.each(data, function (index, order) {
                    $("#searchlist").append($("<p>").text(order.product_label).addClass("list-items"));

                })
            }
        })
    }
});

// To allow clicking on the list result (as it is been added dynamically we have to use delegated events)
$("body").on("click", ".list-items", function () {
    $("#searchcontent").empty();
    $("#searchcontent").val($(this).text());
    $(".list-items").remove();
    $("#searchcontent").focus();
})

// When click outside of the search box and list result, the list result should vanish
$(document).click(function (event) {
    var $target = $(event.target);
    if (!$target.closest('#searchlist').length && !$target.closest('#searchcontent').length && $('#searchlist').is(":visible")) {
        $('.list-items').remove();
    }
});