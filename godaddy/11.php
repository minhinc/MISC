<?
function draw($util){
echo '<ul class="common">
<li class="header"><pre>'.json_decode(mysqli_fetch_row($util->db->get('headername','content','name',$util->subitem))[0],true)['title'].'</pre></li>
<li><pre class="register">Register For Online Training
<!--<span style="color:#ff8844;font-size:14pt">Upcoming training : Qml <a href="http://www.minhinc.com/training/advance-qml-agenda.php" style="text-decoration:underline;font-size:14pt;color:#004000">See Agenda</a></span></pre>--></li>
</ul>
<form class="online" action="'.$util->level.'/php/send_form_online.php" method="post" target="myIframe"">
<div class="row"><pre class="lc bold">Technology</pre>
<select id="selecttech" name="technology" class="l">
   <option value="" selected></option>';
$json=json_decode(mysqli_fetch_row($util->db->get('headername','content','name','training'))[0],true);
foreach($json['child'] as $key){
$json1=json_decode(mysqli_fetch_row($util->db->get('headername','content','name',$key))[0],true);
   echo '<option value="'.$key.'">'.ucfirst(preg_replace("/ training$/i","",$json1['title'])).'</option>';
}
echo '</select></div>
<div class="row"><pre class="lc bold">Fee:</pre><pre class="l bold" id="charge"></pre></div>
<div class="row"><pre class="lc bold">Duration:</pre><pre class="l bold" id="onlineduration"></pre></div>
<div class="row"><pre class="lc bold">Course Content:</pre><a class="l bold block" href="" id="a_course" target="_blank"></a></div>
<div class="row"><pre class="lc bold">Name:</pre><input type="text" name="name" placeholder="Your Name" class="l"></div>
<div class="row"><pre class="lc bold">Email:</pre><input type="text" name="email" placeholder="Email Address" class="l"><pre class="ls bold star">*</pre></div>
<div class="rowtextarea" ><pre class="lc bold">Comment:</pre><textarea rows="5" name="message" cols="40" class="l2"></textarea><pre class="ls bold star">*</pre></div>
<div class="row"><pre class="lc bold">Date:</pre><input type="date" name="tdate"></div>
<div class="row"><img id="imgcaptchaid" src="'.$util->level.'/php/captcha.php" style="float:left" /><input name="captcha_entered" type="text" id="captcha_entered" size="5" maxlength="2" placeholder = "Answer" class="l" style="margin-left:8%"/></div>
<div class="row"><input type="submit" name="submit" value="Submit" class="submit lc bold disable" id="s_submit"><iframe name="myIframe" frameborder="0" scrolling="no" class="l" id="iframeid" style="width:400px"></iframe></div>
</form>
<div style="clear:both"></div>
<script>
var chargearr={"":"",';
$json=json_decode(mysqli_fetch_row($util->db->get('headername','content','name','training'))[0],true);
$first='';
foreach($json['child'] as $key){
echo $first.' '.$key.':"USD $'.json_decode(mysqli_fetch_row($util->db->get('headername','content','name',$key))[0],true)['charge']['us'].', INR '.json_decode(mysqli_fetch_row($util->db->get('headername','content','name',$key))[0],true)['charge']['in'].'/-"';
if(empty($first))
$first=',';
}
echo '}';
echo ';var onlinedurationarr={"":"",';
$json=json_decode(mysqli_fetch_row($util->db->get('headername','content','name','training'))[0],true);
$first='';
foreach($json['child'] as $key){
echo $first.' '.$key.':"'.json_decode(mysqli_fetch_row($util->db->get('headername','content','name',$key))[0],true)['onlineduration']['day'].' Days. 4-5 hours every week. Total duration '.json_decode(mysqli_fetch_row($util->db->get('headername','content','name',$key))[0],true)['onlineduration']['month'].' month(s)"';
if(empty($first))
$first=',';
}
echo '};
if (document.getElementById("selecttech").options[document.getElementById("selecttech").selectedIndex].value == ""){
 document.getElementById("s_submit").disabled=true;
 document.getElementById("s_submit").classList.remove("enable");
 document.getElementById("s_submit").classList.add("disable");
 document.getElementById("a_course").innerHTML="";
 document.getElementById("a_course").setAttribute("href","");
}else{
 document.getElementById("s_submit").disabled=false;
 document.getElementById("s_submit").classList.remove("disable");
 document.getElementById("s_submit").classList.add("enable");
 document.getElementById("a_course").innerHTML="Click here for Course Content";
 document.getElementById("a_course").setAttribute("href","http://www.minhinc.com/training/"+document.getElementById("selecttech").options[document.getElementById("selecttech").selectedIndex].value);
}
document.getElementById("selecttech").onchange=function(){
var e = document.getElementById("selecttech");
var strUser = e.options[e.selectedIndex].value;
document.getElementById("charge").innerHTML=chargearr[strUser];
document.getElementById("onlineduration").innerHTML=onlinedurationarr[strUser];
if (strUser !== ""){
document.getElementById("s_submit").classList.remove("disable");
document.getElementById("s_submit").classList.add("enable");
document.getElementById("s_submit").disabled=false;
document.getElementById("a_course").innerHTML="Click here for Course Content";
document.getElementById("a_course").setAttribute("href","http://www.minhinc.com/training/"+strUser);
}else{
document.getElementById("s_submit").classList.remove("enable");
document.getElementById("s_submit").classList.add("disable");
document.getElementById("s_submit").disabled=true;
document.getElementById("a_course").innerHTML="";
document.getElementById("a_course").setAttribute("href","");
}
}
document.getElementById("iframeid").onload=function(){
document.getElementById("imgcaptchaid").src="'.$util->level.'/php/captcha.php?time="+new Date();
}
</script>';
}
?>
