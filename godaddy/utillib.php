<?php
function googlerecaptchav2(){
 $captcha;
 $errorstring="";
 if(isset($_POST['g-recaptcha-response'])){
  $captcha=$_POST['g-recaptcha-response'];
 }
 if(!$captcha){
  $errorstring.="<e><p style=\"color:#ff0000\">Captcha Error</p></e>";
  return $errorstring;
 }
 $secretKey = preg_replace('/^.*?\\n(.*)/m','$1',file_get_contents('http://www.minhinc.com/donotdelete/captchav2/sitecaptchav2.key'));
 $ip = $_SERVER['REMOTE_ADDR'];
// post request to server
 $url = 'https://www.google.com/recaptcha/api/siteverify?secret=' . urlencode($secretKey) .  '&response=' . urlencode($captcha);
 $response = file_get_contents($url);
 $responseKeys = json_decode($response,true);
 if(!$responseKeys["success"]) {
  $errorstring.="<e><p><span style=\"color:#ff0000\">retry or mailto </span><span style=\"color:#004000\">sales@minhinc.com</span></p></e>";
  return $errorstring;
 }
 return $errorstring;
}

function mail_attachment($filename, $path, $mailto, $from_mail, $from_name, $replyto, $subject, $message) {
 $errorstring="";
 $file = $path.$filename;
 $content = file_get_contents( $file);
 $content = chunk_split(base64_encode($content));
 $uid = md5(uniqid(time()));
 $name = basename($file);
 
 // header
// $header = "From: ".$from_name." <".$from_mail.">\r\n";
 $header = "From:".$from_mail."\r\n";
// $header .= "Reply-To: ".$replyto."\r\n";
 $header .= "MIME-Version: 1.0\r\n";
 $header .= "Content-Type: multipart/mixed; boundary=\"".$uid."\"\r\n\r\n";
 
 // message & attachment
 $nmessage = "--".$uid."\r\n";
 $nmessage .= "Content-type:text/plain; charset=iso-8859-1\r\n";
 $nmessage .= "Content-Transfer-Encoding: 7bit\r\n\r\n";
 $nmessage .= $message."\r\n\r\n";
 $nmessage .= "--".$uid."\r\n";
 $nmessage .= "Content-Type: application/octet-stream; name=\"".$filename."\"\r\n";
 $nmessage .= "Content-Transfer-Encoding: base64\r\n";
 $nmessage .= "Content-Disposition: attachment; filename=\"".$filename."\"\r\n\r\n";
 $nmessage .= $content."\r\n\r\n";
 $nmessage .= "--".$uid."--";
 
 if (!mail($mailto, $subject, $nmessage, $header))
  $errorstring.="<e><p style=\"color:#ff0000\">Error:mail to sales@minhinc.com</p></e>";
 return $errorstring;
}

function validateattachment($filename,$filesize,$filetype){
 $errorstring="";
 $allowed = array("pdf" => "application/pdf",  "docx" => "application/vnd.openxmlformats-officedocument.wordprocessingml.document", "txt" => "text/plain", "jpg" => "image/jpg", "jpeg" => "image/jpeg", "gif" => "image/gif", "png" => "image/png" );
 $ext = pathinfo($filename, PATHINFO_EXTENSION);
 if(!array_key_exists($ext, $allowed))
  $errorstring.="<e><p style=\"color:#ff0000\">File format pdf docx txt png gif jpg supported</p></e>";
 $maxsize = 2 * 1024 * 1024; //2MB 
 if($filesize > $maxsize)
  $errorstring.="<e><p style=\"color:#ff0000\">File size <= 2MB</p></e>";
 // Verify MYME type of the file
 if(!in_array($filetype, $allowed))
  $errorstring.="<e><p style=\"color:#ff0000\">MIME type pdf docx txt jpg gif png supported</p></e>";
 return $errorstring;
}
?>
