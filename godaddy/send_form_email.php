<?php
if(isset($_POST['submit'])){
 $captcha;
 if(isset($_POST['g-recaptcha-response'])){
  $captcha=$_POST['g-recaptcha-response'];
 }
 if(!$captcha){
  echo "<p style=\"color:#ff0000\">Captcha Error!!</p>";
  exit;
 }
 $secretKey = preg_replace('/^.*?\\n(.*)/m','$1',file_get_contents('http://www.minhinc.com/donotdelete/captchav2/sitecaptchav2.key'));
 $ip = $_SERVER['REMOTE_ADDR'];
// post request to server
 $url = 'https://www.google.com/recaptcha/api/siteverify?secret=' . urlencode($secretKey) .  '&response=' . urlencode($captcha);
 $response = file_get_contents($url);
 $responseKeys = json_decode($response,true);
// should return JSON with success as true
 if(!$responseKeys["success"]) {
  echo "<p><span style=\"color:#ff0000\">retry or mailto </span><span style=\"color:#004000\">sales@minhinc.com</span></p>";
  exit;
 }
// session_start();
 $to = "sales@minhinc.com"; // this is your Email address
 $message2 = "Here is a copy of your message:\n    -------\n" . $_POST['message'] . "\n\n+91 9483160610\nweb : http://www.minhinc.com";
 $from = $_POST['email']; // this is the sender's Email address
 $subject = "*** Contact Us *** Form submission";
 $subject2 = "Copy of your form submission";
 $message = "*** Contact Us ***\n\nEmail : " . $from . "\nName : " . $_POST['name'] . "\nwrote the following : " . "\n\n" . $_POST['message'];
 
 $headers = "From:" . $from;
 $headers2 = "From:" . $to;
 $email_exp = '/^[A-Za-z0-9._%-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}$/';
 if(!preg_match($email_exp,$from)) {
  echo "<p style=\"color:#ff0000\">Wrong Email Address.</p>";
 }else if(strlen($_POST['message']) < 2) {
  echo "<p style=\"color:#ff0000\">Message Incomplete.</p>";
 }else if(preg_match('/\b(sex.*?|juicy|girl.*?|fuck.*?|wom.n.*?)\b/i',$_POST['message'])){
  echo "<p><span style=\"color:#ff0000\">obsene found</span><span style=\"color:#000\">mailto sales@minhinc.com</span></p>";
 }else {
  mail($to,$subject,$message,$headers);
  mail($from,$subject2,$message2,$headers2); // sends a copy of the message to the sender
  echo "<p style=\"color:#004000\">Message Sent.</p>";
 }
}
?>
