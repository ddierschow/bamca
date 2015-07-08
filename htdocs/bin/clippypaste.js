//http://kb.mozillazine.org/Granting_JavaScript_access_to_the_clipboard

// In FF 41.0, this should work.  Until then, it just clears the input.
function paste_from_clippy(putid) {
    document.getElementById(putid).value = '';
    document.getElementById(putid).focus();
    document.execCommand('Paste');
}
