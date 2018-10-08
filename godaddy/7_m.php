<?php
function draw($util){
echo ' <ul class="seven">
<li class="header"><pre class="header">File Upload Form</pre></li>
<li class="light">
<pre class="f10">Minh, Inc. is looking for C++ and Python developers in Networking, Multimedia and Graphics domain.</pre>
<h3>Upload Resume</h3>
<p>(.doc(x) .pdf .txt)</p>
<form class="common" action="'.$util->level.'/php/upload_manager.php" method="post" target="myIframe" enctype="multipart/form-data">
<div><pre class="bold f12 inline">Filename:</pre><input class="inline" type="file" name="photo" id="fileSelect"></div>
<p><input type="submit" name="submit" value="Upload"></p>
<iframe name="myIframe" frameborder="0" scrolling="no">
</iframe>
</form>
</li>
 </ul>
<div class="clr"></div>';
}
?>
