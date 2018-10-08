<?php
function draw($util){
$util->drawmenuleft();
$json=json_decode(mysqli_fetch_row($util->db->get('headername','content','name',$util->headername))[0],true);
echo '<div class="downloadright">
<ul class="description">
<li class="header"><p>File Upload Form</p></li>
<li class="light">
<p>Minh, Inc. is looking for C++ and Python developers in Networking, <br>Multimedia and Graphics domain.</p>
<h3>Upload Resume</h3>
<p>(.doc(x) .pdf)</p>
<form class="common" action="'.$util->level.'/php/upload_manager.php" method="post" target="myIframe" enctype="multipart/form-data">
<p>Filename:<input type="file" name="photo" id="fileSelect"></p>
<p><input type="submit" name="submit" value="Upload"></p>
<iframe name="myIframe" frameborder="0" scrolling="no">
</iframe>
</form>
</li>
</ul>
</div>';
}
?>
