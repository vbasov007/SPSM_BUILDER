$(function () {

    initCategorySwitches();

    initCollapsibleTree();

    initTextHighlight();

    initProductPageRedirect();

    highlightDiscontinuedProducts();

    setStateAccordingInputVariables();

    showPage();

});



function initCategorySwitches() {

    $('.selectable-view').hide();

    $('.change-view-but').on('click', function () {

        $(this).addClass("pressed");
        $(this).siblings("button").removeClass("pressed");

        $(this).siblings(".selectable-view").hide();

        const v = $(this).attr("view-id");

        //$(this).siblings(`.selectable-view[view-id="${v}"]`).show();
        //for IE compatibility
        $(this).siblings(".selectable-view[view-id=\"".concat(v, "\"]")).show();

    });

    $('.change-view-but:first-child').trigger('click');

}

function initCollapsibleTree() {
    var tree = document.querySelectorAll('ul.tree div.branch:not(:last-child)');
    for (var i = 0; i < tree.length; i++) {
        tree[i].addEventListener('click', function (e) {
            var parent = this.parentElement;//e.target.parentElement;
            var classList = parent.classList;
            if (classList.contains("open")) {
                classList.remove('open');
                var opensubs = parent.querySelectorAll(':scope .open');
                for (var i = 0; i < opensubs.length; i++) {
                    opensubs[i].classList.remove('open');
                }
            } else {
                classList.add('open');
            }
            e.preventDefault();
        });
    }

}

function highlightDiscontinuedProducts() {
    let x = document.getElementsByClassName('product_status');
    for (let i = 0; i < x.length; i++) {
        if (x[i].innerHTML == 'not for new design' || x[i].innerHTML == 'discontinued') {
            x[i].style.cssText = "color: red; font-weight: bold;";
        }
        else {
            x[i].style.cssText = "color: green; font-weight: bold;";
        }
    }
}

function showPage() {
    $('#load-message').hide();
    $('#body').show();
}

function initTextHighlight() {

    $('#search_text').on('keyup', function (event) {

        let keycode = (event.keyCode ? event.keyCode : event.which);

        if(keycode === 13) {
            let search = $(this).val().toLowerCase();
            highlightText(search);
        }
    });

}

function highlightText(search){

    $('.search-highlight').toggleClass('search-highlight');
    $('.search-highlight-tree').toggleClass('search-highlight-tree');

    if (search.length > 1) {

        $('ul.tree li > div > span').each(function () {
            let val = $(this).text().toLowerCase();
            if (val.match(search)) {
                $(this).parent().parentsUntil('ul.tree').addClass('search-highlight-tree');
                $(this).addClass('search-highlight');
            }
        });

    }
}

function initProductPageRedirect(){

    $('span.product').on('click', function(){
        productPageRedirect($(this).text());
    });
}

function productPageRedirect(part_name) {

    let url;
    url = getDataFromJS(productPageUrl, part_name, 'ProductPageUrl');

    if(isValidURL(url)){
        var win = window.open(url, '_blank');
        win.focus();
    }
}

function isValidURL(string) {
    var res = string.match(/(http(s)?:\/\/.)?(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)/g);
    if (res == null)
        return false;
    else
        return true;
};

function setStateAccordingInputVariables(){

    var category = getQueryVariable('category');
    var subcategory = getQueryVariable('subcategory');
    var view = getQueryVariable('view');
    var highlight = getQueryVariable('highlight');


    setState(category, subcategory, view, highlight, '')
}

function setState(category, subcategory, view, highlight, open_items){

    /*
    $(`.change-view-but[view-id*='${category}']`).trigger('click');
    $(`.change-view-but[view-id*='${subcategory}']`).trigger('click');
    $(`.change-view-but[view-id*='${view}']`).trigger('click');
    $(`#search_text`).val(highlight);
    */
    //replaced  for IE compatibility
    $(".change-view-but[view-id*='".concat(category, "']")).trigger('click');
    $(".change-view-but[view-id*='".concat(subcategory, "']")).trigger('click');
    $(".change-view-but[view-id*='".concat(view, "']")).trigger('click');
    $("#search_text").val(highlight);

    highlightText(highlight);

}

function getQueryVariable(variable)
{
    var query = decodeURI(window.location.search.substring(1));
    var vars = query.split("&");
    for (var i=0;i<vars.length;i++) {
        var pair = vars[i].split("=");
        if(pair[0] == variable){return pair[1];}
    }
    return('');
}

function getDataFromJS(table, key, col_name) {
    let col_index = table.columns.indexOf(col_name);
    let key_index = table.index.indexOf(key);
    return table.data[key_index][col_index];

}

