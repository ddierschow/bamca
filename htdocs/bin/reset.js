function ResetForm(which){
 for (i=0;i<which.length;i++){
  var tempobj=which.elements[i];
  if (tempobj.type=="text"||tempobj.type=="textarea"||tempobj.type=="password"||tempobj.type=="file")
   tempobj.value=tempobj.defaultValue;
  else if (tempobj.type=="checkbox"||tempobj.type=="radio")
   tempobj.checked=tempobj.defaultChecked;
  else if (tempobj.type=="select-one")
   for (var j=0;j<tempobj.options.length;j++)
    if (tempobj.options[j].defaultSelected)
     tempobj.options[j].selected = true;
 }
 return false;
}
