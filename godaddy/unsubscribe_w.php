<html>
<head>
<title>Minh, Inc. Software development and Outsourcing | About</title>
<link rel="stylesheet" type="text/css" href="../agenda.css" media="all"/>
</head>
<?
$option=array("emails too frequent",
              "emails not relevant",
              "emails not personalized and customized",
              "emails not mobile-optimized",
              "email added without sign up",
              "others...");
$email='';
require_once('Databasem.php');
$db=new Databasec;
form('head');
if(isset($_GET['register'])){
 $email=mysqli_fetch_row($db->get('track','email','uuid',$_GET['register']))[0];
 $db->update('track','status',1,'uuid',$_GET['register']);
 form('email');
 form('register');
// sendmail('register');
}elseif(isset($_POST['submit'])){
 $email=mysqli_fetch_row($db->get('track','email','uuid',$_GET['email']))[0];
 $db->update('track','status',2,'uuid',$_GET['email']);
 if(!$db->search('message','name',$_POST['jungle'].":".$_POST['text'])){
  $db->insert('message',$_POST['jungle'].":".$_POST['text']);
 }
 $db->update('track','message',mysqli_fetch_row($db->get('message','id','name',$_POST['jungle'].":".$_POST['text']))[0],'uuid',$_GET['email']);
 form('email');
 form('unregister');
// sendmail('unregister');
}else{
 if(!$db->search('track','uuid',$_GET['email']) || $db->search('track','uuid',$_GET['email'],'status','2')){
 form('notfound');
 }else{
  $email=mysqli_fetch_row($db->get('track','email','uuid',$_GET['email']))[0];
  form('email');
  form('form');
 }
}
form('tail');

/*function sendmail($mode){
global $email;
 if($mode=='register'){
 mail('sales@minhinc.com',$email . " registered back","","From:". $email);
 }elseif($mode=='unregister'){
 mail('sales@minhinc.com',$email . " unregistered","reason:" . $_POST['jungle'] . ":" . $_POST['text'],"From:". $email);
 }
}*/

function form($state){
global $option,$email;
 if($state=='head'){
?>
<body>
<div style='height:60px;margin-top:20px;'><pre style='line-height:60px;background-color:#888888;font-family:mytwcenmt;font-size:26pt;color:#004000'>Minh Inc</pre></div>
<div style='height:450px'>
<?
 }elseif($state=='email'){
?>
 <div style='height:40px;width:600px;margin-top:15px;'>
  <pre style='line-height:40px;width:60px;float:left'>Email* </pre><pre style='float:left;line-height:40px;width:160px;background:#c3c3c3;'>  <? echo $email ?></pre>
 </div>
<?
 }elseif($state=='tail'){
?>
</div>
 <pre style='margin-top:40px;height:20px;background-color:#4383c3;line-height:20px;font-size:7pt'>&copy Minh Inc, Bangalore</pre>
</body>
</html>
<?
 }elseif($state=='form'){
?>
 <form style='clear:left;margin-top:20px;' method="post" action=""> 
 <label>Please provide the reason to unregister</label><br><br>
<? for($count=0;$count<count($option);$count++){
echo "<input type='radio' name='jungle' value='".$option[$count]."'";
echo ($count==(count($option)-1))?' checked':'';
  if($count!=(count($option)-1)){
  echo " onclick=document.getElementById('text').setAttribute('disabled',true)> ".$option[$count]."<br>";
  }else{
  echo " onclick=document.getElementById('text').removeAttribute('disabled')> ".$option[$count]."<br>";
  }
 }
?>
<textarea id='text' name='text' cols='40' rows='5' style='margin:12px 0 10px 10px;background:#ffffff' value=$textarea>
</textarea><br>
<input type="submit" name="submit" value="Unsubscribe"><br>
</form>
<?
 }elseif($state=='register'){
?>
<pre style='margin-top:80px;width:180px;line-height:40px;background:#66cc99;font-size:18pt'>Registered!!! </pre>
<?
 }elseif($state=='unregister'){
?>
 <pre style='margin-top:80px;width:320px;line-height:40px;background:#ffcc33;font-size:18pt'>Unregistered Successfully </pre>
<p style='margin-top:40px'>Click 
 <a style='font-size:14pt;color:#004000' href='http://www.minhinc.com/about/unsubscribe_w.php?register=<? echo $_GET['email'] ?>'>here
 </a> to get registered again.
</p>
<?
 }elseif($state=='notfound'){
?>
 <div style='margin-top:80px;width:200px;height:40px;background:#ffccff'>
  <pre style='line-height:40px;width:180px;font-size:18pt'>Not registered </pre>
  <p style='margin-top:40px'>click <a style='font-size:14pt;color:#004000' href='http://www.minhinc.com/about/unsubscribe_w.php?register=<? echo $_GET['email'] ?>'>here
  </a> to get registered.</p>
 </div>
<?
 }
}
?>
