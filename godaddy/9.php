<?
function draw($util){
 $json=json_decode(mysqli_fetch_row($util->db->get('headername','content','name',$util->subitem))[0],true);
 echo '<ul class="common">
 <li class="header"><pre>'.$json['title'].'</pre></li>
 </ul>
 <form class="online" action="'.$util->level.'/php/send_form_question.php" method="post" target="myIframe" style="width:550px;float:left;">
 <div class="row"><pre class="lc bold">Technology</pre>
 <select name="technology" class="l">';
 $json=json_decode(mysqli_fetch_row($util->db->get('headername','content','name','training'))[0],true);
 foreach($json['child'] as $key){
  $json1=json_decode(mysqli_fetch_row($util->db->get('headername','content','name',$key))[0],true);
  echo '<option value="'.$key.'">'.ucfirst(preg_replace("/ training$/i","",$json1['title'])).'</option>';
 }
 echo '</select></div>

 <div class="row"><pre class="lc bold">Name:</pre><input type="text" name="name" placeholder="Your Name" class="l"></div>
 <div class="row"><pre class="lc bold">Email:</pre><input id="emailid" type="text" name="email" placeholder="Email Address" class="l"></div>
 <div class="rowtextarea"><pre class="lc bold">Query:</pre><textarea id="textareaid" rows="5" name="message" cols="40" class="l2"></textarea></div>
 <div style="margin:10px 0" class="g-recaptcha" data-callback="imNotARobot" data-sitekey="'.preg_replace('/^(.*)\\n.*/m','$1',file_get_contents($util->level.'/donotdelete/captchav2/sitecaptchav2.key')).'"></div>
 <div class="row"><input type="submit" name="submit" value="Submit" class="submit lc bold enable"><iframe name="myIframe" frameborder="0" scrolling="no" class="l" style="width:400px" id="iframeid"></iframe></div>
 </form>
 <div style="width:400px;float:right;"><py>requestm.adsensepaste(400,500,backend="desktop",factor=0.0)</py></div>
 <div style="clear:both"></div>
 <script>
var imNotARobot = function() {
  document.getElementById("iframeid").contentWindow.document.write("");
  };
 document.getElementById("iframeid").onload=function(){
  var framecontent=document.getElementById("iframeid").contentWindow.document.body.innerHTML;
  if (framecontent.match(/40/gi)){
   document.getElementById("emailid").value="";
   document.getElementById("textareaid").value="";
   grecaptcha.reset();
  }
 }
 </script>';
}
?>
