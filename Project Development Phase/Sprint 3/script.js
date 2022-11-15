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


function sizechartfunc(input)
{

if(  (input == 'Women') && (document.getElementById("switchwomen").checked) == true)
   document.getElementById("sizechartwomen").src="https://s3.jp-tok.cloud-object-storage.appdomain.cloud/smartfashion2001/sizechartcm.jpg";

if((input == 'Women') &&(document.getElementById("switchwomen").checked) == false)
    document.getElementById("sizechartwomen").src="https://s3.jp-tok.cloud-object-storage.appdomain.cloud/smartfashion2001/sizechartinches.jpg";

if( (input == 'Men') && (document.getElementById("switchmen").checked) == true )
   document.getElementById("sizechartmen").src="https://s3.jp-tok.cloud-object-storage.appdomain.cloud/smartfashion2001/sizechartmencm.jpg";

if( (input == 'Men') &&  (document.getElementById("switchmen").checked) == false)
    document.getElementById("sizechartmen").src="https://s3.jp-tok.cloud-object-storage.appdomain.cloud/smartfashion2001/sizechartmeninches.jpg";

if( (input == 'Kids') && (document.getElementById("switchkids").checked) == true ){
   document.getElementById("sizechartkids").src="https://s3.jp-tok.cloud-object-storage.appdomain.cloud/smartfashion2001/sizechartkidscm.jpg";
      document.getElementById("sizechartkidsb").src="https://s3.jp-tok.cloud-object-storage.appdomain.cloud/smartfashion2001/sizechartkidsbcm.jpg";
   }
if( (input == 'Kids') &&  (document.getElementById("switchkids").checked) == false){
    document.getElementById("sizechartkids").src="https://s3.jp-tok.cloud-object-storage.appdomain.cloud/smartfashion2001/sizechartkidsinches.jpg";
    document.getElementById("sizechartkidsb").src="https://s3.jp-tok.cloud-object-storage.appdomain.cloud/smartfashion2001/sizechartkidsbinches.jpg";
    }

     if( (input == 'fMen') &&  (document.getElementById("switchfmen").checked) == true)
    document.getElementById("sizechartfmen").src="https://s3.jp-tok.cloud-object-storage.appdomain.cloud/smartfashion2001/sizechartcmfmen.jpg";

    if( (input == 'fMen') &&  (document.getElementById("switchfmen").checked) == false)
    document.getElementById("sizechartfmen").src="https://s3.jp-tok.cloud-object-storage.appdomain.cloud/smartfashion2001/sizechartinchesfmen.jpg";

    if( (input == 'fWomen') &&  (document.getElementById("switchfwomen").checked) == true)
    document.getElementById("sizechartfwomen").src="https://s3.jp-tok.cloud-object-storage.appdomain.cloud/smartfashion2001/sizechartcmfwomen.jpg";

    if( (input == 'fWomen') &&  (document.getElementById("switchfwomen").checked) == false)
    document.getElementById("sizechartfwomen").src="https://s3.jp-tok.cloud-object-storage.appdomain.cloud/smartfashion2001/sizechartinchesfwomen.jpg";


    if( (input == 'fKids') &&  (document.getElementById("switchfkids").checked) == true)
    document.getElementById("sizechartfkids").src="https://s3.jp-tok.cloud-object-storage.appdomain.cloud/smartfashion2001/sizechartfkidscm.jpg";

    if( (input == 'fKids') &&  (document.getElementById("switchfkids").checked) == false)
    document.getElementById("sizechartfkids").src="https://s3.jp-tok.cloud-object-storage.appdomain.cloud/smartfashion2001/sizechartfkidsinches.jpg";


}

function myFunction() {


    var x = document.getElementById("myInput");
    var i=document.getElementById("icon");
    if (x.type === "password") {
      x.type = "text";
      i.classList.add("fa-eye");
      i.classList.remove("fa-eye-slash");
    } else {
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
  } else {
    unsecuredCopyToClipboard(content);
  }
  e.preventDefault();
}