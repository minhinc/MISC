<?php
function form($state,$option='',$email='',$tech=''){
?>
 <pre style="margin-top:5px;line-height:28px;text-align:center;background-color:#888888;font-family:mytwcenmt;font-size:22pt;color:#004000">Minh Inc</pre>
 <pre style="color:#ffa500;font-weight:bold;font-size:18pt;margin:10px 0;text-align:center"><? echo $email ?></pre>
<!--<div style='height:450px'>-->
<?
 if($state=='form'){
?>
 <form method="post" action=""> 
 <label>Please provide the reason to unregister</label><br>
 <a href="http://minhinc.42web.io/image/<? echo $tech ?>"><img style="max-width:80%;margin-left:10%" src="http://minhinc.42web.io/image/<? echo $tech ?>traininglogo.gif"></img></a>
 <br>
<?
  for($count=0;$count<count($option);$count++){
   echo "<input type='radio' name='jungle' value='".$option[$count]."'";
   echo ($count==(count($option)-1))?' checked':'';
   if($count!=(count($option)-1)){
    echo " onclick=document.getElementById('text').setAttribute('disabled',true)> ".$option[$count]."<br>";
   }else{
    echo " onclick=document.getElementById('text').removeAttribute('disabled')> ".$option[$count]."<br>";
   }
  }
?>
<textarea id="text" name="text" cols="40" rows="5" maxlength="100" style="margin:12px 0 10px 10px;background:#ffffff" value=$textarea>
</textarea><br>
<input type="submit" name="submit" value="Unsubscribe" style="background-color:#bbbbbb;border:2px solid red;margin-left:20%;width:60%;color:green;font-weight:bold;font-size:23pt;"><br>
</form>
<?
 }else{
 echo '<a href="http://minhinc.42web.io/image/'.$tech.'"><img style="margin-left:10%;max-width:80%" src="http://minhinc.42web.io/image/'.$tech.'traininglogo.gif"></img></a>';
?>
 <pre style="margin:20px 10%;line-height:48px;text-align:center;background-color:#cccccc;font-family:mytwcenmt;font-size:20pt;color:#FF0000;font-weight:bold;width:80%"><? echo $state ?></pre>
<?
 }
}

function draw($util) {
 $option=array("emails too frequent",
               "emails not relevant",
               "emails not personalized and customized",
               "emails not mobile-optimized",
               "email added without sign up",
               "others...");
 $filedata=file_get_contents('track.txt');
 $email='';
 $tech=json_decode(mysqli_fetch_row($util->db->get('headername','content','name','training'))[0],true)['child'];
 $tech=$tech[rand(0,count($tech)-1)];
 if(!preg_match("/!ABS SBA!".$_GET['email']."!ABS SBA!/",$filedata)) {
  form('Email Not Registered','','',$tech);
 }else{
  $email=preg_replace("/^.*[^']*'([^!]+)!ABS SBA!".$_GET['email'].".*/s","$1",$filedata);
  if(preg_match("/".$email." 2 "."/",$filedata) ||  preg_match("/.*".$_GET['email'].".*!ABS SBA!2!ABS SBA"."/",$filedata)) {
   form('Already Unregistered','',$email,$tech);
  }elseif(isset($_POST['submit'])){
   $filedata=$filedata."\n".$email.' 2 '.$_POST['jungle'].":".$_POST['text'];
   file_put_contents('track.txt',$filedata);
   form('Unregistered Successfully','',$email,$tech);
  }else {
   form('form',$option,$email,$tech);
  }
 }
}
?>
