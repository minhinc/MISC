<title>Minh, Inc. Software development and Outsourcing | About</title>
<link rel="stylesheet" type="text/css" href="../test.css" media="all"/>
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
 sendmail('register');
}elseif(isset($_POST['submit'])){
 $email=mysqli_fetch_row($db->get('track','email','uuid',$_GET['email']))[0];
 $db->update('track','status',2,'uuid',$_GET['email']);
 if(!$db->search('message','name',$_POST['jungle'].":".$_POST['text'])){
  $db->insert('message',$_POST['jungle'].":".$_POST['text']);
 }
 $db->update('track','message',mysqli_fetch_row($db->get('message','id','name',$_POST['jungle'].":".$_POST['text']))[0],'uuid',$_GET['email']);
 form('email');
 form('unregister');
 sendmail('unregister');
}else{
 if(!$db->search('track','uuid',$_GET['email']) || $db->search('track','status','2')){
 form('notfound');
 }else{
  $email=mysqli_fetch_row($db->get('track','email','uuid',$_GET['email']))[0];
  form('email');
  form('form');
 }
}
form('tail');

function sendmail($mode){
global $email;
if($mode=='register'){
mail('sales@minhinc.com',$email . " registered back","","From:". $email);
}elseif($mode=='unregister'){
mail('sales@minhinc.com',$email . " unregistered","reason:" . $_POST['jungle'] . ":" . $_POST['text'],"From:". $email);
}
}

function form($state){
global $option,$email;
if($state=='head'){
?>
<div style='height:60px;margin-top:60px;background:#c3c3c3;position:relative;'>
 <img style='position:absolute;top:50%;transform:translate(0%,-50%);' src='logo.png'/>
</div>
<?
}
elseif($state=='email'){
?>
 <div style='height:40px;margin-top:20px;position:relative;'>
  <label style='position:absolute;top:20px;width:30px;'>Email* </label>
  <div style='position:absolute;top:15px;height:30px;left:70px;width:160px;background:#c3c3c3'>
   <label style='position:absolute;left:50%;top:50%;transform:translate(-50%,-50%)'><? echo $email ?>
   </label>
  </div>
 </div>
<?
}elseif($state=='tail'){ ?>
 <div style='margin-top:90px;height:20px;background:#4383c3'>
  <lebel style='line-height:20px;font-size:7pt'>&copy Minh Inc, Bangalore
  </lebel>
 </div>
<?
}elseif($state=='form'){
?>
 <form style='clear:left;margin-top:40px;' method="post" action=""> 
 <label>Please provide the reason to unregister</label><br><br>
<? for($count=0;$count<count($option);$count++){
echo "<input type='radio' name='jungle' value='".$option[$count]."'";
echo ($count==(count($option)-1))?' checked':'';
if($count!=(count($option)-1)){
echo " onclick=document.getElementById('text').setAttribute('disabled',true)>".$option[$count]."<br>";
}else{
echo " onclick=document.getElementById('text').removeAttribute('disabled')>".$option[$count]."<br>";
}
}
?>
<textarea id='text' name='text' cols='40' rows='5' style='margin:22px 0 20px 10px' value=$textarea>
</textarea><br>
<input type="submit" name="submit" value="Unsubscribe"><br>
</form>
<? }elseif($state=='register'){ ?>
<div style='margin-top:80px;width:200px;height:40px;background:#66cc99'>
 <lebel style='line-height:40px;font-size:18pt'>Registered!!!
 </lebel>
</div>
<? }elseif($state=='unregister'){ ?>
 <div style='margin-top:80px;width:200px;height:40px;background:#ffcc33'>
  <lebel style='line-height:40px;font-size:18pt'>Unregistered Sucessfully
  </lebel>
 </div>
<p style='margin-top:40px'>Click 
 <a style='font-size:14pt;color:#004000' href='http://www.minhinc.com/misc/unsubscribe_w.php?register=<? echo $_GET['email'] ?>'>here
 </a> to get registered again.
</p>
<? }elseif($state=='notfound'){ ?>
 <div style='margin-top:80px;width:200px;height:40px;background:#ffccff'>
  <lebel style='line-height:40px;font-size:18pt'>Not registered
  </lebel>
  <p style='margin-top:40px'>click <a style='font-size:14pt;color:#004000' href='http://www.minhinc.com/about/unsubscribe_w.php?register=<? echo $_GET['email'] ?>'>here
  </a> to get registered.</p>
 </div>
<?
}
}
?>
