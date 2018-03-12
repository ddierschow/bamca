/*jslint browser:true*/
function imageselector(selid, imagelist) {
    "use strict";
    this.selid = selid;
    this.images = imagelist;
    this.current = 0;
    this.select = function (newcurrent) {
        document.getElementById(this.selid + '_' + this.current).innerHTML = '<i class="far fa-circle green"></i>';
        this.current = newcurrent;
        document.getElementById(this.selid + '_' + this.current).innerHTML = '<i class="fas fa-circle green"></i>';
        document.getElementById(this.selid).src = '../' + this.images[this.current];
    };
}
