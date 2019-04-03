<?php
if(isset($_POST['submit'])){
 session_start();
 $to = "sales@minhinc.com"; // this is your Email address
 $message2 = "Hi!\nHere is a copy of your message:\n    -------\n" . $_POST['message'] . "\n    -------\nThanks for writing in! We've noted your concern/enquiry and will respond to your email within 1 business day. We hope to help you out with any query or issue you might have. In case you want to talk to us on the phone/whatsapp about this, we are at +91 9483160610 (Monday - Saturday, 7AM - 6PM).\nRegards,\nTeam Minh\nweb : http://www.minhinc.com";
 $from = $_POST['email']; // this is the sender's Email address
 $subject = "Form submission";
 $subject2 = "Copy of your form submission";
 $message = $_POST['name'] . "\nwrote the following : " . "\n\n" . $_POST['message'];
 
 $headers = "From:" . $from;
 $headers2 = "From:" . $to;
 $email_exp = '/^[A-Za-z0-9._%-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}$/';
 if(!preg_match($email_exp,$from)) {
  echo "<p style=\"color:#ff0000\">Wrong Email Address.</p>";
 }else if(strlen($_POST['message']) < 2) {
  echo "<p style=\"color:#ff0000\">Message Incomplete.</p>";
 }else if (empty($_POST['captcha_entered'])) {
  echo '<p style="color:#ff0000">Answer the Captcha/p>';
 }else if ($_POST['captcha_entered']!=$_SESSION['rand_code']) {
  echo '<p style="color:#ff0000">Incorrect answer.</p>';
 }else if(preg_match('/\b(sex.*?|juicy|girl.*?|fuck.*?|wom.n.*?)\b/i',$_POST['message'])){
  echo "<p style=\"color:#ff0000\">obsene found, send mail to sales@minhinc.com</p>";
 }else {
  mail($to,$subject,$message,$headers);
  mail($from,$subject2,$message2,$headers2); // sends a copy of the message to the sender
  echo "<p style=\"color:#004000\">Message Sent.</p>";
 }
}
?>
