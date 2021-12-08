$(document).ready(() => {
    $('#userbar').click(function(){
        $(this).toggleClass('active');
        $('#header-dropdown').toggleClass('active');
    });
});

function addHave(item) {
    if ($('.well-placeholder').children('.trade-item.form-item').length >= 12) {
        return;
    }
    let div =
       // '<div>\n' +
        `<div class="trade-item form-item" style="" data-left="${item.data('id')}" data-type="normal">\n` +
        '<div class="trade-item-image visible-lg">\n' +
        '<div class="donationitem itemmicro" data-original-title="" title="">\n' +
        `<img src="${item.find('img').attr('src')}" class="item-img">\n` +
        '</div>\n' +
        '</div>\n' +
        '<div class="trade-item-name">\n' +
        `${item.data('displayname')}</div>\n` +
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
    if (!$('.well-placeholder').children('.trade-item.form-item').length) {
        $('#add-trade').addClass('disabled');
    }

}

