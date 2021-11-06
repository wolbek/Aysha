// Give search results when enter key is pressed
$("#searchcontent").on("keydown", function (event) {
    if (event.which == 13) {
        var searchcontent = $(this).val();
        $(".list-items").remove();
        $("#searchcontent").blur();
        $.ajax({
            method: "GET",
            url: "../api/productlist",
            data: {
                searchcontent: searchcontent
            },
            success: function (data) {
                console.log(data)
                $(".productlist").remove()
                $.each(data, function (index, product) {
                    $(".content-table").append($("<tr>").append(
                        $("<td>").text(product.id),
                        $("<td>").text(product.label),
                        $("<td>").text(product.category),
                        $("<td>").text(product.description),
                        $("<td>").text(product.XS),
                        $("<td>").text(product.S),
                        $("<td>").text(product.M),
                        $("<td>").text(product.L),
                        $("<td>").text(product.XL),
                        $("<td>").text(product.XXL),
                        $("<td>").text(product.XXXL),
                        // $("<td>").html("<div> <a href='../editproduct/"+product.id +"'> <button>Edit</button> </a> </div> <div> <button class='delete' pid="+ product.id+">Delete</button> </div>").addClass("tablebuttons"),                   
                        $("<td>").append("<div> <a href='../editproduct/"+product.id +"'> <button>Edit</button> </a> </div>").append("<div> <button class='delete' pid="+ product.id+">Delete</button> </div>").addClass("tablebuttons"),
                        ).addClass("productlist")).hide();
                    $(".content-table").fadeIn(300);
                })

            }
        })

    }
})

// Result list when you type something in search bar
$("#searchcontent").on("click keyup", function (event) {

    if ($(this).val() == "") {
        $(".list-items").remove();
    }
    else if (event.which != 13) {
        var searchcontent = $(this).val();
        $.ajax({
            method: "GET",
            url: "../api/productlist",
            data: {
                searchcontent: searchcontent
            },
            success: function (data) {
                // console.log(data)        
                $(".list-items").remove();
                $.each(data, function (index, product) {
                    $("#searchlist").append($("<p>").text(product.label).addClass("list-items"));

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