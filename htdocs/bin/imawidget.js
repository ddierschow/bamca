/*jslint browser:true*/
// imawidget is the thing that allows me to choose the bounding rectangle
// for images.

// It gets the image from an img element with the id "ima_source".
// The bounds are stuffed into a forn element with the id gotten from
// a div element with the id "ima_query", thus allowing the original
// page to decide where to put the bounds.  These can both be hidden.
// It uses a canvas element with the id "ima_widget".  Elements with
// these three ids should be defined in the html.  A div can be added
// with the id "ima_debug" to get some debug information or "ima_info"
// for useful bounding information.

// To use: click and hold to set one corner, then drag to the other
// corner and release.  Grab any side or corner to move it.  Double
// click to switch between black and white bounds.  Click outside the
// bounds to clear the setting.  Click within the bounds to drag the
// box.  Keypresses:  r (red), g (green), b (blue), c (cyan), c (cyan),
// y (yellow), p (pink), w (white), or B to reset to black.  Use the
// VI-style cursor keys to move the bounds by one pixel, h for left,
// j for top, k for bottom, l for right.  Unshifted expands the box,
// shifted contracts the box.  ESC clears the box, z restores the last
// cleared box.  0-9 make the movement keys move 2^N pixels.  Note
// that the cursor must be inside the picture area to use the keys.

"use strict";
var slop = 1;
var step = 1;
var p1_x = -(slop + 3); // rectangle corners
var p1_y = -(slop + 3);
var p2_x = -(slop + 3);
var p2_y = -(slop + 3);
var ms_x = 0; // mouse (x,y)
var ms_y = 0; // mouse (x,y)
var cr_x = 0; // client recangle upper left (x,y)
var cr_y = 0; // client recangle upper left (x,y)
var sz_x = 0; // client recangle size (x,y)
var sz_y = 0; // client recangle size (x,y)
var mv_x = 0; // are we moving? (x,y)
var mv_y = 0; // are we moving? (x,y)
var l1_x = -(slop + 3); // for undoing
var l1_y = -(slop + 3); // for undoing
var l2_x = -(slop + 3); // for undoing
var l2_y = -(slop + 3); // for undoing
var d1_x = 0; // for dragging
var d1_y = 0; // for dragging
var d2_x = 0; // for dragging
var d2_y = 0; // for dragging
var ms_actv = 0; // mouse is over canvas
var clr = '#000000';

var qyf; // query field
var img; // original image
var can; // canvas element
var qid = 0;
var qyf = 0;
var dbg = 0;
var inf = 0;

function between(v, v1, v2) {
    return (!((v < Math.min(v1, v2) - slop) || (v > Math.max(v1, v2) + slop)));
}

function between_x(v1, v2) {
    return between(ms_x, v1, v2);
}

function between_y(v1, v2) {
    return between(ms_y, v1, v2);
}

function point_over(v, v1) {
    return (Math.abs(v - v1) <= slop);
}

function cursor_over_x(v1) {
    return point_over(ms_x, v1);
}

function cursor_over_y(v1) {
    return point_over(ms_y, v1);
}

function set_bounds(event) {
    var cbr = can.getBoundingClientRect(),
        x,
        y,
        ar;
    cr_x = Math.round(cbr.left);
    cr_y = Math.round(cbr.top);
    sz_x = Math.round(cbr.right - cbr.left);
    sz_y = Math.round(cbr.bottom - cbr.top);
    if (event) {
        ms_x = event.clientX - cr_x;
        ms_y = event.clientY - cr_y;
    }
    if (inf) {
        if (p1_x >= 0) {
            x = Math.abs(p2_x - p1_x);
            y = Math.abs(p2_y - p1_y);
            if (y) {
                ar = x / y;
            }
            else {
                ar = 'lots';
            }
            inf.innerHTML = 'Size: '.concat(x, ',', y, ' a/r ', ar);
        }
        else {
            inf.innerHTML = '';
        }
    }
}

function clear_bounds() {
    if (p1_x >= 0 && !point_over(p1_x, p2_x) && p1_x >= 0 && !point_over(p1_y, p2_y)) {
        l1_x = p1_x;
        l1_y = p1_y;
        l2_x = p2_x;
        l2_y = p2_y;
    }
    p1_x = -(slop + 3);
    p1_y = -(slop + 3);
    p2_x = -(slop + 3);
    p2_y = -(slop + 3);
}

