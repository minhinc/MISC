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
 <div style="width:400px;float:right;"><div style="width:400px;height:500px;position:relative;" align="center"><script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js"></script>
<!-- fixed_200_200 -->
<ins class="adsbygoogle"
     style="position:absolute;left:0px;top:6px;display:inline-block;width:200px;height:200px"
     data-ad-client="ca-pub-8488699542117607"
     data-ad-slot="2697807187"></ins>
<script>
     (adsbygoogle = window.adsbygoogle || []).push({});
</script><script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js"></script>
<!-- fixed_200_200 -->
<ins class="adsbygoogle"
     style="position:absolute;left:200px;top:6px;display:inline-block;width:200px;height:200px"
     data-ad-client="ca-pub-8488699542117607"
     data-ad-slot="2697807187"></ins>
<script>
     (adsbygoogle = window.adsbygoogle || []).push({});
</script><script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js"></script>
<!-- fixed_336_280 -->
<ins class="adsbygoogle"
     style="position:absolute;left:0px;top:212px;display:inline-block;width:336px;height:280px"
     data-ad-client="ca-pub-8488699542117607"
     data-ad-slot="3234005567"></ins>
<script>
     (adsbygoogle = window.adsbygoogle || []).push({});
</script></div></div>
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
