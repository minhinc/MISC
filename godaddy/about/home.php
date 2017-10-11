<?php
if(isset($_POST['submit'])){
    $to = "sales@minhinc.com"; // this is your Email address
    $from = $_POST['email']; // this is the sender's Email address
    $subject = "Form submission";
    $subject2 = "Copy of your form submission";
    $message = " wrote the following:" . "\n\n" . $_POST['message'];
    $message2 = "Here is a copy of your message:\n\n" . $_POST['message'] . "\n\nThanks,\nSales team,\n+91 9483160610 \nwww.minhinc.com";

    $headers = "From:" . $from;
    $headers2 = "From:" . $to;
$email_exp = '/^[A-Za-z0-9._%-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}$/';
if(!preg_match($email_exp,$from)) {
echo "<p style=\"color:#ff0000\">WRONG EMAIL ADDRESS</p>";
}else   if(strlen($_POST['message']) < 2) {
echo "<p style=\"color:#ff0000\">MESSAGE INCOMPLETE</p>";
}else{
    mail($to,$subject,$message,$headers);
    mail($from,$subject2,$message2,$headers2); // sends a copy of the message to the sender
    echo "<p style=\"color:#004000\">Message Sent. We will contact you shortly.</p>";
}
die();
    // You can also use header('Location: thank_you.php'); to redirect to another page.
    }
?>
<html>
<head>
<link rel="stylesheet" href="../dropdownmenu.css" type="text/css" media="all" />
</head>
<body>
<div id="ddm">
<ul id="nav" class="drop">
  <li><a href="../home.html">Home</a></li>
  <li><a href=".././product/home.html">Products</a>
   <ul>
      <li><a href=".././product/nazfs.html">Flight Simulator</a></li>
      <li><a href=".././product/gmp.html">Media Player</a></li>
      <li><a href=".././product/gfd.html">YouTube Downloader</a></li>
   </ul>
  </li>
  <li><a href=".././training/home.html">Training</a>
    <ul>
      <li><a href=".././training/cpp.html">C++</a>
       <ul>
         <li><a href=".././training/advance-cpp-agenda.pdf"  >Agenda</a></li>
</ul>
</li>
      <li><a href=".././training/qt.html">Qt</a>
<ul>
         <li><a href=".././training/advance-qt-agenda.pdf">Agenda</a></li>
</ul>
</li>
    <li><a href=".././training/opengl.html">OpenGL</a>
<ul>
    <li><a href=".././training/advance-gl-agenda.pdf">Agenda</a></li>
</ul>
</li>
      <li><a href=".././training/ldd.html">LDD</a>
<ul>
         <li><a href=".././training/advance-ldd-agenda.pdf">Agenda</a></li>
</ul>
</li>
    </ul>  
  </li>
  <li><a href=".././research/home.html">Research</a>
  </li> 
  <li><a href=".././about/home.php">About Us</a></li>
</ul>
</div>
<div id="content" style="clear:both">
<span style="font-family:calibri;font-size:9pt;"><a href ="../home.html">Home</a>::About</span>
<dl><dt style="font-family:calibri;font-size:20pt;color:#222222;">About Us</dt>
<dd>
<ul>
<li> Minh Inc is formed to provide innovative solution to software designing and development. Company has products with GPLv3 licensing and five disclosures in designing.</li>
<li>The Company provide training in various areas, i.e qt, c++, LDD.</li>
</ul>
</dd></dl>
<dl><dt>We take project for developement in</dt>
<dd>
<ul>
<li>- Networking tcp/ip socket based</li>
<li>- Algorithms based</li>
<li>- Qt(OpenGL) based Advance graphics</li>
<li>- Linux device drivers</li>
</ul>
</dd></dl>

<dl><dt style="font-family:calibri;font-size:20pt;color:#222222;margin-top:20px">Contacting Us</dt>
<dd>
<!-- <blockquote> -->
		<table cellpadding="2" cellspacing="0" border="0" style="margin:5px 0 0 17px">
<!-- <head>
<tr>
<td>Contacting</td>
</tr>
</head> -->
			<tr valign="top">
				<td style="width:200px">Sales, Partnerships or advertising enquiries</td>
				<td>sales@minhinc.com</td>
			</tr>
			<tr valign="top">
				<td>Training enquiries</td>
				<td>training@minhinc.com</td>
			</tr>
			<tr valign="top">
				<td>Project development enquiries</td>
				<td>develop@minhinc.com</td>
			</tr>
			<tr>
				<td>Address</td>
				<td>
				#85 5Mn P&T B'lore India<br />
				560094 Tel +91 9483160610
			</td></tr>
		</table>
	</blockquote>
</dd></dl>


<form action="" method="post" target="myIframe">
Email: <input type="text" name="email"><br>
Message:<br><textarea rows="5" name="message" cols="30"></textarea><br>
<input type="submit" name="submit" value="Submit">
<iframe name="myIframe" frameborder="0" height="30px" style="margin-top:10px">
</iframe>
</form>
</div>
<div id="footer" style="overflow:hidden;clear:both">
<hr align="left" noshade="noshade" width=60px>
  <p style="margin-top:0"><a href="../home.html">Home</a><span area-hidden="true"> | </span>
  <a href=".././product/home.html">Products</a><span area-hidden="true"> | </span>
  <a href=".././training/home.html">Training</a><span area-hidden="true"> | </span>
  <a href=".././research/home.html">Research</a><span area-hidden="true"> | </span>
  <a href=".././about/home.php">About Us</a></p>
</div>
</body>
</html>
