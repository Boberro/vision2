(function () {
    var url_vars = [], hash;
    var _hashes = window.location.href.slice(window.location.href.indexOf('?') + 1).split('&');
    for (var i = 0; i < _hashes.length; i++) {
        hash = _hashes[i].split('=');
        url_vars.push(hash[0]);
        url_vars[hash[0]] = hash[1];
    }

    if (url_vars.alert === '1') {
        var warning = $('#warning');
        var warning_text = 'No faces found in the uploaded picture. File not saved.';
        warning.removeClass('d-none').addClass('show').find('span.inner-text').text(warning_text);
    }
})();