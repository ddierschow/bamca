/*jslint browser:true*/
function imageselector(selid, imagelist) {
    "use strict";
    this.selid = selid;
    this.images = imagelist;
    this.current = 0;
    this.select = function (newcurrent) {
        document.getElementById(this.selid + '_' + this.current).src = "../pic/gfx/circle_empty.gif";
        this.current = newcurrent;
        document.getElementById(this.selid + '_' + this.current).src = "../pic/gfx/circle_full.gif";
        document.getElementById(this.selid).src = '../' + this.images[this.current];
    };
}
