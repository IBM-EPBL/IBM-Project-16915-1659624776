function seemore(status){
   if(status=='true'){
      document.getElementById("hiddendetaildiv").style.visibility="visible";
      document.getElementById("seemoreid").style.visibility="hidden";
   }
}

function seeless(status){
   if(status=='true'){
      document.getElementById("hiddendetaildiv").style.visibility="hidden";
      document.getElementById("seemoreid").style.visibility="visible";
   }
}

function sizechartfunc(input){
   if(  (input == 'Women') && (document.getElementById("switchwomen").checked) == true)
      document.getElementById("sizechartwomen").src="/static/bgs/sizechartcm.jpg";

   if((input == 'Women') &&(document.getElementById("switchwomen").checked) == false)
      document.getElementById("sizechartwomen").src="/static/bgs/sizechartinches.jpg";

   if( (input == 'Men') && (document.getElementById("switchmen").checked) == true )
      document.getElementById("sizechartmen").src="/static/bgs/sizechartmencm.jpg";

   if( (input == 'Men') &&  (document.getElementById("switchmen").checked) == false)
      document.getElementById("sizechartmen").src="/static/bgs/sizechartmeninches.jpg";

   if( (input == 'Kids') && (document.getElementById("switchkids").checked) == true ){
      document.getElementById("sizechartkids").src="/static/bgs/sizechartkidscm.jpg";
      document.getElementById("sizechartkidsb").src="/static/bgs/sizechartkidsbcm.jpg";
   }
   
   if( (input == 'Kids') &&  (document.getElementById("switchkids").checked) == false){
      document.getElementById("sizechartkids").src="/static/bgs/sizechartkidsinches.jpg";
      document.getElementById("sizechartkidsb").src="/static/bgs/sizechartkidsbinches.jpg";
    }

    if( (input == 'fMen') &&  (document.getElementById("switchfmen").checked) == true)
      document.getElementById("sizechartfmen").src="/static/bgs/sizechartcmfmen.jpg";

    if( (input == 'fMen') &&  (document.getElementById("switchfmen").checked) == false)
      document.getElementById("sizechartfmen").src="/static/bgs/sizechartinchesfmen.jpg";

    if( (input == 'fWomen') &&  (document.getElementById("switchfwomen").checked) == true)
      document.getElementById("sizechartfwomen").src="/static/bgs/sizechartcmfwomen.jpg";

    if( (input == 'fWomen') &&  (document.getElementById("switchfwomen").checked) == false)
      document.getElementById("sizechartfwomen").src="/static/bgs/sizechartinchesfwomen.jpg";

    if( (input == 'fKids') &&  (document.getElementById("switchfkids").checked) == true)
      document.getElementById("sizechartfkids").src="/static/bgs/sizechartfkidscm.jpg";

    if( (input == 'fKids') &&  (document.getElementById("switchfkids").checked) == false)
      document.getElementById("sizechartfkids").src="/static/bgs/sizechartfkidsinches.jpg";
}

function myFunction(){
    var x = document.getElementById("myInput");
    var i=document.getElementById("icon");
    if (x.type === "password") {
      x.type = "text";
      i.classList.add("fa-eye");
      i.classList.remove("fa-eye-slash");
    } 
    else{
      x.type = "password";
      i.classList.remove("fa-eye");
      i.classList.add("fa-eye-slash");
    }
 }

function checkboxval(){
if(document.getElementById("checkboxvalue").checked==true)
    document.getElementById("checkboxvalue").value="yes"

}

const shareButton = document.querySelectorAll("button.shareButton")
shareButton[0].addEventListener("click", (e) => {
    for( let i=0; i < shareButton.length; i++ ) {
       shareButton[i].classList.toggle("open")
       shareButton[0].classList.remove("sent")
    }
      e.preventDefault();
})

for( let i=1; i < shareButton.length; i++ ) {
   shareButton[i].addEventListener("click", (e) => {
   for( let i=0; i < shareButton.length; i++ ) {
      shareButton[i].classList.toggle("open")
   }
   shareButton[0].classList.toggle("sent")
     e.preventDefault();
   })
}

const unsecuredCopyToClipboard = (text) => {
const textArea = document.createElement("textarea");
textArea.value=text; document.body.appendChild(textArea);
textArea.select();
try{document.execCommand('copy')}
catch(err){console.error('Unable to copy to clipboard',err)}
   document.body.removeChild(textArea)};

function copyToClipboard(content,e) {
  if (window.isSecureContext && navigator.clipboard) {
    navigator.clipboard.writeText(content);
  }
  else{
    unsecuredCopyToClipboard(content);
  }
  e.preventDefault();
}