function draw_bounds() {
    if (dbg) {
        dbg.innerHTML = 'draw_bounds: '.concat(p1_x, ',', p1_y, ',', p2_x, ',', p2_y,
                '|mouse ', ms_x, ',', ms_y,
                '|client ', cr_x, ',', cr_y,
                '|size ', sz_x, ',', sz_y,
                '|moving ', mv_x, ',', mv_y,
                '|drag ', d1_x, ',', d1_y, ',', d2_x, ',', d2_y,
                '|last ', l1_x, ',', l1_y, ',', l2_x, ',', l2_y);
    }
    var ctx = can.getContext("2d");
    ctx.drawImage(img, 0, 0);
    ctx.beginPath();
    if (p1_x >= 0) {
        ctx.moveTo(p1_x, p1_y);
        ctx.lineTo(p1_x, p2_y);
        ctx.lineTo(p2_x, p2_y);
        ctx.lineTo(p2_x, p1_y);
        ctx.lineTo(p1_x, p1_y);
        qyf.value = ''.concat(p1_x, ',', p1_y, ',', p2_x, ',', p2_y);
    }
    else if (ms_actv) {
        if (dbg) {
            dbg.innerHTML += ' should';
        }
        ctx.moveTo(ms_x, 0);
        ctx.lineTo(ms_x, sz_y);
        ctx.moveTo(0,    ms_y);
        ctx.lineTo(sz_x, ms_y);
        qyf.value = '';
    }
    ctx.strokeStyle = clr;
    ctx.stroke();

    if (p1_x < 0) {
        can.style.cursor = "auto";
    }
    else if (mv_x || mv_y) {
        can.style.cursor = "crosshair";
    }
    else if ((cursor_over_x(p1_x) && cursor_over_y(p1_y)) || (cursor_over_x(p2_x) && cursor_over_y(p2_y))) {
        can.style.cursor = "nwse-resize";
    }
    else if ((cursor_over_x(p2_x) && cursor_over_y(p1_y)) || (cursor_over_x(p1_x) && cursor_over_y(p2_y))) {
        can.style.cursor = "nesw-resize";
    }
    else if ((cursor_over_x(p1_x) || cursor_over_x(p2_x)) && between_y(p1_y, p2_y)) {
        can.style.cursor = "ew-resize";
    }
    else if ((cursor_over_y(p1_y) || cursor_over_y(p2_y)) && between_x(p1_x, p2_x)) {
        can.style.cursor = "ns-resize";
    }
    else {
        can.style.cursor = "auto";
    }
}

function ima_buttondown(event) {
    set_bounds(event);
    if (cursor_over_x(p1_x) && between_y(p1_y, p2_y)) {
        mv_x = 1;
        p1_x = ms_x;
    }
    else if (cursor_over_x(p2_x) && between_y(p1_y, p2_y)) {
        p2_x = p1_x;
        mv_x = 1;
        p1_x = ms_x;
    }
    if (cursor_over_y(p1_y) && between_x(p1_x, p2_x)) {
        mv_y = 1;
        p1_y = ms_y;
    }
    else if (cursor_over_y(p2_y) && between_x(p1_x, p2_x)) {
        p2_y = p1_y;
        mv_y = 1;
        p1_y = ms_y;
    }
    if (!mv_x && !mv_y) {
        if (between_x(p1_x, p2_x) && between_y(p1_y, p2_y)) {
            d1_x = p1_x - ms_x;
            d1_y = p1_y - ms_y;
            d2_x = p2_x - ms_x;
            d2_y = p2_y - ms_y;
        }
        else {
            clear_bounds();
            p1_x = ms_x;
            p2_x = ms_x;
            p1_y = ms_y;
            p2_y = ms_y;
            mv_x = 1;
            mv_y = 1;
        }
    }
    draw_bounds();
}

function ima_doubleclick(event) {
    set_bounds(event);
    if (clr === '#000000') {
        clr = '#FFFFFF';
    }
    else {
        clr = '#000000';
    }
    draw_bounds();
}

