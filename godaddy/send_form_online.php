<?php
if(isset($_POST['submit'])){
session_start();
 $to = "sales@minhinc.com"; // this is your Email address
 $message2 = "Copy of your training request:\n\nTechnology:".$_POST['technology']."\nRequest date:".$_POST['tdate']."\nComment".$_POST['message']."\n\n\nThanks,\nWe will contact you soon.\n\n+91 9483160610 (also on whatsapp)\nwww.minhinc.com";
 $from = $_POST['email']; // this is the sender's Email address
 $subject = "Training Request Submission";
 $subject2 = "Copy of your Training submission";
 $message = $_POST['name']."\nTechnology:".$_POST['technology']."\nRequest date:".$_POST['tdate']."\nComment:".$_POST['message'];

 $headers = "From:" . $from;
 $headers2 = "From:" . $to;
 $email_exp = '/^[A-Za-z0-9._%-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}$/';
 if(!preg_match($email_exp,$from)) {
  echo "<p style=\"color:#ff0000\">Wrong Email Address.</p>";
 }else   if(strlen($_POST['message']) < 2) {
  echo "<p style=\"color:#ff0000\">Message Incomplete.</p>";
 } else if (empty($_POST['captcha_entered'])) {
  echo '<p style="color:#ff0000">Answer Captcha</p>';
 }else if ($_POST['captcha_entered']!=$_SESSION['rand_code']) {
  echo '<p style="color:#ff0000">Incorrect Answer.</p>';
}else if(preg_match('/\b(sex.*?|juicy|girl.*?|fuck.*?|wom.n.*?)\b/i',$_POST['message'])){
  echo "<p style=\"color:#ff0000\">obsenes found, mail sales@minhinc.com</p>";
 }else {
  mail($to,$subject,$message,$headers);
  mail($from,$subject2,$message2,$headers2); // sends a copy of the message to the sender
  echo "<p style=\"color:#004000\">Message Sent.</p>";
}
//die();
    // You can also use header('Location: thank_you.php'); to redirect to another page.
    }
?>
