<?
function draw($util){
$json=json_decode(mysqli_fetch_row($util->db->get('headername','content','name',$util->subitem))[0],true);
echo '<ul class="common">
<li class="header"><pre>'.$json['title'].'</pre></li>
</ul>
<form class="online" action="'.$util->level.'/php/send_form_question.php" method="post" target="myIframe"">
<div class="row"><pre class="lc bold">Technology</pre>
<select name="technology" class="l">';
$json=json_decode(mysqli_fetch_row($util->db->get('headername','content','name','training'))[0],true);
foreach($json['child'] as $key){
$json1=json_decode(mysqli_fetch_row($util->db->get('headername','content','name',$key))[0],true);
   echo '<option value="'.$key.'">'.ucfirst(preg_replace("/ training$/i","",$json1['title'])).'</option>';
}
echo '</select></div>

<div class="row"><pre class="lc bold">Name:</pre><input type="text" name="name" placeholder="Your Name" class="l"></div>
<div class="row"><pre class="lc bold">Email:</pre><input type="text" name="email" placeholder="Email Address" class="l"></div>
<div class="rowtextarea"><pre class="lc bold">Query:</pre><textarea rows="5" name="message" cols="40" class="l2"></textarea></div>
<div class="row"><img id="imgcaptchaid" src="'.$util->level.'/php/captcha.php" style="float:left" /><input name="captcha_entered" type="text" id="captcha_entered" size="5" maxlength="2" placeholder = "Answer" class="l" style="margin-left:8%"/></div>
<div class="row"><input type="submit" name="submit" value="Submit" class="submit lc bold enable"><iframe name="myIframe" frameborder="0" scrolling="no" class="l" style="width:400px" id="iframeid"></iframe></div>
</form>
<div style="clear:both"></div>
<script>
document.getElementById("iframeid").onload=function(){
document.getElementById("imgcaptchaid").src="'.$util->level.'/php/captcha.php?time="+new Date();
}
</script>';
}
?>
