$(document).ready(() => {
    $('#userbar').click(function(){
        $(this).toggleClass('active');
        $('#header-dropdown').toggleClass('active');
    });
});

function addHave(item) {
    let div =
       // '<div>\n' +
        `<div class="trade-item form-item" style="" data-left="${item.data('id')}" data-type="normal">\n` +
        '<div class="trade-item-image visible-lg">\n' +
        '<div class="donationitem itemmicro" data-original-title="" title="">\n' +
        '<img src="https://steamcommunity-a.akamaihd.net/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxDZ7I56KU0Zwwo4NUX4oFJZEHLbXH5ApeO4YmlhxYQknCRvCo04DEVlxkKgpou6rwOANf2-r3fTxA_t2iq42bwsj4OrzZgiVT6sF10-uW8N2h3AHi-kttY2-hLYGVewQ4YF_Y_Qe2lebvhcC7v5TI1zI97SL4IQbf/100fx60f" class="item-img">\n' +
        '</div>\n' +
        '</div>\n' +
        '<div class="trade-item-name">\n' +
        `${item.data('title')}</div>\n` +
        '<div class="trade-item-count">\n' +
        '<div class="form-inline">\n' +
        `<button class="btn btn-danger" type="button" data-original-title="" title="" onclick="removeHave(${item.data('id')})">X</button>\n` +
        '</div>\n' +
        '</div>\n' +
       // '</div>\n' +
        '</div>';

    div = $(div);
    $('#placeholder-left').before(div);
    item.hide();
    $('#add-trade').removeClass('disabled');
}

function removeHave(id) {
    $(`div[data-left=${id}]`).remove();
    $(`div[data-id=${id}]`).show();
    if (!$('#leftTrade.trade-item.form-item').length) {
        $('#add-trade').addClass('disabled');
    }

}