function ima_buttonup(event) {
    d1_x = 0;
    d1_y = 0;
    d2_x = 0;
    d2_y = 0;
    set_bounds(event);
    var tmp = 0;
    if (mv_x) {
        p1_x = Math.min(sz_x, Math.max(0, ms_x));
    }
    if (mv_y) {
        p1_y = Math.min(sz_y, Math.max(0, ms_y));
    }
    mv_x = 0;
    mv_y = 0;
    if (point_over(p1_x, p2_x) && point_over(p1_y, p2_y)) {
        clear_bounds();
    }
    if (p1_x > p2_x) {
        tmp = p1_x;
        p1_x = p2_x;
        p2_x = tmp;
    }
    if (p1_y > p2_y) {
        tmp = p1_y;
        p1_y = p2_y;
        p2_y = tmp;
    }
    if (p2_x > sz_x) {
        p2_x = sz_x - 1;
    }
    if (p2_y > sz_y) {
        p2_y = sz_y - 1;
    }
    draw_bounds();
}

function ima_mouse(event) {
    set_bounds(event);
    if (d1_x !== d2_x) {
        p1_x = Math.max(0, d1_x + ms_x);
        p1_y = Math.max(0, d1_y + ms_y);
        p2_x = Math.min(sz_x, d2_x + ms_x);
        p2_y = Math.min(sz_y, d2_y + ms_y);
    }
    if (event.type === 'mouseleave') {
        ms_actv = 0;
        ima_buttonup(event);
        d1_x = 0;
        d1_y = 0;
        d2_x = 0;
        d2_y = 0;
    }
    else {
        ms_actv = 1;
    }
    if (mv_x) {
        p1_x = ms_x;
    }
    if (mv_y) {
        p1_y = ms_y;
    }
    draw_bounds();
}

function ima_key(event) {
    set_bounds(0);
    if (!mv_x && !mv_y && ms_actv) {
        if (p1_x >= 0 && event.which === 27) {
            clear_bounds();
        }
        else if (p1_x >= 0 && event.which === 104) {
            p1_x = Math.max(0, p1_x - step);
        }
        else if (p2_y >= 0 && event.which === 106) {
            p2_y = Math.min(sz_y, p2_y + step);
        }
        else if (p1_y >= 0 && event.which === 107) {
            p1_y = Math.max(0, p1_y - step);
        }
        else if (p2_x >= 0 && event.which === 108) {
            p2_x = Math.min(sz_x, p2_x + step);
        }
        else if (p1_x >= 0 && event.which === 72) {
            p1_x = Math.min(p2_x, p1_x + step);
        }
        else if (p2_y >= 0 && event.which === 74) {
            p2_y = Math.max(p1_y, p2_y - step);
        }
        else if (p1_y >= 0 && event.which === 75) {
            p1_y = Math.min(p2_y, p1_y + step);
        }
        else if (p2_x >= 0 && event.which === 76) {
            p2_x = Math.max(p1_x, p2_x - step);
        }
        else if (event.which === 66) {
            clr = '#000000';
        }
        else if (event.which === 119) {
            clr = '#FFFFFF';
        }
        else if (event.which === 114) {
            clr = '#FF0000';
        }
        else if (event.which === 103) {
            clr = '#00FF00';
        }
        else if (event.which === 98) {
            clr = '#0000FF';
        }
        else if (event.which === 121) {
            clr = '#FFFF00';
        }
        else if (event.which === 112) {
            clr = '#FF00FF';
        }
        else if (event.which === 99) {
            clr = '#00FFFF';
        }
        else if (event.which === 122) {
            p1_x = l1_x;
            p1_y = l1_y;
            p2_x = l2_x;
            p2_y = l2_y;
        }
        else if (event.which >= 48 && event.which <= 57) {
            step = Math.pow(2, event.which - 48);
        }
        draw_bounds();
        if (dbg) {
            dbg.innerHTML += ' key: ' + event.which;
        }
    }
    else if (dbg) {
        dbg.innerHTML += ' key ignored';
    }
}

function ima_start() {
    qid = document.getElementById("ima_query").innerHTML;
    qyf = document.getElementById(qid);
    dbg = document.getElementById('ima_debug');
    inf = document.getElementById('ima_info');
    img = document.getElementById("ima_source");
    can = document.getElementById("ima_widget");
    set_bounds(0);
    draw_bounds();
    can.addEventListener("mousedown", ima_buttondown);
    can.addEventListener("mouseup", ima_buttonup);
    can.addEventListener("mouseenter", ima_mouse);
    can.addEventListener("mouseleave", ima_mouse);
    can.addEventListener("mousemove", ima_mouse);
    can.addEventListener("dblclick", ima_doubleclick);
    document.addEventListener("keypress", ima_key);
}

window.addEventListener("load", ima_start); // whew!
