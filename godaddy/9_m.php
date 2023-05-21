<?
function form($util,$tech,$state){
if ($state=='form') {
$min=1;
$max=300;
$num1=rand( $min, $max );
$num2=rand( $min, $max );
$sum=$num1 + $num2;
echo '<ul class="common">
<li class="header"><pre>'.json_decode(mysqli_fetch_row($util->db->get('headername','content','name',$util->subitem))[0],true)['title'].'</pre></li>
</ul>
<form class="online" action="" method="post" enctype="multipart/form-data">
<div class="row"><pre class="lc bold">Technology</pre>
<select id="selecttech" name="technology" class="l">
   <option value="" selected></option>';
$json=json_decode(mysqli_fetch_row($util->db->get('headername','content','name','training'))[0],true);
foreach($json['child'] as $key){
 $json1=json_decode(mysqli_fetch_row($util->db->get('headername','content','name',$key))[0],true);
 echo '<option value="'.$key.'">'.ucfirst(preg_replace("/ training$/i","",$json1['title'])).'</option>';
}
echo '</select><pre class="ls bold star">*</pre></div>
<div class="row"><pre class="lc bold">Course Content:</pre><a class="l bold block" href="" id="a_course" target="_blank"></a></div>
<div class="row"><pre class="lc bold">Name:</pre><input type="text" name="name" placeholder="Your Name" class="l"></div>
<div class="row"><pre class="lc bold">Email:</pre><input id="emailid" type="text" name="email" placeholder="Email Address" class="l"><pre class="ls bold star">*</pre></div>
<div class="row" style="margin-top:10px;"><pre class="lc bold" style="font-size:8pt">Supporting'."\n".'Document:</pre><input type="file" name="attachment" id="attachmentid" class="l3" style="width:50%"><pre class="l3" style="font-size:8pt;width:20%">pdf,docx'."\n".'txt,png<2MB</pre></div>

<div class="rowtextarea" ><pre class="lc bold">Comment:</pre><textarea id="messageid" rows="5" name="message" cols="40" class="l2" ></textarea><pre class="ls bold star">*</pre></div>
<div class="row" style="margin-top:20px"><pre class="lc bold" id="quiztextid" style="font-size:14pt;color:#ff0000">'.$num1.'+'.$num2.' ?</pre><input type="text" class="quiz-control l"> <pre class="ls bold star">*</pre></div>
<div class="row" style="margin-top:20px"><input data-res="'.$sum.'" type="submit" name="submit" value="Submit" class="submit lc bold disable" id="s_submit"><pre class="l3" id="iframeid" style="margin-left:5%;font-size:14pt;font-weight:bold;height:30"></pre></div>
</form>
<br>
<a href="http://minhinc.42web.io/training/'.$tech.'"><img style="margin-left:10%;width:80%" src="http://minhinc.42web.io/image/'.$tech.'traininglogo.gif"></img></a>
<div style="clear:both"></div>
<script>
const emailregex = /^([\w\d._\-#])+@([\w\d._\-#]+[.][\w\d._\-#]+)+$/;
function submitenabledisable() {
 //if (document.getElementById("selecttech").options[document.getElementById("selecttech").selectedIndex].value=="" || document.getElementById("messageid").value.length<1 || !document.getElementById("emailid").value.match(emailregex) || document.querySelector(".quiz-control").value!=document.getElementById("s_submit").getAttribute("data-res") || isNaN((new Date(document.getElementById("dateid").value)).getTime()) || document.getElementById("attachmentid").files[0] && document.getElementById("attachmentid").files[0].size > 2*1024*1024) {
 if (document.getElementById("selecttech").options[document.getElementById("selecttech").selectedIndex].value=="" || document.getElementById("messageid").value.length<1 || !document.getElementById("emailid").value.match(emailregex) || document.querySelector(".quiz-control").value!=document.getElementById("s_submit").getAttribute("data-res") || document.getElementById("attachmentid").files[0] && document.getElementById("attachmentid").files[0].size > 2*1024*1024) {
 document.getElementById("s_submit").classList.remove("enable");
 document.getElementById("s_submit").classList.add("disable");
 document.getElementById("s_submit").disabled=true;
 } else {
 document.getElementById("s_submit").classList.remove("disable");
 document.getElementById("s_submit").classList.add("enable");
 document.getElementById("s_submit").disabled=false;
 }
}
document.getElementById("selecttech").onchange=function(){
 var e = document.getElementById("selecttech");
 var strUser = e.options[e.selectedIndex].value;
 if (strUser !== ""){
  this.style.removeProperty("border");
 document.getElementById("a_course").innerHTML="Click here for Course Content";
 document.getElementById("a_course").setAttribute("href","http://minhinc.42web.io/training/"+strUser);
 }else{
 this.style.border="1px solid red";
 document.getElementById("a_course").innerHTML="";
 document.getElementById("a_course").setAttribute("href","");
 }
submitenabledisable();
}
const emailInput = document.getElementById("emailid");
emailInput.addEventListener("input", function(e) {
 if ( this.value.match(emailregex) ) {
  this.style.removeProperty("border");
 } else {
 this.style.border="1px solid red";
 }
submitenabledisable();
});

const attachmentfile = document.getElementById("attachmentid");
attachmentfile.addEventListener("input", function( e ) {
 var file = attachmentfile.files[0];
 if(file && file.size <= 2*1024*1024){
  this.style.removeProperty("border");
  document.getElementById("iframeid").style.removeProperty("color");
  document.getElementById("iframeid").innerHTML="";
 } else {
  this.style.border="1px solid red";
  document.getElementById("iframeid").style.color="red";
  document.getElementById("iframeid").innerHTML="Attachement > 2MB";
 }
submitenabledisable();
});

const messageInput = document.getElementById("messageid");
messageInput.addEventListener("input", function(e) {
 if ( this.value.length>0 ) {
 this.style.removeProperty("border");
 } else {
 this.style.border="1px solid red";
 }
submitenabledisable();
});


const submitButton = document.getElementById("s_submit");
const quizInput = document.querySelector(".quiz-control");
quizInput.addEventListener("input", function(e) {
const res = submitButton.getAttribute("data-res");
if ( this.value == res ) {
this.style.removeProperty("border");
document.getElementById("quiztextid").style.color="blue";
} else {
this.style.border="1px solid red";
document.getElementById("quiztextid").style.color="red";
}
submitenabledisable();
});
submitenabledisable();
</script>';
} else
 echo $state;
}

function draw($util){
$json=json_decode(mysqli_fetch_row($util->db->get('headername','content','name',$util->subitem))[0],true);
$tech=json_decode(mysqli_fetch_row($util->db->get('headername','content','name','training'))[0],true)['child'];
$tech=$tech[rand(0,count($tech)-1)];
$email_exp = '/^[A-Za-z0-9._%-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}$/';
 if(isset($_POST['submit'])){
  $filename=preg_replace('/\W+/','_',$_POST['email']).'_'.preg_replace('/\W+/','_',$_FILES["attachment"]["name"]);
  $filedata=file_get_contents('../../online/message.txt');
  $filedata=$filedata."\n".$_POST['name']."!ABS SBA!".$_POST['technology']."!ABS SBA!".$_POST['email']."!ABS SBA!".$filename."!ABS SBA!".preg_replace("/\r\n/","\\n",$_POST['message'])."!ABS SBA!".date('d-m-y h:i:s');
  $message="Technology- ".$_POST['technology']."\n"."Name- ".$_POST['name']."\n"."Email- ".$_POST['email']."\n"."Message- ".$_POST['message']."\n"."UploadFile- ".$_FILES["attachment"]["name"];
  file_put_contents('../../online/message.txt',$filedata);
  form($util,$tech,"<pre style=\"color:#444444;font-size:18pt;text-align:center\">".$message."</pre><br><br><pre style=\"color:#004000;font-size:28pt;text-align:center\">Message Sent.</pre>");
 }else
  form($util,$tech,'form');
}
?>
