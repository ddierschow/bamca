function incrfield(f,v){
 var id = document.getElementsByName(f)[0].value;
 var p=s=n='';
 for (i=0; i<id.length; i=i+1)
  if (id[i] >= '0' && id[i] <= '9')
   n = n + id[i];
  else if (n.length)
   s = s + id[i];
  else
   p = p + id[i];
 var nf = '00' + (parseInt(n, 10) + v);
 document.getElementsByName(f)[0].value = p + nf.substr(nf.length - n.length, n.length) + s;
}
